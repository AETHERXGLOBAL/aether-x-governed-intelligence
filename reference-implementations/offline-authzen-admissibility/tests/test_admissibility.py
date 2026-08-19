import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from admissibility import assess_access_evaluation

OBSERVED = "2026-08-19T22:26:00+03:00"


def enc(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()


def request(*, subject="principal-A", resource="resource-A", action="write", tool="tool-A", params=None, extra_context=None):
    context = {
        "tool": tool,
        "parameters": {"limit": 1} if params is None else params,
    }
    if extra_context:
        context.update(extra_context)
    return {
        "subject": {"type": "principal", "id": subject},
        "resource": {"type": "resource", "id": resource},
        "action": {"name": action},
        "context": context,
    }


def response(*, decision=True, context=None, claims=None):
    obj = {"decision": decision}
    if context is not None:
        obj["context"] = context
    if claims:
        obj.update(claims)
    return obj


PROPOSAL = {
    "proposal_id": "proposal-001",
    "principal_id": "principal-A",
    "proposed_tool": "tool-A",
    "proposed_action": "write",
    "target_resource": "resource-A",
    "bounded_parameters": {"limit": 1},
}


def binding_verifier(ctx):
    req = ctx["request"]
    proposal = ctx["action_proposal"]
    dimensions = {
        "subject": "PASS" if req.get("subject", {}).get("id") == proposal["principal_id"] else "FAIL",
        "resource": "PASS" if req.get("resource", {}).get("id") == proposal["target_resource"] else "FAIL",
        "action": "PASS" if req.get("action", {}).get("name") == proposal["proposed_action"] else "FAIL",
        "tool": "PASS" if req.get("context", {}).get("tool") == proposal["proposed_tool"] else "UNKNOWN",
        "context": "PASS" if req.get("context", {}).get("parameters") == proposal["bounded_parameters"] else "FAIL",
    }
    allowed_context = {"tool", "parameters"}
    if set(req.get("context", {})) - allowed_context:
        dimensions["context"] = "UNKNOWN"
    if any(v == "FAIL" for v in dimensions.values()):
        status = "FAIL"
    elif any(v == "UNKNOWN" for v in dimensions.values()):
        status = "UNKNOWN"
    else:
        status = "PASS"
    return {
        "status": status,
        "profile_identity": "fixture-authzen-binding",
        "profile_version": "0.1",
        "request_identity": ctx["request_identity"],
        "proposal_id": proposal["proposal_id"],
        "dimensions": dimensions,
    }


def bound_evidence(ctx, *, status="PASS", **extra):
    result = {
        "status": status,
        "source_identity": "fixture-source",
        "verifier_identity": "fixture-verifier",
        "verification_method": "fixture-interface-v1",
        "request_identity": ctx["request_identity"],
        "response_identity": ctx["response_identity"],
        "proposal_id": ctx["proposal_id"],
        "purpose": ctx["purpose"],
        "policy_identity": "fixture-policy",
        "policy_version_or_digest": "sha256:" + "a" * 64,
        "checked_at": OBSERVED,
    }
    result.update(extra)
    return result


def integrity_pass(ctx):
    return bound_evidence(ctx)


def pdp_identity_pass(ctx):
    return bound_evidence(ctx, verified_value="pdp-A")


def trust_pass(ctx):
    return bound_evidence(ctx, trusted_pdp_identity=ctx["verified_pdp_identity"])


def policy_pass(ctx):
    return bound_evidence(
        ctx,
        verified_policy_identity="pdp-policy-A",
        verified_policy_version_or_digest="sha256:" + "b" * 64,
        verified_evaluation_time="2026-08-19T22:25:30+03:00",
    )


def freshness_pass(ctx):
    return bound_evidence(ctx)


def replay_pass(ctx):
    return bound_evidence(ctx)


def valid_kwargs(*, decision=True, req=None, resp=None):
    return {
        "observed_at": OBSERVED,
        "action_proposal": PROPOSAL,
        "request_bytes": enc(request() if req is None else req),
        "response_bytes": enc(response(decision=decision) if resp is None else resp),
        "request_binding_verifier": binding_verifier,
        "response_integrity_verifier": integrity_pass,
        "pdp_identity_verifier": pdp_identity_pass,
        "trust_verifier": trust_pass,
        "policy_provenance_verifier": policy_pass,
        "freshness_verifier": freshness_pass,
        "replay_verifier": replay_pass,
    }


class AuthZENNegativeSemanticCases(unittest.TestCase):
    def test_neg_az_001_malformed_input(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_bytes=b"{",
            response_bytes=enc(response()),
        )
        self.assertEqual(result["states"]["RECEIVED"], "FAIL")
        self.assertEqual(result["states"]["REQUEST_BOUND"], "NOT_REACHED")
        self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_neg_az_002_raw_allow_source_data(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_bytes=enc(request()),
            response_bytes=enc(response(decision=True)),
        )
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertTrue(result["raw_decision"])
        self.assertNotEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_ALLOW")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_neg_az_003_raw_deny_unverified(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_bytes=enc(request()),
            response_bytes=enc(response(decision=False)),
        )
        self.assertFalse(result["raw_decision"])
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertNotEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_DENY")

    def test_neg_az_004_subject_mismatch(self):
        result = assess_access_evaluation(**valid_kwargs(req=request(subject="principal-B")))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "FAIL")
        self.assertNotEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_ALLOW")

    def test_neg_az_005_resource_mismatch(self):
        result = assess_access_evaluation(**valid_kwargs(req=request(resource="resource-B")))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "FAIL")

    def test_neg_az_006_action_mismatch(self):
        result = assess_access_evaluation(**valid_kwargs(req=request(action="delete")))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "FAIL")

    def test_neg_az_007_tool_binding_missing(self):
        req = request()
        del req["context"]["tool"]
        result = assess_access_evaluation(**valid_kwargs(req=req))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")

    def test_neg_az_008_context_parameter_mismatch(self):
        result = assess_access_evaluation(**valid_kwargs(req=request(params={"limit": 2})))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "FAIL")

    def test_neg_az_009_integrity_unknown(self):
        kwargs = valid_kwargs()
        kwargs["response_integrity_verifier"] = lambda ctx: bound_evidence(ctx, status="UNKNOWN")
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["RESPONSE_INTEGRITY_VERIFIED"], "UNKNOWN")
        self.assertEqual(result["states"]["PDP_TRUSTED"], "NOT_EVALUATED")

    def test_neg_az_010_pdp_identity_missing(self):
        kwargs = valid_kwargs()
        kwargs["pdp_identity_verifier"] = lambda ctx: bound_evidence(ctx)
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["PDP_TRUSTED"], "UNKNOWN")

    def test_neg_az_011_trust_policy_version_missing(self):
        def incomplete_trust(ctx):
            ev = bound_evidence(ctx, trusted_pdp_identity=ctx["verified_pdp_identity"])
            ev.pop("policy_version_or_digest")
            return ev
        kwargs = valid_kwargs()
        kwargs["trust_verifier"] = incomplete_trust
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["PDP_TRUSTED"], "UNKNOWN")

    def test_neg_az_012_pdp_policy_provenance_missing(self):
        kwargs = valid_kwargs()
        kwargs["policy_provenance_verifier"] = lambda ctx: bound_evidence(ctx)
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_013_evaluation_time_missing(self):
        def no_eval_time(ctx):
            return bound_evidence(
                ctx,
                verified_policy_identity="pdp-policy-A",
                verified_policy_version_or_digest="sha256:" + "b" * 64,
            )
        kwargs = valid_kwargs()
        kwargs["policy_provenance_verifier"] = no_eval_time
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_014_observed_at_substitution(self):
        resp = response(claims={"evaluation_time": OBSERVED})
        def caller_time_only(_ctx):
            return {
                "status": "PASS",
                "verified_policy_identity": "pdp-policy-A",
                "verified_policy_version_or_digest": "sha256:" + "b" * 64,
                "verified_evaluation_time": OBSERVED,
            }
        kwargs = valid_kwargs(resp=resp)
        kwargs["policy_provenance_verifier"] = caller_time_only
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_015_replay_different_proposal(self):
        kwargs = valid_kwargs()
        kwargs["replay_verifier"] = lambda ctx: bound_evidence(ctx, status="FAIL")
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "FAIL")

    def test_neg_az_016_replay_evidence_missing(self):
        kwargs = valid_kwargs()
        kwargs["replay_verifier"] = None
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_017_stale_allow(self):
        kwargs = valid_kwargs()
        kwargs["freshness_verifier"] = lambda ctx: bound_evidence(ctx, status="FAIL")
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "FAIL")

    def test_neg_az_018_unprofiled_response_context(self):
        kwargs = valid_kwargs(resp=response(context={"obligation": "approve"}))
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")
        self.assertEqual(result["aether_authority"], "NOT_CREATED")

    def test_neg_az_019_unknown_enforcement_context(self):
        result = assess_access_evaluation(**valid_kwargs(req=request(extra_context={"mystery": True})))
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")

    def test_neg_az_020_admissible_deny_no_flip(self):
        result = assess_access_evaluation(**valid_kwargs(decision=False))
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_DENY")
        self.assertEqual(result["adapter_disposition"], "NO_PROCEED")
        self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_neg_az_021_admissible_allow_not_authority(self):
        result = assess_access_evaluation(**valid_kwargs(decision=True))
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_ALLOW")
        self.assertEqual(result["aether_decision"], "NOT_CREATED")
        self.assertEqual(result["aether_authority"], "NOT_CREATED")
        self.assertEqual(result["authority_context"], "NOT_CREATED")
        self.assertEqual(result["tool_use_grant"], "NOT_CREATED")
        self.assertEqual(result["capability"], "NOT_GRANTED")
        self.assertEqual(result["execution_permission"], "NOT_GRANTED")
        self.assertEqual(result["aether_verification"], "NOT_EVALUATED")
        self.assertEqual(result["verified_outcome"], "NOT_ESTABLISHED")

    def test_neg_az_022_trust_without_integrity(self):
        kwargs = valid_kwargs()
        kwargs["response_integrity_verifier"] = lambda ctx: bound_evidence(ctx, status="UNKNOWN")
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["RESPONSE_INTEGRITY_VERIFIED"], "UNKNOWN")
        self.assertEqual(result["states"]["PDP_TRUSTED"], "NOT_EVALUATED")
        self.assertNotEqual(result["states"]["DECISION_ADMISSIBLE"], "ADMISSIBLE_ALLOW")

    def test_neg_az_023_pdp_identity_asserted_only(self):
        resp = response(claims={"pdp_identity": "pdp-A"})
        kwargs = valid_kwargs(resp=resp)
        kwargs["pdp_identity_verifier"] = lambda _ctx: {"status": "PASS", "verified_value": "pdp-A"}
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["evidence_record"]["pdp_identity_claim"], "pdp-A")
        self.assertEqual(result["states"]["PDP_TRUSTED"], "UNKNOWN")

    def test_neg_az_024_pdp_policy_asserted_only(self):
        resp = response(claims={"policy": {"id": "policy-A", "version": "1"}})
        kwargs = valid_kwargs(resp=resp)
        kwargs["policy_provenance_verifier"] = lambda _ctx: {
            "status": "PASS",
            "verified_policy_identity": "policy-A",
            "verified_policy_version_or_digest": "1",
            "verified_evaluation_time": "2026-08-19T22:25:30+03:00",
        }
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_025_evaluation_time_caller_supplied(self):
        resp = response(claims={"evaluation_time": "2026-08-19T22:25:30+03:00"})
        kwargs = valid_kwargs(resp=resp)
        kwargs["policy_provenance_verifier"] = lambda _ctx: {
            "status": "PASS",
            "verified_policy_identity": "policy-A",
            "verified_policy_version_or_digest": "1",
            "verified_evaluation_time": resp["evaluation_time"],
        }
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_026_bare_freshness_pass(self):
        resp = response(claims={"freshness_pass": True})
        kwargs = valid_kwargs(resp=resp)
        kwargs["freshness_verifier"] = lambda _ctx: {"status": "PASS"}
        result = assess_access_evaluation(**kwargs)
        self.assertTrue(result["evidence_record"]["freshness_claim"])
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_027_bare_replay_pass(self):
        resp = response(claims={"replay_pass": True})
        kwargs = valid_kwargs(resp=resp)
        kwargs["replay_verifier"] = lambda _ctx: {"status": "PASS"}
        result = assess_access_evaluation(**kwargs)
        self.assertTrue(result["evidence_record"]["replay_claim"])
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_028_provenance_bound_to_different_decision(self):
        def wrong_bound_policy(ctx):
            ev = policy_pass(ctx)
            ev["proposal_id"] = "proposal-other"
            return ev
        kwargs = valid_kwargs()
        kwargs["policy_provenance_verifier"] = wrong_bound_policy
        result = assess_access_evaluation(**kwargs)
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "UNKNOWN")

    def test_neg_az_029_object_only_immutable_identity_unavailable(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_object=request(),
            response_object=response(),
            request_binding_verifier=binding_verifier,
            response_integrity_verifier=integrity_pass,
            pdp_identity_verifier=pdp_identity_pass,
            trust_verifier=trust_pass,
            policy_provenance_verifier=policy_pass,
            freshness_verifier=freshness_pass,
            replay_verifier=replay_pass,
        )
        self.assertEqual(result["states"]["RECEIVED"], "PASS")
        self.assertEqual(result["evidence_record"]["request_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(result["evidence_record"]["response_identity"]["status"], "UNAVAILABLE")
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")
        self.assertNotIn(result["states"]["DECISION_ADMISSIBLE"], {"ADMISSIBLE_ALLOW", "ADMISSIBLE_DENY"})

    def test_neg_az_030_reserialization_hash_substitution(self):
        req = request()
        resp = response()
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_object=req,
            response_object=resp,
            request_binding_verifier=binding_verifier,
        )
        fake_req_hash = "received-authzen-request-bytes:sha256:" + __import__("hashlib").sha256(enc(req)).hexdigest()
        self.assertEqual(result["evidence_record"]["request_identity"]["status"], "UNAVAILABLE")
        self.assertNotEqual(result["evidence_record"]["request_identity"].get("uri"), fake_req_hash)
        self.assertEqual(result["states"]["REQUEST_BOUND"], "UNKNOWN")

    def test_neg_az_031_boxcarring_unsupported(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_object={"evaluations": [request()]},
            response_object={"evaluations": [response()]},
            api_surface="access_evaluations",
        )
        self.assertEqual(result["evidence_record"]["surface_status"], "UNSUPPORTED")
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "NOT_EVALUATED")
        self.assertEqual(result["execution_permission"], "NOT_GRANTED")

    def test_neg_az_032_search_api_unsupported(self):
        result = assess_access_evaluation(
            observed_at=OBSERVED,
            action_proposal=PROPOSAL,
            request_object={"search": "resource"},
            response_object={"results": []},
            api_surface="search",
        )
        self.assertEqual(result["evidence_record"]["surface_status"], "UNSUPPORTED")
        self.assertEqual(result["states"]["DECISION_ADMISSIBLE"], "NOT_EVALUATED")
        self.assertEqual(result["aether_authority"], "NOT_CREATED")


if __name__ == "__main__":
    unittest.main()