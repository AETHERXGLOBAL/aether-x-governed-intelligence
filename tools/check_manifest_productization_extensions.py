#!/usr/bin/env python3
"""Validate the Gate-05C productization extensions in AX-PUB-MANIFEST-001.

This checker is deliberately additive to the historical manifest checker. It
protects newer API/support/security evidence without rewriting closed-gate
invariants that pre-date these productization artifacts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
SUP = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC = ROOT / "artifacts" / "AX-PUB-SEC-001.json"
CI013 = ROOT / "evidence" / "AX-PUB-CI-013_SDK_SUPPORT_SECURITY_CONTRACT_VALIDATION.md"

RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]
GATE03_DIGEST = "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21"

REQUIRED_RELATIONS = {
    ("AX-PUB-SUP-001", "0.1", "BUILDS_ON", "AX-PUB-API-001", "0.1"),
    ("AX-PUB-SUP-001", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-SEC-001", "0.1", "BUILDS_ON", "AX-PUB-SUP-001", "0.1"),
    ("AX-PUB-SEC-001", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
}

REQUIRED_BOUNDARIES = {
    "VALIDATED SUPPORT CONTRACT CANDIDATE DOES NOT ESTABLISH OR ACTIVATE A SUPPORT COMMITMENT",
    "TARGET DEPRECATION WINDOW DOES NOT APPLY UNTIL EXPLICIT RELEASE AUTHORITY ADOPTS IT",
    "VALIDATED SECURITY OPERATIONS CONTRACT CANDIDATE DOES NOT ESTABLISH SECURITY OPERATIONS READINESS",
    "CROSS-GATE IMMUTABILITY PASS DOES NOT ESTABLISH SDK RELEASE AUTHORITY",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_MANIFEST_PRODUCTIZATION_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain object")
    return value


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    require(isinstance(raw, str), "manifest_version must be string")
    try:
        parts = raw.split("-", 1)[0].split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        fail(f"invalid manifest_version: {raw!r}")


def require_repo_path(raw: Any, label: str) -> None:
    require(isinstance(raw, str) and raw, f"{label} missing")
    path = Path(raw)
    require(not path.is_absolute() and ".." not in path.parts, f"{label} escapes repository")
    require((ROOT / path).is_file(), f"{label} path missing: {raw}")


def main() -> int:
    manifest = load(MANIFEST)
    sup = load(SUP)
    sec = load(SEC)
    require(CI013.is_file(), "AX-PUB-CI-013 evidence missing")

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 24), "manifest must be >= v1.24")

    artifacts = {
        (item.get("id"), item.get("version")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }

    api = artifacts.get(("AX-PUB-API-001", "0.1"))
    require(isinstance(api, dict), "AX-PUB-API-001 missing")

    sup_art = artifacts.get(("AX-PUB-SUP-001", "0.1"))
    require(isinstance(sup_art, dict), "AX-PUB-SUP-001 missing")
    require(sup_art.get("type") == "SDK_SUPPORT_COMPATIBILITY_MAINTENANCE_CONTRACT_CANDIDATE", "SUP artifact type mismatch")
    for field in ("path", "machine_readable_companion", "entrypoint"):
        require_repo_path(sup_art.get(field), f"AX-PUB-SUP-001.{field}")
    sup_maturity = str(sup_art.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-05C SUPPORT CONTRACT CANDIDATE",
        "DIRECT CI VALIDATED PYTHON 3.11-3.14",
        "SUPPORT COMMITMENT NOT ESTABLISHED",
        "SUPPORTED SDK NOT ESTABLISHED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in sup_maturity, f"SUP maturity missing: {marker}")

    sec_art = artifacts.get(("AX-PUB-SEC-001", "0.1"))
    require(isinstance(sec_art, dict), "AX-PUB-SEC-001 missing")
    require(sec_art.get("type") == "SDK_SECURITY_OPERATIONS_READINESS_CONTRACT_CANDIDATE", "SEC artifact type mismatch")
    for field in ("path", "machine_readable_companion", "entrypoint"):
        require_repo_path(sec_art.get(field), f"AX-PUB-SEC-001.{field}")
    sec_maturity = str(sec_art.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-05C SECURITY OPERATIONS CONTRACT CANDIDATE",
        "DIRECT CI VALIDATED PYTHON 3.11-3.14",
        "SECURITY OPERATIONS NOT READY",
        "SUPPORTED SDK NOT ESTABLISHED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in sec_maturity, f"SEC maturity missing: {marker}")

    relations = {
        (
            str(item.get("from_id")),
            str(item.get("from_version")),
            str(item.get("relationship")),
            str(item.get("to_id")),
            str(item.get("to_version")),
        )
        for item in manifest.get("relationships", [])
        if isinstance(item, dict) and item.get("state") == "COMPATIBLE"
    }
    for relation in REQUIRED_RELATIONS:
        require(relation in relations, f"required relation missing: {relation}")

    evidence = {
        item.get("id"): item
        for item in manifest.get("validation_evidence", [])
        if isinstance(item, dict)
    }
    ci013 = evidence.get("AX-PUB-CI-013")
    require(isinstance(ci013, dict), "AX-PUB-CI-013 missing from validation_evidence")
    require(ci013.get("version") == "1.0", "CI013 version mismatch")
    require(ci013.get("path") == "evidence/AX-PUB-CI-013_SDK_SUPPORT_SECURITY_CONTRACT_VALIDATION.md", "CI013 path mismatch")
    require(ci013.get("verified_head_commit") == "b7c0f25eacfa534ae38d71b495fbd2d963d679a5", "CI013 reviewed head mismatch")
    require(ci013.get("merged_main_commit") == "9cced38d62723f05d6bb8142cb9525c89e93a4c9", "CI013 merged commit mismatch")
    require(ci013.get("workflow_run_id") == 32194756205, "CI013 workflow ID mismatch")
    require(ci013.get("workflow_run_number") == 5, "CI013 workflow run number mismatch")
    require(ci013.get("verified_runtime_matrix") == RUNTIMES, "CI013 runtime matrix mismatch")
    require(ci013.get("gate03_identity_preserved") is True, "CI013 Gate-03 preservation missing")
    require(ci013.get("gate03_verified_build_digest") == GATE03_DIGEST, "CI013 Gate-03 digest mismatch")
    for key in (
        "support_commitment_established",
        "security_operations_ready",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        require(ci013.get(key) is False, f"CI013 boundary changed: {key}")
    require(ci013.get("conclusion") == "SUCCESS", "CI013 conclusion mismatch")

    support_state = manifest.get("current_sdk_support_contract")
    require(isinstance(support_state, dict), "current_sdk_support_contract missing")
    require(support_state.get("id") == "AX-PUB-SUP-001", "current support ID mismatch")
    require(support_state.get("version") == "0.1", "current support version mismatch")
    require(support_state.get("validation_evidence") == "AX-PUB-CI-013", "current support evidence mismatch")
    require(support_state.get("state") == "VALIDATED_CANDIDATE_CONTRACT_NOT_ACTIVATED", "current support state mismatch")
    require(support_state.get("target_deprecation_notice_days") == 90, "current support target days mismatch")
    require(support_state.get("target_intervening_minor_releases") == 1, "current support target minor mismatch")
    for key in (
        "support_commitment_established",
        "production_support_activated",
        "commercial_sla_established",
        "supported_sdk_established",
    ):
        require(support_state.get(key) is False, f"current support boundary changed: {key}")
    require(support_state.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current support publication boundary changed")
    for field in ("path", "machine_readable_companion", "checker"):
        require_repo_path(support_state.get(field), f"current_sdk_support_contract.{field}")

    security_state = manifest.get("current_sdk_security_operations_contract")
    require(isinstance(security_state, dict), "current_sdk_security_operations_contract missing")
    require(security_state.get("id") == "AX-PUB-SEC-001", "current security ID mismatch")
    require(security_state.get("version") == "0.1", "current security version mismatch")
    require(security_state.get("validation_evidence") == "AX-PUB-CI-013", "current security evidence mismatch")
    require(security_state.get("state") == "VALIDATED_CANDIDATE_CONTRACT_NOT_READY", "current security state mismatch")
    for key in (
        "security_operations_ready",
        "dedicated_security_channel_established",
        "security_response_owner_assigned",
        "security_response_sla_established",
        "bug_bounty_established",
        "supported_sdk_established",
    ):
        require(security_state.get(key) is False, f"current security boundary changed: {key}")
    require(security_state.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current security publication boundary changed")
    for field in ("path", "machine_readable_companion", "checker"):
        require_repo_path(security_state.get(field), f"current_sdk_security_operations_contract.{field}")

    require(sup.get("support_commitment_established") is False, "SUP source support commitment changed")
    require(sup.get("production_support_activated") is False, "SUP source production support changed")
    require(sup.get("commercial_sla_established") is False, "SUP source SLA changed")
    require(sup.get("sdk_publication_authorized") is False, "SUP source publication changed")
    require(sec.get("security_operations_ready") is False, "SEC source readiness changed")
    require(sec.get("security_response_sla_established") is False, "SEC source SLA changed")
    require(sec.get("sdk_publication_authorized") is False, "SEC source publication changed")

    boundaries = set(manifest.get("claim_boundary", []))
    for boundary in REQUIRED_BOUNDARIES:
        require(boundary in boundaries, f"claim boundary missing: {boundary}")

    print(
        "AX_MANIFEST_PRODUCTIZATION_PASS "
        "manifest>=1.24 api=VALIDATED_CANDIDATE support=NOT_ACTIVATED "
        "security_ops=NOT_READY gate03_identity=PRESERVED publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
