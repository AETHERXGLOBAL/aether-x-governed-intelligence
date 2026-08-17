# AETHER X Public Machine-Readable Schemas

`PUBLIC ENGINEERING MATERIAL · CONTROLLED DISCLOSURE`

This directory contains machine-readable structural contracts that accompany AETHER X public technical specifications.

## Current Schema

| ID | Schema | Related specification | Public state |
|---|---|---|---|
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | `AX-PUB-SPEC-002` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |

## Role of the Schema

`AX-PUB-SCHEMA-001` uses the JSON Schema Draft 2020-12 dialect to make selected Evidence, Decision, Authority, Execution, Verification, and Verified Outcome structures machine-readable.

The schema defines structural constraints such as:

- required fields;
- primitive and collection types;
- selected enumerated states;
- timestamp formats;
- non-empty identifiers;
- bounded reference-bundle metadata.

It intentionally allows additional properties so domain-specific or future reference fields can be added without falsely claiming that this public profile represents a complete production data model.

## Structural Validation vs. Semantic Validation

The machine-readable layer and the executable reference validator have different responsibilities:

```text
AX-PUB-SCHEMA-001
STRUCTURE / TYPES / ENUMS / REQUIRED FIELDS
        ↓
AX-PUB-REF-001
CROSS-RECORD REFERENCES / AUTHORITY SCOPE / TEMPORAL RELATIONSHIPS / VERIFIED-OUTCOME RULES
```

JSON Schema alone does not establish that an `authority_id` references a real grant in the same bundle, that an execution occurs inside the grant's scope, or that a verified outcome is backed by a `PASS` verification. Those relational invariants remain the responsibility of the reference validator.

## Claim Boundary

Publication of this schema does **not** establish or imply:

- adoption by any AETHER X product;
- a production API or SDK contract;
- a shared company-wide data model;
- technical integration between portfolio initiatives;
- production authorization enforcement;
- security certification;
- regulatory compliance;
- customer deployment.

`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`

`SCHEMA CONFORMANCE ≠ AUTHORIZATION`

`STRUCTURAL VALIDITY ≠ VERIFIED OUTCOME`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
