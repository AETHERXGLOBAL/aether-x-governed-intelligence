#!/usr/bin/env python3
"""Validate mandatory public markers in AX-PUB-DEV-008."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AX-PUB-DEV-008_INSTALLABLE_PACKAGE_CANDIDATE.md"

REQUIRED = (
    "AX-PUB-DEV-008",
    "DEV-GATE-05B ENGINEERING CANDIDATE",
    "DIRECT PUBLISHED-BASELINE VALIDATION NOT YET ESTABLISHED",
    "aetherxglobal-governed-intelligence",
    "aetherxglobal.governed_intelligence",
    "PEP 420",
    "CPython 3.11",
    "CPython 3.12",
    "CPython 3.13",
    "CPython 3.14",
    "Hatchling `1.31.0`",
    "SOURCE_DATE_EPOCH = 1787076737",
    "--no-index --no-deps",
    "Apache-2.0",
    "LICENCE GRANTED: NO",
    "CI ARTIFACT ≠ PUBLIC PACKAGE",
    "SDK PUBLICATION NOT AUTHORIZED",
)


def main() -> None:
    if not DOC.is_file():
        raise SystemExit("AX_SDK_RELEASE_CANDIDATE_DOC_FAIL: document missing")
    text = DOC.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED if marker not in text]
    if missing:
        raise SystemExit("AX_SDK_RELEASE_CANDIDATE_DOC_FAIL: missing markers: " + ", ".join(missing))
    print("AX_SDK_RELEASE_CANDIDATE_DOC_PASS")


if __name__ == "__main__":
    main()
