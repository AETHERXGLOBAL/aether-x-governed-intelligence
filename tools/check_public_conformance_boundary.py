#!/usr/bin/env python3
"""Fail closed if the public conformance kit crosses the private-project boundary.

This check intentionally inspects only public conformance runtime/configuration
files. Product names may appear elsewhere in public documentation as claim
boundaries; they must not become runtime dependencies here.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance" / "AX-PUB-TEST-001" / "vectors.json"
RUNNER = ROOT / "conformance" / "AX-PUB-TEST-001" / "run_conformance.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-public-conformance.yml"

PRIVATE_REPOSITORY_SLUGS = (
    "aether-x-quantum",
    "AX-OS",
    "aether-intelligence-core-AIC-",
    "aether-x-research",
    "aether-x-governance",
    "aether-x-global-website",
    "amii-research-lab",
)

ALLOWED_VALIDATORS = {"AX-PUB-REF-001", "AX-PUB-REF-002"}
ALLOWED_BASELINE_PREFIXES = (
    "reference-implementations/eav-contract-validator/examples/",
    "reference-implementations/point-in-time-knowledge-validator/examples/",
)


def main() -> int:
    findings: list[str] = []

    for path in (VECTORS, RUNNER, WORKFLOW):
        if not path.is_file():
            findings.append(f"missing public conformance file: {path.relative_to(ROOT)}")

    if findings:
        for finding in findings:
            print(f"AX_PUBLIC_BOUNDARY_FAIL: {finding}")
        return 1

    runtime_text = "\n".join(
        path.read_text(encoding="utf-8") for path in (VECTORS, RUNNER, WORKFLOW)
    )
    runtime_lower = runtime_text.lower()

    for slug in PRIVATE_REPOSITORY_SLUGS:
        if slug.lower() in runtime_lower:
            findings.append(f"private repository slug referenced by public conformance runtime: {slug}")

    forbidden_runtime_markers = (
        "${{ secrets.",
        "private_key",
        "access_token",
        "personal_access_token",
        "repository:",
        "submodules: true",
    )
    for marker in forbidden_runtime_markers:
        if marker.lower() in runtime_lower:
            findings.append(f"forbidden private-access marker in public conformance runtime: {marker}")

    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    if "permissions:\n  contents: read" not in workflow_text:
        findings.append("public conformance workflow must preserve contents: read permission")

    try:
        vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(f"cannot parse vectors.json: {exc}")
        vectors = {}

    if isinstance(vectors, dict):
        for suite in vectors.get("suites", []):
            if not isinstance(suite, dict):
                findings.append("conformance suite must be an object")
                continue
            validator = suite.get("validator")
            baseline = suite.get("baseline")
            if validator not in ALLOWED_VALIDATORS:
                findings.append(f"non-public validator dependency: {validator}")
            if not isinstance(baseline, str) or not baseline.startswith(ALLOWED_BASELINE_PREFIXES):
                findings.append(f"baseline path is outside approved public examples: {baseline}")
            elif ".." in Path(baseline).parts or Path(baseline).is_absolute():
                findings.append(f"unsafe baseline path: {baseline}")

    if findings:
        for finding in findings:
            print(f"AX_PUBLIC_BOUNDARY_FAIL: {finding}")
        return 1

    print("AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
