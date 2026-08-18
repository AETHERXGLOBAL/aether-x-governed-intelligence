#!/usr/bin/env python3
"""Minimal repository-local DEV-GATE-02 candidate example."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = Path(__file__).with_name("aetherx_sdk_candidate.py")

spec = importlib.util.spec_from_file_location("aetherx_sdk_candidate_example", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load SDK candidate module")
sdk = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdk
spec.loader.exec_module(sdk)

payload = json.loads(
    (ROOT / "reference-implementations/eav-contract-validator/examples/valid_bundle.json").read_text(encoding="utf-8")
)
result = sdk.validate_eav(payload)
print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
if result.valid:
    print("AX_SDK_CANDIDATE_EXAMPLE_PASS")
else:
    raise SystemExit(1)
