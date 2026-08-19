#!/usr/bin/env python3
"""Build the current evaluator handoff while preserving historical CI-014 identity.

The byte-preserved historical builder validates the historical source state.
This adapter supplies only the explicit current package identity and current
handoff guidance/template for the AXGI-REV-001 correction candidate.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "tools" / "build_installable_evaluator_handoff_historical.py"
OVERLAY = ROOT / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json"
PACK = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
CURRENT_GUIDE = "docs/INSTALLABLE_EXTERNAL_EVALUATOR_CURRENT_CANDIDATE_GUIDE.md"
CURRENT_TEMPLATE = "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.current.template.json"


def fail(message: str) -> None:
    raise SystemExit(f"AX_EVALUATOR_CURRENT_CANDIDATE_BUILD_FAIL: {message}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def load_historical():
    spec = importlib.util.spec_from_file_location("ax_eval_handoff_builder_historical", HISTORICAL)
    if spec is None or spec.loader is None:
        fail("cannot load historical evaluator-handoff builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    overlay = load(OVERLAY)
    pack = load(PACK)
    anchors = overlay.get("historical_anchors", {}).get("evaluator_handoff")
    current = overlay.get("current_candidate", {}).get("package")
    if not isinstance(anchors, dict) or not isinstance(current, dict):
        fail("candidate identity evidence is incomplete")
    if anchors.get("validation_subject_zip_sha256") != "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2":
        fail("overlay attempts to redefine historical CI-014 validation subject")
    if pack.get("validation_evidence", {}).get("validation_subject_zip_sha256") != anchors.get("validation_subject_zip_sha256"):
        fail("historical CI-014 validation subject changed")
    if pack.get("validation_evidence", {}).get("id") != "AX-PUB-CI-014":
        fail("historical AX-PUB-CI-014 linkage changed")
    historical_candidate = pack.get("candidate", {})
    if historical_candidate.get("wheel_sha256") != anchors.get("wheel_sha256") or historical_candidate.get("sdist_sha256") != anchors.get("sdist_sha256"):
        fail("historical evaluator package identity changed")

    wheel_sha = current.get("wheel_sha256")
    sdist_sha = current.get("sdist_sha256")
    if current.get("identity_state") != "CI_OBSERVED_DETERMINISTIC_CURRENT_CANDIDATE":
        fail("current package identity is not CI-observed")
    if not isinstance(wheel_sha, str) or len(wheel_sha) != 64 or not isinstance(sdist_sha, str) or len(sdist_sha) != 64:
        fail("current package digests are incomplete")

    historical = load_historical()
    historical.WHEEL_SHA = wheel_sha
    historical.SDIST_SHA = sdist_sha
    source_map = dict(historical.SOURCE_MAP)
    source_map["docs/INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md"] = "HISTORICAL_EVALUATOR_GUIDE.md"
    source_map.pop("examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json", None)
    source_map[CURRENT_GUIDE] = "EVALUATOR_GUIDE.md"
    source_map[CURRENT_TEMPLATE] = "AX-PUB-EVAL-REPORT-002.template.json"
    source_map["artifacts/AX-PUB-CANDIDATE-IDENTITY-001.json"] = "CURRENT_CANDIDATE_IDENTITY.json"
    historical.SOURCE_MAP = source_map
    result = historical.main()
    print(f"AX_EVALUATOR_CURRENT_CANDIDATE_BUILD_PASS wheel={wheel_sha} sdist={sdist_sha} historical_ci014_preserved=true")
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
