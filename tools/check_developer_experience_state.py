#!/usr/bin/env python3
"""Validate the durable closed state for AX-PUB-DEV-003 / DEV-GATE-01.

This checker verifies Gate-01 closure evidence and its own durable state. It must
remain valid as later developer-program gates and manifest versions advance.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEV_PATH = ROOT / "artifacts" / "AX-PUB-DEV-003.json"
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DOC_PATH = ROOT / "docs" / "AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md"
PROGRAM_PATH = ROOT / "docs" / "AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md"
QUICKSTART_PATH = ROOT / "docs" / "QUICKSTART.md"
EVIDENCE_PATH = ROOT / "evidence" / "AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "validate-developer-experience.yml"

EXPECTED_RUNTIMES = ["3.10", "3.11", "3.12", "3.13"]
EXPECTED_CHECK_IDS = {
    "EAV_VALID",
    "EAV_INVALID",
    "PTK_VALID",
    "PTK_INVALID",
    "AGENT_VALID",
    "AGENT_INVALID",
    "PUBLIC_CONFORMANCE",
    "AGENT_CONFORMANCE",
    "PUBLIC_BOUNDARY",
}


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return data


def version_at_least(raw: Any, minimum: tuple[int, int]) -> bool:
    if not isinstance(raw, str):
        return False
    try:
        major, minor = raw.split(".", 1)
        return (int(major), int(minor)) >= minimum
    except (ValueError, TypeError):
        return False


def require_text(path: Path, markers: tuple[str, ...], findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"missing file: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            findings.append(f"{path.relative_to(ROOT)} missing marker: {marker}")


def fail(findings: list[str]) -> int:
    for item in findings:
        print(f"AX_DEV_GATE_01_STATE_FAIL: {item}")
    return 1


def main() -> int:
    findings: list[str] = []

    dev = load_json(DEV_PATH, findings)
    if dev is not None:
        if dev.get("artifact_id") != "AX-PUB-DEV-003":
            findings.append("developer experience artifact_id mismatch")
        if dev.get("version") != "1.0":
            findings.append("developer experience version mismatch")
        if dev.get("state") != "DEV-GATE-01_CLOSED":
            findings.append("DEV-GATE-01 machine-readable state must be CLOSED")
        if dev.get("candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("candidate runtime matrix mismatch")
        if dev.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("verified runtime matrix mismatch")
        if dev.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("Gate-01 publication disposition must remain SDK PUBLICATION NOT AUTHORIZED")
        if dev.get("package_identity_approved") is not False:
            findings.append("Gate-01 artifact must preserve its package-identity boundary")
        if dev.get("registry_publication_authorized") is not False:
            findings.append("Gate-01 artifact must preserve its registry boundary")
        if dev.get("licence_decided") is not False:
            findings.append("Gate-01 artifact must preserve its licence-decision boundary")
        checks = dev.get("checks")
        if not isinstance(checks, list) or {item.get("id") for item in checks if isinstance(item, dict)} != EXPECTED_CHECK_IDS:
            findings.append("declared nine-check inventory mismatch")
        evidence = dev.get("closure_evidence")
        if not isinstance(evidence, dict) or evidence.get("id") != "AX-PUB-CI-004":
            findings.append("closure evidence must identify AX-PUB-CI-004")
        else:
            if evidence.get("developer_experience_workflow_run_id") != 32136562796:
                findings.append("developer experience workflow run ID mismatch")
            if evidence.get("manifest_workflow_run_id") != 32136562828:
                findings.append("manifest workflow run ID mismatch")
            if evidence.get("verified_head_commit") != "8cb092ead19a5a116d51b939845da193ce91c984":
                findings.append("closure evidence verification head mismatch")

    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is not None:
        if not version_at_least(manifest.get("manifest_version"), (1, 12)):
            findings.append("manifest version must be at least 1.12 to contain DEV-GATE-01 closure")

        evidence_items = manifest.get("validation_evidence")
        ci004 = None
        if isinstance(evidence_items, list):
            ci004 = next((item for item in evidence_items if isinstance(item, dict) and item.get("id") == "AX-PUB-CI-004"), None)
        if not isinstance(ci004, dict):
            findings.append("manifest missing AX-PUB-CI-004 validation evidence")
        else:
            if ci004.get("verified_head_commit") != "8cb092ead19a5a116d51b939845da193ce91c984":
                findings.append("manifest AX-PUB-CI-004 verification head mismatch")
            if ci004.get("workflow_run_id") != 32136562796:
                findings.append("manifest AX-PUB-CI-004 developer-experience run mismatch")
            if ci004.get("governance_workflow_run_id") != 32136562828:
                findings.append("manifest AX-PUB-CI-004 governance run mismatch")
            if ci004.get("conclusion") != "SUCCESS":
                findings.append("manifest AX-PUB-CI-004 conclusion must be SUCCESS")

        current = manifest.get("current_developer_experience")
        if not isinstance(current, dict):
            findings.append("manifest current_developer_experience missing")
        else:
            if current.get("id") != "AX-PUB-DEV-003" or current.get("version") != "1.0":
                findings.append("manifest current developer experience identity mismatch")
            if current.get("state") != "CLOSED":
                findings.append("manifest current developer experience must remain CLOSED")
            if current.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
                findings.append("manifest verified runtime matrix mismatch")
            if current.get("closure_evidence") != "AX-PUB-CI-004":
                findings.append("manifest developer experience closure evidence mismatch")

    require_text(
        EVIDENCE_PATH,
        (
            "AX-PUB-CI-004",
            "32136562796",
            "32136562828",
            "Python 3.10",
            "Python 3.11",
            "Python 3.12",
            "Python 3.13",
            "SUCCESS",
        ),
        findings,
    )
    require_text(
        DOC_PATH,
        (
            "DEV-GATE-01 CLOSED",
            "AX-PUB-CI-004",
            "Python 3.10",
            "Python 3.11",
            "Python 3.12",
            "Python 3.13",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
        findings,
    )
    require_text(
        PROGRAM_PATH,
        (
            "DEV-GATE-01: CLOSED",
            "AX-PUB-CI-004",
            "REPRODUCIBLE",
        ),
        findings,
    )
    require_text(
        QUICKSTART_PATH,
        (
            "DEV-GATE-01: CLOSED",
            "AX-PUB-CI-004",
            "VERIFIED RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13",
        ),
        findings,
    )
    require_text(
        WORKFLOW_PATH,
        (
            "tools/check_developer_experience_state.py",
            "Validate closed Gate-01 governance state",
        ),
        findings,
    )

    if findings:
        return fail(findings)
    print("AX_DEV_GATE_01_CLOSED_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
