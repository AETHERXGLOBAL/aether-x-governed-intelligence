# AETHER X Public Machine-Readable Schemas

`PUBLIC ENGINEERING MATERIAL · CONTROLLED DISCLOSURE`

This directory contains machine-readable structural contracts that accompany AETHER X public technical specifications.

## Current Schemas

| ID | Schema | Related specification | Public state |
|---|---|---|---|
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | `AX-PUB-SPEC-002` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-002` | [Point-in-Time Knowledge Envelope](./AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json) | `AX-PUB-SPEC-003` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-003` | [Agent Tool-Use Authority Envelope](./AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json) | `AX-PUB-SPEC-004` | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |

## Role of the Schemas

### AX-PUB-SCHEMA-001 — Governed EAV Contract

Makes selected Evidence, Decision, Authority, Execution, Verification, and Verified Outcome structures machine-readable.

Its companion [`AX-PUB-REF-001`](../reference-implementations/eav-contract-validator/README.md) handles relational semantics that structural validation alone cannot establish.

### AX-PUB-SCHEMA-002 — Point-in-Time Knowledge Envelope

Makes selected `AX-PUB-SPEC-003` structures machine-readable, including query context, source/provenance records, transformation lineage, knowledge assertions, revision state, explicit missing-data state, and point-in-time cutoffs.

Its companion [`AX-PUB-REF-002`](../reference-implementations/point-in-time-knowledge-validator/README.md) applies selected semantic checks including no-future-leakage, source/lineage references, supersession integrity, explicit missing states and reproducibility-cutoff consistency.

### AX-PUB-SCHEMA-003 — Agent Tool-Use Authority Envelope

Makes selected `AX-PUB-SPEC-004` structures machine-readable, including:

- `AgentIdentity`;
- `ToolDescriptor`;
- `ActionProposal`;
- `AuthorityContext`;
- `ToolUseGrant`;
- `ToolInvocationRecord`;
- `ToolResultRecord`;
- selected parameter, resource, environment, time and revocation fields.

Its companion [`AX-PUB-REF-003`](../reference-implementations/agent-tool-authority-validator/README.md) demonstrates selected relational authority semantics. `AX-PUB-REF-003` remains `VALIDATION PENDING` until published-run evidence is directly verified.

## Structural Validation vs. Semantic Validation

```text
AX-PUB-SCHEMA-001
STRUCTURE
        ↓
AX-PUB-REF-001
EAV RELATIONAL / AUTHORITY / VERIFICATION SEMANTICS

AX-PUB-SCHEMA-002
POINT-IN-TIME / PROVENANCE STRUCTURE
        ↓
AX-PUB-REF-002
TEMPORAL / LINEAGE / REVISION SEMANTICS

AX-PUB-SCHEMA-003
AGENT / TOOL / GRANT / INVOCATION STRUCTURE
        ↓
AX-PUB-REF-003
SELECTED PRINCIPAL / TOOL / ACTION / RESOURCE / PARAMETER AUTHORITY SEMANTICS
```

The published schemas use JSON Schema Draft 2020-12. They intentionally permit additional properties so domain-specific or future reference fields can be represented without claiming that these public schemas are complete production data models.

## Claim Boundary

Publication of these schemas and companion reference validators does **not** establish or imply:

- adoption by any AETHER X product;
- a production API or SDK contract;
- a shared company-wide data model, agent runtime or authorization plane;
- technical integration between portfolio initiatives;
- production authorization enforcement;
- autonomous authority for consequential actions;
- production-scale data-quality guarantees;
- security certification;
- regulatory compliance;
- customer deployment.

`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`

`AGENT AUTHORITY SCHEMA ≠ PRODUCTION AUTHORIZATION PLANE`

`SCHEMA CONFORMANCE ≠ AUTHORIZATION`

`STRUCTURAL VALIDITY ≠ VERIFIED OUTCOME`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
