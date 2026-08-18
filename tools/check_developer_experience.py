#!/usr/bin/env python3
"""Validate the AX-PUB-DEV-003 public developer experience.

Uses only the Python standard library and public repository files.
This is a reproducibility check, not an SDK or production-readiness test.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

VALID_CHECKS = [
    {
        "id": "EAV_VALID",
        "argv": [
            "reference-implementations/eav-contract-validator/validator.py",
            "reference-implementations/eav-contract-validator/examples/valid_bundle.json",
        ],
        "marker": "AX_EAV_REFERENCE_VALIDATION_PASS",
    },
    {
        "id": "PTK_VALID",
        "argv": [
            "reference-implementations/point-in-time-knowledge-validator/validator.py",
            "reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json",
        ],
        "marker": "AX_PTK_REFERENCE_VALIDATION_PASS",
    },
    {
        "id": "AGENT_VALID",
        "argv": [
            "reference-implementations/agent-tool-authority-validator/validator.py",
            "reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json",
        ],
        "marker": "AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS",
    },
]

INVALID_CHECKS = [
    {
        "id": "EAV_INVALID",
        "argv": [
            "reference-implementations/eav-contract-validator/validator.py",
            "reference-implementations/eav-contract-validator/examples/invalid_bundle.json",
            "--json",
        ],
    },
    {
        "id": "PTK_INVALID",
        "argv": [
            "reference-implementations/point-in-time-knowledge-validator/validator.py",
            "reference-implementations/point-in-time-knowledge-validator/examples/invalid_envelope.json",
            "--json",
        ],
    },
    {
        "id": "AGENT_INVALID",
        "argv": [
            "reference-implementations/agent-tool-authority-validator/validator.py",
            "reference-implementations/agent-tool-authority-validator/examples/invalid_envelope.json",
            "--json",
        ],
    },
]

CONFORMANCE_CHECKS = [
    {
        "id": "PUBLIC_CONFORMANCE",
        "argv": ["conformance/AX-PUB-TEST-001/run_conformance.py"],
        "markers": ["AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15"],
    },
    {
        "id": "AGENT_CONFORMANCE",
        "argv": ["conformance/AX-PUB-TEST-002/run_conformance.py"],
        "markers": ["AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10"],
    },
    {
        "id": "PUBLIC_BOUNDARY",
        "argv": ["tools/check_public_conformance_boundary.py"],
        "markers": ["AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS"],
    },
]


def invoke(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *argv],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )


def combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stdout or "") + (result.stderr or "")


def valid_check(spec: dict[str, Any]) -> dict[str, Any]:
    result = invoke(spec["argv"])
    output = combined_output(result)
    passed = result.returncode == 0 and spec["marker"] in output
    return {
        "id": spec["id"],
        "kind": "VALID_REFERENCE_EXAMPLE",
        "status": "PASS" if passed else "FAIL",
        "returncode": result.returncode,
        "expected_marker": spec["marker"],
        "marker_observed": spec["marker"] in output,
    }


def invalid_check(spec: dict[str, Any]) -> dict[str, Any]:
    result = invoke(spec["argv"])
    parsed: dict[str, Any] | None = None
    parse_error: str | None = None
    try:
        candidate = json.loads(result.stdout)
        if isinstance(candidate, dict):
            parsed = candidate
        else:
            parse_error = "JSON output was not an object"
    except json.JSONDecodeError as exc:
        parse_error = str(exc)

    findings = parsed.get("findings") if isinstance(parsed, dict) else None
    passed = (
        result.returncode != 0
        and isinstance(parsed, dict)
        and parsed.get("status") == "FAIL"
        and isinstance(findings, list)
        and len(findings) >= 1
    )
    return {
        "id": spec["id"],
        "kind": "INVALID_REFERENCE_EXAMPLE",
        "status": "PASS" if passed else "FAIL",
        "returncode": result.returncode,
        "expected_json_status": "FAIL",
        "observed_json_status": parsed.get("status") if isinstance(parsed, dict) else None,
        "finding_count": len(findings) if isinstance(findings, list) else 0,
        "json_parse_error": parse_error,
    }


def conformance_check(spec: dict[str, Any]) -> dict[str, Any]:
    result = invoke(spec["argv"])
    output = combined_output(result)
    observed = {marker: marker in output for marker in spec["markers"]}
    passed = result.returncode == 0 and all(observed.values())
    return {
        "id": spec["id"],
        "kind": "PUBLIC_CONFORMANCE_OR_BOUNDARY",
        "status": "PASS" if passed else "FAIL",
        "returncode": result.returncode,
        "markers": observed,
    }


def runtime_record() -> dict[str, Any]:
    version = sys.version_info
    return {
        "implementation": sys.implementation.name,
        "major": version.major,
        "minor": version.minor,
        "micro": version.micro,
        "declared_candidate_runtime": f"{version.major}.{version.minor}" in {"3.10", "3.11", "3.12", "3.13"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AX-PUB-DEV-003 reproducible developer experience")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    for spec in VALID_CHECKS:
        checks.append(valid_check(spec))
    for spec in INVALID_CHECKS:
        checks.append(invalid_check(spec))
    for spec in CONFORMANCE_CHECKS:
        checks.append(conformance_check(spec))

    runtime = runtime_record()
    passed = runtime["declared_candidate_runtime"] and all(item["status"] == "PASS" for item in checks)
    report = {
        "artifact_id": "AX-PUB-DEV-003",
        "version": "1.0",
        "runtime": runtime,
        "check_count": len(checks),
        "conforming_checks": sum(item["status"] == "PASS" for item in checks),
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "claim_boundary": "DEVELOPER EXPERIENCE PASS DOES NOT ESTABLISH SDK CANDIDACY OR PRODUCTION READINESS",
    }

    if args.json_output:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for item in checks:
            print(f"{item['status']} {item['id']} kind={item['kind']}")
        marker = "AX_DEVELOPER_EXPERIENCE_PASS" if passed else "AX_DEVELOPER_EXPERIENCE_FAIL"
        print(
            f"{marker} "
            f"python={runtime['major']}.{runtime['minor']}.{runtime['micro']} "
            f"checks={len(checks)} conforming={report['conforming_checks']}"
        )

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
