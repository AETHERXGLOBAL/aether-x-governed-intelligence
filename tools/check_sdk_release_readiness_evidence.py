#!/usr/bin/env python3
"""Validate AX-PUB-CI-016 without upgrading any release authority state."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md"
CONTRACT = ROOT / "artifacts" / "AX-PUB-RELPACK-001.json"

EXPECTED_ESTABLISHED = {
    "ENGINEERING_CANDIDATE_IDENTITY",
    "PUBLIC_API_CONTRACT",
    "EXACT_ARTIFACT_RUNTIME_VALIDATION",
    "SUPPLY_CHAIN_PROVENANCE_SBOM",
}
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
    raise SystemExit(f"AX_RELEASE_PACK_EVIDENCE_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(EVIDENCE.is_file(), "missing AX-PUB-CI-016 evidence")
    require(CONTRACT.is_file(), "missing AX-PUB-RELPACK-001 contract")

    text = EVIDENCE.read_text(encoding="utf-8")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    required_markers = [
        "**Evidence ID:** `AX-PUB-CI-016`",
        "Candidate bootstrap PR: #57",
        "Bootstrap merge commit: 3db51160558335fc9450a17d542e040aa935a61a",
        "Validation PR: #58",
        "Validation head: c9efbf2cb7a2d837c97ff378e9918500e8662e26",
        "GitHub pull-request merge-test commit: 481c80453a40c632aec6b4b5f8783489fdb4c639",
        "Validation merge commit on main: 836217925bcf7e5cff2cf8a09d1d5e7cdb244800",
        "Workflow run ID: 32200229804",
        "Workflow run number: 3",
        "Job ID: 95912269419",
        "Runtime: CPython 3.14.7",
        "Workflow run ID: 32200229793",
        "Workflow run number: 210",
        "required = 13",
        "established = 4",
        "blocked = 9",
        "ready_for_05d = false",
        "Artifact ID: 9347211356",
        "Artifact size: 1915 bytes",
        "e9614ca5b70667e6d2218d1f19c764ce2cf09ada13764282c5758cf1865fa331",
        "DEV-GATE-05D NOT AUTHORIZED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ]
    for marker in required_markers:
        require(marker in text, f"missing evidence marker: {marker}")

    required_dimensions = contract.get("required_dimensions")
    require(isinstance(required_dimensions, list), "contract required_dimensions missing")
    require(len(required_dimensions) == 13, "contract must retain thirteen hard dimensions")

    by_id = {
        item.get("id"): item.get("expected_current_state")
        for item in required_dimensions
        if isinstance(item, dict)
    }
    require(set(by_id) == EXPECTED_ESTABLISHED | set(EXPECTED_BLOCKERS), "dimension identity set drifted")

    for dimension in EXPECTED_ESTABLISHED:
        require(dimension in text, f"established dimension missing from evidence: {dimension}")

    for dimension, state in EXPECTED_BLOCKERS.items():
        require(by_id.get(dimension) == state, f"contract blocker state drifted: {dimension}")
        require(f"{dimension} = {state}" in text, f"evidence blocker state missing: {dimension}")

    disposition = contract.get("current_expected_disposition")
    require(isinstance(disposition, dict), "current_expected_disposition missing")
    require(disposition.get("ready_for_dev_gate_05d_authority_review") is False, "contract must remain blocked before 05D review")
    require(disposition.get("dev_gate_05d_authorized") is False, "05D must remain unauthorized")
    require(disposition.get("sdk_publication_authorized") is False, "SDK publication must remain unauthorized")

    print(
        "AX_RELEASE_PACK_EVIDENCE_PASS "
        "ci=AX-PUB-CI-016 run=32200229804 job=95912269419 "
        "required=13 established=4 blocked=9 ready_for_05d=false "
        "dev_gate_05d=NOT_AUTHORIZED sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
