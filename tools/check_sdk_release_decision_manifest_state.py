#!/usr/bin/env python3
"""Cross-check the closed DEV-GATE-05A state against the public manifest."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV007 = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_RELEASE_DECISION_MANIFEST_FAIL: {message}")


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
        head = raw.split("-", 1)[0].split(".")
        return (int(head[0]), int(head[1])) >= (major, minor)
    except (ValueError, IndexError):
        return False


def main() -> None:
    manifest = load(MANIFEST)
    dev007 = load(DEV007)

    require(dev007.get("artifact_id") == "AX-PUB-DEV-007", "DEV-007 artifact ID mismatch")
    phases = dev007.get("gate_05_phases")
    require(isinstance(phases, dict), "DEV-007 gate_05_phases missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "DEV-GATE-05A is not closed")
    require(phases.get("DEV-GATE-05B") == "ACTIVE_ENGINEERING_OBJECTIVE", "DEV-GATE-05B is not active")
    require(dev007.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "SDK publication boundary changed")
    require(dev007.get("release_authorized") is False, "release authority must remain false")

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest ID mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 19), "manifest version must be >= 1.19 for closed Gate-05A")

    artifacts = manifest.get("artifacts")
    require(isinstance(artifacts, list), "manifest artifacts must be an array")
    dev_entries = [
        item for item in artifacts
        if isinstance(item, dict) and item.get("id") == "AX-PUB-DEV-007" and item.get("version") == "0.1"
    ]
    require(len(dev_entries) == 1, "manifest must contain exactly one AX-PUB-DEV-007 v0.1 entry")
    dev_entry = dev_entries[0]
    require(dev_entry.get("state") == "CURRENT", "AX-PUB-DEV-007 manifest state must be CURRENT")
    maturity = str(dev_entry.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-05A CLOSED",
        "DEV-GATE-05B ACTIVE",
        "DIRECT CI VALIDATED PYTHON 3.11-3.14",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in maturity, f"AX-PUB-DEV-007 public maturity missing {marker}")

    relations = manifest.get("relationships")
    require(isinstance(relations, list), "manifest relationships must be an array")
    relation_set = {
        (
            item.get("from_id"), item.get("from_version"), item.get("relationship"),
            item.get("to_id"), item.get("to_version"), item.get("state")
        )
        for item in relations if isinstance(item, dict)
    }
    for required in (
        ("AX-PUB-DEV-007", "0.1", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0", "COMPATIBLE"),
        ("AX-PUB-DEV-007", "0.1", "BUILDS_ON", "AX-PUB-DEV-006", "1.0", "COMPATIBLE"),
        ("AX-PUB-DEV-007", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0", "COMPATIBLE"),
    ):
        require(required in relation_set, f"missing DEV-007 manifest relation: {required[2]}")

    evidence = manifest.get("validation_evidence")
    require(isinstance(evidence, list), "manifest validation_evidence must be an array")
    ci_entries = [item for item in evidence if isinstance(item, dict) and item.get("id") == "AX-PUB-CI-008"]
    require(len(ci_entries) == 1, "manifest must contain exactly one AX-PUB-CI-008 evidence entry")
    ci = ci_entries[0]
    require(ci.get("validated_base_commit") == "fa1e2d132071ddff195fb998d0d27a6b5b9d4e40", "CI-008 validated base mismatch")
    require(ci.get("verified_head_commit") == "7877abceda8fa6a372300fceb1ae0c124853d2b6", "CI-008 verified head mismatch")
    require(ci.get("workflow_run_id") == 32168696722, "CI-008 workflow run mismatch")
    require(ci.get("governance_workflow_run_id") == 32168696655, "CI-008 governance run mismatch")
    require(ci.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "CI-008 runtime matrix mismatch")
    require(ci.get("sdk_publication_authorized") is False, "CI-008 must not authorize SDK publication")
    require(ci.get("conclusion") == "SUCCESS", "CI-008 conclusion must be SUCCESS")

    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current_developer_program missing")
    require(program.get("active_gate") == "DEV-GATE-05 — SDK Release Decision", "active top-level gate changed")
    require(program.get("closed_phase") == "DEV-GATE-05A — Release Decision Baseline", "closed phase mismatch")
    require(program.get("active_phase") == "DEV-GATE-05B — Installable Package Candidate", "active phase mismatch")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "program publication boundary changed")

    current = manifest.get("current_sdk_release_decision_baseline")
    require(isinstance(current, dict), "current_sdk_release_decision_baseline missing")
    require(current.get("id") == "AX-PUB-DEV-007", "current release-decision baseline ID mismatch")
    require(current.get("state") == "CLOSED", "current release-decision baseline must be CLOSED")
    require(current.get("next_phase") == "DEV-GATE-05B — Installable Package Candidate", "current next phase mismatch")
    require(current.get("closure_evidence") == "AX-PUB-CI-008", "current closure evidence mismatch")
    require(current.get("registry_ownership_established") is False, "registry ownership must remain unestablished")
    require(current.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current publication boundary changed")

    boundaries = manifest.get("claim_boundary")
    require(isinstance(boundaries, list), "manifest claim_boundary must be an array")
    require(
        "DEV-GATE-05A CLOSED DOES NOT ESTABLISH SDK RELEASE AUTHORITY OR PUBLICATION" in boundaries,
        "Gate-05A closure claim boundary missing",
    )

    require(EVIDENCE.is_file(), "AX-PUB-CI-008 evidence file is missing")
    print("AX_DEV_GATE_05A_MANIFEST_CLOSED_STATE_PASS manifest=1.19 active_phase=DEV-GATE-05B sdk_publication=NOT_AUTHORIZED")


if __name__ == "__main__":
    main()
