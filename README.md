<p align="center">
  <img src="https://raw.githubusercontent.com/AETHERXGLOBAL/.github/main/profile/assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

# AETHER X Governed Intelligence

**Public reference architecture, technical specifications, machine-readable contracts, non-production reference implementations and bounded conformance artifacts for governed intelligence systems by AETHER X GLOBAL.**

`PUBLIC ENGINEERING REPOSITORY · CONTROLLED DISCLOSURE`

AETHER X GLOBAL is **A Governed Intelligence Systems Company**. This repository makes selected engineering doctrine independently inspectable without exposing proprietary product implementation, private research, confidential architecture, credentials, customer information or unpublished intellectual property.

> **Institutional Intelligence. Governed Autonomy.**  
> **Build Intelligence That Can Be Trusted to Act.**

## Core Engineering Boundary

```text
GOVERNED KNOWLEDGE
        ↓
TRACEABLE EVIDENCE
        ↓
ANALYSIS / RECOMMENDATION
        ↓
EXPLICIT DECISION
        ↓
BOUNDED AUTHORITY
        ↓
CONTROLLED EXECUTION
        ↓
INDEPENDENT VERIFICATION
        ↓
VERIFIED OUTCOME
        ↓
AUDIT / INSTITUTIONAL LEARNING
```

`OUTPUT ≠ FACT`  
`RECOMMENDATION ≠ DECISION`  
`CAPABILITY ≠ AUTHORITY`  
`TOOL AVAILABILITY ≠ TOOL PERMISSION`  
`EXECUTION COMPLETE ≠ VERIFIED`  
`ARCHITECTURE ≠ IMPLEMENTATION`

## Developer Entry Point

Start with the **[Public Quickstart](./docs/QUICKSTART.md)**.

Current public governance records:

- **[Artifact Compatibility & Versioning Policy](./docs/COMPATIBILITY_AND_VERSIONING.md)** — `AX-PUB-POL-001 v1.3`
- **[Machine-Readable Artifact Manifest](./artifacts/AX-PUB-MANIFEST-001.json)** — `AX-PUB-MANIFEST-001 v1.3`
- **[Public Engineering Snapshot v1.0](./snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)** — immutable historical review state

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## Public Technical Series

| ID | Artifact | Public state |
|---|---|---|
| `AX-PUB-ARCH-001` | [Governed Intelligence Reference Architecture](./specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-002` | [Evidence, Authority & Verification Contract](./specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-003` | [Point-in-Time Knowledge & Provenance Standard](./specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-004` | [Governed Agent Authority & Tool-Use Boundary Standard](./specifications/AX-PUB-SPEC-004_GOVERNED_AGENT_AUTHORITY_TOOL_USE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-002` | [Point-in-Time Knowledge Envelope](./schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json) | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-003` | [Agent Tool-Use Authority Envelope](./schemas/AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json) | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-REF-001` | [EAV Contract Validator](./reference-implementations/eav-contract-validator/README.md) | `v1.0 · CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | [Point-in-Time Knowledge Validator](./reference-implementations/point-in-time-knowledge-validator/README.md) | `v1.0 · CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-003` | [Agent Tool-Use Authority Validator](./reference-implementations/agent-tool-authority-validator/README.md) | `v1.0 · CI WORKFLOW PUBLISHED · VALIDATION PENDING · NON-PRODUCTION` |
| `AX-PUB-TEST-001` | [Governed Intelligence Conformance Test Kit](./conformance/AX-PUB-TEST-001/README.md) | `v1.0 · REPRODUCIBLY VERIFIED · CI RUN UNVERIFIED · NON-PRODUCTION` |
| `AX-PUB-TEST-002` | [Agent Authority Conformance Test Kit](./conformance/AX-PUB-TEST-002/README.md) | `v1.0 · CI WORKFLOW PUBLISHED · VALIDATION PENDING · NON-PRODUCTION` |

## Specification-to-Execution Paths

### Evidence / Authority / Verification

```text
AX-PUB-SPEC-002
        ↓
AX-PUB-SCHEMA-001
        ↓
AX-PUB-REF-001
        ↓
AX-PUB-TEST-001
```

### Point-in-Time Knowledge / Provenance

```text
AX-PUB-SPEC-003
        ↓
AX-PUB-SCHEMA-002
        ↓
AX-PUB-REF-002
        ↓
AX-PUB-TEST-001
```

### Governed Agent Authority / Tool Use

```text
AX-PUB-SPEC-004
        ↓
AX-PUB-SCHEMA-003
        ↓
AX-PUB-REF-003
        ↓
AX-PUB-TEST-002
```

The third path defines selected public reference controls around **principal identity, action proposal, authority context, bounded tool-use grants, resource/parameter/time/environment scope, invocation records and tool-result state**.

It does **not** establish a production agent framework, shared authorization plane, credential broker, production tool registry, autonomous execution authority or implementation by any AETHER X initiative.

## Validation Evidence

`AX-PUB-REF-001` and `AX-PUB-REF-002` have prior public CI evidence for their defined reference checks.

`AX-PUB-TEST-001` has published reproducibility evidence for `15/15` declared synthetic cases and a passing public/private dependency-boundary check. Its GitHub Actions run status remains kept separate from that reproducibility evidence.

For the newly published agent-authority path, schema/reference/conformance workflows are present, but `AX-PUB-REF-003` and `AX-PUB-TEST-002` remain **`VALIDATION PENDING`** until execution against the published repository state is directly verified.

`WORKFLOW PUBLISHED ≠ CI RUN VERIFIED`

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`

`REFERENCE VALIDATOR PASS ≠ PRODUCTION AUTHORIZATION`

## Repository Structure

```text
.
├── specifications/
│   ├── AX-PUB-ARCH-001_...
│   ├── AX-PUB-SPEC-002_...
│   ├── AX-PUB-SPEC-003_...
│   └── AX-PUB-SPEC-004_...
├── schemas/
│   ├── AX-PUB-SCHEMA-001_...
│   ├── AX-PUB-SCHEMA-002_...
│   └── AX-PUB-SCHEMA-003_...
├── reference-implementations/
│   ├── eav-contract-validator/
│   ├── point-in-time-knowledge-validator/
│   └── agent-tool-authority-validator/
├── conformance/
│   ├── AX-PUB-TEST-001/
│   └── AX-PUB-TEST-002/
├── artifacts/
│   └── AX-PUB-MANIFEST-001.json
├── docs/
│   ├── QUICKSTART.md
│   └── COMPATIBILITY_AND_VERSIONING.md
├── snapshots/
├── tools/
├── .github/workflows/
└── SECURITY.md
```

## What This Repository Establishes

A public reviewer can inspect that AETHER X GLOBAL has intentionally published:

- a technology-neutral governed-intelligence reference architecture;
- explicit evidence, decision, authority, execution and verification semantics;
- point-in-time knowledge, provenance, lineage and revision-integrity rules;
- an agent/tool-use authority standard separating capability from permission;
- three machine-readable public structural contracts;
- three bounded non-production reference validators at their stated validation states;
- synthetic public conformance suites;
- machine-readable compatibility/version governance;
- a fixed historical reproducibility snapshot;
- public security and private-project separation boundaries.

These are evidence of **published engineering doctrine, control design, machine-readable contract design, conformance discipline and reproducibility discipline**.

## What This Repository Does Not Establish

Publication here does **not** establish or imply:

- full implementation inside any AETHER X product;
- a shared runtime, shared data platform, agent framework or authorization plane across initiatives;
- production readiness or customer deployment;
- a production API or SDK;
- autonomous authority for consequential actions;
- production financial-data completeness, correctness, latency or scale;
- security certification or regulatory approval;
- predictive, financial or investment performance;
- commercial or product release status.

`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`

`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`

`AGENT AUTHORITY SCHEMA ≠ PRODUCTION AUTHORIZATION PLANE`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

## Private-Project Boundary

This public repository is intentionally self-contained. Public examples and conformance vectors are generic or synthetic.

No private AETHER X project repository is a runtime, checkout, submodule or package dependency of the public reference validators or conformance kits. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside this repository's disclosure boundary.

See [SECURITY.md](./SECURITY.md).

## Organization

**AETHER X GLOBAL**  
[AETHERXGLOBAL on GitHub](https://github.com/AETHERXGLOBAL) · [Official Website](https://www.aetherxglobal.com)

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
