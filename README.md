<p align="center">
  <img src="https://raw.githubusercontent.com/AETHERXGLOBAL/.github/main/profile/assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

# AETHER X Governed Intelligence

**Public reference architecture, technical specifications, machine-readable contracts, non-production reference implementations and bounded conformance evidence for governed intelligence systems by AETHER X GLOBAL.**

`PUBLIC ENGINEERING REPOSITORY · CONTROLLED DISCLOSURE`

> **Institutional Intelligence. Governed Autonomy.**  
> **Build Intelligence That Can Be Trusted to Act.**

## Core Boundary

```text
GOVERNED KNOWLEDGE
→ TRACEABLE EVIDENCE
→ ANALYSIS / RECOMMENDATION
→ EXPLICIT DECISION
→ BOUNDED AUTHORITY
→ CONTROLLED EXECUTION
→ INDEPENDENT VERIFICATION
→ VERIFIED OUTCOME
→ AUDIT / INSTITUTIONAL LEARNING
```

`OUTPUT ≠ FACT` · `RECOMMENDATION ≠ DECISION` · `CAPABILITY ≠ AUTHORITY` · `TOOL AVAILABILITY ≠ TOOL PERMISSION` · `EXECUTION COMPLETE ≠ VERIFIED`

## Developer Entry Point

Start with the **[Public Quickstart](./docs/QUICKSTART.md)**.

### Formal Public Engineering Release

**`public-engineering-vnext-1.0` — AETHER X Governed Intelligence — Public Engineering vNext 1.0**

- Git tag target: `4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6`
- Release evidence: **[AX-PUB-REL-001](./evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)**
- Fixed technical-review snapshot: **[AX-PUB-SNAP-002](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)**

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

Current moving public governance:

- **[AX-PUB-MANIFEST-001 v1.6](./artifacts/AX-PUB-MANIFEST-001.json)** — current machine-readable artifact state including release registration.
- **[AX-PUB-POL-001 v1.5](./docs/COMPATIBILITY_AND_VERSIONING.md)** — compatibility, snapshot and formal public-engineering release semantics.
- **[AX-PUB-CI-001](./evidence/AX-PUB-CI-001_AGENT_AUTHORITY_VNEXT_VALIDATION.md)** — verified agent-authority schema/reference/conformance CI evidence.
- **[AX-PUB-CI-002](./evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)** — verified vNext snapshot and manifest closure evidence.
- **[AX-PUB-SNAP-002](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)** — current fixed `CI-VALIDATED` vNext reproducibility snapshot.
- **[AX-PUB-SNAP-001](./snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)** — historical reproducibility snapshot.

## Public Technical Series

| ID | Artifact | Public state |
|---|---|---|
| `AX-PUB-ARCH-001` | [Governed Intelligence Reference Architecture](./specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-002` | [Evidence, Authority & Verification Contract](./specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-003` | [Point-in-Time Knowledge & Provenance Standard](./specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-004` | [Governed Agent Authority & Tool-Use Boundary Standard](./specifications/AX-PUB-SPEC-004_GOVERNED_AGENT_AUTHORITY_TOOL_USE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-001` | [Governed EAV Contract Schema](./schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json) | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-002` | [Point-in-Time Knowledge Envelope](./schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json) | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-003` | [Agent Tool-Use Authority Envelope](./schemas/AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json) | `JSON SCHEMA · CI-VALIDATED · CONCEPTUAL` |
| `AX-PUB-REF-001` | [EAV Contract Validator](./reference-implementations/eav-contract-validator/README.md) | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | [Point-in-Time Knowledge Validator](./reference-implementations/point-in-time-knowledge-validator/README.md) | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-003` | [Agent Tool-Use Authority Validator](./reference-implementations/agent-tool-authority-validator/README.md) | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-TEST-001` | [Governed Intelligence Conformance Test Kit](./conformance/AX-PUB-TEST-001/README.md) | `REPRODUCIBLY VERIFIED · CI RUN UNVERIFIED · NON-PRODUCTION` |
| `AX-PUB-TEST-002` | [Agent Authority Conformance Test Kit](./conformance/AX-PUB-TEST-002/README.md) | `CI-TESTED · NON-PRODUCTION` |

## Three Public Evidence Paths

```text
AX-PUB-SPEC-002 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001 → AX-PUB-TEST-001
AX-PUB-SPEC-003 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002 → AX-PUB-TEST-001
AX-PUB-SPEC-004 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003 → AX-PUB-TEST-002
```

The third path has direct GitHub Actions evidence recorded by `AX-PUB-CI-001`. The vNext reproducibility state is independently validated and recorded by `AX-PUB-CI-002`.

```text
PUBLIC ENGINEERING vNext
        ↓
AX-PUB-SNAP-002
        ↓
COMMIT-ANCHORED
GIT-BLOB-INVENTORIED
MANIFEST-VALIDATED
SNAPSHOT-CI-VALIDATED
        ↓
public-engineering-vnext-1.0
FORMAL PUBLIC ENGINEERING RELEASE
```

`PUBLIC CI PASS ≠ PRODUCT IMPLEMENTATION`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION AUTHORIZATION`  
`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

## Private-Project Boundary

This repository is intentionally self-contained. Public examples and conformance vectors are generic or synthetic.

No private AETHER X project repository is a runtime, checkout, submodule or package dependency of the public schemas, validators or conformance kits. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside this repository's disclosure boundary.

## What This Repository Does Not Establish

Publication here does **not** establish or imply product implementation, a shared company runtime or authorization plane, production readiness, customer deployment, production API/SDK status, autonomous authority, security certification, regulatory approval, or predictive/investment performance.

`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`  
`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`  
`AGENT AUTHORITY SCHEMA ≠ PRODUCTION AUTHORIZATION PLANE`  
`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

See [SECURITY.md](./SECURITY.md).

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**

