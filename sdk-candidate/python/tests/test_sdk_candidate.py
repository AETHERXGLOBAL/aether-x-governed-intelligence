#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "sdk-candidate" / "python" / "aetherx_sdk_candidate.py"

spec = importlib.util.spec_from_file_location("aetherx_sdk_candidate_test_module", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load SDK candidate module")
sdk = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdk
spec.loader.exec_module(sdk)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class SDKCandidateTests(unittest.TestCase):
    def test_declared_contract_inventory(self) -> None:
        inventory = sdk.supported_contracts()
        self.assertEqual(len(inventory), 3)
        self.assertEqual(
            {item["contract_id"] for item in inventory},
            {"AX-PUB-SPEC-002", "AX-PUB-SPEC-003", "AX-PUB-SPEC-004"},
        )
        self.assertTrue(all(item["contract_version"] == "1.0" for item in inventory))

    def test_valid_eav(self) -> None:
        payload = load_json("reference-implementations/eav-contract-validator/examples/valid_bundle.json")
        result = sdk.validate_eav(payload)
        self.assertTrue(result.valid, result.as_dict())
        self.assertEqual(result.reference_validator_id, "AX-PUB-REF-001")
        self.assertEqual(result.findings, ())

    def test_structurally_incomplete_eav_fails_closed(self) -> None:
        payload = load_json("reference-implementations/eav-contract-validator/examples/valid_bundle.json")
        cases = (
            {},
            {key: value for key, value in payload.items() if key != "schema_id"},
            {**payload, "evidence_records": {}},
        )
        for case in cases:
            with self.subTest(case=case):
                result = sdk.validate_eav(case)
                self.assertFalse(result.valid)
                self.assertGreaterEqual(len(result.findings), 1)
                self.assertTrue(all(f.category is sdk.ErrorCategory.CONTRACT_INVALID for f in result.findings))

    def test_valid_point_in_time(self) -> None:
        payload = load_json("reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json")
        result = sdk.validate_point_in_time(payload)
        self.assertTrue(result.valid, result.as_dict())
        self.assertEqual(result.reference_validator_id, "AX-PUB-REF-002")

    def test_valid_agent_authority(self) -> None:
        payload = load_json("reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json")
        result = sdk.validate_agent_authority(payload)
        self.assertTrue(result.valid, result.as_dict())
        self.assertEqual(result.reference_validator_id, "AX-PUB-REF-003")

    def test_invalid_fixtures_fail_with_mapped_categories(self) -> None:
        cases = (
            (
                sdk.validate_eav,
                "reference-implementations/eav-contract-validator/examples/invalid_bundle.json",
            ),
            (
                sdk.validate_point_in_time,
                "reference-implementations/point-in-time-knowledge-validator/examples/invalid_envelope.json",
            ),
            (
                sdk.validate_agent_authority,
                "reference-implementations/agent-tool-authority-validator/examples/invalid_envelope.json",
            ),
        )
        allowed = {item.value for item in sdk.ErrorCategory}
        for validator, path in cases:
            with self.subTest(path=path):
                result = validator(load_json(path))
                self.assertFalse(result.valid)
                self.assertGreaterEqual(len(result.findings), 1)
                for finding in result.findings:
                    self.assertIn(finding.category.value, allowed)
                    self.assertTrue(finding.source_code.startswith("AX-"))
                    self.assertTrue(finding.path)
                    self.assertTrue(finding.message)

    def test_unsupported_version_fails_explicitly(self) -> None:
        payload = load_json("reference-implementations/eav-contract-validator/examples/valid_bundle.json")
        result = sdk.validate_eav(payload, version="2.0")
        self.assertFalse(result.valid)
        self.assertEqual(result.findings[0].category, sdk.ErrorCategory.VERSION_UNSUPPORTED)
        self.assertEqual(result.findings[0].source_code, "AX-SDK-CANDIDATE-VERSION-UNSUPPORTED")

    def test_unsupported_contract_fails_explicitly(self) -> None:
        result = sdk.validate("AX-PUB-SPEC-999", {}, version="1.0")
        self.assertFalse(result.valid)
        self.assertEqual(result.findings[0].category, sdk.ErrorCategory.UNSUPPORTED_OPERATION)
        self.assertEqual(result.findings[0].source_code, "AX-SDK-CANDIDATE-CONTRACT-UNSUPPORTED")

    def test_result_is_deterministic_for_same_payload(self) -> None:
        payload = load_json("reference-implementations/point-in-time-knowledge-validator/examples/invalid_envelope.json")
        first = sdk.validate_point_in_time(payload).as_dict()
        second = sdk.validate_point_in_time(payload).as_dict()
        self.assertEqual(first, second)

    def test_candidate_has_no_execution_api(self) -> None:
        forbidden = {"execute", "authorize", "trade", "invoke_tool", "send", "publish"}
        self.assertTrue(forbidden.isdisjoint(set(sdk.__all__)))


if __name__ == "__main__":
    unittest.main()
