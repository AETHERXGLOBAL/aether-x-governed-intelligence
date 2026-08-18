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

### Developer Adoption & SDK Readiness Program

**[AX-PUB-DEV-001 — Developer Adoption & SDK Readiness Program](./docs/AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md)**

Current program state:

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-03 — SUPPLY-CHAIN & RELEASE CANDIDATE
SDK CANDIDATE: ESTABLISHED
PUBLIC SDK: NOT PUBLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

The program defines the governed path from inspectable public engineering toward a reproducible developer experience, a bounded SDK candidate, supply-chain evidence, external evaluation readiness and a later explicit SDK release decision.

**[AX-PUB-DEV-002 — Developer Contract Baseline](./docs/AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md)**  
`DEV-GATE-00 CLOSED · PUBLIC DEVELOPER CONTRACT BASELINE ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`

The baseline establishes the initial developer problem, canonical contract inventory, non-goals, semantic error taxonomy, compatibility rules, fail-closed behavior and public/private dependency boundary. Its machine-readable companion is [`artifacts/AX-PUB-DEV-002.json`](./artifacts/AX-PUB-DEV-002.json), with validation evidence recorded in [`AX-PUB-CI-003`](./evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md).

**[AX-PUB-DEV-003 — Reproducible Developer Experience](./docs/AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md)**  
`DEV-GATE-01 CLOSED · VERIFIED REFERENCE RUNTIME MATRIX PYTHON 3.10–3.13 · SDK PUBLICATION NOT AUTHORIZED`

Gate-01 establishes a clean-checkout, standard-library-only public reference developer path with deterministic valid/fail behavior, two public conformance suites, a separate public-only boundary control and direct clean-environment CI evidence across Python 3.10, 3.11, 3.12 and 3.13. Closure evidence is recorded in [`AX-PUB-CI-004`](./evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md).

**[AX-PUB-DEV-004 — SDK Candidate Engineering Baseline](./docs/AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md)**  
`DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED · VERIFIED CANDIDATE RUNTIME MATRIX PYTHON 3.10–3.13 · SDK PUBLICATION NOT AUTHORIZED`

Gate-02 establishes a **bounded repository-local Python SDK candidate** over the three declared public contract paths. It provides explicit result abstractions, deterministic `AXDEV-*` candidate error mapping, unit tests, candidate conformance and a public/private boundary check. Direct validation evidence is recorded in [`AX-PUB-CI-005`](./evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md).

The candidate remains non-distributable: there is no approved package identity, package registry, public SDK licence or support commitment.

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SDK RELEASE`  
`VERIFIED CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`

### Formal Public Engineering Release

**`public-engineering-vnext-1.0` — AETHER X Governed Intelligence — Public Engineering vNext 1.0**

- Git tag target: `4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6`
- Release evidence: **[AX-PUB-REL-001](./evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)**
- Fixed technical-review snapshot: **[AX-PUB-SNAP-002](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)**

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

### Developer SDK Publication Readiness

**[AX-PUB-GATE-001 — Developer SDK Publication Readiness Gate](./docs/AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)**

Current public disposition:

```text
SDK PUBLICATION NOT AUTHORIZED
```

The repository now contains a bounded SDK candidate, not a supported or published SDK. The gate still requires explicit licensing/IP authority, interface compatibility, package/distribution identity, security and credential boundaries, failure semantics, SDK-specific conformance, supply-chain controls, documentation and maintenance/support commitments before SDK publication can be represented as approved.

`SDK CANDIDATE ≠ SUPPORTED SDK`  
`PUBLIC ENGINEERING RELEASE ≠ SDK RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## Current Moving Public Governance

- **[AX-PUB-MANIFEST-001 v1.14](./artifacts/AX-PUB-MANIFEST-001.json)** — current machine-readable artifact state including closed DEV-GATE-00, DEV-GATE-01 and DEV-GATE-02 registration.
- **[AX-PUB-POL-001 v1.6](./docs/COMPATIBILITY_AND_VERSIONING.md)** — compatibility, snapshot, release and publication-readiness semantics.
- **[AX-PUB-CI-001](./evidence/AX-PUB-CI-001_AGENT_AUTHORITY_VNEXT_VALIDATION.md)** — verified agent-authority schema/reference/conformance CI evidence.
- **[AX-PUB-CI-002](./evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)** — verified vNext snapshot and manifest closure evidence.
- **[AX-PUB-CI-003](./evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md)** — verified DEV-GATE-00 validation evidence.
- **[AX-PUB-CI-004](./evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)** — verified DEV-GATE-01 clean-environment runtime-matrix evidence across Python 3.10–3.13.
- **[AX-PUB-CI-005](./evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md)** — verified DEV-GATE-02 candidate unit/conformance/boundary/runtime-matrix evidence across Python 3.10–3.13.
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
| `AX-PUB-GATE-001` | [Developer SDK Publication Readiness Gate](./docs/AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md) | `ACTIVE · SDK PUBLICATION NOT AUTHORIZED` |
| `AX-PUB-DEV-001` | [Developer Adoption & SDK Readiness Program](./docs/AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md) | `UNDER DEVELOPMENT · DEV-GATE-00/01/02 CLOSED · DEV-GATE-03 ACTIVE` |
| `AX-PUB-DEV-002` | [Developer Contract Baseline](./docs/AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md) | `DEV-GATE-00 CLOSED · PUBLIC DEVELOPER CONTRACT BASELINE ESTABLISHED` |
| `AX-PUB-DEV-003` | [Reproducible Developer Experience](./docs/AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md) | `DEV-GATE-01 CLOSED · VERIFIED RUNTIME MATRIX PYTHON 3.10–3.13` |
| `AX-PUB-DEV-004` | [SDK Candidate Engineering Baseline](./docs/AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md) | `DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED · VERIFIED CANDIDATE MATRIX PYTHON 3.10–3.13` |

## Three Public Evidence Paths

```text
AX-PUB-SPEC-002 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001 → AX-PUB-TEST-001
AX-PUB-SPEC-003 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002 → AX-PUB-TEST-001
AX-PUB-SPEC-004 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003 → AX-PUB-TEST-002
```

The third path has direct GitHub Actions evidence recorded by `AX-PUB-CI-001`. The vNext reproducibility state is independently validated and recorded by `AX-PUB-CI-002`. The developer contract baseline evidence is recorded by `AX-PUB-CI-003`. The clean-environment developer-experience runtime matrix is recorded by `AX-PUB-CI-004`. The bounded repository-local SDK candidate validation is recorded by `AX-PUB-CI-005`.

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

## Licensing & Reuse Boundary

No open-source licence or general reuse/distribution permission is granted by publication of this repository at this time.

Public availability is provided for inspection, technical review and reproducibility, and for use of GitHub platform functionality subject to applicable GitHub terms. Any broader reuse, redistribution, adaptation, sublicensing or commercial use requires separate authorization unless otherwise permitted by applicable law.

A future open-source, SDK or other reuse licence may be considered only through an explicit AETHER X publication and IP decision. Repository visibility, a Git tag, a GitHub Release, successful CI, reference implementation availability, conformance evidence or SDK-candidate status does not create such permission by implication.

`PUBLIC VISIBILITY ≠ OPEN-SOURCE LICENCE`  
`PUBLIC ENGINEERING RELEASE ≠ REUSE AUTHORIZATION`  
`SDK CANDIDATE ≠ LICENSED SDK`

## Private-Project Boundary

This repository is intentionally self-contained. Public examples and conformance vectors are generic or synthetic.

No private AETHER X project repository is a runtime, checkout, submodule, package or hidden service dependency of the public schemas, validators, conformance kits, readiness gate, developer-adoption program, developer-contract baseline, Gate-01 developer experience or Gate-02 repository-local SDK candidate. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside this repository's disclosure boundary.

## What This Repository Does Not Establish

Publication here does **not** establish or imply product implementation, a shared company runtime or authorization plane, production readiness, customer deployment, a production API, a supported or published SDK, approved package identity, registry availability, a public reuse licence, autonomous authority, security certification, regulatory approval, predictive/investment performance, external developer adoption or product integration.

`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`  
`MACHINE-READABLE SCHEMA ≠ PRODUCT DATA MODEL`  
`AGENT AUTHORITY SCHEMA ≠ PRODUCTION AUTHORIZATION PLANE`  
`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SDK RELEASE`  
`VERIFIED CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`  
`PUBLIC VISIBILITY ≠ OPEN-SOURCE LICENCE`

See [SECURITY.md](./SECURITY.md).

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
