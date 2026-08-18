#!/usr/bin/env python3
"""AX-PUB-REF-001 — EAV Contract Validator.

Public educational reference implementation for selected invariants from
AX-PUB-SPEC-002. This is not a production authorization or security system.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_EVIDENCE_CLASSIFICATIONS = {
    "FACT",
    "SOURCE_DATA",
    "ASSUMPTION",
    "ESTIMATE",
    "HYPOTHESIS",
    "INFERENCE",
    "FORECAST",
    "SCENARIO",
    "PROFESSIONAL_OPINION",
    "RECOMMENDATION",
    "DECISION",
    "VERIFIED_OUTCOME",
    "UNKNOWN",
    "SUPERSEDED",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def parse_time(value: Any, path: str, findings: list[Finding]) -> datetime | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        findings.append(Finding("AX-REF-TIME-FORMAT", path, "timestamp must be an ISO-8601 string"))
        return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        findings.append(Finding("AX-REF-TIME-FORMAT", path, "invalid ISO-8601 timestamp"))
        return None


def require_fields(record: dict[str, Any], fields: Iterable[str], path: str, findings: list[Finding]) -> None:
    for field in fields:
        if record.get(field) in (None, "", []):
            findings.append(Finding("AX-REF-REQUIRED", f"{path}.{field}", "required field is missing or empty"))


def index_records(
    records: Any,
    id_field: str,
    collection_name: str,
    findings: list[Finding],
) -> dict[str, dict[str, Any]]:
    if records is None:
        return {}
    if not isinstance(records, list):
        findings.append(Finding("AX-REF-COLLECTION", collection_name, "collection must be an array"))
        return {}

    indexed: dict[str, dict[str, Any]] = {}
    for i, record in enumerate(records):
        path = f"{collection_name}[{i}]"
        if not isinstance(record, dict):
            findings.append(Finding("AX-REF-RECORD", path, "record must be an object"))
            continue
        identifier = record.get(id_field)
        if not isinstance(identifier, str) or not identifier:
            findings.append(Finding("AX-REF-ID", f"{path}.{id_field}", "record must have a non-empty string identifier"))
            continue
        if identifier in indexed:
            findings.append(Finding("AX-REF-ID-DUPLICATE", f"{path}.{id_field}", f"duplicate identifier: {identifier}"))
            continue
        indexed[identifier] = record
    return indexed


def validate_bundle(bundle: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(bundle, dict):
        return [Finding("AX-REF-BUNDLE", "$", "bundle must be a JSON object")]

    evidence = index_records(bundle.get("evidence_records"), "evidence_id", "evidence_records", findings)
    decisions = index_records(bundle.get("decision_records"), "decision_id", "decision_records", findings)
    authorities = index_records(bundle.get("authority_grants"), "authority_id", "authority_grants", findings)
    executions = index_records(bundle.get("execution_records"), "execution_id", "execution_records", findings)
    verifications = index_records(bundle.get("verification_records"), "verification_id", "verification_records", findings)
    outcomes = index_records(bundle.get("verified_outcomes"), "outcome_id", "verified_outcomes", findings)

    # Evidence records
    for evidence_id, record in evidence.items():
        path = f"evidence_records[{evidence_id}]"
        require_fields(record, ("classification", "source_identity", "observed_at"), path, findings)
        classification = record.get("classification")
        if classification and classification not in SUPPORTED_EVIDENCE_CLASSIFICATIONS:
            findings.append(Finding("AX-EAV-EVIDENCE-CLASSIFICATION", f"{path}.classification", f"unsupported classification: {classification}"))
        parse_time(record.get("observed_at"), f"{path}.observed_at", findings)
        parse_time(record.get("effective_at"), f"{path}.effective_at", findings)

    # Decisions must reference evidence.
    for decision_id, record in decisions.items():
        path = f"decision_records[{decision_id}]"
        require_fields(record, ("decision_question", "decision_owner", "evidence_refs", "decided_at"), path, findings)
        parse_time(record.get("decided_at"), f"{path}.decided_at", findings)
        refs = record.get("evidence_refs", [])
        if isinstance(refs, list):
            for ref in refs:
                if ref not in evidence:
                    findings.append(Finding("AX-EAV-EVIDENCE-REF", f"{path}.evidence_refs", f"unknown evidence reference: {ref}"))
        elif refs is not None:
            findings.append(Finding("AX-EAV-EVIDENCE-REF-TYPE", f"{path}.evidence_refs", "evidence_refs must be an array"))

    # Authority grants must bind decision, principal, action and resource scope.
    authority_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    for authority_id, record in authorities.items():
        path = f"authority_grants[{authority_id}]"
        require_fields(
            record,
            ("decision_id", "principal", "permitted_action", "resource_scope", "status", "granted_at"),
            path,
            findings,
        )
        if record.get("decision_id") not in decisions:
            findings.append(Finding("AX-EAV-AUTHORITY-DECISION", f"{path}.decision_id", "authority references an unknown decision"))
        if record.get("status") not in {"ACTIVE", "REVOKED", "EXPIRED"}:
            findings.append(Finding("AX-EAV-AUTHORITY-STATUS", f"{path}.status", "authority status must be ACTIVE, REVOKED or EXPIRED"))
        if not isinstance(record.get("resource_scope"), list):
            findings.append(Finding("AX-EAV-AUTHORITY-SCOPE", f"{path}.resource_scope", "resource_scope must be an array"))
        granted = parse_time(record.get("granted_at"), f"{path}.granted_at", findings)
        expires = parse_time(record.get("expires_at"), f"{path}.expires_at", findings)
        if granted and expires and expires <= granted:
            findings.append(Finding("AX-EAV-AUTHORITY-EXPIRY", f"{path}.expires_at", "authority expiry must be after grant time"))
        authority_times[authority_id] = (granted, expires)

    # Executions must remain inside active authority.
    for execution_id, record in executions.items():
        path = f"execution_records[{execution_id}]"
        require_fields(
            record,
            ("decision_id", "authority_id", "actor", "action", "resource", "started_at", "status"),
            path,
            findings,
        )
        decision_id = record.get("decision_id")
        authority_id = record.get("authority_id")
        if decision_id not in decisions:
            findings.append(Finding("AX-EAV-EXEC-DECISION", f"{path}.decision_id", "execution references an unknown decision"))
        authority = authorities.get(authority_id)
        if authority is None:
            findings.append(Finding("AX-EAV-EXEC-AUTHORITY", f"{path}.authority_id", "execution references an unknown authority grant"))
            continue
        if authority.get("decision_id") != decision_id:
            findings.append(Finding("AX-EAV-EXEC-DECISION-MISMATCH", path, "execution decision does not match authority decision"))
        if authority.get("status") != "ACTIVE":
            findings.append(Finding("AX-EAV-EXEC-AUTHORITY-INACTIVE", f"{path}.authority_id", "execution requires ACTIVE authority"))
        if record.get("actor") != authority.get("principal"):
            findings.append(Finding("AX-EAV-EXEC-PRINCIPAL", f"{path}.actor", "execution actor does not match granted principal"))
        if record.get("action") != authority.get("permitted_action"):
            findings.append(Finding("AX-EAV-EXEC-ACTION", f"{path}.action", "execution action exceeds or differs from granted action"))
        scope = authority.get("resource_scope")
        if isinstance(scope, list) and record.get("resource") not in scope:
            findings.append(Finding("AX-EAV-EXEC-SCOPE", f"{path}.resource", "execution resource is outside granted resource scope"))
        started = parse_time(record.get("started_at"), f"{path}.started_at", findings)
        granted, expires = authority_times.get(authority_id, (None, None))
        if started and granted and started < granted:
            findings.append(Finding("AX-EAV-EXEC-BEFORE-GRANT", f"{path}.started_at", "execution began before authority was granted"))
        if started and expires and started > expires:
            findings.append(Finding("AX-EAV-EXEC-AFTER-EXPIRY", f"{path}.started_at", "execution began after authority expired"))

    # Verification references execution and can require independence.
    for verification_id, record in verifications.items():
        path = f"verification_records[{verification_id}]"
        require_fields(record, ("execution_id", "verifier", "verdict", "verified_at"), path, findings)
        execution = executions.get(record.get("execution_id"))
        if execution is None:
            findings.append(Finding("AX-EAV-VERIFY-EXECUTION", f"{path}.execution_id", "verification references an unknown execution"))
        if record.get("verdict") not in {"PASS", "FAIL", "INCONCLUSIVE", "NOT_PERFORMED"}:
            findings.append(Finding("AX-EAV-VERIFY-VERDICT", f"{path}.verdict", "unsupported verification verdict"))
        parse_time(record.get("verified_at"), f"{path}.verified_at", findings)
        if execution and record.get("requires_independent_verifier") is True:
            if record.get("verifier") == execution.get("actor"):
                findings.append(Finding("AX-EAV-VERIFY-INDEPENDENCE", f"{path}.verifier", "independent verifier cannot equal execution actor"))

    # Verified outcomes require PASS verification.
    for outcome_id, record in outcomes.items():
        path = f"verified_outcomes[{outcome_id}]"
        require_fields(record, ("verification_id", "outcome_state", "accepted_at"), path, findings)
        verification = verifications.get(record.get("verification_id"))
        if verification is None:
            findings.append(Finding("AX-EAV-OUTCOME-VERIFICATION", f"{path}.verification_id", "outcome references an unknown verification"))
        elif record.get("outcome_state") == "VERIFIED" and verification.get("verdict") != "PASS":
            findings.append(Finding("AX-EAV-OUTCOME-NOT-PASSED", path, "VERIFIED outcome requires PASS verification"))
        if record.get("outcome_state") != "VERIFIED":
            findings.append(Finding("AX-EAV-OUTCOME-STATE", f"{path}.outcome_state", "reference outcome state must be VERIFIED"))
        parse_time(record.get("accepted_at"), f"{path}.accepted_at", findings)

    return findings


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AX-PUB-SPEC-002 reference bundle")
    parser.add_argument("bundle", type=Path, help="path to JSON bundle")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit findings as JSON")
    args = parser.parse_args()

    try:
        bundle = load_json(args.bundle)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        finding = Finding("AX-REF-INPUT", str(args.bundle), str(exc))
        if args.json_output:
            print(json.dumps({"status": "FAIL", "findings": [asdict(finding)]}, indent=2))
        else:
            print(f"{finding.code} {finding.path}: {finding.message}")
        return 1

    findings = validate_bundle(bundle)
    if args.json_output:
        print(json.dumps({"status": "PASS" if not findings else "FAIL", "findings": [asdict(f) for f in findings]}, indent=2))
    elif findings:
        for finding in findings:
            print(f"{finding.code} {finding.path}: {finding.message}")
    else:
        print("AX_EAV_REFERENCE_VALIDATION_PASS")

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
