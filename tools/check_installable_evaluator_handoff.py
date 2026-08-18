#!/usr/bin/env python3
"""Validate AX-PUB-EVAL-PACK-001 source state and optional built bundle."""
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
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]

REQUIRED_BOUNDARIES = {
    "EVALUATOR HANDOFF PACK DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
    "LOCAL REHEARSAL DOES NOT SATISFY FINAL EXTERNAL-INDEX EVALUATION",
    "CI ARTIFACT DISTRIBUTION DOES NOT ESTABLISH TESTPYPI OR PYPI PUBLICATION",
    "EVALUATION PASS DOES NOT ESTABLISH ENDORSEMENT OR ADOPTION",
    "EVALUATION PASS DOES NOT ESTABLISH A SUPPORTED SDK",
    "EVALUATION PASS DOES NOT ESTABLISH RELEASE AUTHORITY",
    "SDK PUBLICATION NOT AUTHORIZED",
}


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
    pack = load(ARTIFACT)
    api = load(API)
    sup = load(SUP)
    sec = load(SEC)
    dev009 = load(DEV009)

    require(pack.get("artifact_id") == PACK_ID, "pack artifact ID mismatch")
    require(pack.get("version") == PACK_VERSION, "pack artifact version mismatch")
    require(pack.get("state") == "DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CANDIDATE", "pack state mismatch")
    require(pack.get("parent_artifact") == "AX-PUB-DEV-009", "pack parent mismatch")

    candidate = pack.get("candidate")
    require(isinstance(candidate, dict), "pack candidate identity missing")
    require(candidate.get("distribution") == "aetherxglobal-governed-intelligence", "distribution mismatch")
    require(candidate.get("version") == "0.1.0rc1", "candidate version mismatch")
    require(candidate.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(candidate.get("wheel_filename") == WHEEL, "wheel filename mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA, "wheel digest mismatch")
    require(candidate.get("sdist_filename") == SDIST, "sdist filename mismatch")
    require(candidate.get("sdist_sha256") == SDIST_SHA, "sdist digest mismatch")
    require(candidate.get("verified_runtime_matrix") == RUNTIMES, "runtime matrix mismatch")

    report = pack.get("report_contract")
    require(isinstance(report, dict), "report contract missing")
    require(report.get("format") == "AX-PUB-EVAL-REPORT-002", "report format mismatch")
    require(report.get("version") == "1.0", "report version mismatch")
    require(report.get("template_path") == "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json", "template path mismatch")
    require(report.get("checker_path") == "tools/check_installable_external_evaluation_report.py", "report checker path mismatch")
    require(report.get("final_record_state") == "FINAL", "final record state mismatch")
    require(report.get("final_requires_independent_human_evaluator") is True, "human independence requirement missing")
    require(report.get("final_requires_external_index_used") is True, "external-index requirement missing")
    require(report.get("final_requires_issue_disposition_complete") is True, "issue disposition requirement missing")
    require(report.get("final_allows_unresolved_critical") is False, "critical finding boundary changed")
    require(report.get("final_high_requires_fix_or_authorized_risk_acceptance") is True, "high finding disposition requirement missing")

    handoff = pack.get("handoff")
    require(isinstance(handoff, dict), "handoff definition missing")
    require(handoff.get("guide_path") == "docs/INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md", "guide path mismatch")
    require(handoff.get("builder_path") == "tools/build_installable_evaluator_handoff.py", "builder path mismatch")
    require(handoff.get("checker_path") == "tools/check_installable_evaluator_handoff.py", "handoff checker path mismatch")
    require(handoff.get("bundle_filename") == PACK_ZIP, "bundle filename mismatch")
    require(handoff.get("local_rehearsal_payload_includes_exact_wheel_and_sdist") is True, "local payload requirement missing")
    require(handoff.get("local_rehearsal_is_final_human_evaluation") is False, "local rehearsal must not become final evaluation")
    require(handoff.get("actions_artifact_is_package_registry_publication") is False, "Actions artifact must not become registry publication")
    require(handoff.get("final_evaluation_must_acquire_candidate_from_authorized_external_index") is True, "final external-index requirement missing")

    current = pack.get("current_state")
    require(isinstance(current, dict), "pack current state missing")
    require(current.get("handoff_pack_defined") is True, "pack must be defined")
    require(current.get("handoff_pack_ci_validated") is False, "candidate pack must remain pre-evidence on this baseline")
    for key in (
        "external_registry_validation_established",
        "human_external_evaluation_occurred",
        "external_adoption_established",
        "release_control_readiness_established",
        "registry_ownership_established",
        "public_sdk_licence_granted",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        require(current.get(key) is False, f"authority/maturity boundary changed: {key}")

    require(REQUIRED_BOUNDARIES <= set(pack.get("claim_boundaries", [])), "required pack claim boundary missing")

    # Bind the handoff to the current productization contracts without promoting them.
    require(api.get("artifact_id") == "AX-PUB-API-001" and api.get("sdk_version_candidate") == "0.1.0rc1", "API candidate binding mismatch")
    require(api.get("stable_api_guarantee_established") is False, "API stable guarantee must remain false")
    require(sup.get("artifact_id") == "AX-PUB-SUP-001" and sup.get("support_commitment_established") is False, "support contract binding/boundary mismatch")
    require(sec.get("artifact_id") == "AX-PUB-SEC-001" and sec.get("security_operations_ready") is False, "security contract binding/boundary mismatch")
    require(dev009.get("phase") == "DEV-GATE-05C" and dev009.get("phase_state") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C must remain active")
    require(dev009.get("external_registry_write_authorized") is False, "external registry write must remain unauthorized")
    require(dev009.get("supported_sdk_established") is False, "supported SDK must remain false")

    guide = GUIDE.read_text(encoding="utf-8")
    for marker in (
        "AX-PUB-EVAL-PACK-001",
        "LOCAL REHEARSAL ≠ FINAL EXTERNAL-INDEX EVALUATION",
        "external_index_used",
        "<AUTHORIZED_EXTERNAL_INDEX_URL>",
        WHEEL_SHA,
        SDIST_SHA,
        "EVALUATION PASS ≠ SUPPORTED SDK",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in guide, f"guide missing marker: {marker}")

    # The repository template must stay a template; CI validation cannot promote it.
    result = subprocess.run(
        [sys.executable, str(REPORT_CHECKER), str(TEMPLATE), "--allow-template"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"report template checker failed: {result.stdout} {result.stderr}")
    require("AX_INSTALLABLE_EXTERNAL_EVALUATION_TEMPLATE_PASS" in result.stdout, "template success marker missing")


def check_bundle(bundle_dir: Path) -> None:
    bundle_dir = bundle_dir.resolve()
    zip_path = bundle_dir / PACK_ZIP
    manifest_path = bundle_dir / f"{PACK_ID}.manifest.json"
    require(zip_path.is_file(), f"built bundle missing: {zip_path}")
    require(manifest_path.is_file(), f"built manifest missing: {manifest_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse built pack manifest: {exc}")
    require(isinstance(manifest, dict), "built pack manifest must contain object")
    require(manifest.get("manifest_format") == "AX-PUB-EVAL-PACK-MANIFEST-001", "built manifest format mismatch")
    require(manifest.get("pack_id") == PACK_ID and manifest.get("pack_version") == PACK_VERSION, "built manifest identity mismatch")
    require(manifest.get("final_external_index_required") is True, "built manifest must require final external index")
    require(manifest.get("human_external_evaluation_established") is False, "bundle must not claim human evaluation")
    require(manifest.get("external_registry_validation_established") is False, "bundle must not claim external registry validation")
    require(manifest.get("sdk_publication_authorized") is False, "bundle must not authorize publication")

    candidate = manifest.get("candidate")
    require(isinstance(candidate, dict), "built manifest candidate missing")
    require(candidate.get("wheel", {}).get("sha256") == WHEEL_SHA, "built manifest wheel identity mismatch")
    require(candidate.get("sdist", {}).get("sha256") == SDIST_SHA, "built manifest sdist identity mismatch")

    files = manifest.get("files")
    require(isinstance(files, list) and files, "built manifest file inventory missing")
    expected = {item.get("path"): item for item in files if isinstance(item, dict)}
    require(f"payload/{WHEEL}" in expected, "wheel missing from built manifest")
    require(f"payload/{SDIST}" in expected, "sdist missing from built manifest")
    require(expected[f"payload/{WHEEL}"].get("sha256") == WHEEL_SHA, "bundle wheel hash mismatch")
    require(expected[f"payload/{SDIST}"].get("sha256") == SDIST_SHA, "bundle sdist hash mismatch")

    with zipfile.ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP entry")
        for name in names:
            path = Path(name)
            require(not path.is_absolute() and ".." not in path.parts, f"unsafe ZIP path: {name}")
        require(f"{PACK_ID}.manifest.json" in names, "ZIP embedded manifest missing")
        embedded_manifest = json.loads(archive.read(f"{PACK_ID}.manifest.json").decode("utf-8"))
        require(embedded_manifest == manifest, "external and embedded pack manifests differ")

        expected_names = set(expected) | {f"{PACK_ID}.manifest.json"}
        require(set(names) == expected_names, "ZIP inventory differs from built manifest")
        for name, item in expected.items():
            payload = archive.read(name)
            require(digest_bytes(payload) == item.get("sha256"), f"ZIP payload hash mismatch: {name}")
            require(len(payload) == item.get("size_bytes"), f"ZIP payload size mismatch: {name}")

        packed_source = json.loads(archive.read("AX-PUB-EVAL-PACK-001.json").decode("utf-8"))
        state = packed_source.get("current_state", {})
        require(state.get("human_external_evaluation_occurred") is False, "packed source must not claim human evaluation")
        require(state.get("sdk_publication_authorized") is False, "packed source must not authorize publication")

    print(
        "AX_EVALUATOR_HANDOFF_BUNDLE_PASS "
        f"zip_sha256={digest(zip_path)} files={len(expected)} "
        "external_registry=false human_evaluation=false publication=NOT_AUTHORIZED"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", type=Path)
    args = parser.parse_args()

    check_source_state()
    if args.bundle_dir is not None:
        check_bundle(args.bundle_dir)

    print(
        "AX_EVALUATOR_HANDOFF_SOURCE_PASS "
        "state=CANDIDATE local_rehearsal_only=true final_external_index_required=true "
        "human_evaluation=false sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
