#!/usr/bin/env python3
"""Validate machine-readable output from run_external_evaluation.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPECTED_CHECKS = {
    "developer-experience",
    "sdk-candidate-unit-tests",
    "sdk-candidate-example",
    "sdk-candidate-conformance",
    "sdk-candidate-public-boundary",
    "sdk-candidate-governance-state",
    "release-candidate-governance-state",
    "artifact-manifest-governance",
}
VERIFIED_PYTHON = {"3.10", "3.11", "3.12", "3.13"}
REQUIRED_BOUNDARIES = {
    "READINESS RUN PASS DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
    "EXTERNAL EVALUATION READINESS DOES NOT ESTABLISH ADOPTION",
    "SDK CANDIDATE DOES NOT ESTABLISH SUPPORTED SDK",
    "RELEASE-CANDIDATE VALIDATED DOES NOT ESTABLISH SDK RELEASE",
    "SDK PUBLICATION NOT AUTHORIZED",
}


def fail(message: str) -> int:
    print(f"AX_EXTERNAL_EVALUATION_REPORT_FAIL {message}")
    return 1


def load_report(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("report root must be an object")
    return value


def main() -> int:
    if len(sys.argv) != 2:
        return fail("usage=check_external_evaluation_report.py <report.json>")

    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f"missing={path}")

    try:
        report = load_report(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(f"invalid_json={exc}")

    if report.get("report_format") != "AX-PUB-EVAL-REPORT-001":
        return fail("report_format")
    if report.get("report_version") != "1.0":
        return fail("report_version")
    if report.get("overall_result") != "PASS":
        return fail("overall_result")
    if report.get("python_runtime") not in VERIFIED_PYTHON:
        return fail("python_runtime_outside_verified_matrix")
    if report.get("runtime_matrix_state") != "WITHIN_VERIFIED_CANDIDATE_MATRIX":
        return fail("runtime_matrix_state")
    if set(report.get("declared_verified_python_matrix", [])) != VERIFIED_PYTHON:
        return fail("declared_verified_python_matrix")
    if report.get("sdk_publication") != "NOT_AUTHORIZED":
        return fail("sdk_publication_boundary")
    if report.get("external_adoption_established") is not False:
        return fail("external_adoption_boundary")
    if report.get("human_external_evaluation_claim") is not False:
        return fail("human_external_evaluation_claim_boundary")

    checks = report.get("checks")
    if not isinstance(checks, list):
        return fail("checks_not_list")
    by_id = {item.get("id"): item for item in checks if isinstance(item, dict)}
    if set(by_id) != EXPECTED_CHECKS:
        return fail("check_inventory")
    for check_id in sorted(EXPECTED_CHECKS):
        item = by_id[check_id]
        if item.get("result") != "PASS" or item.get("return_code") != 0:
            return fail(f"check_failed={check_id}")
        if not isinstance(item.get("duration_ms"), int) or item["duration_ms"] < 0:
            return fail(f"invalid_duration={check_id}")

    boundaries = set(report.get("claim_boundaries", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        return fail("claim_boundaries")

    print(
        "AX_EXTERNAL_EVALUATION_REPORT_PASS "
        f"checks={len(EXPECTED_CHECKS)} python={report['python_runtime']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
