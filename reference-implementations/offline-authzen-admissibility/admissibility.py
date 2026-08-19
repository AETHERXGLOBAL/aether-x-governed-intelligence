from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from typing import Any, Callable, Mapping
from uuid import uuid4

STAGES = (
    "RECEIVED",
    "REQUEST_BOUND",
    "RESPONSE_INTEGRITY_VERIFIED",
    "PDP_TRUSTED",
    "DECISION_ADMISSIBLE",
)

SUPPORTED_SURFACE = "single_access_evaluation"
UNSUPPORTED_SURFACES = {"access_evaluations", "search"}
EAV_SOURCE_IDENTITY = "offline-authzen-caller-supplied-input"

EvidenceVerifier = Callable[[Mapping[str, Any]], Mapping[str, Any]]
BindingVerifier = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _iso_timestamp(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("observed_at must be a non-empty ISO-8601 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return value


def _identity(label: str, raw: bytes | None) -> dict[str, Any]:
    if raw is None:
        return {"status": "UNAVAILABLE", "kind": label}
    digest = _sha256(raw)
    return {
        "status": "AVAILABLE",
        "kind": label,
        "sha256": digest,
        "uri": f"{label}:sha256:{digest}",
    }


def _load_input(raw: bytes | None, obj: Mapping[str, Any] | None, label: str) -> tuple[dict[str, Any] | None, dict[str, Any], str | None]:
    if raw is not None and obj is not None:
        return None, _identity(label, raw), "provide bytes or parsed object, not both"
    if raw is not None:
        if not isinstance(raw, (bytes, bytearray)):
            return None, _identity(label, None), f"{label} bytes must be bytes"
        raw = bytes(raw)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, _identity(label, raw), f"malformed {label} JSON"
        if not isinstance(parsed, dict):
            return None, _identity(label, raw), f"{label} must decode to an object"
        return parsed, _identity(label, raw), None
    if obj is not None:
        if not isinstance(obj, Mapping):
            return None, _identity(label, None), f"{label} parsed input must be an object"
        return deepcopy(dict(obj)), _identity(label, None), None
    return None, _identity(label, None), f"missing {label}"


def _base_result(observed_at: str, surface: str) -> dict[str, Any]:
    observed = _iso_timestamp(observed_at)
    return {
        "target": "evidence_record",
        "evidence_record": {
            "evidence_id": f"authzen-admissibility:{uuid4()}",
            "classification": "SOURCE_DATA",
            "source_identity": EAV_SOURCE_IDENTITY,
            "semantic_role": "EXTERNAL_AUTHORIZATION_DECISION_SOURCE_DATA",
            "observed_at": observed,
            "api_surface": surface,
            "promotion": "NONE",
        },
        "states": {stage: "NOT_EVALUATED" for stage in STAGES},
        "verification_evidence": {},
        "raw_decision": None,
        "adapter_disposition": "NO_PROCEED",
        "aether_decision": "NOT_CREATED",
        "aether_authority": "NOT_CREATED",
        "authority_context": "NOT_CREATED",
        "tool_use_grant": "NOT_CREATED",
        "capability": "NOT_GRANTED",
        "execution_permission": "NOT_GRANTED",
        "aether_verification": "NOT_EVALUATED",
        "verified_outcome": "NOT_ESTABLISHED",
    }


def _bind_evidence_identity(
    evidence_record: dict[str, Any],
    request_identity: Mapping[str, Any],
    response_identity: Mapping[str, Any],
) -> None:
    """Derive evidence_id from immutable input identities when available.

    This does not change source_identity and does not treat a PDP identity claim
    as the source. Request/response identities remain separately preserved.
    Object-only imports retain an independent record identifier and do not
    synthesize a canonical-object or content identity.
    """
    req_uri = _identity_uri(request_identity)
    resp_uri = _identity_uri(response_identity)
    if req_uri and resp_uri:
        digest = _sha256(f"{req_uri}|{resp_uri}".encode("utf-8"))
        evidence_record["evidence_id"] = f"authzen-admissibility:{digest}"


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _validate_optional_properties(container: Mapping[str, Any], label: str) -> str | None:
    if "properties" in container and not isinstance(container.get("properties"), Mapping):
        return f"request {label}.properties, when present, must be an object"
    return None


def _validate_single_access_evaluation_request(request: Mapping[str, Any]) -> str | None:
    """Validate the bounded AuthZEN 1.0 single Access Evaluation request shape."""
    subject = request.get("subject")
    if not isinstance(subject, Mapping):
        return "request subject must be an object"
    if not _non_empty_string(subject.get("type")):
        return "request subject.type must be a non-empty string"
    if not _non_empty_string(subject.get("id")):
        return "request subject.id must be a non-empty string"
    properties_error = _validate_optional_properties(subject, "subject")
    if properties_error:
        return properties_error

    resource = request.get("resource")
    if not isinstance(resource, Mapping):
        return "request resource must be an object"
    if not _non_empty_string(resource.get("type")):
        return "request resource.type must be a non-empty string"
    if not _non_empty_string(resource.get("id")):
        return "request resource.id must be a non-empty string"
    properties_error = _validate_optional_properties(resource, "resource")
    if properties_error:
        return properties_error

    action = request.get("action")
    if not isinstance(action, Mapping):
        return "request action must be an object"
    if not _non_empty_string(action.get("name")):
        return "request action.name must be a non-empty string"
    properties_error = _validate_optional_properties(action, "action")
    if properties_error:
        return properties_error

    if "context" in request and not isinstance(request.get("context"), Mapping):
        return "request context, when present, must be an object"
    return None


def _unprofiled_non_empty_properties(request: Mapping[str, Any]) -> tuple[str, ...]:
    """Return structurally valid properties that v0.1 does not profile for binding."""
    unprofiled: list[str] = []
    for label in ("subject", "resource", "action"):
        container = request.get(label)
        if not isinstance(container, Mapping):
            continue
        properties = container.get("properties")
        if isinstance(properties, Mapping) and properties:
            unprofiled.append(f"{label}.properties")
    return tuple(unprofiled)


def _later_not_reached(result: dict[str, Any], after: str) -> None:
    seen = False
    for stage in STAGES:
        if stage == after:
            seen = True
            continue
        if seen:
            result["states"][stage] = "NOT_REACHED"


def _identity_uri(identity: Mapping[str, Any]) -> str | None:
    if identity.get("status") != "AVAILABLE":
        return None
    return identity.get("uri")


def _common_evidence_complete(
    evidence: Mapping[str, Any],
    *,
    request_identity: str,
    response_identity: str,
    proposal_id: str,
    purpose: str,
    require_policy: bool = True,
    require_checked_at: bool = True,
) -> bool:
    if evidence.get("status") not in {"PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED"}:
        return False
    required = (
        "source_identity",
        "verifier_identity",
        "verification_method",
        "request_identity",
        "response_identity",
        "proposal_id",
        "purpose",
    )
    if any(not evidence.get(key) for key in required):
        return False
    if evidence.get("request_identity") != request_identity:
        return False
    if evidence.get("response_identity") != response_identity:
        return False
    if evidence.get("proposal_id") != proposal_id:
        return False
    if evidence.get("purpose") != purpose:
        return False
    if require_policy:
        if not evidence.get("policy_identity"):
            return False
        if not evidence.get("policy_version_or_digest"):
            return False
    if require_checked_at and not evidence.get("checked_at"):
        return False
    return True


def _normalized_verification(
    verifier: EvidenceVerifier | None,
    context: Mapping[str, Any],
    *,
    request_identity: str,
    response_identity: str,
    proposal_id: str,
    purpose: str,
    require_policy: bool = True,
    require_checked_at: bool = True,
) -> dict[str, Any]:
    if verifier is None:
        return {"status": "NOT_EVALUATED", "reason": "interface not supplied"}
    try:
        raw = verifier(context)
    except Exception as exc:  # proof boundary: interface failure is fail-closed
        return {"status": "UNKNOWN", "reason": f"interface error: {type(exc).__name__}"}
    if not isinstance(raw, Mapping):
        return {"status": "UNKNOWN", "reason": "interface result must be an object"}
    evidence = deepcopy(dict(raw))
    if evidence.get("status") not in {"PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED"}:
        return {"status": "UNKNOWN", "reason": "invalid interface status", "source": evidence}
    if evidence.get("status") == "PASS" and not _common_evidence_complete(
        evidence,
        request_identity=request_identity,
        response_identity=response_identity,
        proposal_id=proposal_id,
        purpose=purpose,
        require_policy=require_policy,
        require_checked_at=require_checked_at,
    ):
        evidence["status"] = "UNKNOWN"
        evidence["reason"] = "PASS forbidden: provenance incomplete, unbound, or unattributable"
    return evidence


def _normalize_binding(
    verifier: BindingVerifier | None,
    context: Mapping[str, Any],
    *,
    request_identity: str,
    proposal_id: str,
) -> dict[str, Any]:
    if verifier is None:
        return {"status": "UNKNOWN", "reason": "binding interface not supplied"}
    try:
        raw = verifier(context)
    except Exception as exc:
        return {"status": "UNKNOWN", "reason": f"binding interface error: {type(exc).__name__}"}
    if not isinstance(raw, Mapping):
        return {"status": "UNKNOWN", "reason": "binding result must be an object"}
    result = deepcopy(dict(raw))
    if result.get("status") not in {"PASS", "FAIL", "UNKNOWN"}:
        return {"status": "UNKNOWN", "reason": "invalid binding status"}
    if result.get("status") == "PASS":
        dimensions = result.get("dimensions")
        complete = (
            result.get("profile_identity")
            and result.get("profile_version")
            and result.get("request_identity") == request_identity
            and result.get("proposal_id") == proposal_id
            and isinstance(dimensions, Mapping)
            and all(dimensions.get(name) == "PASS" for name in ("subject", "resource", "action", "tool", "context"))
        )
        if not complete:
            result["status"] = "UNKNOWN"
            result["reason"] = "PASS forbidden: incomplete or unbound request-binding evidence"
    return result


def assess_access_evaluation(
    *,
    observed_at: str,
    action_proposal: Mapping[str, Any],
    request_bytes: bytes | None = None,
    response_bytes: bytes | None = None,
    request_object: Mapping[str, Any] | None = None,
    response_object: Mapping[str, Any] | None = None,
    api_surface: str = SUPPORTED_SURFACE,
    request_binding_verifier: BindingVerifier | None = None,
    response_integrity_verifier: EvidenceVerifier | None = None,
    pdp_identity_verifier: EvidenceVerifier | None = None,
    trust_verifier: EvidenceVerifier | None = None,
    policy_provenance_verifier: EvidenceVerifier | None = None,
    freshness_verifier: EvidenceVerifier | None = None,
    replay_verifier: EvidenceVerifier | None = None,
) -> dict[str, Any]:
    """Evaluate one offline AuthZEN single Access Evaluation as SOURCE_DATA.

    All integrity, identity, trust, policy-provenance, freshness, and replay
    determinations are supplied through interfaces. This proof creates no
    AETHER Decision, Authority, capability, grant, or execution permission.
    """
    result = _base_result(observed_at, api_surface)
    evidence_record = result["evidence_record"]

    request, request_identity, request_error = _load_input(request_bytes, request_object, "received-authzen-request-bytes")
    response, response_identity, response_error = _load_input(response_bytes, response_object, "received-authzen-response-bytes")
    evidence_record["request_identity"] = request_identity
    evidence_record["response_identity"] = response_identity
    _bind_evidence_identity(evidence_record, request_identity, response_identity)

    if api_surface in UNSUPPORTED_SURFACES:
        evidence_record["surface_status"] = "UNSUPPORTED"
        evidence_record["request_source_data"] = request
        evidence_record["response_source_data"] = response
        result["states"]["DECISION_ADMISSIBLE"] = "NOT_EVALUATED"
        return result
    if api_surface != SUPPORTED_SURFACE:
        evidence_record["surface_status"] = "UNKNOWN"
        return result

    if request_error or response_error:
        result["states"]["RECEIVED"] = "FAIL"
        result["receive_error"] = request_error or response_error
        _later_not_reached(result, "RECEIVED")
        return result

    if not isinstance(request, dict) or not isinstance(response, dict):
        result["states"]["RECEIVED"] = "FAIL"
        _later_not_reached(result, "RECEIVED")
        return result

    structural_error = _validate_single_access_evaluation_request(request)
    if structural_error:
        result["states"]["RECEIVED"] = "FAIL"
        result["receive_error"] = structural_error
        _later_not_reached(result, "RECEIVED")
        return result

    if not isinstance(response.get("decision"), bool):
        result["states"]["RECEIVED"] = "FAIL"
        result["receive_error"] = "single Access Evaluation response decision must be boolean"
        _later_not_reached(result, "RECEIVED")
        return result

    if "context" in response and not isinstance(response.get("context"), Mapping):
        result["states"]["RECEIVED"] = "FAIL"
        result["receive_error"] = "single Access Evaluation response context, when present, must be an object"
        _later_not_reached(result, "RECEIVED")
        return result

    result["states"]["RECEIVED"] = "PASS"
    result["raw_decision"] = response["decision"]
    evidence_record["request_source_data"] = request
    evidence_record["response_source_data"] = response
    evidence_record["pdp_identity_claim"] = response.get("pdp_identity")
    evidence_record["pdp_policy_claim"] = response.get("policy")
    evidence_record["pdp_evaluation_time_claim"] = response.get("evaluation_time")
    evidence_record["freshness_claim"] = response.get("freshness_pass")
    evidence_record["replay_claim"] = response.get("replay_pass")

    req_uri = _identity_uri(request_identity)
    resp_uri = _identity_uri(response_identity)
    proposal_id = action_proposal.get("proposal_id") if isinstance(action_proposal, Mapping) else None
    if not proposal_id:
        result["states"]["REQUEST_BOUND"] = "UNKNOWN"
        return result

    if req_uri is None:
        result["states"]["REQUEST_BOUND"] = "UNKNOWN"
        result["verification_evidence"]["request_binding"] = {
            "status": "UNKNOWN",
            "reason": "original immutable request identity unavailable",
        }
        return result

    unprofiled_properties = _unprofiled_non_empty_properties(request)
    if unprofiled_properties:
        result["states"]["REQUEST_BOUND"] = "UNKNOWN"
        result["verification_evidence"]["request_binding"] = {
            "status": "UNKNOWN",
            "reason": "v0.1 does not profile enforcement semantics for non-empty AuthZEN properties",
            "unprofiled_properties": list(unprofiled_properties),
        }
        return result

    binding = _normalize_binding(
        request_binding_verifier,
        {
            "request": request,
            "request_identity": req_uri,
            "action_proposal": deepcopy(dict(action_proposal)),
        },
        request_identity=req_uri,
        proposal_id=proposal_id,
    )
    result["verification_evidence"]["request_binding"] = binding
    result["states"]["REQUEST_BOUND"] = binding["status"]
    if binding["status"] != "PASS":
        return result

    if resp_uri is None:
        result["states"]["RESPONSE_INTEGRITY_VERIFIED"] = "UNKNOWN"
        result["verification_evidence"]["response_integrity"] = {
            "status": "UNKNOWN",
            "reason": "original immutable response identity unavailable",
        }
        return result

    common = {
        "request": request,
        "response": response,
        "request_identity": req_uri,
        "response_identity": resp_uri,
        "proposal_id": proposal_id,
        "purpose": "authzen-single-access-evaluation-admissibility",
        "observed_at": observed_at,
    }

    integrity = _normalized_verification(
        response_integrity_verifier,
        common,
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    result["verification_evidence"]["response_integrity"] = integrity
    result["states"]["RESPONSE_INTEGRITY_VERIFIED"] = integrity["status"]
    if integrity["status"] != "PASS":
        return result

    pdp_identity = _normalized_verification(
        pdp_identity_verifier,
        {**common, "response_integrity": integrity},
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    if pdp_identity.get("status") == "PASS" and not pdp_identity.get("verified_value"):
        pdp_identity["status"] = "UNKNOWN"
        pdp_identity["reason"] = "PASS forbidden without verified PDP identity value"
    result["verification_evidence"]["pdp_identity"] = pdp_identity
    if pdp_identity["status"] != "PASS":
        result["states"]["PDP_TRUSTED"] = "UNKNOWN" if pdp_identity["status"] in {"UNKNOWN", "NOT_EVALUATED"} else "FAIL"
        return result

    trust = _normalized_verification(
        trust_verifier,
        {**common, "verified_pdp_identity": pdp_identity["verified_value"], "pdp_identity_evidence": pdp_identity},
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    if trust.get("status") == "PASS" and trust.get("trusted_pdp_identity") != pdp_identity["verified_value"]:
        trust["status"] = "UNKNOWN"
        trust["reason"] = "PASS forbidden: trusted identity does not match verified PDP identity"
    result["verification_evidence"]["pdp_trust"] = trust
    result["states"]["PDP_TRUSTED"] = trust["status"]
    if trust["status"] != "PASS":
        return result

    policy = _normalized_verification(
        policy_provenance_verifier,
        {**common, "verified_pdp_identity": pdp_identity["verified_value"], "pdp_trust": trust},
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    if policy.get("status") == "PASS":
        if not policy.get("verified_policy_identity") or not policy.get("verified_policy_version_or_digest"):
            policy["status"] = "UNKNOWN"
            policy["reason"] = "PASS forbidden without verified PDP policy identity/version-or-digest"
        if not policy.get("verified_evaluation_time"):
            policy["status"] = "UNKNOWN"
            policy["reason"] = "PASS forbidden without verified PDP evaluation time"
    result["verification_evidence"]["policy_provenance"] = policy
    if policy["status"] != "PASS":
        result["states"]["DECISION_ADMISSIBLE"] = "FAIL" if policy["status"] == "FAIL" else "UNKNOWN"
        return result

    response_context = response.get("context", {})
    if not isinstance(response_context, Mapping):
        result["states"]["DECISION_ADMISSIBLE"] = "UNKNOWN"
        result["verification_evidence"]["response_context"] = {
            "status": "UNKNOWN",
            "reason": "response context is not an object",
        }
        return result
    if response_context:
        result["states"]["DECISION_ADMISSIBLE"] = "UNKNOWN"
        result["verification_evidence"]["response_context"] = {
            "status": "UNKNOWN",
            "reason": "v0.1 profiles no response-context fields; enforcement relevance unknown",
        }
        return result

    freshness = _normalized_verification(
        freshness_verifier,
        {**common, "verified_evaluation_time": policy["verified_evaluation_time"], "policy_provenance": policy},
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    if freshness.get("status") == "PASS" and freshness.get("verified_pdp_evaluation_time") != policy["verified_evaluation_time"]:
        freshness["status"] = "UNKNOWN"
        freshness["reason"] = "PASS forbidden: freshness evidence missing or mismatched verified PDP evaluation-time binding"
    result["verification_evidence"]["freshness"] = freshness
    if freshness["status"] != "PASS":
        result["states"]["DECISION_ADMISSIBLE"] = "FAIL" if freshness["status"] == "FAIL" else "UNKNOWN"
        return result

    replay = _normalized_verification(
        replay_verifier,
        {**common, "verified_evaluation_time": policy["verified_evaluation_time"], "policy_provenance": policy},
        request_identity=req_uri,
        response_identity=resp_uri,
        proposal_id=proposal_id,
        purpose=common["purpose"],
    )
    result["verification_evidence"]["replay"] = replay
    if replay["status"] != "PASS":
        result["states"]["DECISION_ADMISSIBLE"] = "FAIL" if replay["status"] == "FAIL" else "UNKNOWN"
        return result

    if response["decision"] is False:
        result["states"]["DECISION_ADMISSIBLE"] = "ADMISSIBLE_DENY"
        result["adapter_disposition"] = "NO_PROCEED"
    else:
        result["states"]["DECISION_ADMISSIBLE"] = "ADMISSIBLE_ALLOW"
        result["adapter_disposition"] = "MAY_INFORM_SEPARATE_AETHER_DECISION_PROCESS"

    return result
