import unittest

from admissibility import assess_access_evaluation
from test_admissibility import (
    OBSERVED,
    PROPOSAL,
    binding_verifier,
    bound_evidence,
    enc,
    policy_pass,
    request,
    response,
    valid_kwargs,
)


class AuthZENImplementationCorrections008To010(unittest.TestCase):
    def test_imp_008_same_subject_id_with_unprofiled_type_fails_closed(self):
        req = request()
        req["subject"]["type"] = "service-account"
        result = assess_access_evaluation(**valid_kwargs(req=req))
        self.assertEqual(result["states"]["RECEIVED"], "PASS")
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
        self.assertNotIn(result["states"]["DECISION_ADMISSIBLE"], {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"})

    def test_imp_008_same_resource_id_with_unprofiled_type_fails_closed(self):
        req = request()
        req["resource"]["type"] = "document"
        result = assess_access_evaluation(**valid_kwargs(req=req))
        self.assertEqual(result["states"]["RECEIVED"], "PASS")
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
        self.assertNotIn(result["states"]["DECISION_ADMISSIBLE"], {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"})

    def test_imp_008_id_only_binding_claim_cannot_pass_without_type_scope_evidence(self):
        def id_only_binding(ctx):
            evidence = binding_verifier(ctx)
            evidence.pop("subject_identity_binding")
            evidence.pop("resource_identity_binding")
            return evidence

        kwargs = valid_kwargs()
        kwargs["request_binding_verifier"] = id_only_binding
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_imp_009_duplicate_json_members_fail_received(self):
        cases = (
            (
                "nested-request-id",
                b'{"subject":{"type":"principal","id":"principal-A","id":"principal-A"},"resource":{"type":"resource","id":"resource-A"},"action":{"name":"write"},"context":{"tool":"tool-A","parameters":{"limit":1}}}',
                enc(response()),
            ),
            (
                "duplicate-decision",
                enc(request()),
                b'{"decision":false,"decision":true}',
            ),
        )
        for label, request_bytes, response_bytes in cases:
            with self.subTest(label=label):
                result = assess_access_evaluation(
                    observed_at=OBSERVED,
                    action_proposal=PROPOSAL,
                    request_bytes=request_bytes,
                    response_bytes=response_bytes,
                )
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_imp_009_non_finite_json_numbers_fail_received(self):
        request_templates = (
            b'{"subject":{"type":"principal","id":"principal-A"},"resource":{"type":"resource","id":"resource-A"},"action":{"name":"write"},"context":{"tool":"tool-A","parameters":{"limit":NaN}}}',
            b'{"subject":{"type":"principal","id":"principal-A"},"resource":{"type":"resource","id":"resource-A"},"action":{"name":"write"},"context":{"tool":"tool-A","parameters":{"limit":Infinity}}}',
            b'{"subject":{"type":"principal","id":"principal-A"},"resource":{"type":"resource","id":"resource-A"},"action":{"name":"write"},"context":{"tool":"tool-A","parameters":{"limit":-Infinity}}}',
        )
        for request_bytes in request_templates:
            with self.subTest(request_bytes=request_bytes):
                result = assess_access_evaluation(
                    observed_at=OBSERVED,
                    action_proposal=PROPOSAL,
                    request_bytes=request_bytes,
                    response_bytes=enc(response()),
                )
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")

    def test_imp_010_checked_at_must_be_timezone_aware_timestamp(self):
        invalid_times = ("not-a-time", "2026-08-19T22:26:00", 12345)
        for invalid_time in invalid_times:
            with self.subTest(invalid_time=invalid_time):
                kwargs = valid_kwargs()
                kwargs["response_integrity_verifier"] = lambda ctx, value=invalid_time: bound_evidence(ctx, checked_at=value)
                result = assess_access_evaluation(**kwargs)
                self.assertEqual(result["states"]["RESPONSE_INTEGRITY_VERIFIED"], "UNKNOWN")
                self.assertEqual(result["states"]["PDP_TRUSTED"], "NOT_EVALUATED")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_imp_010_verified_evaluation_time_must_be_timezone_aware_timestamp(self):
        invalid_times = ("not-a-time", "2026-08-19T22:25:30", 12345)
        for invalid_time in invalid_times:
            with self.subTest(invalid_time=invalid_time):
                def invalid_policy(ctx, value=invalid_time):
                    evidence = policy_pass(ctx)
                    evidence["verified_evaluation_time"] = value
                    return evidence

                kwargs = valid_kwargs()
                kwargs["policy_provenance_verifier"] = invalid_policy
                result = assess_access_evaluation(**kwargs)
                self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_imp_010_freshness_time_binding_remains_validated_and_exact(self):
        kwargs = valid_kwargs()
        kwargs["freshness_verifier"] = lambda ctx: bound_evidence(
            ctx,
            verified_pdp_evaluation_time="2026-08-19T22:25:30",
        )
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["verification_evidence"]["freshness"]["status"], "UNKNOWN")
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")


if __name__ == "__main__":
    unittest.main()
