#!/usr/bin/env python3
"""Check AX-PUB-SCHEMA-003 alignment with its public reference validator/examples."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json"
VALID = ROOT / "reference-implementations" / "agent-tool-authority-validator" / "examples" / "valid_envelope.json"
INVALID = ROOT / "reference-implementations" / "agent-tool-authority-validator" / "examples" / "invalid_envelope.json"
VALIDATOR = ROOT / "reference-implementations" / "agent-tool-authority-validator" / "validator.py"
REQUIRED_TOP_LEVEL = {"schema_id","schema_version","envelope_id","agent_identities","tool_descriptors","action_proposals","authority_contexts","tool_use_grants","tool_invocations","tool_results"}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    findings: list[str] = []
    for path in (SCHEMA, VALID, INVALID, VALIDATOR):
        if not path.is_file(): findings.append(f"missing: {path.relative_to(ROOT)}")
    if findings:
        for x in findings: print(f"AX_AGENT_SCHEMA_ALIGN_FAIL: {x}")
        return 1
    schema, valid, invalid = load(SCHEMA), load(VALID), load(INVALID)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema": findings.append("schema must declare JSON Schema Draft 2020-12")
    if schema.get("$id") != "urn:aetherx:public-schema:AX-PUB-SCHEMA-003:1.0": findings.append("schema $id mismatch")
    props = schema.get("properties", {})
    if props.get("schema_id", {}).get("const") != "AX-PUB-SCHEMA-003": findings.append("schema_id const mismatch")
    if props.get("schema_version", {}).get("const") != "1.0": findings.append("schema_version const mismatch")
    if set(schema.get("required", [])) != REQUIRED_TOP_LEVEL: findings.append("top-level required fields drifted from reference contract")
    for label, example in (("valid", valid), ("invalid", invalid)):
        if example.get("schema_id") != "AX-PUB-SCHEMA-003" or example.get("schema_version") != "1.0": findings.append(f"{label} example schema identity mismatch")
        missing = REQUIRED_TOP_LEVEL - set(example)
        if missing: findings.append(f"{label} example missing top-level fields: {sorted(missing)}")
    validator_text = VALIDATOR.read_text(encoding="utf-8")
    for required in ('EXPECTED_SCHEMA_ID = "AX-PUB-SCHEMA-003"','EXPECTED_SCHEMA_VERSION = "1.0"',"AX-AGT-INVOKE-AUTHORITY-INACTIVE","AX-AGT-INVOKE-RESOURCE","AX-AGT-PARAM-ALLOWED-VALUES"):
        if required not in validator_text: findings.append(f"validator alignment marker missing: {required}")
    if findings:
        for x in findings: print(f"AX_AGENT_SCHEMA_ALIGN_FAIL: {x}")
        return 1
    print("AX_AGENT_AUTHORITY_SCHEMA_ALIGNMENT_PASS")
    return 0

if __name__ == "__main__": raise SystemExit(main())
