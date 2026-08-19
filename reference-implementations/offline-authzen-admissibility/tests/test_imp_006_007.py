import unittest

from test_admissibility import request, response, valid_kwargs
from admissibility import assess_access_evaluation


class AuthZENImplementationCorrections006To007(unittest.TestCase):
    def test_imp_006_non_empty_properties_without_profile_handling_fail_closed(self):
        cases = []

        req = request()
        req["subject"]["properties"] = {"tenant": "tenant-A"}
        cases.append(("subject.properties", req))

        req = request()
        req["resource"]["properties"] = {"classification": "restricted"}
        cases.append(("resource.properties", req))

        req = request()
        req["action"]["properties"] = {"mode": "bounded"}
        cases.append(("action.properties", req))

        for label, property_request in cases:
            with self.subTest(label=label):
                result = assess_access_evaluation(**valid_kwargs(req=property_request))
                self.assertEqual(result["states"]["RECEIVED"], "PASS")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
                self.assertNotIn(
                    result["states"]["DECISION_ADMISSIBLE"],
                    {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"},
                )
                binding = result["verification_evidence"]["request_binding"]
                self.assertEqual(binding["status"], "UNKNOWN")
                self.assertIn(label, binding["unprofiled_properties"])
                self.assertEqual(result["aether_decision"], "NOT_CREATED")
                self.assertEqual(result["aether_authority"], "NOT_CREATED")
                self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_imp_007_explicit_null_response_context_fails_received_allow_and_deny(self):
        for decision in (True, False):
            with self.subTest(decision=decision):
                resp = response(decision=decision)
                resp["context"] = None
                result = assess_access_evaluation(**valid_kwargs(decision=decision, resp=resp))
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
                self.assertEqual(result["states"]["RESPONSE_INTEGRITY_VERIFIED"], "NOT_REACHED")
                self.assertEqual(result["states"]["PDP_TRUSTED"], "NOT_REACHED")
                self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "NOT_REACHED")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
                self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_imp_007_non_object_response_context_fails_received_allow_and_deny(self):
        for decision, invalid_context in ((True, "not-an-object"), (False, ["not", "an", "object"])):
            with self.subTest(decision=decision, invalid_context=invalid_context):
                resp = response(decision=decision, context=invalid_context)
                result = assess_access_evaluation(**valid_kwargs(decision=decision, resp=resp))
                self.assertEqual(result["states"]["RECEIVED"], "FAIL")
                self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
                self.assertEqual(result["states"]["RESPONSE_INTEGRITY_VERIFIED"], "NOT_REACHED")
                self.assertEqual(result["states"]["PDP_TRUSTED"], "NOT_REACHED")
                self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "NOT_REACHED")
                self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
                self.assertEqual(result["aether_decision"], "NOT_CREATED")
                self.assertEqual(result["aether_authority"], "NOT_CREATED")


if __name__ == "__main__":
    unittest.main()
