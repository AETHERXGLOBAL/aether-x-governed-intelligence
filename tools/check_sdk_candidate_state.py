#!/usr/bin/env python3
"""Validate AX-PUB-DEV-004 candidate-state governance coherence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "AX-PUB-DEV-004.json"
DOC = ROOT / "docs" / "AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md"
MODULE = ROOT / "sdk-candidate" / "python" / "aetherx_sdk_candidate.py"
README = ROOT / "sdk-candidate" / "python" / "README.md"
TESTS = ROOT / "sdk-candidate" / "python" / "tests" / "test_sdk_candidate.py"
CONFORMANCE = ROOT / "sdk-candidate" / "python" / "run_candidate_conformance.py"
BOUNDARY = ROOT / "tools" / "check_sdk_candidate_boundary.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-sdk-candidate.yml"

EXPECTED_RUNTIMES = ["3.10", "3.11", "3.12", "3.13"]
EXPECTED_OPERATIONS = [
    "supported_contracts",
    "validate",
    "validate_eav",
    "validate_point_in_time",
    "validate_agent_authority",
]
EXPECTED_CONTRACTS = {
    ("AX-PUB-SPEC-002", "1.0", "AX-PUB-SCHEMA-001", "AX-PUB-REF-001"),
    ("AX-PUB-SPEC-003", "1.0", "AX-PUB-SCHEMA-002", "AX-PUB-REF-002"),
    ("AX-PUB-SPEC-004", "1.0", "AX-PUB-SCHEMA-003", "AX-PUB-REF-003"),
}


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain an object")
        return None
    return data


def require_file(path: Path, findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"missing file: {path.relative_to(ROOT)}")


def require_markers(path: Path, markers: tuple[str, ...], findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"missing file: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            findings.append(f"{path.relative_to(ROOT)} missing marker: {marker}")


def main() -> int:
    findings: list[str] = []
    data = load_json(ARTIFACT, findings)
    if data is not None:
        if data.get("artifact_id") != "AX-PUB-DEV-004":
            findings.append("artifact_id mismatch")
        if data.get("version") != "1.0":
            findings.append("artifact version mismatch")
        if data.get("state") != "DEV-GATE-02_CANDIDATE_NOT_ESTABLISHED":
            findings.append("candidate state must remain DEV-GATE-02_CANDIDATE_NOT_ESTABLISHED")
        if data.get("candidate_version") != "0.1.0-candidate":
            findings.append("candidate version mismatch")
        if data.get("sdk_candidate_established") is not False:
            findings.append("SDK candidate must not yet be established")
        if data.get("package_identity_status") != "NOT APPROVED":
            findings.append("package identity must remain NOT APPROVED")
        if data.get("registry_status") != "NOT AUTHORIZED":
            findings.append("registry must remain NOT AUTHORIZED")
        if data.get("distribution_metadata_present") is not False:
            findings.append("distribution metadata must remain absent")
        if data.get("licence_decided") is not False:
            findings.append("public SDK licence must remain undecided")
        if data.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("SDK publication disposition mismatch")
        if data.get("supported_candidate_operations") != EXPECTED_OPERATIONS:
            findings.append("candidate operation inventory mismatch")
        if data.get("candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("candidate runtime matrix mismatch")
        if data.get("verified_runtime_matrix") != []:
            findings.append("candidate runtime matrix must remain unverified before CI evidence")

        mappings = data.get("contract_mapping")
        observed: set[tuple[str, str, str, str]] = set()
        if isinstance(mappings, list):
            for item in mappings:
                if isinstance(item, dict):
                    observed.add(
                        (
                            str(item.get("contract_id")),
                            str(item.get("contract_version")),
                            str(item.get("schema_id")),
                            str(item.get("reference_validator_id")),
                        )
                    )
        if observed != EXPECTED_CONTRACTS:
            findings.append("candidate contract mapping mismatch")

    for path in (MODULE, README, TESTS, CONFORMANCE, BOUNDARY, WORKFLOW):
        require_file(path, findings)

    require_markers(
        DOC,
        (
            "DEV-GATE-02 CANDIDATE",
            "SDK CANDIDATE NOT YET ESTABLISHED",
            "SDK PUBLICATION NOT AUTHORIZED",
            "0.1.0-candidate",
            "AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9",
            "DEV-GATE-03 — Supply-Chain & Release Candidate",
        ),
        findings,
    )
    require_markers(
        README,
        (
            "REPOSITORY-LOCAL",
            "NON-DISTRIBUTABLE",
            "SDK CANDIDATE CODE PRESENT ≠ SDK CANDIDATE ESTABLISHED",
            "AX_SDK_CANDIDATE_BOUNDARY_PASS",
        ),
        findings,
    )
    require_markers(
        MODULE,
        (
            'SDK_CANDIDATE_VERSION = "0.1.0-candidate"',
            '"AX-PUB-SPEC-002"',
            '"AX-PUB-SPEC-003"',
            '"AX-PUB-SPEC-004"',
            "AXDEV-VERSION-UNSUPPORTED",
            "AXDEV-UNSUPPORTED-OPERATION",
        ),
        findings,
    )
    require_markers(
        WORKFLOW,
        (
            "Python 3.10",
            "Python 3.11",
            "Python 3.12",
            "Python 3.13",
            "Run SDK candidate unit tests",
            "Run SDK candidate conformance",
            "Validate SDK candidate public boundary",
            "Validate DEV-GATE-02 candidate state",
        ),
        findings,
    )

    if findings:
        for item in findings:
            print(f"AX_DEV_GATE_02_CANDIDATE_STATE_FAIL: {item}")
        return 1
    print("AX_DEV_GATE_02_CANDIDATE_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
