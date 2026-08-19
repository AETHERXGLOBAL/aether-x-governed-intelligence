#!/usr/bin/env python3
"""Validate current AX-PUB-EVAL-REPORT-002 records without rewriting historical evidence.

The historical report checker is preserved byte-for-byte and reused as the
validation engine. This adapter binds it to the explicit current/superseding
candidate identity recorded after AXGI-REV-001. It works both in the repository
and inside the standalone evaluator handoff bundle.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
HISTORICAL = HERE / "check_installable_external_evaluation_report_historical.py"
OVERLAY_CANDIDATES = (
    HERE.parent / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json",
    HERE / "CURRENT_CANDIDATE_IDENTITY.json",
)
EXPECTED_HISTORICAL_WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
EXPECTED_HISTORICAL_SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"


def fail(message: str) -> None:
    raise SystemExit(f"AX_INSTALLABLE_EXTERNAL_EVALUATION_CURRENT_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.name}: {exc}")
    require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def load_overlay() -> dict[str, Any]:
    for path in OVERLAY_CANDIDATES:
        if path.is_file():
            return load_json(path)
    fail("current candidate identity evidence is unavailable")


def load_historical():
    require(HISTORICAL.is_file(), "historical report checker missing")
    spec = importlib.util.spec_from_file_location("ax_external_eval_report_historical", HISTORICAL)
    require(spec is not None and spec.loader is not None, "cannot load historical report checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def current_identity(overlay: dict[str, Any]) -> tuple[str, str]:
    require(overlay.get("artifact_id") == "AX-PUB-CANDIDATE-IDENTITY-001", "candidate identity artifact mismatch")
    require(overlay.get("type") == "CURRENT_SUPERSEDING_CANDIDATE_EVIDENCE", "candidate identity type mismatch")
    require(overlay.get("state") == "CURRENT_CANDIDATE_IDENTITY_ALIGNED", "candidate identity state mismatch")

    anchors = overlay.get("historical_anchors", {}).get("evaluator_handoff")
    require(isinstance(anchors, dict), "historical evaluator anchor missing")
    require(anchors.get("evidence_id") == "AX-PUB-CI-014", "historical evaluator evidence identity changed")
    require(anchors.get("wheel_sha256") == EXPECTED_HISTORICAL_WHEEL_SHA, "historical evaluator wheel digest changed")
    require(anchors.get("sdist_sha256") == EXPECTED_HISTORICAL_SDIST_SHA, "historical evaluator sdist digest changed")

    current = overlay.get("current_candidate", {}).get("package")
    require(isinstance(current, dict), "current package identity missing")
    require(current.get("identity_state") == "CI_OBSERVED_DETERMINISTIC_CURRENT_CANDIDATE", "current package identity is not CI-observed")
    wheel_sha = current.get("wheel_sha256")
    sdist_sha = current.get("sdist_sha256")
    require(isinstance(wheel_sha, str) and len(wheel_sha) == 64, "current wheel digest missing")
    require(isinstance(sdist_sha, str) and len(sdist_sha) == 64, "current sdist digest missing")
    return wheel_sha, sdist_sha


def main() -> int:
    overlay = load_overlay()
    wheel_sha, sdist_sha = current_identity(overlay)
    historical = load_historical()
    historical.WHEEL_SHA = wheel_sha
    historical.SDIST_SHA = sdist_sha
    result = historical.main()
    print(
        "AX_INSTALLABLE_EXTERNAL_EVALUATION_CURRENT_CANDIDATE_PASS "
        f"wheel={wheel_sha} sdist={sdist_sha} historical_ci014_preserved=true"
    )
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
