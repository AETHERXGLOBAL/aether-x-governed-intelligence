#!/usr/bin/env python3
"""Fail closed if the public surface acquires unauthorized enabling or sensitive material.

The parent repository remains a controlled-disclosure technology showcase. A small,
explicitly licensed public-source subtree may exist only when allowlisted here.
This checker protects that boundary while continuing to scan the full repository for
common secret and sensitive-artifact patterns.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path("tools/check_public_surface.py")

# Explicitly reviewed open-source exceptions. Adding another entry is itself a
# public-boundary policy change and must pass review.
SCOPED_PUBLIC_SOURCE_ROOTS = {
    Path("tools/reprocert"),
}

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

TEXT_SUFFIXES = {".md", ".txt", ".yml", ".yaml", ".json", ".svg", ".py", ".toml"}


def is_ignored(path: Path) -> bool:
    return ".git" in path.parts


def is_scoped_public_source(path: Path) -> bool:
    return any(path == root or root in path.parents for root in SCOPED_PUBLIC_SOURCE_ROOTS)


def validate_scoped_source_contract(findings: list[str]) -> None:
    for root in sorted(SCOPED_PUBLIC_SOURCE_ROOTS):
        absolute = ROOT / root
        if not absolute.is_dir():
            findings.append(f"allowlisted public-source subtree is missing: {root}")
            continue

        license_path = absolute / "LICENSE"
        scope_path = absolute / "LICENSE_SCOPE.md"

        if not license_path.is_file():
            findings.append(f"scoped public-source subtree lacks LICENSE: {root}")
        if not scope_path.is_file():
            findings.append(f"scoped public-source subtree lacks LICENSE_SCOPE.md: {root}")

        if license_path.is_file():
            text = license_path.read_text(encoding="utf-8", errors="replace")
            if "Apache License" not in text or "Version 2.0" not in text:
                findings.append(
                    f"unexpected scoped licence content: {license_path.relative_to(ROOT)}"
                )

        if scope_path.is_file():
            text = scope_path.read_text(encoding="utf-8", errors="replace")
            if "only" not in text.lower() or "Apache License 2.0" not in text:
                findings.append(
                    f"scoped licence boundary is not explicit: {scope_path.relative_to(ROOT)}"
                )


def main() -> int:
    findings: list[str] = []
    checked_files = 0
    scoped_source_files = 0

    validate_scoped_source_contract(findings)

    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT)
        if is_ignored(rel):
            continue
        checked_files += 1

        scoped_source = is_scoped_public_source(rel)
        if scoped_source:
            scoped_source_files += 1

        if rel != SELF:
            if rel.parts and rel.parts[0] in FORBIDDEN_TOP_LEVEL:
                findings.append(f"forbidden public path: {rel}")
            if path.suffix.lower() == ".py" and not scoped_source:
                findings.append(
                    f"source code is not allowed outside scoped public-source subtrees: {rel}"
                )

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
        f"files={checked_files} scoped_source_files={scoped_source_files} "
        "mode=CONTROLLED_SHOWCASE_WITH_SCOPED_PUBLIC_SOURCE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
