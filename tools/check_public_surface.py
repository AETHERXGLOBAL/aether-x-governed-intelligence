#!/usr/bin/env python3
"""Fail closed if the public showcase acquires enabling or sensitive material.

This checker protects the *repository boundary*, not the Governed Intelligence
technology itself. It is intentionally small, dependency-free and suitable for
public inspection.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path("tools/check_public_surface.py")

FORBIDDEN_TOP_LEVEL = {
    "src",
    "sdk",
    "sdk-candidate",
    "sdk-release-candidate",
    "schemas",
    "reference-implementations",
    "release-candidate",
    "artifacts",
    "evidence",
    "conformance",
    "snapshots",
}

FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".whl",
    ".so",
    ".dll",
    ".dylib",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".jks",
}

FORBIDDEN_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
}

SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}

TEXT_SUFFIXES = {".md", ".txt", ".yml", ".yaml", ".json", ".svg"}


def is_ignored(path: Path) -> bool:
    parts = path.parts
    return ".git" in parts


def main() -> int:
    findings: list[str] = []
    checked_files = 0

    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT)
        if is_ignored(rel):
            continue
        checked_files += 1

        if rel != SELF:
            if rel.parts and rel.parts[0] in FORBIDDEN_TOP_LEVEL:
                findings.append(f"forbidden public path: {rel}")
            if path.suffix.lower() == ".py":
                findings.append(f"source code is not allowed in public showcase: {rel}")

        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"sensitive/build artifact is not allowed: {rel}")

        if path.suffix.lower() in TEXT_SUFFIXES or rel == SELF:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                findings.append(f"expected text file is not valid UTF-8: {rel}")
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    findings.append(f"possible {label} material in: {rel}")

    if findings:
        for finding in findings:
            print(f"AX_PUBLIC_DISCLOSURE_FAIL: {finding}")
        return 1

    print(
        "AX_PUBLIC_DISCLOSURE_PASS "
        f"files={checked_files} mode=NON_ENABLING_SHOWCASE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
