import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ax_pub_ref_003", BASE / "validator.py")
module = importlib.util.module_from_spec(spec)
sys.modules["ax_pub_ref_003"] = module
assert spec.loader is not None
spec.loader.exec_module(module)

with (BASE / "examples" / "valid_envelope.json").open("r", encoding="utf-8") as handle:
    VALID = json.load(handle)

def codes(payload):
    return {f.code for f in module.validate_envelope(payload)}

class AgentAuthorityValidatorTests(unittest.TestCase):
    def test_valid_envelope(self):
        self.assertEqual(module.validate_envelope(copy.deepcopy(VALID)), [])
    def test_revoked_authority_blocks_invocation(self):
        payload = copy.deepcopy(VALID); payload["authority_contexts"][0]["revocation_state"] = "REVOKED"
        self.assertIn("AX-AGT-INVOKE-AUTHORITY-INACTIVE", codes(payload))
    def test_principal_mismatch(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["principal_id"] = "agent:other"
        self.assertIn("AX-AGT-INVOKE-PRINCIPAL", codes(payload))
    def test_tool_mismatch(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["tool_id"] = "tool:other"
        self.assertIn("AX-AGT-INVOKE-TOOL", codes(payload))
    def test_action_mismatch(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["action"] = "DELETE_RECORD"
        self.assertIn("AX-AGT-INVOKE-ACTION", codes(payload))
    def test_resource_outside_scope(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["target_resource"] = "sandbox:item-2"
        self.assertIn("AX-AGT-INVOKE-RESOURCE", codes(payload))
    def test_after_expiry(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["invoked_at"] = "2026-08-18T00:16:00Z"
        self.assertIn("AX-AGT-INVOKE-AFTER-GRANT", codes(payload))
    def test_parameter_outside_allowed_values(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["effective_parameters"]["value"] = "rejected"
        self.assertIn("AX-AGT-PARAM-ALLOWED-VALUES", codes(payload))
    def test_environment_outside_context(self):
        payload = copy.deepcopy(VALID); payload["tool_invocations"][0]["environment"] = "PRODUCTION"
        self.assertIn("AX-AGT-INVOKE-ENVIRONMENT", codes(payload))
    def test_grant_cannot_broaden_context_parameters(self):
        payload = copy.deepcopy(VALID); payload["tool_use_grants"][0]["parameter_constraints"]["value"]["allowed_values"].append("rejected")
        self.assertIn("AX-AGT-GRANT-PARAM-SCOPE", codes(payload))

if __name__ == "__main__":
    unittest.main()
