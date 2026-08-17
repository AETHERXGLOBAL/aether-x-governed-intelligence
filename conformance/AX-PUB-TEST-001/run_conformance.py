#!/usr/bin/env python3
"""Run AX-PUB-TEST-001 public conformance vectors.

This runner exercises only the public reference validators in this repository.
It does not inspect or invoke any private AETHER X product repository.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
VECTORS_PATH = Path(__file__).with_name("vectors.json")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def set_path(document: Any, path: list[Any], value: Any) -> None:
    node = document
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = value


def delete_path(document: Any, path: list[Any]) -> None:
    node = document
    for part in path[:-1]:
        node = node[part]
    del node[path[-1]]


def apply_mutations(document: dict[str, Any], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    mutated = copy.deepcopy(document)
    for mutation in mutations:
        operation = mutation.get("op")
        path = mutation.get("path")
        if not isinstance(path, list) or not path:
            raise ValueError(f"invalid mutation path: {path}")
        if operation == "set":
            set_path(mutated, path, mutation.get("value"))
        elif operation == "delete":
            delete_path(mutated, path)
        else:
            raise ValueError(f"unsupported mutation operation: {operation}")
    return mutated


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AX-PUB-TEST-001 public conformance vectors")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit machine-readable report")
    args = parser.parse_args()

    vectors = load_json(VECTORS_PATH)
    if vectors.get("test_kit_id") != "AX-PUB-TEST-001" or vectors.get("version") != "1.0":
        raise SystemExit("AX_CONFORMANCE_ERROR: unsupported test kit identity/version")

    eav = load_module(
        "ax_pub_ref_001",
        ROOT / "reference-implementations" / "eav-contract-validator" / "validator.py",
    )
    ptk = load_module(
        "ax_pub_ref_002",
        ROOT / "reference-implementations" / "point-in-time-knowledge-validator" / "validator.py",
    )

    validators: dict[str, Callable[[dict[str, Any]], list[Any]]] = {
        "AX-PUB-REF-001": eav.validate_bundle,
        "AX-PUB-REF-002": ptk.validate_envelope,
    }

    report_cases: list[dict[str, Any]] = []
    failed_cases = 0

    for suite in vectors.get("suites", []):
        validator_id = suite["validator"]
        validator = validators.get(validator_id)
        if validator is None:
            raise SystemExit(f"AX_CONFORMANCE_ERROR: no public validator for {validator_id}")

        baseline_path = ROOT / suite["baseline"]
        baseline = load_json(baseline_path)

        for case in suite.get("cases", []):
            payload = apply_mutations(baseline, case.get("mutations", []))
            findings = validator(payload)
            actual = "PASS" if not findings else "FAIL"
            actual_codes = {finding.code for finding in findings}
            required = set(case.get("required_findings", []))
            result_ok = actual == case["expected"] and required.issubset(actual_codes)
            if not result_ok:
                failed_cases += 1

            report_cases.append(
                {
                    "id": case["id"],
                    "suite": suite["suite_id"],
                    "title": case["title"],
                    "expected": case["expected"],
                    "actual": actual,
                    "required_findings": sorted(required),
                    "actual_findings": [asdict(finding) for finding in findings],
                    "conformance_result": "PASS" if result_ok else "FAIL",
                }
            )

    report = {
        "test_kit_id": "AX-PUB-TEST-001",
        "version": "1.0",
        "case_count": len(report_cases),
        "conforming_cases": len(report_cases) - failed_cases,
        "nonconforming_cases": failed_cases,
        "status": "PASS" if failed_cases == 0 else "FAIL",
        "cases": report_cases,
        "claim_boundary": "CONFORMANCE PASS DOES NOT ESTABLISH PRODUCT IMPLEMENTATION OR PRODUCTION READINESS",
    }

    if args.json_output:
        print(json.dumps(report, indent=2))
    else:
        for item in report_cases:
            print(
                f"{item['conformance_result']} {item['id']} "
                f"expected={item['expected']} actual={item['actual']}"
            )
        print(
            f"AX_PUBLIC_CONFORMANCE_{report['status']} "
            f"cases={report['case_count']} conforming={report['conforming_cases']}"
        )

    return 0 if failed_cases == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
