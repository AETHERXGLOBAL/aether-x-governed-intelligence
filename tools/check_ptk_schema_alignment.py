#!/usr/bin/env python3
"""Repository-integrity checks for AX-PUB-SCHEMA-002.

This script checks the published schema profile and example for deterministic
alignment with selected AX-PUB-SPEC-003 states. It is not a general-purpose
JSON Schema engine and not a production temporal-integrity validator.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json"
EXAMPLE_PATH = ROOT / "schemas" / "examples" / "AX-PUB-SCHEMA-002_example.json"

EXPECTED_SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_SCHEMA_ID = "AX-PUB-SCHEMA-002"
EXPECTED_SCHEMA_VERSION = "1.0"

EXPECTED_REVISION_KINDS = {
    "NEW_INFORMATION",
    "CORRECTION",
    "RESTATEMENT",
    "RECLASSIFICATION",
    "SUPERSESSION",
    "DELETION_OR_WITHDRAWAL",
}

EXPECTED_FRESHNESS_STATES = {
    "CURRENT_FOR_POLICY",
    "AGING",
    "STALE",
    "EXPIRED",
    "UNKNOWN_FRESHNESS",
}

EXPECTED_MISSING_STATES = {
    "MISSING",
    "NOT_YET_PUBLISHED",
    "NOT_YET_OBSERVED",
    "UNAVAILABLE",
    "NOT_APPLICABLE",
    "WITHHELD_OR_RESTRICTED",
    "UNKNOWN",
    "CONFLICTED",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def check_schema(schema: dict) -> None:
    if schema.get("$schema") != EXPECTED_SCHEMA_URI:
        fail("unexpected JSON Schema dialect")

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    expected_required = {
        "schema_id",
        "schema_version",
        "envelope_id",
        "query_context",
        "source_records",
        "transformation_records",
        "knowledge_assertions",
    }
    if not expected_required.issubset(required):
        fail("top-level point-in-time envelope fields drifted")

    if properties.get("schema_id", {}).get("const") != EXPECTED_SCHEMA_ID:
        fail("schema_id const drifted")
    if properties.get("schema_version", {}).get("const") != EXPECTED_SCHEMA_VERSION:
        fail("schema_version const drifted")

    defs = schema.get("$defs", {})
    assertion_properties = defs.get("knowledge_assertion", {}).get("properties", {})

    revision_kinds = set(assertion_properties.get("revision_kind", {}).get("enum", []))
    if revision_kinds != EXPECTED_REVISION_KINDS:
        fail("revision-kind states drifted from AX-PUB-SPEC-003 reference states")

    freshness_states = set(assertion_properties.get("freshness_state", {}).get("enum", []))
    if freshness_states != EXPECTED_FRESHNESS_STATES:
        fail("freshness states drifted from AX-PUB-SPEC-003")

    missing_states = set(assertion_properties.get("missing_state", {}).get("enum", []))
    if missing_states != EXPECTED_MISSING_STATES:
        fail("missing-data states drifted from AX-PUB-SPEC-003")


def check_example(example: dict) -> None:
    if example.get("schema_id") != EXPECTED_SCHEMA_ID:
        fail("example schema_id mismatch")
    if example.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        fail("example schema_version mismatch")
    if not isinstance(example.get("envelope_id"), str) or not example["envelope_id"]:
        fail("example envelope_id must be non-empty")

    for collection in ("source_records", "transformation_records", "knowledge_assertions"):
        if not isinstance(example.get(collection), list):
            fail(f"example {collection} must be an array")

    context = example.get("query_context")
    if not isinstance(context, dict):
        fail("example query_context must be an object")

    cutoff = parse_time(context["knowledge_cutoff_time"])

    # The published example represents a point-in-time package, so its source
    # retrieval and assertion observation times should not exceed the cutoff.
    for source in example["source_records"]:
        if parse_time(source["retrieved_at"]) > cutoff:
            fail("example source retrieved_at exceeds knowledge cutoff")

    source_ids = {record["source_record_id"] for record in example["source_records"]}
    transformation_ids = {record["transformation_id"] for record in example["transformation_records"]}

    for assertion in example["knowledge_assertions"]:
        if parse_time(assertion["observed_at"]) > cutoff:
            fail("example assertion observed_at exceeds knowledge cutoff")
        if assertion["source_record_id"] not in source_ids:
            fail("example assertion references unknown source record")
        for transformation_ref in assertion.get("transformation_references", []):
            if transformation_ref not in transformation_ids:
                fail("example assertion references unknown transformation")


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)
    check_schema(schema)
    check_example(example)
    print("AX_PTK_SCHEMA_ALIGNMENT_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"AX_PTK_SCHEMA_ALIGNMENT_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
