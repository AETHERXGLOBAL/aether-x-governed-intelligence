#!/usr/bin/env python3
"""Cross-check closed DEV-GATE-05B state against manifest v1.20+."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV007 = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
DEV008 = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md"

WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
ARTIFACT_SHA = "9b2e050d59146e2b768cb5f9468b2035c078aa1abbb4e0fd0ac4148e8d58d4a2"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_INSTALLABLE_PACKAGE_MANIFEST_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain an object")
    return data


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    if not isinstance(raw, str):
        return False
    try:
        parts = raw.split("-", 1)[0].split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        return False


def main() -> None:
    manifest = load(MANIFEST)
    dev007 = load(DEV007)
    dev008 = load(DEV008)

    phases = dev007.get("gate_05_phases")
    require(isinstance(phases, dict), "DEV-007 Gate-05 phases missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "Gate-05A must remain closed")
    require(phases.get("DEV-GATE-05B") == "CLOSED", "Gate-05B must be closed")
    require(phases.get("DEV-GATE-05C") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C must be active")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "Gate-05D must remain unauthorized")
    require(dev007.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "DEV-007 publication boundary changed")
    require(dev007.get("release_authorized") is False, "DEV-007 release authority must remain false")

    require(dev008.get("artifact_id") == "AX-PUB-DEV-008", "DEV-008 ID mismatch")
    require(dev008.get("phase") == "DEV-GATE-05B" and dev008.get("phase_state") == "CLOSED", "DEV-008 closed state mismatch")
    require(dev008.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "DEV-008 next phase mismatch")
    require(dev008.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "DEV-008 publication boundary changed")
    require(dev008.get("distribution_authorized") is False, "DEV-008 distribution authority must remain false")
    require(dev008.get("license_granted") is False, "DEV-008 licence must remain ungranted")
    require(dev008.get("supported_sdk_established") is False, "DEV-008 must not establish a supported SDK")
    closure = dev008.get("closure_evidence")
    require(isinstance(closure, dict) and closure.get("id") == "AX-PUB-CI-009" and closure.get("conclusion") == "SUCCESS", "DEV-008 closure evidence mismatch")

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest ID mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 20), "manifest version must be >=1.20 for closed Gate-05B")

    artifacts = manifest.get("artifacts")
    require(isinstance(artifacts, list), "manifest artifacts missing")
    entries = [x for x in artifacts if isinstance(x, dict) and x.get("id") == "AX-PUB-DEV-008" and x.get("version") == "0.1"]
    require(len(entries) == 1, "manifest must contain exactly one AX-PUB-DEV-008 v0.1")
    entry = entries[0]
    require(entry.get("state") == "CURRENT", "DEV-008 manifest state must be CURRENT")
    maturity = str(entry.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-05B CLOSED",
        "DETERMINISTIC INSTALLABLE PACKAGE CANDIDATE",
        "PYTHON 3.11-3.14",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in maturity, f"DEV-008 maturity missing {marker}")

    relations = manifest.get("relationships")
    require(isinstance(relations, list), "manifest relationships missing")
    relation_set = {
        (x.get("from_id"), x.get("from_version"), x.get("relationship"), x.get("to_id"), x.get("to_version"), x.get("state"))
        for x in relations if isinstance(x, dict)
    }
    for expected in (
        ("AX-PUB-DEV-008", "0.1", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0", "COMPATIBLE"),
        ("AX-PUB-DEV-008", "0.1", "BUILDS_ON", "AX-PUB-DEV-007", "0.1", "COMPATIBLE"),
        ("AX-PUB-DEV-008", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0", "COMPATIBLE"),
    ):
        require(expected in relation_set, f"missing DEV-008 relation {expected[2]}")

    evidence = manifest.get("validation_evidence")
    require(isinstance(evidence, list), "manifest validation_evidence missing")
    ci_entries = [x for x in evidence if isinstance(x, dict) and x.get("id") == "AX-PUB-CI-009"]
    require(len(ci_entries) == 1, "manifest must contain exactly one AX-PUB-CI-009")
    ci = ci_entries[0]
    expected_ci = {
        "published_baseline_commit": "774abcce340c3fbaf3481ab5244ee1d41b88243c",
        "verification_head_commit": "63477bb11124aebbad4034587a366d5ef882b3c2",
        "verification_merge_commit": "3267c66681e417bf5eb0f8a384e8c2d992d266c0",
        "verification_pr": 36,
        "workflow_run_id": 32171606094,
        "workflow_run_number": 19,
        "job_id": 95823835258,
        "governance_workflow_run_id": 32171606079,
        "governance_workflow_run_number": 168,
        "wheel_sha256": WHEEL_SHA,
        "sdist_sha256": SDIST_SHA,
        "actions_artifact_sha256": ARTIFACT_SHA,
        "conclusion": "SUCCESS",
    }
    for key, value in expected_ci.items():
        require(ci.get(key) == value, f"CI-009 manifest mismatch for {key}")
    require(ci.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "CI-009 runtime matrix mismatch")
    require(ci.get("sdk_publication_authorized") is False, "CI-009 must not authorize SDK publication")

    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current_developer_program missing")
    require(program.get("active_gate") == "DEV-GATE-05 — SDK Release Decision", "top-level Gate-05 must remain active")
    require(program.get("closed_phase") == "DEV-GATE-05B — Installable Package Candidate", "closed phase mismatch")
    require(program.get("active_phase") == "DEV-GATE-05C — Distribution & External Validation", "active phase mismatch")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "program publication boundary changed")

    current = manifest.get("current_installable_package_candidate")
    require(isinstance(current, dict), "current_installable_package_candidate missing")
    require(current.get("id") == "AX-PUB-DEV-008" and current.get("state") == "CLOSED", "current installable package state mismatch")
    require(current.get("closure_evidence") == "AX-PUB-CI-009", "current installable package closure evidence mismatch")
    require(current.get("wheel_sha256") == WHEEL_SHA, "current wheel digest mismatch")
    require(current.get("sdist_sha256") == SDIST_SHA, "current sdist digest mismatch")
    require(current.get("registry_ownership_established") is False, "registry ownership must remain unestablished")
    require(current.get("license_granted") is False, "licence must remain ungranted")
    require(current.get("supported_sdk_established") is False, "supported SDK must remain unestablished")
    require(current.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current package publication boundary changed")

    boundaries = manifest.get("claim_boundary")
    require(isinstance(boundaries, list), "manifest claim_boundary missing")
    require("DEV-GATE-05B CLOSED DOES NOT ESTABLISH REGISTRY OWNERSHIP, A SOFTWARE LICENCE, A SUPPORTED SDK OR SDK PUBLICATION" in boundaries, "Gate-05B claim boundary missing")

    require(EVIDENCE.is_file(), "AX-PUB-CI-009 evidence file missing")
    print(f"AX_DEV_GATE_05B_MANIFEST_CLOSED_STATE_PASS manifest={manifest.get('manifest_version')} active_phase=DEV-GATE-05C sdk_publication=NOT_AUTHORIZED")


if __name__ == "__main__":
    main()
