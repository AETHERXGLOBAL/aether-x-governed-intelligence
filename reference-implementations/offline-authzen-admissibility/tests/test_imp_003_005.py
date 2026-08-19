import sys
from pathlib import Path
import unittest
from unittest.mock import patch
from uuid import UUID

PROOF_ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROOF_ROOT))
sys.path.insert(0, str(TEST_ROOT))

import admissibility
from test_admissibility import OBSERVED, PROPOSAL, bound_evidence, request, response, valid_kwargs
from test_p1_structural_eav import _load_existing_eav_validator


class AuthZENImplementationCorrections003To005(unittest.TestCase):
    def test_imp_003_malformed_optional_properties_fail_received(self):
        cases = []

        req = request()
        req["subject"]["properties"] = ["not", "an", "object"]
        cases.append(("subject.properties", req))

        req = request()
        req["resource"]["properties"] = "not-an-object"
        cases.append(("resource.properties", req))

        req = request()
        req["action"]["properties"] = 7
        cases.append(("action.properties", req))

        for label, malformed in cases:
            with self.subTest(label=label):
                result = admissibility.assess_access_evaluation(**valid_kwargs(req=malformed))
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
                self.assertNotIn(
                    result["states"]["DECISION_ADMISSIBLE"],
                    {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"},
                )
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_imp_004_freshness_mismatched_evaluation_time_fails_closed(self):
        def mismatched_freshness(ctx):
            return bound_evidence(
                ctx,
                verified_pdp_evaluation_time="2026-08-19T22:24:30+03:00",
            )

        kwargs = valid_kwargs()
        kwargs["freshness_verifier"] = mismatched_freshness
        result = admissibility.assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")
        self.assertEqual(result["verification_evidence"]["freshness"]["status"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
        self.assertNotEqual(result["execution_permission"], "GRANTED")

    def test_imp_004_freshness_missing_evaluation_time_binding_fails_closed(self):
        kwargs = valid_kwargs()
        kwargs["freshness_verifier"] = lambda ctx: bound_evidence(ctx)
        result = admissibility.assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")
        self.assertEqual(result["verification_evidence"]["freshness"]["status"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
        self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_imp_005_object_only_record_ids_are_independent_in_eav_bundle(self):
        first_uuid = UUID("00000000-0000-4000-8000-000000000001")
        second_uuid = UUID("00000000-0000-4000-8000-000000000002")

        with patch.object(admissibility, "uuid4", side_effect=[first_uuid, second_uuid]):
            first = admissibility.assess_access_evaluation(
                observed_at=OBSERVED,
                action_proposal=PROPOSAL,
                request_object=request(subject="principal-A"),
                response_object=response(decision=True),
            )
            second = admissibility.assess_access_evaluation(
                observed_at=OBSERVED,
                action_proposal=PROPOSAL,
                request_object=request(subject="principal-B"),
                response_object=response(decision=False),
            )

        first_record = first["evidence_record"]
        second_record = second["evidence_record"]
        self.assertNotEqual(first_record["evidence_id"], second_record["evidence_id"])
        self.assertEqual(first_record["request_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(first_record["response_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(second_record["request_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(second_record["response_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(first["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertEqual(second["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertNotIn(first["states"]["DECISION_ADMISSIBLE"], {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"})
        self.assertNotIn(second["states"]["DECISION_ADMISSIBLE"], {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"})

        bundle = {
            "schema_id": "AX-PUB-SCHEMA-001",
            "schema_version": "1.0",
            "bundle_id": "authzen-object-only-independent-evidence-ids",
            "evidence_records": [first_record, second_record],
            "decision_records": [],
            "authority_grants": [],
            "execution_records": [],
            "verification_records": [],
            "verified_outcomes": [],
        }
        validator = _load_existing_eav_validator()
        findings = validator.validate_bundle(bundle)
        duplicate_findings = [item for item in findings if getattr(item, "code", None) == "AX-REF-ID-DUPLICATE"]
        self.assertEqual(duplicate_findings, [])
        self.assertEqual(findings, [], msg=[getattr(item, "message", repr(item)) for item in findings])


if __name__ == "__main__":
    unittest.main()
