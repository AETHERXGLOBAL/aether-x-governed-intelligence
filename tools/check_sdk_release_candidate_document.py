#!/usr/bin/env python3
"""Validate mandatory public markers in AX-PUB-DEV-008 across candidate/closed states."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AX-PUB-DEV-008_INSTALLABLE_PACKAGE_CANDIDATE.md"
STATE = ROOT / "artifacts" / "AX-PUB-DEV-008.json"

COMMON = (
    "AX-PUB-DEV-008",
    "`0.1`",
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

CANDIDATE = (
    "DEV-GATE-05B ENGINEERING CANDIDATE",
    "DIRECT PUBLISHED-BASELINE VALIDATION NOT YET ESTABLISHED",
)

CLOSED = (
    "DEV-GATE-05B CLOSED",
    "DEV-GATE-05C ACTIVE",
    "AX-PUB-CI-009",
    "32171606094",
    "95823835258",
    "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac",
    "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99",
    "DEV-GATE-05B CLOSED ≠ DEV-GATE-05 CLOSED",
)


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_RELEASE_CANDIDATE_DOC_FAIL: {message}")


def main() -> None:
    if not DOC.is_file():
        fail("document missing")
    if not STATE.is_file():
        fail("machine-readable state missing")

    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse machine-readable state: {exc}")
    if not isinstance(state, dict):
        fail("machine-readable state must be an object")

    text = DOC.read_text(encoding="utf-8")
    required = list(COMMON)
    if state.get("phase_state") == "CLOSED":
        required.extend(CLOSED)
    else:
        required.extend(CANDIDATE)

    missing = [marker for marker in required if marker not in text]
    if missing:
        fail("missing markers: " + ", ".join(missing))

    if state.get("phase_state") == "CLOSED":
        if state.get("publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            fail("closed document state may not authorize publication")
        if state.get("distribution_authorized") is not False:
            fail("closed document state may not authorize distribution")
        if state.get("license_granted") is not False:
            fail("closed document state may not grant a licence")
        if state.get("supported_sdk_established") is not False:
            fail("closed document state may not establish a supported SDK")
        print("AX_SDK_RELEASE_CANDIDATE_DOC_PASS state=CLOSED evidence=AX-PUB-CI-009")
    else:
        print("AX_SDK_RELEASE_CANDIDATE_DOC_PASS state=ENGINEERING_CANDIDATE")


if __name__ == "__main__":
    main()
