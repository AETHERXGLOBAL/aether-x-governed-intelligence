#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 v1.26 release-readiness aggregation extension."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
PACK = ROOT / "artifacts" / "AX-PUB-RELPACK-001.json"
CI016 = ROOT / "evidence" / "AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md"
PACK_DOC = ROOT / "docs" / "AX-PUB-RELPACK-001_SDK_RELEASE_READINESS_EVIDENCE_PACK.md"

ACTIONS_SHA = "e9614ca5b70667e6d2218d1f19c764ce2cf09ada13764282c5758cf1865fa331"
EXPECTED_BLOCKERS = {
    "EXTERNAL_REGISTRY_VALIDATION": "NOT_ESTABLISHED",
    "INDEPENDENT_HUMAN_EXTERNAL_EVALUATION": "NOT_ESTABLISHED",
    "RELEASE_CONTROL_READINESS": "NOT_ESTABLISHED",
    "REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER": "NOT_ESTABLISHED",
    "LICENCE_AND_IP_CLEARANCE": "NOT_ESTABLISHED",
    "SUPPORT_CONTRACT_ACTIVATION": "NOT_ACTIVATED",
    "SECURITY_OPERATIONS_READINESS": "NOT_READY",
    "RELEASE_OWNER_AND_ACCOUNTABILITY": "NOT_ESTABLISHED",
    "EXPLICIT_RELEASE_AUTHORITY": "NOT_AUTHORIZED",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_MANIFEST_RELEASE_READINESS_FAIL: {message}")


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


def main() -> int:
    manifest = load(MANIFEST)
    pack = load(PACK)
    require(CI016.is_file() and PACK_DOC.is_file(), "release-readiness governed paths missing")

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 26), "manifest must be >= v1.26")

    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current developer program missing")
    require(program.get("active_gate") == "DEV-GATE-05 — SDK Release Decision", "Gate-05 must remain active")
    require(program.get("active_phase") == "DEV-GATE-05C — Distribution & External Validation", "Gate-05C must remain active")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "program publication boundary changed")

    artifacts = [x for x in manifest.get("artifacts", []) if isinstance(x, dict) and x.get("id") == "AX-PUB-RELPACK-001"]
    require(len(artifacts) == 1, "manifest must contain exactly one AX-PUB-RELPACK-001 artifact")
    item = artifacts[0]
    require(item.get("version") == "0.1", "RELPACK artifact version mismatch")
    require(item.get("type") == "SDK_RELEASE_READINESS_EVIDENCE_AGGREGATION", "RELPACK artifact type mismatch")
    require(item.get("path") == "docs/AX-PUB-RELPACK-001_SDK_RELEASE_READINESS_EVIDENCE_PACK.md", "RELPACK artifact path mismatch")
    require(item.get("machine_readable_companion") == "artifacts/AX-PUB-RELPACK-001.json", "RELPACK companion mismatch")
    require(item.get("entrypoint") == "tools/build_sdk_release_readiness_pack.py", "RELPACK entrypoint mismatch")
    maturity = str(item.get("public_maturity", ""))
    for marker in (
        "CI-VALIDATED",
        "CURRENTLY BLOCKED",
        "4 OF 13 HARD DIMENSIONS ESTABLISHED",
        "9 BLOCKED",
        "DEV-GATE-05D NOT AUTHORIZED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in maturity, f"RELPACK maturity missing: {marker}")

    relations = {
        (str(x.get("from_id")), str(x.get("from_version")), str(x.get("relationship")), str(x.get("to_id")), str(x.get("to_version")))
        for x in manifest.get("relationships", [])
        if isinstance(x, dict) and x.get("state") == "COMPATIBLE"
    }
    for relation in (
        ("AX-PUB-RELPACK-001", "0.1", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
        ("AX-PUB-RELPACK-001", "0.1", "BUILDS_ON", "AX-PUB-EVAL-PACK-001", "0.1"),
        ("AX-PUB-RELPACK-001", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ):
        require(relation in relations, f"RELPACK relationship missing: {relation}")

    evidence_records = [x for x in manifest.get("validation_evidence", []) if isinstance(x, dict) and x.get("id") == "AX-PUB-CI-016"]
    require(len(evidence_records) == 1, "manifest must contain exactly one AX-PUB-CI-016 evidence record")
    ci016 = evidence_records[0]
    require(ci016.get("version") == "1.0", "CI-016 version mismatch")
    require(ci016.get("path") == "evidence/AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md", "CI-016 path mismatch")
    require(ci016.get("verified_head_commit") == "c9efbf2cb7a2d837c97ff378e9918500e8662e26", "CI-016 validated head mismatch")
    require(ci016.get("validation_merge_commit") == "836217925bcf7e5cff2cf8a09d1d5e7cdb244800", "CI-016 validation merge mismatch")
    require(ci016.get("workflow_run_id") == 32200229804 and ci016.get("workflow_run_number") == 3, "CI-016 workflow identity mismatch")
    require(ci016.get("job_id") == 95912269419, "CI-016 job identity mismatch")
    require(ci016.get("governance_workflow_run_id") == 32200229793 and ci016.get("governance_workflow_run_number") == 210, "CI-016 governance workflow identity mismatch")
    require(ci016.get("actions_artifact_id") == 9347211356 and ci016.get("actions_artifact_sha256") == ACTIONS_SHA, "CI-016 Actions artifact mismatch")
    require(ci016.get("required_dimension_count") == 13, "CI-016 required dimension count mismatch")
    require(ci016.get("established_dimension_count") == 4, "CI-016 established dimension count mismatch")
    require(ci016.get("blocked_dimension_count") == 9, "CI-016 blocked dimension count mismatch")
    require(ci016.get("ready_for_dev_gate_05d_authority_review") is False, "CI-016 must remain blocked before 05D authority review")
    require(ci016.get("dev_gate_05d_authorized") is False, "CI-016 must not authorize 05D")
    require(ci016.get("sdk_publication_authorized") is False, "CI-016 must not authorize publication")
    require(ci016.get("conclusion") == "SUCCESS", "CI-016 conclusion mismatch")

    current = manifest.get("current_sdk_release_readiness_aggregation")
    require(isinstance(current, dict), "current release-readiness aggregation missing")
    require(current.get("id") == "AX-PUB-RELPACK-001" and current.get("version") == "0.1", "current RELPACK identity mismatch")
    require(current.get("validation_evidence") == "AX-PUB-CI-016", "current RELPACK evidence mismatch")
    require(current.get("state") == "CI_VALIDATED_BLOCKED_BEFORE_DEV_GATE_05D_AUTHORITY_REVIEW", "current RELPACK state mismatch")
    require(current.get("required_dimension_count") == 13, "current required count mismatch")
    require(current.get("established_dimension_count") == 4, "current established count mismatch")
    require(current.get("blocked_dimension_count") == 9, "current blocked count mismatch")
    require(current.get("ready_for_dev_gate_05d_authority_review") is False, "current readiness must remain false")
    for key in (
        "external_registry_validation_established",
        "independent_human_external_evaluation_established",
        "release_control_readiness_established",
        "registry_ownership_and_trusted_publisher_established",
        "licence_and_ip_clearance_established",
        "support_contract_activated",
        "security_operations_ready",
        "release_owner_and_accountability_established",
        "dev_gate_05d_authorized",
        "supported_sdk_established",
    ):
        require(current.get(key) is False, f"current release boundary changed: {key}")
    require(current.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current publication boundary changed")

    require(pack.get("state") == "CI_VALIDATED_DEV_GATE_05D_RELEASE_READINESS_PACK_BLOCKED", "RELPACK source state mismatch")
    require(pack.get("validation_evidence") == "AX-PUB-CI-016", "RELPACK source evidence mismatch")
    disposition = pack.get("current_expected_disposition")
    require(isinstance(disposition, dict), "RELPACK source disposition missing")
    require(disposition.get("ready_for_dev_gate_05d_authority_review") is False, "RELPACK source readiness changed")
    require(disposition.get("dev_gate_05d_authorized") is False, "RELPACK source 05D authority changed")
    require(disposition.get("sdk_publication_authorized") is False, "RELPACK source publication changed")

    dims = pack.get("required_dimensions")
    require(isinstance(dims, list) and len(dims) == 13, "RELPACK must retain thirteen hard dimensions")
    blocker_states = {
        str(x.get("id")): str(x.get("expected_current_state"))
        for x in dims if isinstance(x, dict) and str(x.get("id")) in EXPECTED_BLOCKERS
    }
    require(blocker_states == EXPECTED_BLOCKERS, "RELPACK blocker state map drifted")

    boundaries = set(manifest.get("claim_boundary", []))
    for marker in (
        "RELEASE READINESS AGGREGATION PASS DOES NOT ESTABLISH RELEASE READINESS WHILE HARD DIMENSIONS ARE BLOCKED",
        "READY FOR DEV-GATE-05D AUTHORITY REVIEW DOES NOT AUTHORIZE DEV-GATE-05D OR SDK PUBLICATION",
        "DEV-GATE-05C ENGINEERING DOES NOT ESTABLISH DEV-GATE-05D RELEASE AUTHORITY",
        "SDK PUBLICATION REMAINS NOT AUTHORIZED",
    ):
        require(marker in boundaries, f"manifest claim boundary missing: {marker}")

    print(
        "AX_MANIFEST_RELEASE_READINESS_PASS manifest>=1.26 relpack=CI_VALIDATED_BLOCKED "
        "required=13 established=4 blocked=9 ready_for_05d=false "
        "gate05c=ACTIVE gate05d=NOT_AUTHORIZED supported_sdk=false publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
