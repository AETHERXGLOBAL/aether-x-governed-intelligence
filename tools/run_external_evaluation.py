#!/usr/bin/env python3
"""Run the bounded public developer surface as a self-service evaluation.

This runner is DEV-GATE-04 readiness infrastructure. A CI run of this tool is
not evidence that a human external evaluator participated or adopted the SDK
candidate.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERIFIED_PYTHON = {"3.10", "3.11", "3.12", "3.13"}
REPORT_FORMAT = "AX-PUB-EVAL-REPORT-001"
REPORT_VERSION = "1.0"

CHECKS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("developer-experience", ("{python}", "tools/check_developer_experience.py")),
    ("sdk-candidate-unit-tests", ("{python}", "-m", "unittest", "discover", "-s", "sdk-candidate/python/tests", "-v")),
    ("sdk-candidate-example", ("{python}", "sdk-candidate/python/example.py")),
    ("sdk-candidate-conformance", ("{python}", "sdk-candidate/python/run_candidate_conformance.py")),
    ("sdk-candidate-public-boundary", ("{python}", "tools/check_sdk_candidate_boundary.py")),
    ("sdk-candidate-governance-state", ("{python}", "tools/check_sdk_candidate_state.py")),
    ("release-candidate-governance-state", ("{python}", "tools/check_supply_chain_release_candidate.py")),
    ("artifact-manifest-governance", ("{python}", "tools/check_artifact_manifest.py")),
)

CLAIM_BOUNDARIES = [
    "READINESS RUN PASS DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
    "EXTERNAL EVALUATION READINESS DOES NOT ESTABLISH ADOPTION",
    "SDK CANDIDATE DOES NOT ESTABLISH SUPPORTED SDK",
    "RELEASE-CANDIDATE VALIDATED DOES NOT ESTABLISH SDK RELEASE",
    "SDK PUBLICATION NOT AUTHORIZED",
]


def _tail(value: str, limit: int = 4000) -> str:
    return value[-limit:]


def _git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return "UNAVAILABLE"
    return completed.stdout.strip()


def _runtime_key() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def _run_check(check_id: str, command_template: tuple[str, ...]) -> dict[str, Any]:
    command = [sys.executable if part == "{python}" else part for part in command_template]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed_ms = int((time.monotonic() - started) * 1000)
    return {
        "id": check_id,
        "command": command,
        "return_code": completed.returncode,
        "duration_ms": elapsed_ms,
        "stdout_tail": _tail(completed.stdout),
        "stderr_tail": _tail(completed.stderr),
        "result": "PASS" if completed.returncode == 0 else "FAIL",
    }


def build_report(context: str) -> dict[str, Any]:
    runtime = _runtime_key()
    checks: list[dict[str, Any]] = []

    if runtime in VERIFIED_PYTHON:
        checks = [_run_check(check_id, command) for check_id, command in CHECKS]
        overall = "PASS" if all(check["return_code"] == 0 for check in checks) else "FAIL"
        runtime_state = "WITHIN_VERIFIED_CANDIDATE_MATRIX"
    else:
        overall = "FAIL"
        runtime_state = "OUTSIDE_VERIFIED_CANDIDATE_MATRIX"

    return {
        "report_format": REPORT_FORMAT,
        "report_version": REPORT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_context": context,
        "repository_head": _git_head(),
        "python_runtime": runtime,
        "python_full_version": platform.python_version(),
        "platform": platform.platform(),
        "runtime_matrix_state": runtime_state,
        "declared_verified_python_matrix": sorted(VERIFIED_PYTHON),
        "checks": checks,
        "overall_result": overall,
        "sdk_publication": "NOT_AUTHORIZED",
        "external_adoption_established": False,
        "human_external_evaluation_claim": False,
        "claim_boundaries": CLAIM_BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--context", choices=("SELF_SERVICE", "CI"), default="SELF_SERVICE")
    args = parser.parse_args()

    report = build_report(args.context)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if report["runtime_matrix_state"] != "WITHIN_VERIFIED_CANDIDATE_MATRIX":
        print(
            "AX_EXTERNAL_EVALUATION_RUNTIME_UNVERIFIED "
            f"python={report['python_runtime']} declared=3.10,3.11,3.12,3.13"
        )
        return 2

    if report["overall_result"] != "PASS":
        failed = [check["id"] for check in report["checks"] if check["result"] != "PASS"]
        print(f"AX_EXTERNAL_EVALUATION_RUN_FAIL failed={','.join(failed)}")
        return 1

    print(f"AX_EXTERNAL_EVALUATION_RUN_PASS checks={len(report['checks'])} python={report['python_runtime']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
