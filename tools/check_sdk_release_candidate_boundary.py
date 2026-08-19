#!/usr/bin/env python3
"""Current-candidate adapter for immutable DEV-GATE-05B closure evidence.

All historical Gate-05B evidence remains validated by the byte-preserved
historical checker. Only live validator-source identity is resolved from the
explicit current superseding candidate evidence for AXGI-REV-001.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "tools" / "check_sdk_release_candidate_boundary_historical.py"
OVERLAY = ROOT / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json"
DEV008 = ROOT / "artifacts" / "AX-PUB-DEV-008.json"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_CURRENT_CANDIDATE_IDENTITY_FAIL: {message}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def load_historical():
    spec = importlib.util.spec_from_file_location("ax_gate05b_historical", HISTORICAL)
    if spec is None or spec.loader is None:
        fail("cannot load historical Gate-05B checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    overlay = load(OVERLAY)
    artifact = load(DEV008)
    if overlay.get("artifact_id") != "AX-PUB-CANDIDATE-IDENTITY-001":
        fail("current candidate overlay identity mismatch")
    reason = overlay.get("reason")
    if not isinstance(reason, dict) or reason.get("finding_id") != "AXGI-REV-001" or reason.get("correction_revision") != "3e8be5b097df0049dbf4cad134fbc6706269ca9c":
        fail("AXGI-REV-001 correction linkage mismatch")

    anchors = overlay.get("historical_anchors", {}).get("gate_05b")
    if not isinstance(anchors, dict):
        fail("Gate-05B historical anchor missing")
    old_validator_identity = {
        "AX-PUB-REF-001": "10b31f990cdeb0a2285081d4b4a8cc2457564c69",
        "AX-PUB-REF-002": "f4344dfb70685b490e716e33f8f2fd2da1f0ca50",
        "AX-PUB-REF-003": "6c8f4d325ef3d3f2041909f8bba7d554ced4366e",
    }
    if anchors.get("validator_source_identity") != old_validator_identity:
        fail("overlay attempts to redefine historical validator identity")
    if artifact.get("validator_source_identity") != old_validator_identity:
        fail("historical DEV-008 validator identity changed")
    historical_dist = artifact.get("verified_distribution_identity", {})
    if anchors.get("wheel_sha256") != "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac" or anchors.get("sdist_sha256") != "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99":
        fail("overlay attempts to redefine historical package identity")
    if historical_dist.get("wheel", {}).get("sha256") != anchors.get("wheel_sha256") or historical_dist.get("sdist", {}).get("sha256") != anchors.get("sdist_sha256"):
        fail("historical DEV-008 package identity changed")
    if artifact.get("closure_evidence", {}).get("id") != "AX-PUB-CI-009":
        fail("historical AX-PUB-CI-009 linkage changed")

    current_expected = overlay.get("current_candidate", {}).get("validator_source_identity")
    if not isinstance(current_expected, dict):
        fail("current validator identity map missing")

    historical = load_historical()

    def check_current_validator_identity(_artifact: dict[str, Any]) -> None:
        for artifact_id, (reference, packaged) in historical.VALIDATOR_PAIRS.items():
            historical.require(reference.is_file(), f"missing reference validator for {artifact_id}")
            historical.require(packaged.is_file(), f"missing packaged validator for {artifact_id}")
            reference_bytes = reference.read_bytes()
            packaged_bytes = packaged.read_bytes()
            historical.require(reference_bytes == packaged_bytes, f"packaged validator drift detected for {artifact_id}")
            digest = historical.git_blob_sha1(packaged_bytes)
            historical.require(digest == current_expected.get(artifact_id), f"current Git blob identity mismatch for {artifact_id}: {digest}")

    historical.check_validator_identity = check_current_validator_identity
    historical.main()
    print("AX_SDK_CURRENT_CANDIDATE_IDENTITY_PASS historical_gate05b_preserved=true current_validators=3")


if __name__ == "__main__":
    main()
