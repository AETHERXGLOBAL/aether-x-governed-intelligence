#!/usr/bin/env python3
"""Run bounded DEV-GATE-02 SDK-candidate conformance cases."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = Path(__file__).with_name("aetherx_sdk_candidate.py")

spec = importlib.util.spec_from_file_location("aetherx_sdk_candidate_conformance", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load SDK candidate module")
sdk = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdk
spec.loader.exec_module(sdk)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    results: list[tuple[str, bool]] = []

    valid_cases = (
        ("EAV_VALID", sdk.validate_eav, "reference-implementations/eav-contract-validator/examples/valid_bundle.json"),
        ("PTK_VALID", sdk.validate_point_in_time, "reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json"),
        ("AGENT_VALID", sdk.validate_agent_authority, "reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json"),
    )
    for case_id, validator, path in valid_cases:
        result = validator(load_json(path))
        results.append((case_id, result.valid and not result.findings))

    invalid_cases = (
        ("EAV_INVALID", sdk.validate_eav, "reference-implementations/eav-contract-validator/examples/invalid_bundle.json"),
        ("PTK_INVALID", sdk.validate_point_in_time, "reference-implementations/point-in-time-knowledge-validator/examples/invalid_envelope.json"),
        ("AGENT_INVALID", sdk.validate_agent_authority, "reference-implementations/agent-tool-authority-validator/examples/invalid_envelope.json"),
    )
    allowed = {item.value for item in sdk.ErrorCategory}
    for case_id, validator, path in invalid_cases:
        result = validator(load_json(path))
        ok = (
            not result.valid
            and len(result.findings) >= 1
            and all(item.category.value in allowed for item in result.findings)
            and all(item.source_code.startswith("AX-") for item in result.findings)
        )
        results.append((case_id, ok))

    version_result = sdk.validate_eav(
        load_json("reference-implementations/eav-contract-validator/examples/valid_bundle.json"),
        version="2.0",
    )
    results.append(
        (
            "UNSUPPORTED_VERSION",
            not version_result.valid
            and version_result.findings[0].category == sdk.ErrorCategory.VERSION_UNSUPPORTED,
        )
    )

    contract_result = sdk.validate("AX-PUB-SPEC-999", {}, version="1.0")
    results.append(
        (
            "UNSUPPORTED_CONTRACT",
            not contract_result.valid
            and contract_result.findings[0].category == sdk.ErrorCategory.UNSUPPORTED_OPERATION,
        )
    )

    payload = load_json("reference-implementations/point-in-time-knowledge-validator/examples/invalid_envelope.json")
    first = sdk.validate_point_in_time(payload).as_dict()
    second = sdk.validate_point_in_time(payload).as_dict()
    results.append(("DETERMINISTIC_RESULT", first == second))

    failed = [case_id for case_id, ok in results if not ok]
    for case_id, ok in results:
        print(f"{'PASS' if ok else 'FAIL'} {case_id}")

    if failed:
        print(f"AX_SDK_CANDIDATE_CONFORMANCE_FAIL cases={len(results)} conforming={len(results)-len(failed)}")
        return 1

    print(f"AX_SDK_CANDIDATE_CONFORMANCE_PASS cases={len(results)} conforming={len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
