#!/usr/bin/env python3
"""Validate AX-PUB-DEV-002 developer contract baseline consistency."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASELINE_DOC = ROOT / "docs" / "AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md"
BASELINE_JSON = ROOT / "artifacts" / "AX-PUB-DEV-002.json"
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"

REQUIRED_ERRORS = {
    "AXDEV-CONTRACT-INVALID",
    "AXDEV-VERSION-UNSUPPORTED",
    "AXDEV-EVIDENCE-INSUFFICIENT",
    "AXDEV-AUTHORITY-UNESTABLISHED",
    "AXDEV-AUTHORITY-INACTIVE",
    "AXDEV-AUTHORITY-SCOPE-VIOLATION",
    "AXDEV-TEMPORAL-CUTOFF-VIOLATION",
    "AXDEV-PROVENANCE-INCOMPLETE",
    "AXDEV-CONFLICT-UNRESOLVED",
    "AXDEV-VERIFICATION-FAILED",
    "AXDEV-VERIFICATION-INCONCLUSIVE",
    "AXDEV-EXECUTION-NOT-VERIFIED",
    "AXDEV-UNSUPPORTED-OPERATION",
}

EXPECTED_PATHS = {
    "EAV": ("AX-PUB-SPEC-002", "AX-PUB-SCHEMA-001", "AX-PUB-REF-001", "AX-PUB-TEST-001"),
    "POINT_IN_TIME_PROVENANCE": ("AX-PUB-SPEC-003", "AX-PUB-SCHEMA-002", "AX-PUB-REF-002", "AX-PUB-TEST-001"),
    "AGENT_AUTHORITY_TOOL_USE": ("AX-PUB-SPEC-004", "AX-PUB-SCHEMA-003", "AX-PUB-REF-003", "AX-PUB-TEST-002"),
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


def fail(findings: list[str]) -> int:
    for item in findings:
        print(f"AX_DEVELOPER_CONTRACT_BASELINE_FAIL: {item}")
    return 1


def main() -> int:
    findings: list[str] = []

    if not BASELINE_DOC.is_file():
        findings.append("developer contract baseline document missing")
    else:
        text = BASELINE_DOC.read_text(encoding="utf-8")
        for marker in (
            "AX-PUB-DEV-002",
            "`1.0`",
            "DEV-GATE-00",
            "SDK PUBLICATION NOT AUTHORIZED",
            "Baseline Error Taxonomy",
            "Public / Private Dependency Boundary",
            "DEV-GATE-01 — REPRODUCIBLE DEVELOPER EXPERIENCE",
        ):
            if marker not in text:
                findings.append(f"baseline document missing marker: {marker}")
        for error_id in REQUIRED_ERRORS:
            if error_id not in text:
                findings.append(f"baseline document missing error taxonomy id: {error_id}")

    baseline = load_json(BASELINE_JSON, findings)
    if baseline is not None:
        if baseline.get("artifact_id") != "AX-PUB-DEV-002":
            findings.append("baseline artifact_id mismatch")
        if baseline.get("version") != "1.0":
            findings.append("baseline version mismatch")
        if baseline.get("state") not in {"DEV-GATE-00_CANDIDATE", "DEV-GATE-00_CLOSED"}:
            findings.append("baseline gate state invalid")
        if baseline.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("baseline SDK publication disposition mismatch")
        if baseline.get("sdk_semver_active") is not False:
            findings.append("SDK SemVer must remain inactive at DEV-GATE-00")
        if baseline.get("package_identity_approved") is not False:
            findings.append("package identity must remain unapproved at DEV-GATE-00")
        if baseline.get("registry_publication_authorized") is not False:
            findings.append("registry publication must remain unauthorized at DEV-GATE-00")
        if baseline.get("licence_decided") is not False:
            findings.append("licence decision must remain false at DEV-GATE-00")

        errors = baseline.get("error_taxonomy")
        if not isinstance(errors, list):
            findings.append("error_taxonomy must be an array")
        else:
            if len(errors) != len(set(errors)):
                findings.append("error_taxonomy contains duplicate identifiers")
            missing = REQUIRED_ERRORS - set(errors)
            for item in sorted(missing):
                findings.append(f"required error taxonomy identifier missing: {item}")

        paths = baseline.get("contract_paths")
        if not isinstance(paths, list):
            findings.append("contract_paths must be an array")
        else:
            observed: dict[str, tuple[str, str, str, str]] = {}
            for item in paths:
                if not isinstance(item, dict):
                    findings.append("contract_paths entry must be an object")
                    continue
                try:
                    observed[str(item["path_id"])] = (
                        str(item["specification"]["id"]),
                        str(item["schema"]["id"]),
                        str(item["reference"]["id"]),
                        str(item["conformance"]["id"]),
                    )
                    for role in ("specification", "schema", "reference", "conformance"):
                        if item[role].get("version") != "1.0":
                            findings.append(f"{item.get('path_id')} {role} version must be 1.0")
                except (KeyError, TypeError):
                    findings.append("contract_paths entry malformed")
            if observed != EXPECTED_PATHS:
                findings.append("contract path inventory mismatch")

        boundary = baseline.get("public_private_boundary")
        if not isinstance(boundary, dict):
            findings.append("public_private_boundary must be an object")
        else:
            for key in (
                "private_repository_dependency_allowed",
                "private_endpoint_dependency_allowed",
                "private_credential_dependency_allowed",
                "private_package_index_dependency_allowed",
                "unpublished_schema_dependency_allowed",
            ):
                if boundary.get(key) is not False:
                    findings.append(f"{key} must be false")

    manifest = load_json(MANIFEST, findings)
    if manifest is not None:
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
        registered = [a for a in artifacts if isinstance(a, dict) and a.get("id") == "AX-PUB-DEV-002" and a.get("version") == "1.0"]
        if len(registered) != 1:
            findings.append("manifest must register AX-PUB-DEV-002 v1.0 exactly once")
        current = manifest.get("current_developer_contract_baseline")
        if not isinstance(current, dict) or current.get("id") != "AX-PUB-DEV-002" or current.get("version") != "1.0":
            findings.append("manifest current_developer_contract_baseline mismatch")

    if findings:
        return fail(findings)

    print("AX_DEVELOPER_CONTRACT_BASELINE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
