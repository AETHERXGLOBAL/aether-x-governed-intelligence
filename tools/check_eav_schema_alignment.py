#!/usr/bin/env python3
"""Check alignment between AX-PUB-SCHEMA-001, examples, and AX-PUB-REF-001.

This is a deterministic repository-integrity check, not a general-purpose JSON
Schema implementation and not a production conformance validator.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json"
VALID_EXAMPLE = ROOT / "reference-implementations" / "eav-contract-validator" / "examples" / "valid_bundle.json"
INVALID_EXAMPLE = ROOT / "reference-implementations" / "eav-contract-validator" / "examples" / "invalid_bundle.json"
VALIDATOR_PATH = ROOT / "reference-implementations" / "eav-contract-validator" / "validator.py"

EXPECTED_SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_SCHEMA_ID = "AX-PUB-SCHEMA-001"
EXPECTED_SCHEMA_VERSION = "1.0"

COLLECTIONS = {
    "evidence_records": ("evidence_record", {"evidence_id", "classification", "source_identity", "observed_at"}),
    "decision_records": ("decision_record", {"decision_id", "decision_question", "decision_owner", "evidence_refs", "decided_at"}),
    "authority_grants": ("authority_grant", {"authority_id", "decision_id", "principal", "permitted_action", "resource_scope", "status", "granted_at"}),
    "execution_records": ("execution_record", {"execution_id", "decision_id", "authority_id", "actor", "action", "resource", "started_at", "status"}),
    "verification_records": ("verification_record", {"verification_id", "execution_id", "verifier", "verdict", "verified_at"}),
    "verified_outcomes": ("verified_outcome", {"outcome_id", "verification_id", "outcome_state", "accepted_at"}),
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_validator_module():
    spec = importlib.util.spec_from_file_location("ax_eav_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        fail("unable to load reference validator module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check_schema_structure(schema: dict) -> None:
    if schema.get("$schema") != EXPECTED_SCHEMA_URI:
        fail("unexpected JSON Schema dialect")

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    expected_top_level = {"schema_id", "schema_version", "bundle_id", *COLLECTIONS.keys()}
    if not expected_top_level.issubset(required):
        fail(f"top-level required fields drifted: expected at least {sorted(expected_top_level)}")

    if properties.get("schema_id", {}).get("const") != EXPECTED_SCHEMA_ID:
        fail("schema_id const does not match AX-PUB-SCHEMA-001")
    if properties.get("schema_version", {}).get("const") != EXPECTED_SCHEMA_VERSION:
        fail("schema_version const does not match 1.0")

    defs = schema.get("$defs", {})
    for collection, (definition_name, expected_required) in COLLECTIONS.items():
        ref = properties.get(collection, {}).get("items", {}).get("$ref")
        if ref != f"#/$defs/{definition_name}":
            fail(f"{collection} does not reference {definition_name}")
        actual_required = set(defs.get(definition_name, {}).get("required", []))
        if actual_required != expected_required:
            fail(
                f"{definition_name} required fields drifted: "
                f"expected {sorted(expected_required)}, got {sorted(actual_required)}"
            )


def check_validator_enums(schema: dict, validator) -> None:
    defs = schema["$defs"]

    schema_evidence = set(defs["evidence_record"]["properties"]["classification"]["enum"])
    if schema_evidence != set(validator.SUPPORTED_EVIDENCE_CLASSIFICATIONS):
        fail("evidence classification enum drifted between schema and validator")

    authority_states = set(defs["authority_grant"]["properties"]["status"]["enum"])
    if authority_states != {"ACTIVE", "REVOKED", "EXPIRED"}:
        fail("authority status enum drifted")

    verification_verdicts = set(defs["verification_record"]["properties"]["verdict"]["enum"])
    if verification_verdicts != {"PASS", "FAIL", "INCONCLUSIVE", "NOT_PERFORMED"}:
        fail("verification verdict enum drifted")

    outcome_const = defs["verified_outcome"]["properties"]["outcome_state"].get("const")
    if outcome_const != "VERIFIED":
        fail("verified outcome state drifted")


def check_example_metadata(example: dict, path: Path) -> None:
    if example.get("schema_id") != EXPECTED_SCHEMA_ID:
        fail(f"{path.name} must declare schema_id={EXPECTED_SCHEMA_ID}")
    if example.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        fail(f"{path.name} must declare schema_version={EXPECTED_SCHEMA_VERSION}")
    bundle_id = example.get("bundle_id")
    if not isinstance(bundle_id, str) or not bundle_id:
        fail(f"{path.name} must declare a non-empty bundle_id")

    for collection in COLLECTIONS:
        if collection not in example or not isinstance(example[collection], list):
            fail(f"{path.name} must contain array collection {collection}")


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    valid_example = load_json(VALID_EXAMPLE)
    invalid_example = load_json(INVALID_EXAMPLE)
    validator = load_validator_module()

    check_schema_structure(schema)
    check_validator_enums(schema, validator)
    check_example_metadata(valid_example, VALID_EXAMPLE)
    check_example_metadata(invalid_example, INVALID_EXAMPLE)

    valid_findings = validator.validate_bundle(valid_example)
    if valid_findings:
        fail(f"conforming example failed reference validator: {valid_findings}")

    invalid_findings = validator.validate_bundle(invalid_example)
    if not invalid_findings:
        fail("intentionally invalid example unexpectedly passed reference validator")

    print("AX_EAV_SCHEMA_ALIGNMENT_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, json.JSONDecodeError) as exc:
        print(f"AX_EAV_SCHEMA_ALIGNMENT_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
