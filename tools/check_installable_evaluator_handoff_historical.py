#!/usr/bin/env python3
"""Validate promoted AX-PUB-EVAL-PACK-001 source state and optional built bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
GUIDE = ROOT / "docs" / "INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md"
TEMPLATE = ROOT / "examples" / "external-evaluation" / "AX-PUB-EVAL-REPORT-002.template.json"
REPORT_CHECKER = ROOT / "tools" / "check_installable_external_evaluation_report.py"
CI014 = ROOT / "evidence" / "AX-PUB-CI-014_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF_VALIDATION.md"
API = ROOT / "artifacts" / "AX-PUB-API-001.json"
SUP = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC = ROOT / "artifacts" / "AX-PUB-SEC-001.json"
DEV009 = ROOT / "artifacts" / "AX-PUB-DEV-009.json"
PACK_ID = "AX-PUB-EVAL-PACK-001"
PACK_VERSION = "0.1"
PACK_ZIP = "AX-PUB-EVAL-PACK-001.zip"
WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
SDIST = "aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
VALIDATION_SUBJECT_SHA = "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]


def fail(message: str) -> None:
    raise SystemExit(f"AX_EVALUATOR_HANDOFF_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def check_source_state() -> None:
    pack, api, sup, sec, dev009 = map(load, (ARTIFACT, API, SUP, SEC, DEV009))
    require(CI014.is_file(), "CI-014 evidence missing")
    require(pack.get("artifact_id") == PACK_ID and pack.get("version") == PACK_VERSION, "pack identity mismatch")
    require(pack.get("state") == "DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CI_VALIDATED", "promoted pack state mismatch")
    require(pack.get("parent_artifact") == "AX-PUB-DEV-009", "pack parent mismatch")

    evidence = pack.get("validation_evidence")
    require(isinstance(evidence, dict), "pack validation evidence missing")
    require(evidence.get("id") == "AX-PUB-CI-014" and evidence.get("version") == "1.0", "CI-014 identity mismatch")
    require(evidence.get("verified_head_commit") == "8817b4540a8dee4ab0b1e1ad1fcb21c4826d710f", "CI-014 verified head mismatch")
    require(evidence.get("workflow_run_id") == 32196714529 and evidence.get("workflow_run_number") == 7, "CI-014 workflow mismatch")
    require(evidence.get("job_id") == 95902129022, "CI-014 job mismatch")
    require(evidence.get("validation_subject_zip_sha256") == VALIDATION_SUBJECT_SHA, "CI-014 validation-subject digest mismatch")
    require(evidence.get("conclusion") == "SUCCESS", "CI-014 conclusion mismatch")

    candidate = pack.get("candidate")
    require(isinstance(candidate, dict), "candidate identity missing")
    require(candidate.get("distribution") == "aetherxglobal-governed-intelligence", "distribution mismatch")
    require(candidate.get("version") == "0.1.0rc1", "candidate version mismatch")
    require(candidate.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(candidate.get("wheel_filename") == WHEEL and candidate.get("wheel_sha256") == WHEEL_SHA, "wheel identity mismatch")
    require(candidate.get("sdist_filename") == SDIST and candidate.get("sdist_sha256") == SDIST_SHA, "sdist identity mismatch")
    require(candidate.get("verified_runtime_matrix") == RUNTIMES, "runtime matrix mismatch")

    report = pack.get("report_contract")
    require(isinstance(report, dict), "report contract missing")
    require(report.get("format") == "AX-PUB-EVAL-REPORT-002" and report.get("version") == "1.0", "report contract identity mismatch")
    for key in ("final_requires_independent_human_evaluator", "final_requires_external_index_used", "final_requires_issue_disposition_complete"):
        require(report.get(key) is True, f"report requirement missing: {key}")
    require(report.get("final_allows_unresolved_critical") is False, "critical finding firewall changed")
    require(report.get("final_high_requires_fix_or_authorized_risk_acceptance") is True, "HIGH finding firewall changed")

    handoff = pack.get("handoff")
    require(isinstance(handoff, dict), "handoff definition missing")
    require(handoff.get("bundle_filename") == PACK_ZIP, "bundle filename mismatch")
    require(handoff.get("local_rehearsal_is_final_human_evaluation") is False, "local rehearsal boundary changed")
    require(handoff.get("actions_artifact_is_package_registry_publication") is False, "Actions artifact boundary changed")
    require(handoff.get("final_evaluation_must_acquire_candidate_from_authorized_external_index") is True, "final external-index requirement missing")

    current = pack.get("current_state")
    require(isinstance(current, dict), "pack current state missing")
    require(current.get("handoff_pack_defined") is True and current.get("handoff_pack_ci_validated") is True, "handoff validation state mismatch")
    for key in (
        "external_registry_validation_established", "human_external_evaluation_occurred", "external_adoption_established",
        "release_control_readiness_established", "registry_ownership_established", "public_sdk_licence_granted",
        "supported_sdk_established", "sdk_publication_authorized",
    ):
        require(current.get(key) is False, f"authority/maturity boundary changed: {key}")

    boundaries = set(pack.get("claim_boundaries", []))
    for marker in (
        "EVALUATOR HANDOFF PACK DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
        "LOCAL REHEARSAL DOES NOT SATISFY FINAL EXTERNAL-INDEX EVALUATION",
        "CI ARTIFACT DISTRIBUTION DOES NOT ESTABLISH TESTPYPI OR PYPI PUBLICATION",
        "EVALUATION PASS DOES NOT ESTABLISH A SUPPORTED SDK",
        "EVALUATION PASS DOES NOT ESTABLISH RELEASE AUTHORITY",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in boundaries, f"claim boundary missing: {marker}")

    require(api.get("artifact_id") == "AX-PUB-API-001" and api.get("stable_api_guarantee_established") is False, "API binding/boundary mismatch")
    require(sup.get("artifact_id") == "AX-PUB-SUP-001" and sup.get("support_commitment_established") is False, "support binding/boundary mismatch")
    require(sec.get("artifact_id") == "AX-PUB-SEC-001" and sec.get("security_operations_ready") is False, "security binding/boundary mismatch")
    require(dev009.get("phase") == "DEV-GATE-05C" and dev009.get("phase_state") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C must remain active")
    require(dev009.get("external_registry_write_authorized") is False and dev009.get("supported_sdk_established") is False, "Gate-05C authority boundary changed")

    guide = GUIDE.read_text(encoding="utf-8")
    for marker in ("AX-PUB-EVAL-PACK-001", "LOCAL REHEARSAL ≠ FINAL EXTERNAL-INDEX EVALUATION", "external_index_used", "<AUTHORIZED_EXTERNAL_INDEX_URL>", WHEEL_SHA, SDIST_SHA, "SDK PUBLICATION NOT AUTHORIZED"):
        require(marker in guide, f"guide missing marker: {marker}")

    result = subprocess.run([sys.executable, str(REPORT_CHECKER), str(TEMPLATE), "--allow-template"], cwd=ROOT, text=True, capture_output=True, check=False)
    require(result.returncode == 0 and "AX_INSTALLABLE_EXTERNAL_EVALUATION_TEMPLATE_PASS" in result.stdout, "report template validation failed")


def check_bundle(bundle_dir: Path) -> None:
    bundle_dir = bundle_dir.resolve()
    zip_path = bundle_dir / PACK_ZIP
    manifest_path = bundle_dir / f"{PACK_ID}.manifest.json"
    require(zip_path.is_file() and manifest_path.is_file(), "built handoff outputs missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("manifest_format") == "AX-PUB-EVAL-PACK-MANIFEST-001", "built manifest format mismatch")
    require(manifest.get("manifest_version") == "1.1", "built manifest version mismatch")
    require(manifest.get("pack_id") == PACK_ID and manifest.get("pack_version") == PACK_VERSION, "built manifest identity mismatch")
    require(manifest.get("source_state") == "CI_VALIDATED_HANDOFF_SOURCE", "built source-state marker mismatch")
    require(manifest.get("validation_evidence") == "AX-PUB-CI-014", "built CI-014 linkage missing")
    require(manifest.get("final_external_index_required") is True, "built final external-index requirement missing")
    require(manifest.get("human_external_evaluation_established") is False, "bundle must not claim human evaluation")
    require(manifest.get("external_registry_validation_established") is False, "bundle must not claim external registry validation")
    require(manifest.get("sdk_publication_authorized") is False, "bundle must not authorize publication")
    files = manifest.get("files")
    require(isinstance(files, list) and files, "built file inventory missing")
    expected = {item.get("path"): item for item in files if isinstance(item, dict)}
    require(expected.get(f"payload/{WHEEL}", {}).get("sha256") == WHEEL_SHA, "bundle wheel digest mismatch")
    require(expected.get(f"payload/{SDIST}", {}).get("sha256") == SDIST_SHA, "bundle sdist digest mismatch")

    with zipfile.ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP entry")
        for name in names:
            path = Path(name)
            require(not path.is_absolute() and ".." not in path.parts, f"unsafe ZIP path: {name}")
        embedded = json.loads(archive.read(f"{PACK_ID}.manifest.json").decode("utf-8"))
        require(embedded == manifest, "embedded/external manifests differ")
        require(set(names) == set(expected) | {f"{PACK_ID}.manifest.json"}, "ZIP inventory mismatch")
        for name, item in expected.items():
            payload = archive.read(name)
            require(digest_bytes(payload) == item.get("sha256") and len(payload) == item.get("size_bytes"), f"ZIP payload identity mismatch: {name}")
        packed_source = json.loads(archive.read("AX-PUB-EVAL-PACK-001.json").decode("utf-8"))
        packed_state = packed_source.get("current_state", {})
        require(packed_state.get("handoff_pack_ci_validated") is True, "packed promoted validation state missing")
        require(packed_state.get("human_external_evaluation_occurred") is False, "packed source must not claim human evaluation")
        require(packed_state.get("sdk_publication_authorized") is False, "packed source must not authorize publication")

    print(f"AX_EVALUATOR_HANDOFF_BUNDLE_PASS zip_sha256={digest(zip_path)} files={len(expected)} human_evaluation=false external_registry=false publication=NOT_AUTHORIZED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", type=Path)
    args = parser.parse_args()
    check_source_state()
    if args.bundle_dir is not None:
        check_bundle(args.bundle_dir)
    print("AX_EVALUATOR_HANDOFF_SOURCE_PASS state=CI_VALIDATED_HANDOFF_SOURCE final_external_index_required=true human_evaluation=false sdk_publication=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
