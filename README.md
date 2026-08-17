<p align="center">
  <img src="https://raw.githubusercontent.com/AETHERXGLOBAL/.github/main/profile/assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

# AETHER X Governed Intelligence

**Public reference architecture, technical specifications, machine-readable contracts, and non-production reference implementations for governed intelligence systems by AETHER X GLOBAL.**

`PUBLIC ENGINEERING REPOSITORY · CONTROLLED DISCLOSURE`

AETHER X GLOBAL is **A Governed Intelligence Systems Company**. This repository makes selected parts of the company's engineering doctrine independently inspectable without exposing proprietary product implementation, private research, confidential architecture, credentials, customer information, or unpublished intellectual property.

> **Institutional Intelligence. Governed Autonomy.**  
> **Build Intelligence That Can Be Trusted to Act.**

---

## Public Engineering Chain

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

The core distinction is deliberate:

`OUTPUT ≠ FACT`  
`RECOMMENDATION ≠ DECISION`  
`CAPABILITY ≠ AUTHORITY`  
`EXECUTION COMPLETE ≠ VERIFIED`  
`CURRENT TRUTH ≠ HISTORICAL TRUTH`  
`ARCHITECTURE ≠ IMPLEMENTATION`

---

## Developer Entry Point

New to the repository? Start with the **[Public Quickstart](./docs/QUICKSTART.md)**.

For compatibility and reproducibility:

- **[Artifact Compatibility & Versioning Policy](./docs/COMPATIBILITY_AND_VERSIONING.md)** — `AX-PUB-POL-001 v1.0`
- **[Machine-Readable Public Artifact Manifest](./artifacts/AX-PUB-MANIFEST-001.json)** — `AX-PUB-MANIFEST-001 v1.0`
- **[Public Engineering Snapshot v1.0](./snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)** — `AX-PUB-SNAP-001 v1.0`
- **[Machine-Readable Snapshot Record](./snapshots/AX-PUB-SNAP-001.json)** — anchored to commit `f839d4ac0a0b69dcbb682e900f02aad7e24524eb`
- **Public manifest CI** validates declared artifact paths, versions, schema identity and compatibility relationships.
- **Public snapshot CI** validates the immutable snapshot anchor and recorded Git blob inventory.

For reproducible external review, use the validated snapshot or pin an explicit Git commit SHA. The `main` branch represents the current public engineering state and may advance.

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

---

## Public Technical Series

| ID | Artifact | Type | Public state |
|---|---|---|---|
| `AX-PUB-ARCH-001` | [Governed Intelligence Reference Architecture](./specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md) | Reference Architecture | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-002` | [Evidence, Authority & Verification Contract](./specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md) | Control Specification | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-003` | [Point-in-Time Knowledge & Provenance Standard](./specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md) | Data / Knowledge Integrity Specification | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | Machine-Readable Control Contract | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-002` | [Point-in-Time Knowledge Envelope](./schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json) | Machine-Readable Temporal / Provenance Contract | `JSON SCHEMA · CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-REF-001` | [EAV Contract Validator](./reference-implementations/eav-contract-validator/README.md) | Executable Reference Implementation | `v1.0 · CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | [Point-in-Time Knowledge Validator](./reference-implementations/point-in-time-knowledge-validator/README.md) | Executable Temporal / Provenance Reference Implementation | `v1.0 · CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-POL-001` | [Artifact Compatibility & Versioning Policy](./docs/COMPATIBILITY_AND_VERSIONING.md) | Public Engineering Policy | `v1.0 · ACTIVE FOR THIS REPOSITORY` |

### Specification-to-Execution Evidence Paths

```text
AX-PUB-ARCH-001
REFERENCE ARCHITECTURE
        ↓
AX-PUB-SPEC-002
EVIDENCE / AUTHORITY / VERIFICATION SPECIFICATION
        ↓
AX-PUB-SCHEMA-001
MACHINE-READABLE STRUCTURAL CONTRACT
        ↓
AX-PUB-REF-001
EXECUTABLE RELATIONAL / SEMANTIC CHECKS
        ↓
PUBLIC CI
```

```text
AX-PUB-SPEC-003
POINT-IN-TIME KNOWLEDGE / PROVENANCE SPECIFICATION
        ↓
AX-PUB-SCHEMA-002
MACHINE-READABLE TEMPORAL / PROVENANCE ENVELOPE
        ↓
AX-PUB-REF-002
NO-FUTURE-LEAKAGE / LINEAGE / REVISION SEMANTICS
        ↓
PUBLIC CI
```

The JSON Schemas and reference validators deliberately have different responsibilities. Schemas define structure, types, required fields, selected enums, timestamp fields and reference-envelope metadata. Executable validators apply selected relational semantics that structural validation alone cannot establish.

### Reproducibility Snapshot

`AX-PUB-SNAP-001` records **Governed Intelligence Public v1.0** against the immutable Git anchor:

```text
f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

The machine-readable snapshot records the public artifact inventory, Git blob identities and selected CI evidence. Snapshot integrity is independently checked by a public workflow using full Git history.

This snapshot is not a GitHub Release, Git tag or product release.

---

## Repository Structure

```text
.
├── docs/
│   ├── QUICKSTART.md
│   └── COMPATIBILITY_AND_VERSIONING.md
├── artifacts/
│   └── AX-PUB-MANIFEST-001.json
├── snapshots/
│   ├── README.md
│   ├── AX-PUB-SNAP-001.json
│   └── AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md
├── specifications/
│   ├── AX-PUB-ARCH-001_...
│   ├── AX-PUB-SPEC-002_...
│   └── AX-PUB-SPEC-003_...
├── schemas/
│   ├── README.md
│   ├── AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json
│   ├── AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json
│   └── examples/
│       └── AX-PUB-SCHEMA-002_example.json
├── reference-implementations/
│   ├── README.md
│   ├── eav-contract-validator/
│   │   ├── validator.py
│   │   ├── examples/
│   │   └── tests/
│   └── point-in-time-knowledge-validator/
│       ├── validator.py
│       ├── examples/
│       └── tests/
├── tools/
│   ├── check_eav_schema_alignment.py
│   ├── check_ptk_schema_alignment.py
│   ├── check_artifact_manifest.py
│   └── check_public_snapshot.py
├── .github/workflows/
│   ├── validate-eav-reference.yml
│   ├── validate-eav-schema.yml
│   ├── validate-ptk-schema.yml
│   ├── validate-ptk-reference.yml
│   ├── validate-public-artifact-manifest.yml
│   └── validate-public-snapshot.yml
└── SECURITY.md
```

---

## What This Repository Establishes

A public reviewer can inspect that AETHER X GLOBAL has published:

- a technology-neutral governed-intelligence reference architecture;
- explicit evidence, decision, authority, execution and verification semantics;
- point-in-time knowledge, provenance and revision-integrity rules;
- machine-readable JSON Schema profiles for selected EAV and point-in-time knowledge / provenance structures;
- an executable EAV reference validator implementing selected cross-record control invariants;
- an executable point-in-time knowledge validator implementing selected no-future-leakage, lineage, revision and missing-state invariants;
- an explicit public artifact compatibility and versioning policy;
- a machine-readable manifest that declares the current public artifact/version relationships;
- a validated public reproducibility snapshot anchored to an immutable Git commit and recorded Git blob identities;
- public automated checks for schema alignment, both bounded reference implementations, artifact-manifest integrity and snapshot integrity.

These artifacts are evidence of **published engineering doctrine, reference control design, machine-readable contract design, versioned public-artifact governance, reproducibility discipline and inspectable reference engineering**.

## What This Repository Does Not Establish

Publication here does **not** establish or imply:

- full implementation inside any AETHER X product;
- completion or production readiness of AETHER Intelligence Core (AIC);
- a production API, SDK, or company-wide data model;
- stable product API or SDK compatibility;
- a shared runtime or shared data platform across company initiatives;
- technical integration between AETHER X Quantum, AX-OS, AIC, or AETHER X Research;
- production readiness;
- customer deployment;
- ownership or availability of any particular financial-data source;
- production-scale data completeness, correctness, timeliness or latency guarantees;
- regulatory approval or security certification;
- production-scale global financial-data infrastructure;
- predictive, financial, or investment performance;
- autonomous authority for consequential actions;
- commercial or product release status merely because a public engineering snapshot exists.

`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`

`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

`REFERENCE TEMPORAL VALIDATION ≠ PRODUCTION DATA QUALITY`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

---

## Portfolio Boundary

AETHER X initiatives may adopt all, some, or none of these reference patterns according to their domain, maturity, risk, and explicit implementation decisions.

Shared engineering doctrine must not be interpreted as shared runtime, deployment dependency, interoperability, or integration. Those claims require separate implementation evidence and authority.

---

## Security & Intellectual Property

This repository is intentionally bounded for public disclosure. Do not publish credentials, customer information, private research, confidential architecture, unresolved exploit details, proprietary implementation, or restricted data here.

See [SECURITY.md](./SECURITY.md) for the public reporting boundary.

---

## Organization

**AETHER X GLOBAL**  
[AETHERXGLOBAL on GitHub](https://github.com/AETHERXGLOBAL) · [Official Website](https://www.aetherxglobal.com)

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**