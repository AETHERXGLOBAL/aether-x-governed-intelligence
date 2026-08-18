#!/usr/bin/env python3
"""Build deterministic AX-PUB-EVAL-PACK-001 from the promoted source state.

The bundle is engineering transport for evaluator handoff preparation. It does
not perform an external registry write and cannot establish human evaluation,
adoption, supported-SDK status, or publication authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "sdk-release-candidate" / "python"
PACK_SOURCE = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
PACK_ID = "AX-PUB-EVAL-PACK-001"
PACK_VERSION = "0.1"
PACK_ZIP = "AX-PUB-EVAL-PACK-001.zip"
SOURCE_DATE_EPOCH = "1787076737"
WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
SDIST = "aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
VALIDATION_SUBJECT_SHA = "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2"

SOURCE_MAP = {
    "artifacts/AX-PUB-EVAL-PACK-001.json": "AX-PUB-EVAL-PACK-001.json",
    "docs/INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md": "EVALUATOR_GUIDE.md",
    "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json": "AX-PUB-EVAL-REPORT-002.template.json",
    "tools/check_installable_external_evaluation_report.py": "check_installable_external_evaluation_report.py",
    "artifacts/AX-PUB-API-001.json": "contracts/AX-PUB-API-001.json",
    "artifacts/AX-PUB-SUP-001.json": "contracts/AX-PUB-SUP-001.json",
    "artifacts/AX-PUB-SEC-001.json": "contracts/AX-PUB-SEC-001.json",
    "docs/LIMITATIONS_AND_UNSUPPORTED_USES.md": "LIMITATIONS_AND_UNSUPPORTED_USES.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_EVALUATOR_HANDOFF_BUILD_FAIL: {message}")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def validate_source() -> None:
    pack = load_json(PACK_SOURCE)
    if pack.get("artifact_id") != PACK_ID or pack.get("version") != PACK_VERSION:
        fail("pack identity mismatch")
    if pack.get("state") != "DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CI_VALIDATED":
        fail("promoted pack state mismatch")
    evidence = pack.get("validation_evidence")
    if not isinstance(evidence, dict) or evidence.get("id") != "AX-PUB-CI-014":
        fail("CI-014 validation evidence linkage missing")
    if evidence.get("validation_subject_zip_sha256") != VALIDATION_SUBJECT_SHA:
        fail("CI-014 validation-subject digest mismatch")
    if evidence.get("conclusion") != "SUCCESS":
        fail("CI-014 conclusion mismatch")
    state = pack.get("current_state")
    if not isinstance(state, dict) or state.get("handoff_pack_defined") is not True:
        fail("handoff pack definition state missing")
    if state.get("handoff_pack_ci_validated") is not True:
        fail("handoff pack CI validation state missing")
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
        if state.get(key) is not False:
            fail(f"authority boundary changed: {key}")


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command), flush=True)
    result = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if result.returncode != 0:
        fail(f"command failed exit={result.returncode}: {' '.join(command)}")


def write_manifest(stage: Path) -> Path:
    files: list[dict[str, Any]] = []
    manifest_name = f"{PACK_ID}.manifest.json"
    for path in sorted(p for p in stage.rglob("*") if p.is_file()):
        rel = path.relative_to(stage).as_posix()
        if rel == manifest_name:
            continue
        files.append({"path": rel, "sha256": sha(path), "size_bytes": path.stat().st_size})
    manifest = {
        "manifest_format": "AX-PUB-EVAL-PACK-MANIFEST-001",
        "manifest_version": "1.1",
        "pack_id": PACK_ID,
        "pack_version": PACK_VERSION,
        "source_state": "CI_VALIDATED_HANDOFF_SOURCE",
        "validation_evidence": "AX-PUB-CI-014",
        "candidate": {
            "distribution": "aetherxglobal-governed-intelligence",
            "version": "0.1.0rc1",
            "wheel": {"filename": WHEEL, "sha256": WHEEL_SHA},
            "sdist": {"filename": SDIST, "sha256": SDIST_SHA},
        },
        "transport_scope": "CI_OR_LOCAL_EVALUATOR_HANDOFF_REHEARSAL",
        "final_external_index_required": True,
        "human_external_evaluation_established": False,
        "external_registry_validation_established": False,
        "sdk_publication_authorized": False,
        "files": files,
        "claim_boundaries": [
            "HANDOFF PACK CI VALIDATION DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
            "LOCAL REHEARSAL DOES NOT SATISFY FINAL EXTERNAL-INDEX EVALUATION",
            "CI ARTIFACT DOES NOT ESTABLISH TESTPYPI OR PYPI PUBLICATION",
            "SDK PUBLICATION NOT AUTHORIZED",
        ],
    }
    target = stage / manifest_name
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def write_zip(stage: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            rel = path.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    validate_source()

    env = os.environ.copy()
    env.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_CACHE_DIR": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
    })
    shutil.rmtree(output, ignore_errors=True)
    work = output / ".work"
    dist = work / "dist"
    stage = work / "stage"
    dist.mkdir(parents=True)
    stage.mkdir(parents=True)

    run([sys.executable, "-m", "build", "--no-isolation", "--wheel", "--sdist", "--outdir", str(dist), "."], cwd=PACKAGE, env=env)
    wheel, sdist = dist / WHEEL, dist / SDIST
    if not wheel.is_file() or not sdist.is_file():
        fail("exact wheel/sdist missing")
    if sha(wheel) != WHEEL_SHA or sha(sdist) != SDIST_SHA:
        fail("exact Gate-05B package identity changed")

    for source_rel, target_rel in SOURCE_MAP.items():
        source = ROOT / source_rel
        if not source.is_file():
            fail(f"missing handoff source: {source_rel}")
        target = stage / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    payload = stage / "payload"
    payload.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(wheel, payload / WHEEL)
    shutil.copyfile(sdist, payload / SDIST)

    manifest = write_manifest(stage)
    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / PACK_ZIP
    write_zip(stage, zip_path)
    shutil.copyfile(manifest, output / manifest.name)
    shutil.rmtree(work, ignore_errors=True)

    print(
        "AX_EVALUATOR_HANDOFF_BUILD_PASS "
        f"pack={PACK_ID} state=CI_VALIDATED_SOURCE zip_sha256={sha(zip_path)} "
        f"wheel={WHEEL_SHA} sdist={SDIST_SHA} external_write=false "
        "human_evaluation=false sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
