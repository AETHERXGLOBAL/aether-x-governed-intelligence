#!/usr/bin/env python3
"""AX-PUB-REF-003 — public educational validator for selected AX-PUB-SPEC-004 invariants.

This is not a production authorization, policy, security, or agent-runtime system.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

EXPECTED_SCHEMA_ID = "AX-PUB-SCHEMA-003"
EXPECTED_SCHEMA_VERSION = "1.0"

@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

def parse_time(value: Any, path: str, findings: list[Finding]) -> datetime | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        findings.append(Finding("AX-AGT-TIME-FORMAT", path, "timestamp must be an ISO-8601 string")); return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        findings.append(Finding("AX-AGT-TIME-FORMAT", path, "invalid ISO-8601 timestamp")); return None

def require_fields(record: dict[str, Any], fields: Iterable[str], path: str, findings: list[Finding]) -> None:
    for field in fields:
        if record.get(field) in (None, "", []):
            findings.append(Finding("AX-AGT-REQUIRED", f"{path}.{field}", "required field is missing or empty"))

def index_records(records: Any, id_field: str, name: str, findings: list[Finding]) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        findings.append(Finding("AX-AGT-COLLECTION", name, "collection must be an array")); return {}
    out: dict[str, dict[str, Any]] = {}
    for i, record in enumerate(records):
        path = f"{name}[{i}]"
        if not isinstance(record, dict):
            findings.append(Finding("AX-AGT-RECORD", path, "record must be an object")); continue
        identifier = record.get(id_field)
        if not isinstance(identifier, str) or not identifier:
            findings.append(Finding("AX-AGT-ID", f"{path}.{id_field}", "record must have a non-empty string identifier")); continue
        if identifier in out:
            findings.append(Finding("AX-AGT-ID-DUPLICATE", f"{path}.{id_field}", f"duplicate identifier: {identifier}")); continue
        out[identifier] = record
    return out

def allowed_values(rule: Any) -> set[Any] | None:
    if not isinstance(rule, dict) or not isinstance(rule.get("allowed_values"), list): return None
    try: return set(rule["allowed_values"])
    except TypeError: return None

def constraints_within(child: dict[str, Any], parent: dict[str, Any]) -> bool:
    for key, child_rule in child.items():
        parent_rule = parent.get(key)
        if parent_rule is None: return False
        cvals, pvals = allowed_values(child_rule), allowed_values(parent_rule)
        if pvals is not None and (cvals is None or not cvals.issubset(pvals)): return False
        if isinstance(child_rule, dict) and isinstance(parent_rule, dict):
            cmin, pmin = child_rule.get("minimum"), parent_rule.get("minimum")
            cmax, pmax = child_rule.get("maximum"), parent_rule.get("maximum")
            if pmin is not None and (cmin is None or cmin < pmin): return False
            if pmax is not None and (cmax is None or cmax > pmax): return False
    return True

def validate_parameters(parameters: dict[str, Any], constraints: dict[str, Any], path: str, findings: list[Finding]) -> None:
    for key, rule in constraints.items():
        if not isinstance(rule, dict): continue
        if rule.get("required") is True and key not in parameters:
            findings.append(Finding("AX-AGT-PARAM-REQUIRED", f"{path}.{key}", "required authorized parameter is missing")); continue
        if key not in parameters: continue
        value = parameters[key]
        allowed = rule.get("allowed_values")
        if isinstance(allowed, list) and value not in allowed:
            findings.append(Finding("AX-AGT-PARAM-ALLOWED-VALUES", f"{path}.{key}", "parameter value is outside the authorized set"))
        minimum, maximum = rule.get("minimum"), rule.get("maximum")
        if minimum is not None and isinstance(value, (int, float)) and value < minimum:
            findings.append(Finding("AX-AGT-PARAM-MINIMUM", f"{path}.{key}", "parameter value is below the authorized minimum"))
        if maximum is not None and isinstance(value, (int, float)) and value > maximum:
            findings.append(Finding("AX-AGT-PARAM-MAXIMUM", f"{path}.{key}", "parameter value exceeds the authorized maximum"))

def validate_envelope(envelope: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(envelope, dict): return [Finding("AX-AGT-ENVELOPE", "$", "envelope must be a JSON object")]
    if envelope.get("schema_id") != EXPECTED_SCHEMA_ID: findings.append(Finding("AX-AGT-SCHEMA-ID", "schema_id", f"schema_id must be {EXPECTED_SCHEMA_ID}"))
    if envelope.get("schema_version") != EXPECTED_SCHEMA_VERSION: findings.append(Finding("AX-AGT-SCHEMA-VERSION", "schema_version", f"schema_version must be {EXPECTED_SCHEMA_VERSION}"))

    identities = index_records(envelope.get("agent_identities"), "principal_id", "agent_identities", findings)
    tools = index_records(envelope.get("tool_descriptors"), "tool_id", "tool_descriptors", findings)
    proposals = index_records(envelope.get("action_proposals"), "proposal_id", "action_proposals", findings)
    contexts = index_records(envelope.get("authority_contexts"), "authority_context_id", "authority_contexts", findings)
    grants = index_records(envelope.get("tool_use_grants"), "grant_id", "tool_use_grants", findings)
    invocations = index_records(envelope.get("tool_invocations"), "invocation_id", "tool_invocations", findings)
    results = index_records(envelope.get("tool_results"), "result_id", "tool_results", findings)

    context_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    grant_times: dict[str, tuple[datetime | None, datetime | None]] = {}

    for pid, record in proposals.items():
        path = f"action_proposals[{pid}]"
        require_fields(record, ("principal_id","proposed_tool","proposed_action","target_resource","bounded_parameters","requested_at"), path, findings)
        if record.get("principal_id") not in identities: findings.append(Finding("AX-AGT-PROPOSAL-PRINCIPAL", f"{path}.principal_id", "proposal references an unknown principal"))
        tool = tools.get(record.get("proposed_tool"))
        if tool is None: findings.append(Finding("AX-AGT-PROPOSAL-TOOL", f"{path}.proposed_tool", "proposal references an unknown tool"))
        else:
            if record.get("proposed_action") not in tool.get("supported_actions", []): findings.append(Finding("AX-AGT-PROPOSAL-ACTION", f"{path}.proposed_action", "proposed action is not declared by the tool descriptor"))
            if tool.get("lifecycle_state") != "ACTIVE": findings.append(Finding("AX-AGT-TOOL-INACTIVE", f"{path}.proposed_tool", "proposal requires an ACTIVE tool descriptor"))
        requested = parse_time(record.get("requested_at"), f"{path}.requested_at", findings)
        expires = parse_time(record.get("expires_at"), f"{path}.expires_at", findings)
        if requested and expires and expires <= requested: findings.append(Finding("AX-AGT-PROPOSAL-EXPIRY", f"{path}.expires_at", "proposal expiry must be after requested_at"))

    for cid, record in contexts.items():
        path = f"authority_contexts[{cid}]"
        require_fields(record, ("principal_id","permitted_tools","permitted_actions","resource_scope","parameter_constraints","valid_from","valid_until","revocation_state","environment_constraints","evaluated_at"), path, findings)
        if record.get("principal_id") not in identities: findings.append(Finding("AX-AGT-CONTEXT-PRINCIPAL", f"{path}.principal_id", "authority context references an unknown principal"))
        if record.get("revocation_state") not in {"ACTIVE","REVOKED","EXPIRED","UNKNOWN"}: findings.append(Finding("AX-AGT-CONTEXT-STATE", f"{path}.revocation_state", "unsupported authority revocation state"))
        start = parse_time(record.get("valid_from"), f"{path}.valid_from", findings); end = parse_time(record.get("valid_until"), f"{path}.valid_until", findings)
        parse_time(record.get("evaluated_at"), f"{path}.evaluated_at", findings)
        if start and end and end <= start: findings.append(Finding("AX-AGT-CONTEXT-WINDOW", path, "authority context valid_until must be after valid_from"))
        context_times[cid] = (start, end)

    for gid, record in grants.items():
        path = f"tool_use_grants[{gid}]"
        require_fields(record, ("principal_id","proposal_reference","authority_context_reference","tool_id","permitted_action","resource_scope","parameter_constraints","valid_from","valid_until","single_use_or_reusable","maximum_invocations","issued_by","issued_at"), path, findings)
        proposal = proposals.get(record.get("proposal_reference")); context = contexts.get(record.get("authority_context_reference"))
        if proposal is None: findings.append(Finding("AX-AGT-GRANT-PROPOSAL", f"{path}.proposal_reference", "grant references an unknown proposal"))
        if context is None: findings.append(Finding("AX-AGT-GRANT-CONTEXT", f"{path}.authority_context_reference", "grant references an unknown authority context"))
        if record.get("principal_id") not in identities: findings.append(Finding("AX-AGT-GRANT-PRINCIPAL", f"{path}.principal_id", "grant references an unknown principal"))
        if proposal and record.get("principal_id") != proposal.get("principal_id"): findings.append(Finding("AX-AGT-GRANT-PRINCIPAL-MISMATCH", f"{path}.principal_id", "grant principal does not match proposal principal"))
        if context and record.get("principal_id") != context.get("principal_id"): findings.append(Finding("AX-AGT-GRANT-CONTEXT-PRINCIPAL", f"{path}.principal_id", "grant principal does not match authority context principal"))
        if proposal and record.get("tool_id") != proposal.get("proposed_tool"): findings.append(Finding("AX-AGT-GRANT-TOOL-MISMATCH", f"{path}.tool_id", "grant tool does not match proposed tool"))
        if proposal and record.get("permitted_action") != proposal.get("proposed_action"): findings.append(Finding("AX-AGT-GRANT-ACTION-MISMATCH", f"{path}.permitted_action", "grant action does not match proposed action"))
        if context:
            if record.get("tool_id") not in context.get("permitted_tools", []): findings.append(Finding("AX-AGT-GRANT-TOOL-SCOPE", f"{path}.tool_id", "grant tool is outside authority context"))
            if record.get("permitted_action") not in context.get("permitted_actions", []): findings.append(Finding("AX-AGT-GRANT-ACTION-SCOPE", f"{path}.permitted_action", "grant action is outside authority context"))
            cscope, gscope = context.get("resource_scope", []), record.get("resource_scope", [])
            if isinstance(cscope, list) and isinstance(gscope, list) and not set(gscope).issubset(set(cscope)): findings.append(Finding("AX-AGT-GRANT-RESOURCE-SCOPE", f"{path}.resource_scope", "grant resource scope exceeds authority context"))
            gc, cc = record.get("parameter_constraints", {}), context.get("parameter_constraints", {})
            if isinstance(gc, dict) and isinstance(cc, dict) and not constraints_within(gc, cc): findings.append(Finding("AX-AGT-GRANT-PARAM-SCOPE", f"{path}.parameter_constraints", "grant parameter constraints exceed authority context"))
        if proposal and isinstance(record.get("resource_scope"), list) and proposal.get("target_resource") not in record["resource_scope"]: findings.append(Finding("AX-AGT-GRANT-PROPOSAL-RESOURCE", f"{path}.resource_scope", "grant does not include the proposed target resource"))
        start = parse_time(record.get("valid_from"), f"{path}.valid_from", findings); end = parse_time(record.get("valid_until"), f"{path}.valid_until", findings); issued = parse_time(record.get("issued_at"), f"{path}.issued_at", findings)
        if start and end and end <= start: findings.append(Finding("AX-AGT-GRANT-WINDOW", path, "grant valid_until must be after valid_from"))
        if context:
            cstart, cend = context_times.get(record.get("authority_context_reference"), (None, None))
            if start and cstart and start < cstart: findings.append(Finding("AX-AGT-GRANT-BEFORE-CONTEXT", f"{path}.valid_from", "grant begins before authority context"))
            if end and cend and end > cend: findings.append(Finding("AX-AGT-GRANT-AFTER-CONTEXT", f"{path}.valid_until", "grant extends beyond authority context"))
        if issued and start and issued > start: findings.append(Finding("AX-AGT-GRANT-ISSUED-AFTER-START", f"{path}.issued_at", "grant issued_at must not be after valid_from"))
        max_inv = record.get("maximum_invocations")
        if not isinstance(max_inv, int) or isinstance(max_inv, bool) or max_inv < 1: findings.append(Finding("AX-AGT-GRANT-MAX-INVOCATIONS", f"{path}.maximum_invocations", "maximum_invocations must be an integer >= 1"))
        grant_times[gid] = (start, end)

    counts: dict[str, int] = {}
    for iid, record in invocations.items():
        path = f"tool_invocations[{iid}]"
        require_fields(record, ("grant_id","principal_id","tool_id","tool_version","action","target_resource","effective_parameters","environment","invoked_at","status"), path, findings)
        gid = record.get("grant_id"); grant = grants.get(gid)
        if grant is None: findings.append(Finding("AX-AGT-INVOKE-GRANT", f"{path}.grant_id", "invocation references an unknown grant")); continue
        counts[gid] = counts.get(gid, 0) + 1
        context = contexts.get(grant.get("authority_context_reference"))
        if context and context.get("revocation_state") != "ACTIVE": findings.append(Finding("AX-AGT-INVOKE-AUTHORITY-INACTIVE", f"{path}.grant_id", "invocation requires ACTIVE authority context"))
        if record.get("principal_id") != grant.get("principal_id"): findings.append(Finding("AX-AGT-INVOKE-PRINCIPAL", f"{path}.principal_id", "invocation principal does not match grant"))
        if record.get("tool_id") != grant.get("tool_id"): findings.append(Finding("AX-AGT-INVOKE-TOOL", f"{path}.tool_id", "invocation tool does not match grant"))
        if record.get("action") != grant.get("permitted_action"): findings.append(Finding("AX-AGT-INVOKE-ACTION", f"{path}.action", "invocation action does not match grant"))
        if record.get("target_resource") not in grant.get("resource_scope", []): findings.append(Finding("AX-AGT-INVOKE-RESOURCE", f"{path}.target_resource", "invocation target is outside grant resource scope"))
        invoked = parse_time(record.get("invoked_at"), f"{path}.invoked_at", findings); completed = parse_time(record.get("completed_at"), f"{path}.completed_at", findings); start, end = grant_times.get(gid, (None, None))
        if invoked and start and invoked < start: findings.append(Finding("AX-AGT-INVOKE-BEFORE-GRANT", f"{path}.invoked_at", "invocation occurred before grant validity"))
        if invoked and end and invoked > end: findings.append(Finding("AX-AGT-INVOKE-AFTER-GRANT", f"{path}.invoked_at", "invocation occurred after grant expiry"))
        if invoked and completed and completed < invoked: findings.append(Finding("AX-AGT-INVOKE-TIME-ORDER", path, "completed_at cannot precede invoked_at"))
        if context and record.get("environment") not in context.get("environment_constraints", []): findings.append(Finding("AX-AGT-INVOKE-ENVIRONMENT", f"{path}.environment", "invocation environment is outside authority context"))
        params = record.get("effective_parameters")
        if isinstance(params, dict):
            constraints = grant.get("parameter_constraints", {})
            if isinstance(constraints, dict): validate_parameters(params, constraints, f"{path}.effective_parameters", findings)
        else: findings.append(Finding("AX-AGT-INVOKE-PARAMETERS", f"{path}.effective_parameters", "effective_parameters must be an object"))

    for gid, count in counts.items():
        grant = grants.get(gid, {}); max_inv = grant.get("maximum_invocations")
        if isinstance(max_inv, int) and count > max_inv: findings.append(Finding("AX-AGT-GRANT-INVOCATION-LIMIT", f"tool_use_grants[{gid}]", "grant invocation count exceeds maximum_invocations"))
        if grant.get("single_use_or_reusable") == "SINGLE_USE" and count > 1: findings.append(Finding("AX-AGT-GRANT-SINGLE-USE", f"tool_use_grants[{gid}]", "single-use grant was used more than once"))

    for rid, record in results.items():
        path = f"tool_results[{rid}]"
        require_fields(record, ("invocation_id","tool_reported_status","observed_at"), path, findings)
        if record.get("invocation_id") not in invocations: findings.append(Finding("AX-AGT-RESULT-INVOCATION", f"{path}.invocation_id", "tool result references an unknown invocation"))
        parse_time(record.get("observed_at"), f"{path}.observed_at", findings)
        if not isinstance(record.get("verification_required"), bool): findings.append(Finding("AX-AGT-RESULT-VERIFICATION-STATE", f"{path}.verification_required", "verification_required must be explicit boolean"))
    return findings

def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict): raise ValueError("top-level JSON value must be an object")
    return data

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AX-PUB-SPEC-004 agent tool-use authority reference envelope")
    parser.add_argument("envelope", type=Path); parser.add_argument("--json", action="store_true", dest="json_output"); args = parser.parse_args()
    try: envelope = load_json(args.envelope)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        finding = Finding("AX-AGT-INPUT", str(args.envelope), str(exc))
        print(json.dumps({"status":"FAIL","findings":[asdict(finding)]}, indent=2) if args.json_output else f"{finding.code} {finding.path}: {finding.message}"); return 1
    findings = validate_envelope(envelope)
    if args.json_output: print(json.dumps({"status":"PASS" if not findings else "FAIL","findings":[asdict(f) for f in findings]}, indent=2))
    elif findings:
        for finding in findings: print(f"{finding.code} {finding.path}: {finding.message}")
    else: print("AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS")
    return 0 if not findings else 1

if __name__ == "__main__": raise SystemExit(main())
