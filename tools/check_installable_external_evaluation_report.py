#!/usr/bin/env python3
"""Validate AX-PUB-EVAL-REPORT-002 installable human-evaluation records.

By default this checker requires FINAL human evidence. Use --allow-template only
for CI validation of the repository-provided blank template; template success
never establishes that a human evaluation occurred.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

FORMAT = "AX-PUB-EVAL-REPORT-002"
VERSION = "1.0"
PROJECT = "aetherxglobal-governed-intelligence"
PACKAGE_VERSION = "0.1.0rc1"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
RUNTIMES = {"3.11", "3.12", "3.13", "3.14"}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"}
DISPOSITIONS = {"FIXED", "ACCEPTED_RISK", "NOT_REPRODUCIBLE", "OUT_OF_SCOPE", "DEFERRED_BLOCKS_CLOSURE"}
BOUNDARIES = {
    "HUMAN EVALUATION DOES NOT ESTABLISH ENDORSEMENT",
    "HUMAN EVALUATION DOES NOT ESTABLISH ADOPTION",
    "EVALUATION PASS DOES NOT ESTABLISH A SUPPORTED SDK",
    "EVALUATION PASS DOES NOT ESTABLISH RELEASE AUTHORITY",
    "SDK PUBLICATION NOT AUTHORIZED",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_INSTALLABLE_EXTERNAL_EVALUATION_REPORT_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def parse_time(value: Any, field: str) -> None:
    require(isinstance(value, str) and value, f"{field} missing")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"{field} invalid ISO-8601: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    require(args.report.is_file(), "report file missing")
    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON: {exc}")
    require(isinstance(data, dict), "report must be an object")
    require(data.get("report_format") == FORMAT, "report format mismatch")
    require(data.get("report_version") == VERSION, "report version mismatch")

    candidate = data.get("candidate")
    require(isinstance(candidate, dict), "candidate identity missing")
    require(candidate.get("distribution") == PROJECT, "distribution mismatch")
    require(candidate.get("version") == PACKAGE_VERSION, "candidate version mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA, "wheel digest mismatch")
    require(candidate.get("sdist_sha256") == SDIST_SHA, "sdist digest mismatch")
    require(data.get("sdk_publication") == "NOT_AUTHORIZED", "SDK publication boundary changed")
    require(data.get("external_adoption_established") is False, "evaluation must not infer adoption")
    require(data.get("endorsement_claimed") is False, "evaluation must not claim endorsement")
    require(data.get("supported_sdk_established") is False, "evaluation must not establish a supported SDK")
    require(BOUNDARIES <= set(data.get("claim_boundaries", [])), "required claim boundaries missing")

    state = data.get("record_state")
    if state == "TEMPLATE":
        require(args.allow_template, "template is not human evaluation evidence")
        require(data.get("overall_result") == "NOT_EVALUATED", "template must remain NOT_EVALUATED")
        require(data.get("issue_disposition_complete") is False, "template cannot pre-complete issue disposition")
        print("AX_INSTALLABLE_EXTERNAL_EVALUATION_TEMPLATE_PASS human_evaluation=false")
        return

    require(state == "FINAL", "final evaluation must use record_state=FINAL")
    evaluator = data.get("evaluator")
    require(isinstance(evaluator, dict), "evaluator record missing")
    identifier = evaluator.get("identifier")
    require(isinstance(identifier, str) and identifier.strip(), "evaluator identifier missing")
    require("REPLACE_" not in identifier, "placeholder evaluator identifier prohibited")
    require(evaluator.get("independent_of_implementation") is True, "evaluator independence must be explicitly true")

    evaluation = data.get("evaluation")
    require(isinstance(evaluation, dict), "evaluation environment missing")
    parse_time(evaluation.get("started_at_utc"), "started_at_utc")
    parse_time(evaluation.get("completed_at_utc"), "completed_at_utc")
    require(isinstance(evaluation.get("platform"), str) and evaluation["platform"].strip(), "platform missing")
    require(evaluation.get("python_runtime") in RUNTIMES, "runtime outside declared Gate-05C matrix")
    require(isinstance(evaluation.get("installation_source"), str) and evaluation["installation_source"].strip(), "installation source missing")
    require(evaluation.get("external_index_used") is True, "Gate-05C final human evidence requires controlled external-index installation")

    checks = data.get("checks")
    require(isinstance(checks, list) and checks, "final evaluation requires at least one check")
    for i, check in enumerate(checks):
        require(isinstance(check, dict), f"check {i} must be an object")
        require(isinstance(check.get("id"), str) and check["id"].strip(), f"check {i} id missing")
        require(check.get("result") in {"PASS", "FAIL", "NOT_APPLICABLE"}, f"check {i} result invalid")

    findings = data.get("findings")
    require(isinstance(findings, list), "findings must be an array")
    unresolved_critical = 0
    unresolved_high = 0
    for i, finding in enumerate(findings):
        require(isinstance(finding, dict), f"finding {i} must be an object")
        require(isinstance(finding.get("id"), str) and finding["id"].strip(), f"finding {i} id missing")
        severity = finding.get("severity")
        disposition = finding.get("disposition")
        require(severity in SEVERITIES, f"finding {i} severity invalid")
        require(disposition in DISPOSITIONS, f"finding {i} disposition invalid")
        require(isinstance(finding.get("summary"), str) and finding["summary"].strip(), f"finding {i} summary missing")
        require(isinstance(finding.get("reproduction"), str) and finding["reproduction"].strip(), f"finding {i} reproduction missing")
        if severity == "CRITICAL" and disposition not in {"FIXED", "NOT_REPRODUCIBLE", "OUT_OF_SCOPE"}:
            unresolved_critical += 1
        if severity == "HIGH" and disposition not in {"FIXED", "ACCEPTED_RISK", "NOT_REPRODUCIBLE", "OUT_OF_SCOPE"}:
            unresolved_high += 1

    require(data.get("unresolved_critical_findings") == unresolved_critical, "critical finding count mismatch")
    require(data.get("unresolved_high_findings") == unresolved_high, "high finding count mismatch")
    require(unresolved_critical == 0, "unresolved critical finding blocks Gate-05C")
    require(unresolved_high == 0, "unresolved high finding lacks fix/risk acceptance")
    require(data.get("issue_disposition_complete") is True, "issue disposition must be complete")
    require(data.get("overall_result") in {"PASS", "PASS_WITH_FINDINGS"}, "overall result cannot support Gate-05C")

    print(
        "AX_INSTALLABLE_EXTERNAL_EVALUATION_REPORT_PASS "
        f"evaluator={identifier} python={evaluation['python_runtime']} findings={len(findings)}"
    )


if __name__ == "__main__":
    main()
