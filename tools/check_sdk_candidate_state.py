#!/usr/bin/env python3
"""Validate the durable closed state for AX-PUB-DEV-004 / DEV-GATE-02."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "AX-PUB-DEV-004.json"
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DOC = ROOT / "docs" / "AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md"
PROGRAM = ROOT / "docs" / "AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md"
QUICKSTART = ROOT / "docs" / "QUICKSTART.md"
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md"
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
GATE_RANK = {
    "DEV-GATE-00 — Contract Baseline": 0,
    "DEV-GATE-01 — Reproducible Developer Experience": 1,
    "DEV-GATE-02 — SDK Candidate": 2,
    "DEV-GATE-03 — Supply-Chain & Release Candidate": 3,
    "DEV-GATE-04 — External Evaluation Readiness": 4,
    "DEV-GATE-05 — SDK Release Decision": 5,
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


def version_at_least(raw: Any, minimum: tuple[int, int]) -> bool:
    if not isinstance(raw, str):
        return False
    try:
        base = raw.split("-", 1)[0]
        parts = base.split(".")
        return (int(parts[0]), int(parts[1])) >= minimum
    except (ValueError, TypeError, IndexError):
        return False


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
        if data.get("state") != "DEV-GATE-02_CLOSED":
            findings.append("DEV-GATE-02 machine-readable state must be CLOSED")
        if data.get("candidate_version") != "0.1.0-candidate":
            findings.append("candidate version mismatch")
        if data.get("sdk_candidate_established") is not True:
            findings.append("SDK candidate must be established after Gate-02 closure")
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
        if data.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("verified candidate runtime matrix mismatch")

        mappings = data.get("contract_mapping")
        observed: set[tuple[str, str, str, str]] = set()
        if isinstance(mappings, list):
            for item in mappings:
                if isinstance(item, dict):
                    observed.add((
                        str(item.get("contract_id")),
                        str(item.get("contract_version")),
                        str(item.get("schema_id")),
                        str(item.get("reference_validator_id")),
                    ))
        if observed != EXPECTED_CONTRACTS:
            findings.append("candidate contract mapping mismatch")

        closure = data.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-005":
            findings.append("closure evidence must identify AX-PUB-CI-005")
        else:
            if closure.get("validated_base_commit") != "4d4bb5e3bc7c4a104361e2950618badb15d9ff1f":
                findings.append("closure validated base mismatch")
            if closure.get("verified_head_commit") != "74285009eb7ba151291e56490f60e483cc8dba85":
                findings.append("closure verified head mismatch")
            if closure.get("sdk_candidate_workflow_run_id") != 32144445255:
                findings.append("SDK candidate workflow run mismatch")
            if closure.get("manifest_workflow_run_id") != 32144445221:
                findings.append("manifest workflow run mismatch")
            if closure.get("conclusion") != "SUCCESS":
                findings.append("closure evidence conclusion must be SUCCESS")

    manifest = load_json(MANIFEST, findings)
    if manifest is not None:
        if not version_at_least(manifest.get("manifest_version"), (1, 14)):
            findings.append("manifest version must be at least 1.14 for DEV-GATE-02 closure")
        evidence_items = manifest.get("validation_evidence")
        ci005 = None
        if isinstance(evidence_items, list):
            ci005 = next((item for item in evidence_items if isinstance(item, dict) and item.get("id") == "AX-PUB-CI-005"), None)
        if not isinstance(ci005, dict):
            findings.append("manifest missing AX-PUB-CI-005 validation evidence")
        else:
            if ci005.get("verified_head_commit") != "74285009eb7ba151291e56490f60e483cc8dba85":
                findings.append("manifest AX-PUB-CI-005 verification head mismatch")
            if ci005.get("workflow_run_id") != 32144445255:
                findings.append("manifest AX-PUB-CI-005 SDK candidate run mismatch")
            if ci005.get("governance_workflow_run_id") != 32144445221:
                findings.append("manifest AX-PUB-CI-005 governance run mismatch")
            if ci005.get("conclusion") != "SUCCESS":
                findings.append("manifest AX-PUB-CI-005 conclusion must be SUCCESS")

        program = manifest.get("current_developer_program")
        if not isinstance(program, dict):
            findings.append("manifest current_developer_program missing")
        else:
            closed_gate = program.get("closed_gate")
            active_gate = program.get("active_gate")
            if GATE_RANK.get(str(closed_gate), -1) < 2:
                findings.append("developer program must preserve DEV-GATE-02 as closed or later")
            if GATE_RANK.get(str(active_gate), -1) < 3:
                findings.append("developer program active gate must be DEV-GATE-03 or later")
            if program.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
                findings.append("developer program SDK publication boundary mismatch")

        candidate = manifest.get("current_sdk_candidate")
        if not isinstance(candidate, dict):
            findings.append("manifest current_sdk_candidate missing")
        else:
            if candidate.get("state") != "CLOSED":
                findings.append("manifest current SDK candidate state must be CLOSED")
            if candidate.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
                findings.append("manifest verified SDK candidate runtime matrix mismatch")
            if candidate.get("closure_evidence") != "AX-PUB-CI-005":
                findings.append("manifest SDK candidate closure evidence mismatch")

    for path in (MODULE, README, TESTS, CONFORMANCE, BOUNDARY, WORKFLOW, EVIDENCE):
        require_file(path, findings)

    require_markers(
        DOC,
        (
            "DEV-GATE-02 CLOSED",
            "SDK CANDIDATE ESTABLISHED",
            "AX-PUB-CI-005",
            "Python 3.10",
            "Python 3.11",
            "Python 3.12",
            "Python 3.13",
            "AX_DEV_GATE_02_CLOSED_STATE_PASS",
            "DEV-GATE-03 — Supply-Chain & Release Candidate",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
        findings,
    )
    require_markers(
        PROGRAM,
        (
            "DEV-GATE-02: CLOSED",
            "SDK CANDIDATE: ESTABLISHED",
            "AX-PUB-CI-005",
            "CURRENT ENGINEERING OBJECTIVE: DEV-GATE-",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
        findings,
    )
    require_markers(
        QUICKSTART,
        (
            "DEV-GATE-02: CLOSED",
            "SDK CANDIDATE: ESTABLISHED",
            "AX-PUB-CI-005",
            "CURRENT ENGINEERING OBJECTIVE: DEV-GATE-",
            "SDK PUBLICATION: NOT AUTHORIZED",
        ),
        findings,
    )
    require_markers(
        README,
        (
            "REPOSITORY-LOCAL",
            "NON-DISTRIBUTABLE",
            "SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK",
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
        EVIDENCE,
        (
            "AX-PUB-CI-005",
            "32144445255",
            "32144445221",
            "Python 3.10",
            "Python 3.11",
            "Python 3.12",
            "Python 3.13",
            "SUCCESS",
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
            "Validate closed DEV-GATE-02 governance state",
        ),
        findings,
    )

    if findings:
        for item in findings:
            print(f"AX_DEV_GATE_02_STATE_FAIL: {item}")
        return 1
    print("AX_DEV_GATE_02_CLOSED_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
