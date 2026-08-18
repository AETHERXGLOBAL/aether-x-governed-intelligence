#!/usr/bin/env python3
"""Run deterministic DEV-GATE-05C pre-distribution CI.

This runner performs local/reversible engineering only. It installs the fixed
build toolchain, rebuilds the exact Gate-05B candidate, validates its immutable
hashes, exercises index-based installation through loopback on CPython
3.11-3.14, and re-runs inherited governance. It performs no external registry
write and cannot establish human external evaluation or release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "sdk-release-candidate" / "python"
DIST = PACKAGE / "dist-gate05c"
REPORTS = ROOT / "gate05c-reports"
WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
SDIST = "aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
RUNTIMES = ("3.11", "3.12", "3.13", "3.14")


def run(cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=cwd, env=env, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_governance(py: str) -> None:
    for script in (
        "tools/check_sdk_distribution_external_validation.py",
        "tools/check_sdk_release_candidate_document.py",
        "tools/check_sdk_release_candidate_boundary.py",
        "tools/check_sdk_release_decision_baseline.py",
        "tools/check_sdk_release_decision_manifest_state.py",
        "tools/check_supply_chain_release_candidate.py",
        "tools/check_external_evaluation_readiness.py",
        "tools/check_artifact_manifest.py",
    ):
        run([py, script])
    run([
        py,
        "tools/check_installable_external_evaluation_report.py",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json",
        "--allow-template",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    for runtime in RUNTIMES:
        parser.add_argument(f"--py{runtime.replace('.', '')}", required=True)
    args = parser.parse_args()
    pythons = {
        runtime: str(Path(getattr(args, f"py{runtime.replace('.', '')}")).resolve())
        for runtime in RUNTIMES
    }
    py314 = pythons["3.14"]

    for runtime, exe in pythons.items():
        completed = subprocess.run([exe, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"], text=True, capture_output=True, check=True)
        actual = completed.stdout.strip()
        if actual != runtime:
            raise SystemExit(f"AX_GATE05C_RUNTIME_IDENTITY_FAIL expected={runtime} actual={actual}")
    print("AX_GATE05C_RUNTIME_MATRIX_IDENTITY_PASS runtimes=3.11,3.12,3.13,3.14")

    for path in (
        "artifacts/AX-PUB-DEV-009.json",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json",
    ):
        run([py314, "-m", "json.tool", path], cwd=ROOT)
    for script in (
        "tools/run_sdk_local_index_validation.py",
        "tools/run_gate05c_ci.py",
        "tools/check_sdk_distribution_external_validation.py",
        "tools/check_installable_external_evaluation_report.py",
    ):
        run([py314, "-m", "py_compile", script], cwd=ROOT)

    check_governance(py314)

    env = os.environ.copy()
    env.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_CACHE_DIR": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOURCE_DATE_EPOCH": "1787076737",
    })
    run([py314, "-m", "pip", "install", "--disable-pip-version-check", "build==1.5.0", "hatchling==1.31.0"], env=env)
    run([
        py314,
        "-c",
        "import importlib.metadata as m; assert m.version('build')=='1.5.0'; assert m.version('hatchling')=='1.31.0'; print('AX_GATE05C_BUILD_TOOLCHAIN_PASS')",
    ], env=env)

    shutil.rmtree(DIST, ignore_errors=True)
    run([py314, "-m", "build", "--no-isolation", "--wheel", "--sdist", "--outdir", str(DIST), "."], cwd=PACKAGE, env=env)
    wheel = DIST / WHEEL
    sdist = DIST / SDIST
    if not wheel.is_file() or not sdist.is_file():
        raise SystemExit("AX_GATE05C_EXACT_CANDIDATE_FAIL missing wheel/sdist")
    wh = digest(wheel)
    sh = digest(sdist)
    if wh != WHEEL_SHA or sh != SDIST_SHA:
        raise SystemExit(f"AX_GATE05C_EXACT_CANDIDATE_FAIL wheel={wh} sdist={sh}")
    print(f"AX_GATE05C_EXACT_CANDIDATE_IDENTITY_PASS wheel={wh} sdist={sh}")

    shutil.rmtree(REPORTS, ignore_errors=True)
    REPORTS.mkdir(parents=True)
    for runtime, exe in pythons.items():
        report = REPORTS / f"python-{runtime}.json"
        run([
            exe,
            "tools/run_sdk_local_index_validation.py",
            "--dist-dir", str(DIST),
            "--json-out", str(report),
        ], env=env)

    observed: list[str] = []
    for path in sorted(REPORTS.glob("*.json")):
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["result"] == "PASS"
        assert report["external_registry_validation"] is False
        assert report["external_registry_write_performed"] is False
        assert report["sdk_publication_authorized"] is False
        assert report["wheel"]["sha256"] == WHEEL_SHA
        assert report["sdist"]["sha256"] == SDIST_SHA
        observed.append(report["runtime"])
    if observed != list(RUNTIMES):
        raise SystemExit(f"AX_GATE05C_LOCAL_INDEX_MATRIX_FAIL observed={observed}")
    print("AX_GATE05C_LOCAL_INDEX_MATRIX_PASS runtimes=3.11,3.12,3.13,3.14 external_write=false")

    shutil.rmtree(DIST, ignore_errors=True)
    check_governance(py314)

    print("TESTPYPI UPLOAD NOT AUTHORIZED")
    print("PYPI UPLOAD NOT AUTHORIZED")
    print("HUMAN EXTERNAL EVALUATION NOT ESTABLISHED BY CI")
    print("SDK PUBLICATION NOT AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
