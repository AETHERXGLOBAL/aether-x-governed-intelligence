import copy
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import validator  # noqa: E402


def valid_bundle():
    return {
        "evidence_records": [
            {
                "evidence_id": "ev-1",
                "classification": "SOURCE_DATA",
                "source_identity": "example-source",
                "observed_at": "2026-08-17T20:00:00Z",
            }
        ],
        "decision_records": [
            {
                "decision_id": "dec-1",
                "decision_question": "Proceed?",
                "decision_owner": "human:owner",
                "evidence_refs": ["ev-1"],
                "decided_at": "2026-08-17T20:01:00Z",
            }
        ],
        "authority_grants": [
            {
                "authority_id": "auth-1",
                "decision_id": "dec-1",
                "principal": "agent:1",
                "permitted_action": "WRITE_EXAMPLE",
                "resource_scope": ["sandbox:item"],
                "status": "ACTIVE",
                "granted_at": "2026-08-17T20:02:00Z",
                "expires_at": "2026-08-17T21:02:00Z",
            }
        ],
        "execution_records": [
            {
                "execution_id": "exec-1",
                "decision_id": "dec-1",
                "authority_id": "auth-1",
                "actor": "agent:1",
                "action": "WRITE_EXAMPLE",
                "resource": "sandbox:item",
                "started_at": "2026-08-17T20:03:00Z",
                "status": "COMPLETED",
            }
        ],
        "verification_records": [
            {
                "verification_id": "ver-1",
                "execution_id": "exec-1",
                "verifier": "checker:1",
                "verdict": "PASS",
                "verified_at": "2026-08-17T20:04:00Z",
                "requires_independent_verifier": True,
            }
        ],
        "verified_outcomes": [
            {
                "outcome_id": "out-1",
                "verification_id": "ver-1",
                "outcome_state": "VERIFIED",
                "accepted_at": "2026-08-17T20:05:00Z",
            }
        ],
    }


class EAVValidatorTests(unittest.TestCase):
    def codes(self, bundle):
        return {finding.code for finding in validator.validate_bundle(bundle)}

    def test_valid_bundle_passes(self):
        self.assertEqual(validator.validate_bundle(valid_bundle()), [])

    def test_revoked_authority_blocks_execution(self):
        bundle = valid_bundle()
        bundle["authority_grants"][0]["status"] = "REVOKED"
        self.assertIn("AX-EAV-EXEC-AUTHORITY-INACTIVE", self.codes(bundle))

    def test_wrong_principal_is_rejected(self):
        bundle = valid_bundle()
        bundle["execution_records"][0]["actor"] = "agent:other"
        self.assertIn("AX-EAV-EXEC-PRINCIPAL", self.codes(bundle))

    def test_wrong_action_is_rejected(self):
        bundle = valid_bundle()
        bundle["execution_records"][0]["action"] = "DELETE_EXAMPLE"
        self.assertIn("AX-EAV-EXEC-ACTION", self.codes(bundle))

    def test_out_of_scope_resource_is_rejected(self):
        bundle = valid_bundle()
        bundle["execution_records"][0]["resource"] = "sandbox:other"
        self.assertIn("AX-EAV-EXEC-SCOPE", self.codes(bundle))

    def test_expired_authority_is_rejected_at_execution_time(self):
        bundle = valid_bundle()
        bundle["authority_grants"][0]["expires_at"] = "2026-08-17T20:02:30Z"
        self.assertIn("AX-EAV-EXEC-AFTER-EXPIRY", self.codes(bundle))

    def test_independent_verifier_cannot_equal_actor(self):
        bundle = valid_bundle()
        bundle["verification_records"][0]["verifier"] = "agent:1"
        self.assertIn("AX-EAV-VERIFY-INDEPENDENCE", self.codes(bundle))

    def test_failed_verification_cannot_create_verified_outcome(self):
        bundle = valid_bundle()
        bundle["verification_records"][0]["verdict"] = "FAIL"
        self.assertIn("AX-EAV-OUTCOME-NOT-PASSED", self.codes(bundle))

    def test_unknown_evidence_reference_is_rejected(self):
        bundle = valid_bundle()
        bundle["decision_records"][0]["evidence_refs"] = ["ev-missing"]
        self.assertIn("AX-EAV-EVIDENCE-REF", self.codes(bundle))

    def test_invalid_timestamp_is_rejected(self):
        bundle = valid_bundle()
        bundle["evidence_records"][0]["observed_at"] = "not-a-time"
        self.assertIn("AX-REF-TIME-FORMAT", self.codes(bundle))


if __name__ == "__main__":
    unittest.main()
