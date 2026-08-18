#!/usr/bin/env python3
"""Validate the exact Gate-05B wheel through a local Python Simple Index.

This is reversible DEV-GATE-05C engineering evidence. It deliberately performs
no TestPyPI/PyPI write and must never be interpreted as external registry
validation, registry ownership, licence grant, supported-SDK status or release
authority.
"""
from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "aetherxglobal-governed-intelligence"
VERSION = "0.1.0rc1"
IMPORT = "aetherxglobal.governed_intelligence"
WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
SDIST = "aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz"
WHEEL_SHA256 = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA256 = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
REPORT_FORMAT = "AX-PUB-DIST-REPORT-001"
REPORT_VERSION = "1.0"
VERIFIED_PYTHON = {"3.11", "3.12", "3.13", "3.14"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout:\n{completed.stdout[-4000:]}\n"
            f"stderr:\n{completed.stderr[-4000:]}"
        )
    return completed


def runtime_key() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def write_index(root: Path, wheel: Path) -> None:
    packages = root / "packages"
    simple = root / "simple" / PROJECT
    packages.mkdir(parents=True)
    simple.mkdir(parents=True)
    shutil.copy2(wheel, packages / WHEEL)
    (root / "simple" / "index.html").write_text(
        f'<!doctype html><html><body><a href="{PROJECT}/">{PROJECT}</a></body></html>\n',
        encoding="utf-8",
    )
    (simple / "index.html").write_text(
        '<!doctype html><html><body>'
        f'<a href="../../packages/{WHEEL}#sha256={WHEEL_SHA256}">{WHEEL}</a>'
        '</body></html>\n',
        encoding="utf-8",
    )


def make_handler(directory: Path) -> type[http.server.SimpleHTTPRequestHandler]:
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return QuietHandler


def validate(dist_dir: Path) -> dict[str, Any]:
    runtime = runtime_key()
    if runtime not in VERIFIED_PYTHON:
        raise RuntimeError(f"runtime {runtime} outside declared Gate-05C matrix")

    wheel = dist_dir / WHEEL
    sdist = dist_dir / SDIST
    if not wheel.is_file() or not sdist.is_file():
        raise RuntimeError("exact wheel/sdist candidate not found in dist directory")
    wheel_hash = sha256(wheel)
    sdist_hash = sha256(sdist)
    if wheel_hash != WHEEL_SHA256:
        raise RuntimeError(f"wheel SHA-256 mismatch: {wheel_hash}")
    if sdist_hash != SDIST_SHA256:
        raise RuntimeError(f"sdist SHA-256 mismatch: {sdist_hash}")

    with tempfile.TemporaryDirectory(prefix="ax-gate05c-") as raw:
        temp = Path(raw)
        index_root = temp / "index"
        venv = temp / "venv"
        outside = temp / "outside"
        outside.mkdir()
        write_index(index_root, wheel)

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), make_handler(index_root))
        port = int(server.server_address[1])
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        time.sleep(0.1)
        try:
            run([sys.executable, "-m", "venv", str(venv)])
            vpython = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            env = os.environ.copy()
            env.update({
                "PIP_DISABLE_PIP_VERSION_CHECK": "1",
                "PIP_NO_CACHE_DIR": "1",
                "PYTHONNOUSERSITE": "1",
            })
            index_url = f"http://127.0.0.1:{port}/simple/"
            install = run([
                str(vpython), "-m", "pip", "install",
                "--no-deps", "--no-cache-dir", "--index-url", index_url,
                f"{PROJECT}=={VERSION}",
            ], cwd=outside, env=env)
            verify_code = (
                "import importlib.metadata as m, json; "
                f"import {IMPORT} as sdk; "
                f"assert m.version('{PROJECT}') == '{VERSION}'; "
                "contracts=sdk.supported_contracts(); "
                "assert tuple(contracts)==('AX-PUB-SPEC-002','AX-PUB-SPEC-003','AX-PUB-SPEC-004'); "
                "assert getattr(sdk,'SDK_VERSION')=='0.1.0rc1'; "
                "print(json.dumps({'version':m.version('aetherxglobal-governed-intelligence'),'contracts':list(contracts),'sdk_version':sdk.SDK_VERSION}, sort_keys=True))"
            )
            verify = run([str(vpython), "-c", verify_code], cwd=outside, env=env)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    return {
        "report_format": REPORT_FORMAT,
        "report_version": REPORT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "validation_type": "LOCAL_SIMPLE_INDEX_SIMULATION",
        "external_registry_validation": False,
        "external_registry_write_performed": False,
        "sdk_publication_authorized": False,
        "project": PROJECT,
        "version": VERSION,
        "runtime": runtime,
        "wheel": {"filename": WHEEL, "sha256": wheel_hash},
        "sdist": {"filename": SDIST, "sha256": sdist_hash},
        "index_protocol": "PYTHON_SIMPLE_REPOSITORY_API_COMPATIBLE_TEST_SURFACE",
        "install_method": "PIP_INDEX_DISCOVERY / LOOPBACK_ONLY / NO_DEPS",
        "installed_verification": json.loads(verify.stdout.strip().splitlines()[-1]),
        "pip_output_tail": install.stdout[-2000:],
        "result": "PASS",
        "claim_boundaries": [
            "LOCAL INDEX PASS DOES NOT ESTABLISH TESTPYPI OR PYPI VALIDATION",
            "LOCAL INDEX PASS DOES NOT ESTABLISH REGISTRY OWNERSHIP",
            "LOCAL INDEX PASS DOES NOT GRANT A SOFTWARE LICENCE",
            "LOCAL INDEX PASS DOES NOT ESTABLISH A SUPPORTED SDK",
            "SDK PUBLICATION NOT AUTHORIZED",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist-dir", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.dist_dir.resolve())
    except Exception as exc:
        print(f"AX_SDK_LOCAL_INDEX_VALIDATION_FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "AX_SDK_LOCAL_INDEX_VALIDATION_PASS "
        f"python={report['runtime']} wheel={report['wheel']['sha256']} external_write=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
