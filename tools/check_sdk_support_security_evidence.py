#!/usr/bin/env python3
"""Validate AX-PUB-CI-013 evidence integrity and claim boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-013_SDK_SUPPORT_SECURITY_CONTRACT_VALIDATION.md"
SUP = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC = ROOT / "artifacts" / "AX-PUB-SEC-001.json"

EXPECTED_MARKERS = (
    "AX-PUB-CI-013",
    "Pull request: #50",
    "Reviewed head: b7c0f25eacfa534ae38d71b495fbd2d963d679a5",
    "Merged main commit: 9cced38d62723f05d6bb8142cb9525c89e93a4c9",
    "Workflow run ID: 32194756205",
    "Workflow run number: 5",
    "CPython 3.11 — job 95896362054 — SUCCESS",
    "CPython 3.12 — job 95896362020 — SUCCESS",
    "CPython 3.13 — job 95896362021 — SUCCESS",
    "CPython 3.14 — job 95896362076 — SUCCESS",
    "Job ID: 95896362012",
    "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21",
    "1787064230",
    "Run ID: 32194756195",
    "Run number: 190",
    "Run ID: 32194756191",
    "Run number: 35",
    "SUPPORT COMMITMENT: NOT ESTABLISHED",
    "SECURITY OPERATIONS READY: NO",
    "RELEASE CONTROL READY: NO",
    "SUPPORTED SDK: NOT ESTABLISHED",
    "DEV-GATE-05D: NOT AUTHORIZED",
    "SDK PUBLICATION: NOT AUTHORIZED",
    "CONTRACT VALIDATION ≠ CONTRACT ACTIVATION",
)


def fail(message: str) -> None:
    raise SystemExit(f"AX_CI013_EVIDENCE_FAIL: {message}")


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def main() -> int:
    if not EVIDENCE.is_file():
        fail("evidence file missing")
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in EXPECTED_MARKERS:
        if marker not in text:
            fail(f"evidence missing marker: {marker}")

    sup = load_json(SUP)
    sec = load_json(SEC)

    if sup.get("artifact_id") != "AX-PUB-SUP-001" or sup.get("version") != "0.1":
        fail("support artifact identity mismatch")
    if sec.get("artifact_id") != "AX-PUB-SEC-001" or sec.get("version") != "0.1":
        fail("security artifact identity mismatch")

    for key in (
        "support_commitment_established",
        "production_support_activated",
        "stable_1_0_semver_commitment",
        "commercial_sla_established",
        "sdk_publication_authorized",
    ):
        if sup.get(key) is not False:
            fail(f"support boundary changed: {key}")

    for key in (
        "security_operations_ready",
        "dedicated_security_channel_established",
        "security_response_owner_assigned",
        "security_response_sla_established",
        "bug_bounty_established",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        if sec.get(key) is not False:
            fail(f"security boundary changed: {key}")

    print(
        "AX_CI013_EVIDENCE_PASS "
        "run=32194756205 runtimes=3.11-3.14 gate03_identity=PRESERVED "
        "support=NOT_ACTIVATED security_ops=NOT_READY publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
