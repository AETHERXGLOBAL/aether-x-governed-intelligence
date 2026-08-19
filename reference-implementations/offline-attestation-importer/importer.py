from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime
from typing import Any, Callable, Mapping, Sequence

IN_TOTO_STATEMENT_V1 = "https://in-toto.io/Statement/v1"
SLSA_PROVENANCE_V1 = "https://slsa.dev/provenance/v1"
SLSA_VSA_V1 = "https://slsa.dev/verification_summary/v1"

SUPPORTED_PREDICATES = {
    SLSA_PROVENANCE_V1: "BUILD_PROVENANCE_EXTERNAL_CLAIM",
    SLSA_VSA_V1: "EXTERNAL_VERIFIER_ASSESSMENT",
}

TERMINAL_STAGES = (
    "PARSED",
    "SUBJECT_BOUND",
    "SIGNATURE_VERIFIED",
    "TRUSTED_ISSUER",
    "PREDICATE_POLICY_VALIDATED",
)

Verifier = Callable[[Mapping[str, Any]], Mapping[str, Any]]
SignaturePolicy = Callable[[Sequence[Mapping[str, Any]]], str]
TrustPolicy = Callable[[Mapping[str, Any]], Mapping[str, Any]]
PredicatePolicy = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _iso_timestamp(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("observed_at must be a non-empty ISO-8601 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return value


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _not_reached(states: dict[str, str], after: str) -> None:
    seen = False
    for stage in TERMINAL_STAGES:
        if stage == after:
            seen = True
            continue
        if seen:
            states[stage] = "NOT_REACHED"


def _base_result(raw_bytes: bytes, observed_at: str) -> dict[str, Any]:
    digest = _sha256(raw_bytes)
    return {
        "target": "evidence_record",
        "evidence_record": {
            "evidence_id": f"attestation:sha256:{digest}",
            "classification": "SOURCE_DATA",
            "source_identity": f"received-attestation-bytes:sha256:{digest}",
            "observed_at": _iso_timestamp(observed_at),
            "semantic_status": "UNVERIFIED_EXTERNAL_CLAIM",
            "raw_attestation_identity": {"sha256": digest},
        },
        "states": {
            "PARSED": "NOT_EVALUATED",
            "SUBJECT_BOUND": "NOT_EVALUATED",
            "SIGNATURE_VERIFIED": "NOT_EVALUATED",
            "TRUSTED_ISSUER": "NOT_EVALUATED",
            "PREDICATE_POLICY_VALIDATED": "NOT_EVALUATED",
        },
        "per_signature_results": [],
        "aether_verification": "NOT_EVALUATED",
        "verified_outcome": "NOT_ESTABLISHED",
        "promotion": "NONE",
    }


def _parse(raw_bytes: bytes) -> tuple[dict[str, Any], bytes, list[dict[str, Any]], str, str | None]:
    try:
        outer = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("malformed JSON attestation") from exc
    if not isinstance(outer, dict):
        raise ValueError("attestation must be a JSON object")

    signatures: list[dict[str, Any]] = []
    envelope_form = "bare_statement"
    payload_type: str | None = None
    signed_payload = raw_bytes

    if {"payloadType", "payload", "signatures"}.issubset(outer):
        envelope_form = "dsse_envelope"
        if not isinstance(outer["payloadType"], str) or not outer["payloadType"]:
            raise ValueError("envelope payloadType must be a non-empty string")
        payload_type = outer["payloadType"]
        if not isinstance(outer["signatures"], list):
            raise ValueError("envelope signatures must be an array")
        signatures = [dict(s) for s in outer["signatures"] if isinstance(s, dict)]
        try:
            signed_payload = base64.b64decode(outer["payload"], validate=True)
            statement = json.loads(signed_payload.decode("utf-8"))
        except (TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid encoded statement payload") from exc
    else:
        statement = outer

    if not isinstance(statement, dict):
        raise ValueError("statement must be a JSON object")
    if statement.get("_type") != IN_TOTO_STATEMENT_V1:
        raise ValueError("unsupported or missing in-toto Statement v1 _type")
    if not isinstance(statement.get("subject"), list):
        raise ValueError("statement subject must be an array")
    if not isinstance(statement.get("predicateType"), str) or not statement["predicateType"]:
        raise ValueError("statement predicateType must be a non-empty string")
    if "predicate" not in statement or not isinstance(statement["predicate"], dict):
        raise ValueError("statement predicate must be an object")
    for subject in statement["subject"]:
        if not isinstance(subject, dict):
            raise ValueError("each subject must be an object")
        if "digest" not in subject or not isinstance(subject["digest"], dict):
            raise ValueError("each subject must preserve a digest object")

    return statement, signed_payload, signatures, envelope_form, payload_type


def _bind_subjects(
    subjects: Sequence[Mapping[str, Any]],
    expected_subjects: Sequence[Mapping[str, Any]] | None,
) -> tuple[str, list[int]]:
    if expected_subjects is None:
        return "UNKNOWN", []
    matched: list[int] = []
    for expected in expected_subjects:
        expected_digest = expected.get("digest")
        if not isinstance(expected_digest, Mapping) or not expected_digest:
            return "UNKNOWN", matched
        supported_pairs = [(alg, val) for alg, val in expected_digest.items() if alg == "sha256" and isinstance(val, str)]
        if not supported_pairs:
            return "UNKNOWN", matched
        found = False
        for idx, subject in enumerate(subjects):
            digest = subject.get("digest", {})
            if any(digest.get(alg) == val for alg, val in supported_pairs):
                if "name" in expected and expected.get("name") != subject.get("name"):
                    continue
                matched.append(idx)
                found = True
                break
        if not found:
            return "FAIL", matched
    return "PASS", matched


def _verify_signatures(
    signed_payload: bytes,
    payload_type: str | None,
    envelope_form: str,
    signatures: Sequence[Mapping[str, Any]],
    verifier: Verifier | None,
    signature_policy: SignaturePolicy | None,
) -> tuple[list[dict[str, Any]], str]:
    if not signatures:
        return [], "NOT_EVALUATED"

    per_signature: list[dict[str, Any]] = []
    for index, signature in enumerate(signatures):
        identity = {
            "index": index,
            "keyid_claim": signature.get("keyid"),
            "signature_value_sha256": _sha256(str(signature.get("sig", "")).encode("utf-8")),
        }
        if verifier is None:
            identity.update({"result": "NOT_EVALUATED", "signer_identity": None, "reason": "no verifier supplied"})
        else:
            verdict = dict(
                verifier(
                    {
                        "signed_payload": signed_payload,
                        "payload_type": payload_type,
                        "envelope_form": envelope_form,
                        "signature": dict(signature),
                    }
                )
            )
            result = verdict.get("result", "UNKNOWN")
            if result not in {"PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED"}:
                raise ValueError("signature verifier returned invalid result")
            identity.update(
                {
                    "result": result,
                    "signer_identity": verdict.get("signer_identity"),
                    "verification_material_identity": verdict.get("verification_material_identity"),
                    "reason": verdict.get("reason"),
                }
            )
        per_signature.append(identity)

    if signature_policy is None:
        return per_signature, "UNKNOWN"

    aggregate = signature_policy(per_signature)
    if aggregate not in {"PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED"}:
        raise ValueError("signature policy returned invalid result")
    return per_signature, aggregate


def import_attestation(
    raw_bytes: bytes,
    *,
    observed_at: str,
    expected_subjects: Sequence[Mapping[str, Any]] | None = None,
    signature_verifier: Verifier | None = None,
    signature_policy: SignaturePolicy | None = None,
    trust_policy: TrustPolicy | None = None,
    predicate_policy: PredicatePolicy | None = None,
) -> dict[str, Any]:
    """Import supplied local bytes into one SOURCE_DATA evidence_record.

    This reference implementation never creates Decision, Authority, Execution,
    AETHER Verification, Acceptance, or Verified Outcome records.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise TypeError("raw_bytes must be bytes")
    raw_bytes = bytes(raw_bytes)
    result = _base_result(raw_bytes, observed_at)
    states = result["states"]

    try:
        statement, signed_payload, signatures, envelope_form, payload_type = _parse(raw_bytes)
    except ValueError as exc:
        states["PARSED"] = "FAIL"
        _not_reached(states, "PARSED")
        result["parse_error"] = str(exc)
        return result

    states["PARSED"] = "PASS"
    evidence = result["evidence_record"]
    evidence.update(
        {
            "envelope_form": envelope_form,
            "signed_payload_identity": {"sha256": _sha256(signed_payload)},
            "payload_type": payload_type,
            "predicate_type": statement["predicateType"],
            "subjects": statement["subject"],
            "attestation_asserted_timestamps": _extract_asserted_timestamps(statement),
        }
    )

    subject_status, matched_indices = _bind_subjects(statement["subject"], expected_subjects)
    states["SUBJECT_BOUND"] = subject_status
    evidence["subject_binding"] = {
        "matched_subject_indices": matched_indices,
        "complete_subject_set_preserved": True,
    }

    per_signature, aggregate_signature = _verify_signatures(
        signed_payload, payload_type, envelope_form, signatures, signature_verifier, signature_policy
    )
    result["per_signature_results"] = per_signature
    states["SIGNATURE_VERIFIED"] = aggregate_signature

    signer_claims = [item.get("signer_identity") for item in per_signature if item.get("signer_identity")]
    evidence["signer_identity_claims"] = signer_claims
    evidence["signer_identity_status"] = "UNTRUSTED_CLAIM" if signer_claims else "ABSENT_OR_UNVERIFIED"

    trust_context = {
        "observed_at": observed_at,
        "predicate_type": statement["predicateType"],
        "signer_identities": signer_claims,
        "signature_verified": aggregate_signature,
        "verifier_id": _vsa_verifier_id(statement),
    }
    trust_result: dict[str, Any] = {
        "status": "NOT_EVALUATED",
        "pair_accepted": False,
        "policy_identity": None,
        "policy_digest": None,
    }
    if aggregate_signature == "PASS":
        if trust_policy is None:
            trust_result["status"] = "UNKNOWN"
        else:
            trust_result.update(dict(trust_policy(trust_context)))
            if trust_result.get("status") not in {"PASS", "FAIL", "UNKNOWN", "NOT_EVALUATED"}:
                raise ValueError("trust policy returned invalid status")
            if trust_result.get("status") == "PASS":
                if not trust_result.get("policy_identity") or not trust_result.get("policy_digest"):
                    trust_result["status"] = "UNKNOWN"
                    trust_result["reason"] = "PASS forbidden without immutable trust-policy identity"
    states["TRUSTED_ISSUER"] = trust_result["status"]
    evidence["trust_evaluation"] = trust_result

    predicate_type = statement["predicateType"]
    evidence["semantic_role"] = SUPPORTED_PREDICATES.get(predicate_type, "UNSUPPORTED_EXTERNAL_PREDICATE")
    if predicate_type not in SUPPORTED_PREDICATES:
        states["PREDICATE_POLICY_VALIDATED"] = "UNSUPPORTED"
        return result

    if subject_status != "PASS":
        states["PREDICATE_POLICY_VALIDATED"] = "NOT_EVALUATED"
        return result

    if predicate_type == SLSA_VSA_V1:
        if aggregate_signature != "PASS":
            states["PREDICATE_POLICY_VALIDATED"] = "NOT_EVALUATED"
            return result
        if trust_result["status"] != "PASS":
            states["PREDICATE_POLICY_VALIDATED"] = "NOT_EVALUATED"
            return result
        if trust_result.get("pair_accepted") is not True:
            states["PREDICATE_POLICY_VALIDATED"] = "FAIL"
            return result

    if predicate_policy is None:
        states["PREDICATE_POLICY_VALIDATED"] = "UNKNOWN"
        return result

    predicate_context = {
        "statement": statement,
        "observed_at": observed_at,
        "trust_evaluation": trust_result,
    }
    predicate_result = dict(predicate_policy(predicate_context))
    predicate_status = predicate_result.get("status", "UNKNOWN")
    if predicate_status not in {"PASS", "FAIL", "UNKNOWN", "UNSUPPORTED", "NOT_EVALUATED"}:
        raise ValueError("predicate policy returned invalid result")
    if predicate_status == "PASS":
        if not predicate_result.get("policy_identity") or not predicate_result.get("policy_digest"):
            predicate_status = "UNKNOWN"
            predicate_result["status"] = "UNKNOWN"
            predicate_result["reason"] = "PASS forbidden without immutable predicate-policy identity"
    evidence["predicate_policy_evaluation"] = predicate_result
    states["PREDICATE_POLICY_VALIDATED"] = predicate_status
    return result


def _vsa_verifier_id(statement: Mapping[str, Any]) -> Any:
    if statement.get("predicateType") != SLSA_VSA_V1:
        return None
    predicate = statement.get("predicate", {})
    verifier = predicate.get("verifier", {}) if isinstance(predicate, Mapping) else {}
    return verifier.get("id") if isinstance(verifier, Mapping) else None


def _extract_asserted_timestamps(statement: Mapping[str, Any]) -> dict[str, Any]:
    predicate = statement.get("predicate", {})
    if not isinstance(predicate, Mapping):
        return {}
    values: dict[str, Any] = {}
    for key in ("timeVerified",):
        if key in predicate:
            values[key] = predicate[key]
    run_details = predicate.get("runDetails")
    if isinstance(run_details, Mapping):
        metadata = run_details.get("metadata")
        if isinstance(metadata, Mapping):
            for key in ("startedOn", "finishedOn"):
                if key in metadata:
                    values[f"runDetails.metadata.{key}"] = metadata[key]
    return values
