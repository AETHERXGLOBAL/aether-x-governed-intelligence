# EAV Contract Validator — Public Reference Implementation

**Artifact ID:** `AX-PUB-REF-001`  
**Status:** `PUBLIC REFERENCE IMPLEMENTATION · CI-TESTED · EDUCATIONAL / NON-PRODUCTION`  
**Related Specification:** [`AX-PUB-SPEC-002 — Evidence, Authority & Verification Contract`](../../specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md)  
**Related Machine-Readable Contract:** [`AX-PUB-SCHEMA-001 — Governed EAV Contract Schema`](../../schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json)  
**Organization:** AETHER X GLOBAL

## Purpose

This bounded reference implementation demonstrates how selected invariants from `AX-PUB-SPEC-002` can be represented as deterministic validation rules.

It validates a JSON bundle containing:

```text
Evidence Records
→ Decision Records
→ Authority Grants
→ Execution Records
→ Verification Records
→ Verified Outcome Records
```

The implementation is dependency-free and intentionally favors semantic clarity over framework complexity.

## Schema vs. Validator

`AX-PUB-SCHEMA-001` and this validator are complementary, not interchangeable:

```text
JSON SCHEMA
structure · types · required fields · selected enums · timestamp formats
        ↓
REFERENCE VALIDATOR
cross-record references · authority scope · time windows · verifier independence · verified-outcome semantics
```

Structural conformance does not establish authorization or a verified outcome.

## What It Checks

The validator checks selected reference conditions including:

- unique control-object identifiers;
- required evidence metadata and supported classification states;
- decisions reference existing evidence;
- authority grants reference existing decisions;
- authority state is explicit;
- authority expiry follows grant time;
- execution references an existing decision and authority grant;
- execution requires `ACTIVE` authority;
- execution actor matches the granted principal;
- execution action matches the permitted action;
- execution resource remains inside granted scope;
- execution occurs within the grant time window;
- verification references an execution;
- independent-verification requirements are enforced when requested;
- only a `PASS` verification may produce a `VERIFIED` outcome.

## Public Claim Boundary

This artifact is **not** a production authorization system, security control plane, policy engine, identity system, transaction system or product SDK.

It does **not** establish or imply:

- implementation inside AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- production readiness;
- secure authorization enforcement;
- cryptographic integrity;
- distributed-consistency guarantees;
- regulatory compliance;
- customer deployment;
- technical integration between AETHER X initiatives.

`REFERENCE IMPLEMENTATION ≠ PRODUCT IMPLEMENTATION`

`VALIDATOR PASS ≠ SECURITY APPROVAL`

`EXECUTION COMPLETE ≠ VERIFIED`

## Requirements

Python 3.10+ is recommended. The implementation uses only the Python standard library.

## Run

Validate the conforming example:

```bash
python3 validator.py examples/valid_bundle.json
```

Expected output:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

Validate the intentionally invalid example:

```bash
python3 validator.py examples/invalid_bundle.json
```

The command exits with status `1` and prints the detected contract violations.

For structured output:

```bash
python3 validator.py examples/invalid_bundle.json --json
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The reference workflow compiles the validator, runs unit tests, validates the conforming example and confirms that the intentionally invalid example is rejected.

A separate schema workflow parses `AX-PUB-SCHEMA-001`, verifies schema / validator / example alignment, and fails closed on reference-contract drift.

## Design Intent

This is deliberately **not an SDK**. The purpose is to make selected governance concepts inspectable in executable code before any developer-facing package is considered mature enough for public release.

## Related Public Material

- [Repository overview](../../README.md)
- [AX-PUB-ARCH-001](../../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md)
- [AX-PUB-SPEC-002](../../specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md)
- [AX-PUB-SPEC-003](../../specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)
- [AX-PUB-SCHEMA-001](../../schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json)
- [Schema index](../../schemas/README.md)

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
