#!/usr/bin/env python3
"""AX-PUB-REF-002 — Point-in-Time Knowledge Validator.

Public educational reference implementation for selected invariants from
AX-PUB-SPEC-003. This is not a production data-quality, market-data, or AIC
implementation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


EXPECTED_SCHEMA_ID = "AX-PUB-SCHEMA-002"
EXPECTED_SCHEMA_VERSION = "1.0"

REVISION_KINDS = {
    "NEW_INFORMATION",
    "CORRECTION",
    "RESTATEMENT",
    "RECLASSIFICATION",
    "SUPERSESSION",
    "DELETION_OR_WITHDRAWAL",
}

FRESHNESS_STATES = {
    "CURRENT_FOR_POLICY",
    "AGING",
    "STALE",
    "EXPIRED",
    "UNKNOWN_FRESHNESS",
}

MISSING_STATES = {
    "MISSING",
    "NOT_YET_PUBLISHED",
    "NOT_YET_OBSERVED",
    "UNAVAILABLE",
    "NOT_APPLICABLE",
    "WITHHELD_OR_RESTRICTED",
    "UNKNOWN",
    "CONFLICTED",
}

TRANSFORMATION_MODES = {"DETERMINISTIC", "PROBABILISTIC", "MIXED"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def parse_time(value: Any, path: str, findings: list[Finding]) -> datetime | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        findings.append(Finding("AX-PTK-TIME-FORMAT", path, "timestamp must be an ISO-8601 string"))
        return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        findings.append(Finding("AX-PTK-TIME-FORMAT", path, "invalid ISO-8601 timestamp"))
        return None


def require_fields(record: dict[str, Any], fields: Iterable[str], path: str, findings: list[Finding]) -> None:
    for field in fields:
        if record.get(field) in (None, "", []):
            findings.append(Finding("AX-PTK-REQUIRED", f"{path}.{field}", "required field is missing or empty"))


def index_records(records: Any, id_field: str, collection_name: str, findings: list[Finding]) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        findings.append(Finding("AX-PTK-COLLECTION", collection_name, "collection must be an array"))
        return {}

    indexed: dict[str, dict[str, Any]] = {}
    for i, record in enumerate(records):
        path = f"{collection_name}[{i}]"
        if not isinstance(record, dict):
            findings.append(Finding("AX-PTK-RECORD", path, "record must be an object"))
            continue
        identifier = record.get(id_field)
        if not isinstance(identifier, str) or not identifier:
            findings.append(Finding("AX-PTK-ID", f"{path}.{id_field}", "record must have a non-empty string identifier"))
            continue
        if identifier in indexed:
            findings.append(Finding("AX-PTK-ID-DUPLICATE", f"{path}.{id_field}", f"duplicate identifier: {identifier}"))
            continue
        indexed[identifier] = record
    return indexed


def validate_envelope(envelope: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(envelope, dict):
        return [Finding("AX-PTK-ENVELOPE", "$", "envelope must be a JSON object")]

    if envelope.get("schema_id") != EXPECTED_SCHEMA_ID:
        findings.append(Finding("AX-PTK-SCHEMA-ID", "schema_id", f"schema_id must be {EXPECTED_SCHEMA_ID}"))
    if envelope.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        findings.append(Finding("AX-PTK-SCHEMA-VERSION", "schema_version", f"schema_version must be {EXPECTED_SCHEMA_VERSION}"))
    if not isinstance(envelope.get("envelope_id"), str) or not envelope.get("envelope_id"):
        findings.append(Finding("AX-PTK-ENVELOPE-ID", "envelope_id", "envelope_id must be a non-empty string"))

    context = envelope.get("query_context")
    if not isinstance(context, dict):
        findings.append(Finding("AX-PTK-QUERY-CONTEXT", "query_context", "query_context must be an object"))
        context = {}

    require_fields(
        context,
        (
            "as_of_time",
            "knowledge_cutoff_time",
            "effective_time_policy",
            "publication_time_policy",
            "observed_time_policy",
            "source_scope",
            "revision_policy",
            "quality_policy",
            "conflict_policy",
            "missing_data_policy",
        ),
        "query_context",
        findings,
    )

    parse_time(context.get("as_of_time"), "query_context.as_of_time", findings)
    cutoff = parse_time(context.get("knowledge_cutoff_time"), "query_context.knowledge_cutoff_time", findings)
    if context.get("source_scope") is not None and not isinstance(context.get("source_scope"), list):
        findings.append(Finding("AX-PTK-SOURCE-SCOPE", "query_context.source_scope", "source_scope must be an array"))

    sources = index_records(envelope.get("source_records"), "source_record_id", "source_records", findings)
    transformations = index_records(
        envelope.get("transformation_records"),
        "transformation_id",
        "transformation_records",
        findings,
    )
    assertions = index_records(
        envelope.get("knowledge_assertions"),
        "assertion_id",
        "knowledge_assertions",
        findings,
    )

    # Reference identifiers should not collide across public envelope namespaces.
    namespace_owner: dict[str, str] = {}
    for collection_name, indexed in (
        ("source_records", sources),
        ("transformation_records", transformations),
        ("knowledge_assertions", assertions),
    ):
        for identifier in indexed:
            previous = namespace_owner.get(identifier)
            if previous is not None:
                findings.append(
                    Finding(
                        "AX-PTK-ID-COLLISION",
                        identifier,
                        f"identifier is reused across {previous} and {collection_name}",
                    )
                )
            else:
                namespace_owner[identifier] = collection_name

    source_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    for source_id, record in sources.items():
        path = f"source_records[{source_id}]"
        require_fields(record, ("source_identity", "source_type", "retrieved_at"), path, findings)
        published = parse_time(record.get("published_at"), f"{path}.published_at", findings)
        retrieved = parse_time(record.get("retrieved_at"), f"{path}.retrieved_at", findings)
        if cutoff and published and published > cutoff:
            findings.append(
                Finding(
                    "AX-PTK-FUTURE-SOURCE-PUBLICATION",
                    f"{path}.published_at",
                    "source was published after the declared knowledge cutoff",
                )
            )
        if cutoff and retrieved and retrieved > cutoff:
            findings.append(
                Finding(
                    "AX-PTK-FUTURE-SOURCE-RETRIEVAL",
                    f"{path}.retrieved_at",
                    "source was retrieved after the declared knowledge cutoff",
                )
            )
        if published and retrieved and retrieved < published:
            findings.append(
                Finding(
                    "AX-PTK-SOURCE-TIME-ORDER",
                    path,
                    "retrieved_at cannot precede published_at in the reference profile",
                )
            )
        source_times[source_id] = (published, retrieved)

    assertion_times: dict[str, datetime | None] = {}
    for assertion_id, record in assertions.items():
        path = f"knowledge_assertions[{assertion_id}]"
        require_fields(
            record,
            ("subject_id", "predicate", "classification", "source_record_id", "observed_at", "version_id"),
            path,
            findings,
        )

        observed = parse_time(record.get("observed_at"), f"{path}.observed_at", findings)
        published = parse_time(record.get("published_at"), f"{path}.published_at", findings)
        effective = parse_time(record.get("effective_at"), f"{path}.effective_at", findings)
        effective_until = parse_time(record.get("effective_until"), f"{path}.effective_until", findings)
        valid_from = parse_time(record.get("valid_from"), f"{path}.valid_from", findings)
        valid_until = parse_time(record.get("valid_until"), f"{path}.valid_until", findings)
        parse_time(record.get("superseded_at"), f"{path}.superseded_at", findings)
        parse_time(record.get("created_at"), f"{path}.created_at", findings)
        assertion_times[assertion_id] = observed

        if cutoff and observed and observed > cutoff:
            findings.append(
                Finding(
                    "AX-PTK-FUTURE-ASSERTION-OBSERVED",
                    f"{path}.observed_at",
                    "assertion was observed after the declared knowledge cutoff",
                )
            )
        if cutoff and published and published > cutoff:
            findings.append(
                Finding(
                    "AX-PTK-FUTURE-ASSERTION-PUBLISHED",
                    f"{path}.published_at",
                    "assertion was published after the declared knowledge cutoff",
                )
            )
        if published and observed and observed < published:
            findings.append(
                Finding(
                    "AX-PTK-ASSERTION-TIME-ORDER",
                    path,
                    "observed_at cannot precede published_at in the reference profile",
                )
            )
        if effective and effective_until and effective_until <= effective:
            findings.append(
                Finding(
                    "AX-PTK-EFFECTIVE-INTERVAL",
                    path,
                    "effective_until must be later than effective_at",
                )
            )
        if valid_from and valid_until and valid_until <= valid_from:
            findings.append(
                Finding(
                    "AX-PTK-VALIDITY-INTERVAL",
                    path,
                    "valid_until must be later than valid_from",
                )
            )

        source_id = record.get("source_record_id")
        if source_id not in sources:
            findings.append(
                Finding(
                    "AX-PTK-SOURCE-REFERENCE",
                    f"{path}.source_record_id",
                    "assertion references an unknown source record",
                )
            )
        else:
            _, retrieved = source_times.get(source_id, (None, None))
            if retrieved and observed and observed < retrieved:
                findings.append(
                    Finding(
                        "AX-PTK-OBSERVED-BEFORE-RETRIEVAL",
                        f"{path}.observed_at",
                        "assertion cannot be observed before its source was retrieved",
                    )
                )

        revision_kind = record.get("revision_kind")
        if revision_kind is not None and revision_kind not in REVISION_KINDS:
            findings.append(Finding("AX-PTK-REVISION-KIND", f"{path}.revision_kind", "unsupported revision kind"))
        if revision_kind in REVISION_KINDS - {"NEW_INFORMATION"} and not record.get("supersedes"):
            findings.append(
                Finding(
                    "AX-PTK-REVISION-SUPERSEDES-REQUIRED",
                    f"{path}.supersedes",
                    "correction/restatement/reclassification/supersession/withdrawal must identify the prior assertion",
                )
            )

        freshness_state = record.get("freshness_state")
        if freshness_state is not None and freshness_state not in FRESHNESS_STATES:
            findings.append(Finding("AX-PTK-FRESHNESS-STATE", f"{path}.freshness_state", "unsupported freshness state"))

        missing_state = record.get("missing_state")
        if missing_state is not None and missing_state not in MISSING_STATES:
            findings.append(Finding("AX-PTK-MISSING-STATE", f"{path}.missing_state", "unsupported missing-data state"))
        if ("value" not in record or record.get("value") is None) and missing_state is None:
            findings.append(
                Finding(
                    "AX-PTK-MISSING-STATE-REQUIRED",
                    path,
                    "an absent/null value must preserve an explicit missing_state",
                )
            )

    # Supersession relationships are checked after all assertions are indexed.
    for assertion_id, record in assertions.items():
        path = f"knowledge_assertions[{assertion_id}]"
        supersedes = record.get("supersedes")
        if supersedes:
            prior = assertions.get(supersedes)
            if prior is None:
                findings.append(
                    Finding(
                        "AX-PTK-SUPERSEDES-REFERENCE",
                        f"{path}.supersedes",
                        "supersedes references an unknown assertion",
                    )
                )
            elif supersedes == assertion_id:
                findings.append(Finding("AX-PTK-SUPERSEDES-SELF", f"{path}.supersedes", "assertion cannot supersede itself"))
            else:
                if prior.get("subject_id") != record.get("subject_id") or prior.get("predicate") != record.get("predicate"):
                    findings.append(
                        Finding(
                            "AX-PTK-SUPERSESSION-SCOPE",
                            f"{path}.supersedes",
                            "reference supersession should preserve subject and predicate identity",
                        )
                    )
                prior_observed = assertion_times.get(supersedes)
                current_observed = assertion_times.get(assertion_id)
                if prior_observed and current_observed and current_observed <= prior_observed:
                    findings.append(
                        Finding(
                            "AX-PTK-SUPERSESSION-TIME",
                            f"{path}.observed_at",
                            "superseding assertion should be observed after the prior assertion",
                        )
                    )

        superseded_by = record.get("superseded_by")
        if superseded_by and superseded_by not in assertions:
            findings.append(
                Finding(
                    "AX-PTK-SUPERSEDED-BY-REFERENCE",
                    f"{path}.superseded_by",
                    "superseded_by references an unknown assertion",
                )
            )

    valid_input_refs = set(sources) | set(assertions)
    for transformation_id, record in transformations.items():
        path = f"transformation_records[{transformation_id}]"
        require_fields(
            record,
            ("input_references", "output_references", "method", "executed_at", "deterministic_or_probabilistic"),
            path,
            findings,
        )
        parse_time(record.get("executed_at"), f"{path}.executed_at", findings)
        mode = record.get("deterministic_or_probabilistic")
        if mode not in TRANSFORMATION_MODES:
            findings.append(Finding("AX-PTK-TRANSFORMATION-MODE", f"{path}.deterministic_or_probabilistic", "unsupported transformation mode"))

        inputs = record.get("input_references")
        if not isinstance(inputs, list):
            findings.append(Finding("AX-PTK-TRANSFORMATION-INPUTS", f"{path}.input_references", "input_references must be an array"))
        else:
            for ref in inputs:
                if ref not in valid_input_refs:
                    findings.append(Finding("AX-PTK-TRANSFORMATION-INPUT-REF", f"{path}.input_references", f"unknown input reference: {ref}"))

        outputs = record.get("output_references")
        if not isinstance(outputs, list):
            findings.append(Finding("AX-PTK-TRANSFORMATION-OUTPUTS", f"{path}.output_references", "output_references must be an array"))
        else:
            for ref in outputs:
                if ref not in assertions:
                    findings.append(Finding("AX-PTK-TRANSFORMATION-OUTPUT-REF", f"{path}.output_references", f"unknown assertion output reference: {ref}"))

    for assertion_id, record in assertions.items():
        path = f"knowledge_assertions[{assertion_id}]"
        refs = record.get("transformation_references", [])
        if not isinstance(refs, list):
            findings.append(Finding("AX-PTK-TRANSFORMATION-REFS", f"{path}.transformation_references", "transformation_references must be an array"))
        else:
            for ref in refs:
                if ref not in transformations:
                    findings.append(Finding("AX-PTK-TRANSFORMATION-REFERENCE", f"{path}.transformation_references", f"unknown transformation reference: {ref}"))

    reproducibility = envelope.get("reproducibility_package")
    if reproducibility is not None:
        if not isinstance(reproducibility, dict):
            findings.append(Finding("AX-PTK-REPRODUCIBILITY", "reproducibility_package", "reproducibility_package must be an object"))
        else:
            repro_cutoff = parse_time(
                reproducibility.get("point_in_time_cutoff"),
                "reproducibility_package.point_in_time_cutoff",
                findings,
            )
            if cutoff and repro_cutoff and repro_cutoff != cutoff:
                findings.append(
                    Finding(
                        "AX-PTK-REPRODUCIBILITY-CUTOFF",
                        "reproducibility_package.point_in_time_cutoff",
                        "reproducibility cutoff must match query_context.knowledge_cutoff_time",
                    )
                )

    return findings


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AX-PUB-SPEC-003 point-in-time reference envelope")
    parser.add_argument("envelope", type=Path, help="path to point-in-time knowledge envelope JSON")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit findings as JSON")
    args = parser.parse_args()

    try:
        envelope = load_json(args.envelope)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        finding = Finding("AX-PTK-INPUT", str(args.envelope), str(exc))
        if args.json_output:
            print(json.dumps({"status": "FAIL", "findings": [asdict(finding)]}, indent=2))
        else:
            print(f"{finding.code} {finding.path}: {finding.message}")
        return 1

    findings = validate_envelope(envelope)
    if args.json_output:
        print(json.dumps({"status": "PASS" if not findings else "FAIL", "findings": [asdict(f) for f in findings]}, indent=2))
    elif findings:
        for finding in findings:
            print(f"{finding.code} {finding.path}: {finding.message}")
    else:
        print("AX_PTK_REFERENCE_VALIDATION_PASS")

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
