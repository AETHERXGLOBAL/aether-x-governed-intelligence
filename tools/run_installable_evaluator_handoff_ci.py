#!/usr/bin/env python3
"""Run bounded CI validation for AX-PUB-EVAL-PACK-001.

The runner performs only local/CI engineering: source-state checks, exact
candidate rebuild, deterministic handoff double-build, bundle integrity checks,
local rehearsal installation across CPython 3.11-3.14, and blank report-template
validation. It performs no external registry write and cannot establish human
external evaluation or SDK release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ZIP = "AX-PUB-EVAL-PACK-001.zip"
WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
RUNTIMES = ("3.11", "3.12", "3.13", "3.14")


def fail(message: str) -> None:
    raise SystemExit(f"AX_EVALUATOR_HANDOFF_CI_FAIL: {message}")


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, env=env, text=True, check=False)
    if completed.returncode != 0:
        fail(f"command failed with exit={completed.returncode}: {' '.join(command)}")


def expect_failure(
    command: list[str],
    *,
    contains: str,
    env: dict[str, str] | None = None,
) -> None:
    print("+ EXPECT_FAIL", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    combined = f"{completed.stdout}\n{completed.stderr}"
    if completed.returncode == 0 or contains not in combined:
        fail(f"expected fail-closed result containing {contains!r}: {' '.join(command)}")
    print(f"AX_EVALUATOR_REPORT_NEGATIVE_PASS expected={contains}")


def output(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    return completed.stdout.strip()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    for runtime in RUNTIMES:
        parser.add_argument(f"--py{runtime.replace('.', '')}", required=True)
    parser.add_argument("--output-dir", default="dist-evaluator-handoff-ci")
    args = parser.parse_args()

    pythons = {
        runtime: str(Path(getattr(args, f"py{runtime.replace('.', '')}")).resolve())
        for runtime in RUNTIMES
    }
    py314 = pythons["3.14"]

    for runtime, executable in pythons.items():
        actual = output([
            executable,
            "-c",
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
        ])
        if actual != runtime:
            fail(f"runtime identity mismatch expected={runtime} actual={actual}")
    print("AX_EVALUATOR_HANDOFF_RUNTIME_MATRIX_IDENTITY_PASS runtimes=3.11,3.12,3.13,3.14")

    for path in (
        "artifacts/AX-PUB-EVAL-PACK-001.json",
        "artifacts/AX-PUB-CANDIDATE-IDENTITY-001.json",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.current.template.json",
        "artifacts/AX-PUB-API-001.json",
        "artifacts/AX-PUB-SUP-001.json",
        "artifacts/AX-PUB-SEC-001.json",
    ):
        run([py314, "-m", "json.tool", path])

    for path in (
        "tools/build_installable_evaluator_handoff.py",
        "tools/check_installable_evaluator_handoff.py",
        "tools/check_installable_external_evaluation_report.py",
        "tools/check_installable_external_evaluation_report_historical.py",
        "tools/run_installable_evaluator_handoff_ci.py",
    ):
        run([py314, "-m", "py_compile", path])

    run([py314, "tools/check_installable_evaluator_handoff.py"])
    run([
        py314,
        "tools/check_installable_external_evaluation_report.py",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.current.template.json",
        "--allow-template",
    ])
    run([
        py314,
        "tools/check_installable_external_evaluation_report_historical.py",
        "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.template.json",
        "--allow-template",
    ])

    env = os.environ.copy()
    env.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_CACHE_DIR": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SOURCE_DATE_EPOCH": "1787076737",
    })
    run([
        py314,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "build==1.5.0",
        "hatchling==1.31.0",
    ], env=env)
    run([
        py314,
        "-c",
        "import importlib.metadata as m; assert m.version('build')=='1.5.0'; assert m.version('hatchling')=='1.31.0'; print('AX_EVALUATOR_HANDOFF_BUILD_TOOLCHAIN_PASS')",
    ], env=env)

    root_output = ROOT / args.output_dir
    first = root_output / "first"
    second = root_output / "second"
    shutil.rmtree(root_output, ignore_errors=True)
    root_output.mkdir(parents=True, exist_ok=True)

    current_template = json.loads(
        (ROOT / "examples/external-evaluation/AX-PUB-EVAL-REPORT-002.current.template.json").read_text(encoding="utf-8")
    )
    current_template["candidate"]["wheel_filename"] = "tampered-0.1.0rc1-py3-none-any.whl"
    negative_report = root_output / "negative-wheel-filename.json"
    negative_report.write_text(json.dumps(current_template, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    expect_failure([
        py314,
        "tools/check_installable_external_evaluation_report.py",
        str(negative_report),
        "--allow-template",
    ], contains="wheel filename mismatch", env=env)

    run([py314, "tools/build_installable_evaluator_handoff.py", "--output-dir", str(first)], env=env)
    run([py314, "tools/build_installable_evaluator_handoff.py", "--output-dir", str(second)], env=env)

    first_zip = first / PACK_ZIP
    second_zip = second / PACK_ZIP
    first_manifest = first / "AX-PUB-EVAL-PACK-001.manifest.json"
    second_manifest = second / "AX-PUB-EVAL-PACK-001.manifest.json"
    if digest(first_zip) != digest(second_zip):
        fail("double-build handoff ZIP digest mismatch")
    if first_manifest.read_bytes() != second_manifest.read_bytes():
        fail("double-build handoff manifest mismatch")
    pack_sha = digest(first_zip)
    print(f"AX_EVALUATOR_HANDOFF_REPRODUCIBILITY_PASS sha256={pack_sha}")

    run([py314, "tools/check_installable_evaluator_handoff.py", "--bundle-dir", str(first)])

    rehearsal = root_output / "rehearsal"
    rehearsal.mkdir(parents=True, exist_ok=True)
    import zipfile
    with zipfile.ZipFile(first_zip) as archive:
        archive.extractall(rehearsal)
    wheel = rehearsal / "payload" / WHEEL
    packed_checker = rehearsal / "check_installable_external_evaluation_report.py"
    packed_template = rehearsal / "AX-PUB-EVAL-REPORT-002.template.json"
    packed_historical_checker = rehearsal / "check_installable_external_evaluation_report_historical.py"
    if not wheel.is_file():
        fail("rehearsal wheel missing")
    for path in (packed_checker, packed_template, packed_historical_checker, rehearsal / "CURRENT_CANDIDATE_IDENTITY.json"):
        if not path.is_file():
            fail(f"rehearsal evaluator component missing: {path.name}")

    expect_failure([
        py314,
        str(packed_checker),
        str(negative_report),
        "--allow-template",
    ], contains="wheel filename mismatch", env=env)

    for runtime, executable in pythons.items():
        venv = root_output / f"venv-{runtime}"
        run([executable, "-m", "venv", str(venv)], env=env)
        vpy = venv / "bin" / "python"
        if os.name == "nt":
            vpy = venv / "Scripts" / "python.exe"
        run([str(vpy), "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", str(wheel)], env=env)
        run([
            str(vpy),
            "-c",
            (
                "import aetherxglobal.governed_intelligence as sdk; "
                "assert sdk.__version__=='0.1.0rc1'; "
                "ids={x['contract_id'] for x in sdk.supported_contracts()}; "
                "assert ids=={'AX-PUB-SPEC-002','AX-PUB-SPEC-003','AX-PUB-SPEC-004'}; "
                "print('AX_EVALUATOR_LOCAL_REHEARSAL_IMPORT_PASS')"
            ),
        ], env=env)
        run([
            executable,
            str(packed_checker),
            str(packed_template),
            "--allow-template",
        ], env=env)
        print(f"AX_EVALUATOR_LOCAL_REHEARSAL_RUNTIME_PASS runtime={runtime}")

    # Publishable CI output directory contains only the deterministic handoff
    # and its machine-readable manifest, not rehearsal virtual environments.
    publish = root_output / "publish"
    publish.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(first_zip, publish / PACK_ZIP)
    shutil.copyfile(first_manifest, publish / "AX-PUB-EVAL-PACK-001.manifest.json")

    print(f"AX_EVALUATOR_HANDOFF_CI_PASS pack_sha256={pack_sha}")
    print("EVALUATOR HANDOFF PACK: CI VALIDATION ONLY")
    print("LOCAL REHEARSAL: NOT FINAL HUMAN EXTERNAL EVALUATION")
    print("FINAL REPORT REQUIRES AUTHORIZED EXTERNAL INDEX")
    print("TESTPYPI UPLOAD NOT AUTHORIZED")
    print("PYPI UPLOAD NOT AUTHORIZED")
    print("HUMAN EXTERNAL EVALUATION NOT ESTABLISHED BY CI")
    print("SDK PUBLICATION NOT AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
