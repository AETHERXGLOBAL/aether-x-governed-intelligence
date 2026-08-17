# AETHER X Public Machine-Readable Schemas

`PUBLIC ENGINEERING MATERIAL · CONTROLLED DISCLOSURE`

This directory contains machine-readable structural contracts that accompany AETHER X public technical specifications.

## Current Schemas

| ID | Schema | Related specification | Public state |
|---|---|---|---|
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | `AX-PUB-SPEC-002` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-002` | [Point-in-Time Knowledge Envelope](./AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json) | `AX-PUB-SPEC-003` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |

A public reference envelope for `AX-PUB-SCHEMA-002` is available at [schemas/examples/AX-PUB-SCHEMA-002_example.json](./examples/AX-PUB-SCHEMA-002_example.json).

## Role of the Schemas

### AX-PUB-SCHEMA-001 — Governed EAV Contract

Makes selected Evidence, Decision, Authority, Execution, Verification, and Verified Outcome structures machine-readable.

Its companion [`AX-PUB-REF-001`](../reference-implementations/eav-contract-validator/README.md) handles relational semantics that structural validation alone cannot establish.

### AX-PUB-SCHEMA-002 — Point-in-Time Knowledge Envelope

Makes selected `AX-PUB-SPEC-003` structures machine-readable, including:

- `QueryContext`;
- `SourceRecord`;
- `TransformationRecord`;
- `KnowledgeAssertion`;
- reproducibility-package metadata;
- observation, publication, effective, validity, and cutoff time dimensions;
- revision, freshness, and explicit missing-data states.

Its companion [`AX-PUB-REF-002`](../reference-implementations/point-in-time-knowledge-validator/README.md) applies selected semantic checks including no-future-leakage, source/lineage references, supersession integrity, explicit missing states and reproducibility-cutoff consistency.

## Structural Validation vs. Semantic Validation

```text
AX-PUB-SCHEMA-001
STRUCTURE / TYPES / ENUMS / REQUIRED FIELDS
        ↓
AX-PUB-REF-001
CROSS-RECORD REFERENCES / AUTHORITY SCOPE / TEMPORAL RELATIONSHIPS / VERIFIED-OUTCOME RULES

AX-PUB-SCHEMA-002
POINT-IN-TIME STRUCTURE / TEMPORAL FIELDS / PROVENANCE ENVELOPE
        ↓
AX-PUB-REF-002
NO-FUTURE-LEAKAGE / CROSS-RECORD TEMPORAL & LINEAGE INVARIANTS
```

Both schemas use the JSON Schema Draft 2020-12 dialect. They intentionally permit additional properties so domain-specific or future reference fields can be represented without claiming that these public schemas are complete production data models.

## Claim Boundary

Publication of these schemas and companion reference validators does **not** establish or imply:

- adoption by any AETHER X product;
- completion or production readiness of AETHER Intelligence Core (AIC);
- a production API or SDK contract;
- a shared company-wide data model;
- technical integration between portfolio initiatives;
- production authorization enforcement;
- ownership or availability of any particular financial-data source;
- production-scale data-quality guarantees;
- security certification;
- regulatory compliance;
- customer deployment.

`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`

`SCHEMA CONFORMANCE ≠ AUTHORIZATION`

`REFERENCE TEMPORAL VALIDATION ≠ PRODUCTION DATA QUALITY`

`STRUCTURAL VALIDITY ≠ VERIFIED OUTCOME`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
