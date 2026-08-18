#!/usr/bin/env python3
"""Build the deterministic AX-PUB-EVAL-PACK-001 evaluator handoff bundle.

This is a local/CI engineering transport. It rebuilds and verifies the exact
Gate-05B installable candidate, then packages bounded public evaluation
materials for independent-human handoff preparation. It performs no external
registry write and does not establish human evaluation or SDK publication.
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


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command), flush=True)
    result = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if result.returncode != 0:
        fail(f"command failed with exit={result.returncode}: {' '.join(command)}")


def load_pack_source() -> dict[str, Any]:
    try:
        data = json.loads(PACK_SOURCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {PACK_SOURCE.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail("pack artifact root must be an object")
    if data.get("artifact_id") != PACK_ID or data.get("version") != PACK_VERSION:
        fail("pack artifact identity mismatch")
    state = data.get("current_state")
    if not isinstance(state, dict):
        fail("pack current_state missing")
    for key in (
        "handoff_pack_ci_validated",
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
            fail(f"pre-validation/authority boundary changed: {key}")
    return data


def copy_source(relative: str, target_relative: str, stage: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        fail(f"missing source: {relative}")
    target = stage / target_relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def write_manifest(stage: Path) -> None:
    files: list[dict[str, Any]] = []
    for path in sorted(p for p in stage.rglob("*") if p.is_file()):
        relative = path.relative_to(stage).as_posix()
        if relative == f"{PACK_ID}.manifest.json":
            continue
        files.append({
            "path": relative,
            "sha256": digest(path),
            "size_bytes": path.stat().st_size,
        })

    manifest = {
        "manifest_format": "AX-PUB-EVAL-PACK-MANIFEST-001",
        "manifest_version": "1.0",
        "pack_id": PACK_ID,
        "pack_version": PACK_VERSION,
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
            "HANDOFF PACK BUILD DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
            "LOCAL REHEARSAL DOES NOT SATISFY FINAL EXTERNAL-INDEX EVALUATION",
            "CI ARTIFACT DOES NOT ESTABLISH TESTPYPI OR PYPI PUBLICATION",
            "SDK PUBLICATION NOT AUTHORIZED",
        ],
    }
    (stage / f"{PACK_ID}.manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_deterministic_zip(stage: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            relative = path.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()

    load_pack_source()

    env = os.environ.copy()
    env.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_CACHE_DIR": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
    })

    work = output_dir / ".work"
    dist = work / "dist"
    stage = work / "stage"
    shutil.rmtree(output_dir, ignore_errors=True)
    dist.mkdir(parents=True)
    stage.mkdir(parents=True)

    run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--wheel",
            "--sdist",
            "--outdir",
            str(dist),
            ".",
        ],
        cwd=PACKAGE,
        env=env,
    )

    wheel = dist / WHEEL
    sdist = dist / SDIST
    if not wheel.is_file() or not sdist.is_file():
        fail("exact wheel/sdist missing after build")
    observed_wheel = digest(wheel)
    observed_sdist = digest(sdist)
    if observed_wheel != WHEEL_SHA:
        fail(f"wheel digest mismatch: {observed_wheel}")
    if observed_sdist != SDIST_SHA:
        fail(f"sdist digest mismatch: {observed_sdist}")

    for source, target in SOURCE_MAP.items():
        copy_source(source, target, stage)

    payload = stage / "payload"
    payload.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(wheel, payload / WHEEL)
    shutil.copyfile(sdist, payload / SDIST)

    write_manifest(stage)

    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / PACK_ZIP
    write_deterministic_zip(stage, zip_path)
    zip_sha = digest(zip_path)

    # Keep only the final transport bundle and a copy of its manifest for CI inspection.
    shutil.copyfile(stage / f"{PACK_ID}.manifest.json", output_dir / f"{PACK_ID}.manifest.json")
    shutil.rmtree(work, ignore_errors=True)

    print(
        "AX_EVALUATOR_HANDOFF_BUILD_PASS "
        f"pack={PACK_ID} version={PACK_VERSION} zip_sha256={zip_sha} "
        f"wheel={WHEEL_SHA} sdist={SDIST_SHA} external_write=false "
        "human_evaluation=false sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
