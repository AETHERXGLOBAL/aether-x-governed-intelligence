#!/usr/bin/env python3
"""Validate the DEV-GATE-02 SDK candidate disclosure/dependency boundary."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "sdk-candidate" / "python"
MODULE = CANDIDATE_DIR / "aetherx_sdk_candidate.py"

ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "importlib",
    "sys",
    "dataclasses",
    "enum",
    "functools",
    "pathlib",
    "typing",
}

FORBIDDEN_DISTRIBUTION_FILES = {
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "MANIFEST.in",
}

FORBIDDEN_CODE_MARKERS = (
    "AETHERXGLOBAL/aether-x-quantum",
    "AETHERXGLOBAL/AX-OS",
    "AETHERXGLOBAL/aether-intelligence-core-AIC-",
    "AETHERXGLOBAL/aether-x-research",
    "AETHERXGLOBAL/aether-x-governance",
    "private package",
    "private endpoint",
    "api_key",
    "access_token",
    "requests.",
    "urllib.request",
    "subprocess.",
)

REQUIRED_PUBLIC_PATHS = (
    "reference-implementations/eav-contract-validator/validator.py",
    "reference-implementations/point-in-time-knowledge-validator/validator.py",
    "reference-implementations/agent-tool-authority-validator/validator.py",
)


def main() -> int:
    findings: list[str] = []
    if not MODULE.is_file():
        findings.append("candidate module missing")
    else:
        source = MODULE.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            findings.append(f"candidate module syntax error: {exc}")
            tree = None

        if tree is not None:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root not in ALLOWED_IMPORT_ROOTS:
                            findings.append(f"non-standard candidate import not allowlisted: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    root = module.split(".", 1)[0]
                    if root not in ALLOWED_IMPORT_ROOTS:
                        findings.append(f"non-standard candidate import not allowlisted: {module}")

        lowered = source.lower()
        for marker in FORBIDDEN_CODE_MARKERS:
            if marker.lower() in lowered:
                findings.append(f"forbidden candidate code marker: {marker}")

        for path in REQUIRED_PUBLIC_PATHS:
            if path not in source:
                findings.append(f"candidate does not explicitly bind public reference path: {path}")
            if not (ROOT / path).is_file():
                findings.append(f"declared public reference path missing: {path}")

    for name in FORBIDDEN_DISTRIBUTION_FILES:
        if (CANDIDATE_DIR / name).exists():
            findings.append(f"distribution metadata not authorized in DEV-GATE-02 candidate: {name}")

    if findings:
        for item in findings:
            print(f"AX_SDK_CANDIDATE_BOUNDARY_FAIL: {item}")
        return 1

    print("AX_SDK_CANDIDATE_BOUNDARY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
