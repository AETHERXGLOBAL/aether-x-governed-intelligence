import copy
import importlib.util
import sys
from pathlib import Path
import unittest

PROOF_ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROOF_ROOT))
sys.path.insert(0, str(TEST_ROOT))

from admissibility import assess_access_evaluation
from test_admissibility import OBSERVED, PROPOSAL, request, response, valid_kwargs


def _load_existing_eav_validator():
    path = REPO_ROOT / "reference-implementations" / "eav-contract-validator" / "validator.py"
    spec = importlib.util.spec_from_file_location("existing_eav_contract_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load existing EAV validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AuthZENStructuralAndEAVCorrections(unittest.TestCase):
    def test_p1_001_missing_or_wrong_type_required_fields_fail_received(self):
        cases = []

        req = request()
        del req["subject"]["type"]
        cases.append(("subject.type missing", req))

        req = request()
        req["subject"]["id"] = 7
        cases.append(("subject.id wrong type", req))

        req = request()
        req["resource"]["type"] = ["resource"]
        cases.append(("resource.type wrong type", req))

        req = request()
        del req["resource"]["id"]
        cases.append(("resource.id missing", req))

        req = request()
        del req["action"]["name"]
        cases.append(("action.name missing", req))

        req = request()
        req["action"]["name"] = {"value": "write"}
        cases.append(("action.name wrong type", req))

        for label, invalid_request in cases:
            with self.subTest(label=label):
                result = assess_access_evaluation(**valid_kwargs(req=invalid_request))
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
                self.assertNotIn(
                    result["states"]["DECISION_ADMISSIBLE"],
                    {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"},
                )
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_p1_001_structurally_invalid_deny_cannot_become_admissible_deny(self):
        invalid_request = request()
        invalid_request["subject"]["type"] = None
        result = assess_access_evaluation(**valid_kwargs(decision=False, req=invalid_request))
        self.assertEqual(result["states"]["RECEIVED"], "FAIL")
        self.assertNotEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_DENY")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_p1_001_optional_context_omitted_is_received_pass_but_binding_unknown(self):
        context_omitted = request()
        del context_omitted["context"]
        kwargs = valid_kwargs(req=context_omitted)
        kwargs["request_binding_verifier"] = lambda _ctx: {
            "status": "UNKNOWN",
            "reason": "optional AuthZEN context absent; tool/parameters/context cannot be established",
        }
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["RECEIVED"], "PASS")
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertNotIn(
            result["states"]["DECISION_ADMISSIBLE"],
            {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"},
        )
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_p1_002_emitted_evidence_record_passes_existing_eav_validator(self):
        asserted_pdp = "asserted-pdp-must-not-be-source-identity"
        kwargs = valid_kwargs(resp=response(claims={"pdp_identity": asserted_pdp}))
        result = assess_access_evaluation(**kwargs)
        record = copy.deepcopy(result["evidence_record"])

        self.assertEqual(result["target"], "evidence_record")
        self.assertEqual(record["classification"], "SOURCE_DATA")
        for field in ("evidence_id", "classification", "source_identity", "observed_at"):
            self.assertIn(field, record)
            self.assertNotIn(record[field], (None, ""))
        self.assertNotEqual(record["source_identity"], asserted_pdp)
        self.assertEqual(record["pdp_identity_claim"], asserted_pdp)
        self.assertEqual(record["request_identity"]["status"], "AVAILABLE")
        self.assertEqual(record["response_identity"]["status"], "AVAILABLE")

        bundle = {
            "schema_id": "AX-PUB-SCHEMA-001",
            "schema_version": "1.0",
            "bundle_id": "authzen-eav-cross-contract-regression",
            "evidence_records": [record],
            "decision_records": [],
            "authority_grants": [],
            "execution_records": [],
            "verification_records": [],
            "verified_outcomes": [],
        }
        validator = _load_existing_eav_validator()
        findings = validator.validate_bundle(bundle)
        self.assertEqual(findings, [], msg=[getattr(item, "message", repr(item)) for item in findings])


if __name__ == "__main__":
    unittest.main()
