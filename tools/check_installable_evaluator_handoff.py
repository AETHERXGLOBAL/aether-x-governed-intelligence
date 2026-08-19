#!/usr/bin/env python3
"""Validate current evaluator handoff without rewriting historical CI-014 evidence."""
from __future__ import annotations

import argparse
import importlib.util
import json
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "tools" / "check_installable_evaluator_handoff_historical.py"
HISTORICAL_REPORT_CHECKER = ROOT / "tools" / "check_installable_external_evaluation_report_historical.py"
OVERLAY = ROOT / "artifacts" / "AX-PUB-CANDIDATE-IDENTITY-001.json"
PACK = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
CURRENT_GUIDE = ROOT / "docs" / "INSTALLABLE_EXTERNAL_EVALUATOR_CURRENT_CANDIDATE_GUIDE.md"
CURRENT_TEMPLATE = ROOT / "examples" / "external-evaluation" / "AX-PUB-EVAL-REPORT-002.current.template.json"
PACK_ZIP = "AX-PUB-EVAL-PACK-001.zip"


def fail(message: str) -> None:
    raise SystemExit(f"AX_EVALUATOR_CURRENT_CANDIDATE_FAIL: {message}")


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
    spec = importlib.util.spec_from_file_location("ax_eval_handoff_checker_historical", HISTORICAL)
    if spec is None or spec.loader is None:
        fail("cannot load historical evaluator-handoff checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def current_identity() -> tuple[dict[str, Any], str, str]:
    overlay = load(OVERLAY)
    pack = load(PACK)
    anchors = overlay.get("historical_anchors", {}).get("evaluator_handoff")
    current = overlay.get("current_candidate", {}).get("package")
    require(isinstance(anchors, dict) and isinstance(current, dict), "candidate identity evidence incomplete")
    require(anchors.get("validation_subject_zip_sha256") == "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2", "historical validation subject anchor changed")
    require(pack.get("validation_evidence", {}).get("id") == "AX-PUB-CI-014", "historical AX-PUB-CI-014 linkage changed")
    require(pack.get("validation_evidence", {}).get("validation_subject_zip_sha256") == anchors.get("validation_subject_zip_sha256"), "historical CI-014 validation subject changed")
    historical_candidate = pack.get("candidate", {})
    require(historical_candidate.get("wheel_sha256") == anchors.get("wheel_sha256"), "historical evaluator wheel identity changed")
    require(historical_candidate.get("sdist_sha256") == anchors.get("sdist_sha256"), "historical evaluator sdist identity changed")
    require(current.get("identity_state") == "CI_OBSERVED_DETERMINISTIC_CURRENT_CANDIDATE", "current package identity not CI-observed")
    wheel_sha = current.get("wheel_sha256")
    sdist_sha = current.get("sdist_sha256")
    require(isinstance(wheel_sha, str) and len(wheel_sha) == 64, "current wheel digest missing")
    require(isinstance(sdist_sha, str) and len(sdist_sha) == 64, "current sdist digest missing")
    require(HISTORICAL_REPORT_CHECKER.is_file(), "historical external-evaluation report checker missing")

    guide = CURRENT_GUIDE.read_text(encoding="utf-8")
    require(wheel_sha in guide and sdist_sha in guide, "current evaluator guide package identity mismatch")
    template = load(CURRENT_TEMPLATE)
    candidate = template.get("candidate", {})
    require(candidate.get("wheel_sha256") == wheel_sha and candidate.get("sdist_sha256") == sdist_sha, "current evaluator template package identity mismatch")
    require(template.get("sdk_publication") == "NOT_AUTHORIZED", "current evaluator template publication boundary changed")
    return overlay, wheel_sha, sdist_sha


def check_current_bundle(bundle_dir: Path, overlay: dict[str, Any], wheel_sha: str, sdist_sha: str) -> None:
    zip_path = bundle_dir.resolve() / PACK_ZIP
    require(zip_path.is_file(), "current evaluator handoff ZIP missing")
    with zipfile.ZipFile(zip_path, "r") as archive:
        names = set(archive.namelist())
        for required in (
            "EVALUATOR_GUIDE.md",
            "HISTORICAL_EVALUATOR_GUIDE.md",
            "AX-PUB-EVAL-REPORT-002.template.json",
            "CURRENT_CANDIDATE_IDENTITY.json",
            "check_installable_external_evaluation_report.py",
            "check_installable_external_evaluation_report_historical.py",
        ):
            require(required in names, f"current handoff missing {required}")
        packed_overlay = json.loads(archive.read("CURRENT_CANDIDATE_IDENTITY.json").decode("utf-8"))
        require(packed_overlay == overlay, "packed current candidate identity differs from repository evidence")
        packed_template = json.loads(archive.read("AX-PUB-EVAL-REPORT-002.template.json").decode("utf-8"))
        candidate = packed_template.get("candidate", {})
        require(candidate.get("wheel_sha256") == wheel_sha and candidate.get("sdist_sha256") == sdist_sha, "packed evaluator template package identity mismatch")
        packed_guide = archive.read("EVALUATOR_GUIDE.md").decode("utf-8")
        require(wheel_sha in packed_guide and sdist_sha in packed_guide, "packed current evaluator guide identity mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", type=Path)
    args = parser.parse_args()
    overlay, wheel_sha, sdist_sha = current_identity()
    historical = load_historical()

    # Preserve historical source-state verification by using the byte-preserved
    # historical report checker rather than the current candidate adapter.
    historical.REPORT_CHECKER = HISTORICAL_REPORT_CHECKER
    historical.check_source_state()

    if args.bundle_dir is not None:
        historical.WHEEL_SHA = wheel_sha
        historical.SDIST_SHA = sdist_sha
        historical.check_bundle(args.bundle_dir)
        check_current_bundle(args.bundle_dir, overlay, wheel_sha, sdist_sha)

    print(f"AX_EVALUATOR_CURRENT_CANDIDATE_PASS wheel={wheel_sha} sdist={sdist_sha} historical_ci014_preserved=true sdk_publication=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
