#!/usr/bin/env python3
"""Current-candidate adapter for immutable DEV-GATE-03 historical evidence.

Historical closure state is validated by the byte-preserved historical checker.
Only the built artifact identity is evaluated against the explicit current
superseding candidate evidence for AXGI-REV-001.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "tools" / "check_supply_chain_release_candidate_historical.py"
OVERLAY = ROOT / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json"
RC = ROOT / "release-candidate" / "AX-PUB-RC-001.json"
DEV005 = ROOT / "artifacts" / "AX-PUB-DEV-005.json"


def fail(message: str) -> None:
    raise SystemExit(f"AX_CURRENT_CANDIDATE_IDENTITY_FAIL: {message}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def load_historical():
    spec = importlib.util.spec_from_file_location("ax_gate03_historical", HISTORICAL)
    if spec is None or spec.loader is None:
        fail("cannot load historical Gate-03 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_immutability(overlay: dict[str, Any]) -> None:
    anchors = overlay.get("historical_anchors")
    if not isinstance(anchors, dict):
        fail("historical anchors missing")
    gate03 = anchors.get("gate_03")
    if not isinstance(gate03, dict):
        fail("Gate-03 historical anchor missing")
    rc = load(RC)
    dev = load(DEV005)
    expected_digest = gate03.get("verified_build_digest")
    expected_epoch = gate03.get("verified_source_date_epoch")
    if expected_digest != "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21":
        fail("overlay attempts to redefine historical Gate-03 digest")
    if expected_epoch != 1787064230:
        fail("overlay attempts to redefine historical Gate-03 source epoch")
    if rc.get("verified_build_digest") != expected_digest or dev.get("verified_build_digest") != expected_digest:
        fail("historical Gate-03 digest changed")
    if rc.get("verified_source_date_epoch") != expected_epoch or dev.get("verified_source_date_epoch") != expected_epoch:
        fail("historical Gate-03 source epoch changed")
    if rc.get("closure_evidence", {}).get("id") != "AX-PUB-CI-006" or dev.get("closure_evidence", {}).get("id") != "AX-PUB-CI-006":
        fail("historical AX-PUB-CI-006 linkage changed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate historical Gate-03 state plus current candidate identity")
    parser.add_argument("--dist", type=Path)
    args = parser.parse_args()
    overlay = load(OVERLAY)
    if overlay.get("artifact_id") != "AX-PUB-CANDIDATE-IDENTITY-001":
        fail("current candidate overlay identity mismatch")
    if overlay.get("state") != "CURRENT_CANDIDATE_IDENTITY_ALIGNMENT":
        fail("current candidate overlay state mismatch")
    reason = overlay.get("reason")
    if not isinstance(reason, dict) or reason.get("finding_id") != "AXGI-REV-001":
        fail("AXGI-REV-001 linkage missing")
    if reason.get("correction_revision") != "3e8be5b097df0049dbf4cad134fbc6706269ca9c":
        fail("correction revision mismatch")
    check_immutability(overlay)

    historical = load_historical()
    original_argv = sys.argv
    try:
        sys.argv = [str(HISTORICAL)]
        historical_result = historical.main()
    finally:
        sys.argv = original_argv
    if historical_result not in (None, 0):
        return int(historical_result)

    if args.dist is not None:
        current = overlay.get("current_candidate", {}).get("release_candidate")
        if not isinstance(current, dict):
            fail("current release-candidate identity missing")
        if current.get("source_revision") != "3e8be5b097df0049dbf4cad134fbc6706269ca9c":
            fail("current release-candidate source revision mismatch")
        digest = current.get("bundle_sha256")
        epoch = current.get("source_date_epoch")
        if not isinstance(digest, str) or len(digest) != 64 or epoch != 1787064230:
            fail("current release-candidate identity incomplete")
        findings: list[str] = []
        descriptor = historical.load_json(historical.DESCRIPTOR, findings)
        if descriptor is None:
            fail("cannot load release-candidate descriptor")
        effective = dict(descriptor)
        effective["verified_build_digest"] = digest
        effective["verified_source_date_epoch"] = epoch
        dist = args.dist if args.dist.is_absolute() else ROOT / args.dist
        historical.validate_dist(dist, effective, findings)
        if findings:
            for item in findings:
                print(f"AX_CURRENT_CANDIDATE_IDENTITY_FAIL: {item}")
            return 1
        print(f"AX_CURRENT_RELEASE_CANDIDATE_IDENTITY_PASS sha256={digest} historical_digest_preserved=true")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
