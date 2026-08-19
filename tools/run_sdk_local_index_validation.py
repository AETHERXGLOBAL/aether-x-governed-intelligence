#!/usr/bin/env python3
"""Run current Gate-05C local-index validation using superseding candidate evidence.

The historical AX-PUB-CI-010-era runner is preserved byte-for-byte and reused
as the validation engine. This adapter changes only the exact package digests
to the current CI-observed candidate recorded after AXGI-REV-001.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "tools" / "run_sdk_local_index_validation_historical.py"
OVERLAY = ROOT / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json"
EXPECTED_HISTORICAL_WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
EXPECTED_HISTORICAL_SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_CURRENT_LOCAL_INDEX_VALIDATION_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def load_historical():
    require(HISTORICAL.is_file(), "historical local-index runner missing")
    spec = importlib.util.spec_from_file_location("ax_sdk_local_index_historical", HISTORICAL)
    require(spec is not None and spec.loader is not None, "cannot load historical local-index runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def current_identity() -> tuple[str, str]:
    overlay = load(OVERLAY)
    require(overlay.get("artifact_id") == "AX-PUB-CANDIDATE-IDENTITY-001", "candidate identity artifact mismatch")
    require(overlay.get("type") == "CURRENT_SUPERSEDING_CANDIDATE_EVIDENCE", "candidate identity type mismatch")
    require(overlay.get("state") == "CURRENT_CANDIDATE_IDENTITY_ALIGNED", "candidate identity state mismatch")

    anchors = overlay.get("historical_anchors", {}).get("gate_05b")
    require(isinstance(anchors, dict), "historical Gate-05B anchor missing")
    require(anchors.get("evidence_id") == "AX-PUB-CI-009", "historical Gate-05B evidence identity changed")
    require(anchors.get("wheel_sha256") == EXPECTED_HISTORICAL_WHEEL_SHA, "historical Gate-05B wheel digest changed")
    require(anchors.get("sdist_sha256") == EXPECTED_HISTORICAL_SDIST_SHA, "historical Gate-05B sdist digest changed")

    current = overlay.get("current_candidate", {}).get("package")
    require(isinstance(current, dict), "current package identity missing")
    require(current.get("identity_state") == "CI_OBSERVED_DETERMINISTIC_CURRENT_CANDIDATE", "current package identity is not CI-observed")
    wheel_sha = current.get("wheel_sha256")
    sdist_sha = current.get("sdist_sha256")
    require(isinstance(wheel_sha, str) and len(wheel_sha) == 64, "current wheel digest missing")
    require(isinstance(sdist_sha, str) and len(sdist_sha) == 64, "current sdist digest missing")
    return wheel_sha, sdist_sha


def main() -> int:
    wheel_sha, sdist_sha = current_identity()
    historical = load_historical()
    historical.WHEEL_SHA256 = wheel_sha
    historical.SDIST_SHA256 = sdist_sha
    result = historical.main()
    print(
        "AX_SDK_CURRENT_LOCAL_INDEX_IDENTITY_PASS "
        f"wheel={wheel_sha} sdist={sdist_sha} historical_ci010_preserved=true"
    )
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
