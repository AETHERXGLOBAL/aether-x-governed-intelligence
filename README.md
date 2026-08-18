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
DEV-GATE-03: CLOSED
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-04 — EXTERNAL EVALUATION READINESS
SDK CANDIDATE: ESTABLISHED
RELEASE CANDIDATE: VALIDATED / NON-PUBLISHED
PUBLIC SDK: NOT PUBLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

The program defines the governed path from inspectable public engineering toward a reproducible developer experience, a bounded SDK candidate, supply-chain evidence, external evaluation readiness and a later explicit SDK release decision.

**[AX-PUB-DEV-002 — Developer Contract Baseline](./docs/AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md)**  
`DEV-GATE-00 CLOSED · PUBLIC DEVELOPER CONTRACT BASELINE ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`

The baseline establishes the initial developer problem, canonical contract inventory, non-goals, semantic error taxonomy, compatibility rules, fail-closed behavior and public/private dependency boundary. Validation evidence is recorded in [`AX-PUB-CI-003`](./evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md).

**[AX-PUB-DEV-003 — Reproducible Developer Experience](./docs/AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md)**  
`DEV-GATE-01 CLOSED · VERIFIED REFERENCE RUNTIME MATRIX PYTHON 3.10–3.13 · SDK PUBLICATION NOT AUTHORIZED`

Gate-01 establishes a clean-checkout, standard-library-only public reference developer path with direct clean-environment CI evidence across Python 3.10, 3.11, 3.12 and 3.13. Closure evidence is recorded in [`AX-PUB-CI-004`](./evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md).

**[AX-PUB-DEV-004 — SDK Candidate Engineering Baseline](./docs/AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md)**  
`DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED · VERIFIED CANDIDATE RUNTIME MATRIX PYTHON 3.10–3.13 · SDK PUBLICATION NOT AUTHORIZED`

Gate-02 establishes a **bounded repository-local Python SDK candidate** over the three declared public contract paths. Direct validation evidence is recorded in [`AX-PUB-CI-005`](./evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md).

**[AX-PUB-DEV-005 — Supply-Chain & Release Candidate](./docs/AX-PUB-DEV-005_SUPPLY_CHAIN_RELEASE_CANDIDATE.md)**  
`DEV-GATE-03 CLOSED · RELEASE-CANDIDATE VALIDATED · SDK PUBLICATION NOT AUTHORIZED`

Gate-03 establishes a validated **non-published engineering release candidate** [`AX-PUB-RC-001 v0.1.0-rc1`](./release-candidate/AX-PUB-RC-001.json) over the bounded Gate-02 candidate. Direct evidence is recorded in [`AX-PUB-CI-006 v1.1`](./evidence/AX-PUB-CI-006_SUPPLY_CHAIN_RELEASE_CANDIDATE_VALIDATION.md).

Verified engineering-bundle identity:

```text
AX-PUB-RC-001.zip
SHA-256: 8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
SOURCE_DATE_EPOCH: 1787064230
```

The validated Gate-03 path includes byte-identical deterministic rebuilds, a build manifest, SPDX 2.3 SBOM, GitHub build-provenance and SBOM attestations, attestation verification, extracted-bundle unit/conformance execution and public/private supply-chain boundary checks.

The Gate-03 artifact remains a CI-only, non-published engineering object. It is not a public package, GitHub Release asset, supported SDK or approved distribution identity.

`RELEASE-CANDIDATE VALIDATED ≠ SUPPORTED SDK`  
`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SBOM ≠ SOFTWARE REUSE LICENCE`

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

The repository contains a bounded SDK candidate and a validated non-published engineering release candidate, not a supported or published SDK. The gate still requires explicit licensing/IP authority, interface compatibility, package/distribution identity, security and credential boundaries, documentation and maintenance/support commitments, and explicit release authority before SDK publication can be represented as approved.

`SDK CANDIDATE ≠ SUPPORTED SDK`  
`RELEASE-CANDIDATE VALIDATED ≠ SDK RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## Current Moving Public Governance

- **[AX-PUB-MANIFEST-001 v1.16](./artifacts/AX-PUB-MANIFEST-001.json)** — current machine-readable artifact state including closed DEV-GATE-00/01/02/03 and DEV-GATE-04 as the active engineering objective.
- **[AX-PUB-POL-001 v1.6](./docs/COMPATIBILITY_AND_VERSIONING.md)** — compatibility, snapshot, release and publication-readiness semantics.
- **[AX-PUB-CI-001](./evidence/AX-PUB-CI-001_AGENT_AUTHORITY_VNEXT_VALIDATION.md)** — verified agent-authority schema/reference/conformance CI evidence.
- **[AX-PUB-CI-002](./evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)** — verified vNext snapshot and manifest closure evidence.
- **[AX-PUB-CI-003](./evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md)** — DEV-GATE-00 validation evidence.
- **[AX-PUB-CI-004](./evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)** — DEV-GATE-01 clean-environment runtime-matrix evidence.
- **[AX-PUB-CI-005](./evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md)** — DEV-GATE-02 SDK-candidate validation evidence.
- **[AX-PUB-CI-006 v1.1](./evidence/AX-PUB-CI-006_SUPPLY_CHAIN_RELEASE_CANDIDATE_VALIDATION.md)** — DEV-GATE-03 deterministic-build, SBOM, provenance, attestation-verification, extracted-bundle and public-boundary evidence.
- **[AX-PUB-SNAP-002](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)** — current fixed vNext reproducibility snapshot.

## Public Technical Series

| ID | Artifact | Public state |
|---|---|---|
| `AX-PUB-ARCH-001` | [Governed Intelligence Reference Architecture](./specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-002` | [Evidence, Authority & Verification Contract](./specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-003` | [Point-in-Time Knowledge & Provenance Standard](./specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SPEC-004` | [Governed Agent Authority & Tool-Use Boundary Standard](./specifications/AX-PUB-SPEC-004_GOVERNED_AGENT_AUTHORITY_TOOL_USE_STANDARD.md) | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| `AX-PUB-SCHEMA-001` | Governed EAV Contract Schema | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-002` | Point-in-Time Knowledge Envelope | `JSON SCHEMA · CONCEPTUAL` |
| `AX-PUB-SCHEMA-003` | Agent Tool-Use Authority Envelope | `JSON SCHEMA · CI-VALIDATED · CONCEPTUAL` |
| `AX-PUB-REF-001` | EAV Contract Validator | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | Point-in-Time Knowledge Validator | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-003` | Agent Tool-Use Authority Validator | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-TEST-001` | Governed Intelligence Conformance Test Kit | `REPRODUCIBLY VERIFIED · CI RUN UNVERIFIED · NON-PRODUCTION` |
| `AX-PUB-TEST-002` | Agent Authority Conformance Test Kit | `CI-TESTED · NON-PRODUCTION` |
| `AX-PUB-GATE-001` | [Developer SDK Publication Readiness Gate](./docs/AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md) | `ACTIVE · SDK PUBLICATION NOT AUTHORIZED` |
| `AX-PUB-DEV-001` | Developer Adoption & SDK Readiness Program | `UNDER DEVELOPMENT · DEV-GATE-04 ACTIVE` |
| `AX-PUB-DEV-002` | Developer Contract Baseline | `DEV-GATE-00 CLOSED` |
| `AX-PUB-DEV-003` | Reproducible Developer Experience | `DEV-GATE-01 CLOSED · PYTHON 3.10–3.13` |
| `AX-PUB-DEV-004` | SDK Candidate Engineering Baseline | `DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED` |
| `AX-PUB-DEV-005` | Supply-Chain & Release Candidate | `DEV-GATE-03 CLOSED · RELEASE-CANDIDATE VALIDATED` |
| `AX-PUB-RC-001` | Non-published engineering release candidate | `VALIDATED · CI-ONLY · NON-PUBLISHED` |

## Three Public Evidence Paths

```text
AX-PUB-SPEC-002 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001 → AX-PUB-TEST-001
AX-PUB-SPEC-003 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002 → AX-PUB-TEST-001
AX-PUB-SPEC-004 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003 → AX-PUB-TEST-002
```

## Licensing & Reuse Boundary

No open-source licence or general reuse/distribution permission is granted by publication of this repository at this time.

Public availability is provided for inspection, technical review and reproducibility, and for use of GitHub platform functionality subject to applicable GitHub terms. Any broader reuse, redistribution, adaptation, sublicensing or commercial use requires separate authorization unless otherwise permitted by applicable law.

`PUBLIC VISIBILITY ≠ OPEN-SOURCE LICENCE`  
`SBOM ≠ SOFTWARE REUSE LICENCE`  
`CI ARTIFACT ≠ PUBLIC DISTRIBUTION`

## Private-Project Boundary

This repository is intentionally self-contained. Public examples and conformance vectors are generic or synthetic.

No private AETHER X project repository is a runtime, checkout, submodule, package or hidden service dependency of the public engineering path, including the validated Gate-03 engineering release candidate. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside this repository's disclosure boundary.

## What This Repository Does Not Establish

Publication here does **not** establish or imply product implementation, a shared company runtime or authorization plane, production readiness, customer deployment, a production API, a supported or published SDK, approved package identity, registry availability, a public reuse licence, autonomous authority, security certification, regulatory approval, external developer adoption or product integration.

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`RELEASE-CANDIDATE VALIDATED ≠ SDK RELEASE`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SDK PUBLICATION NOT AUTHORIZED`

See [SECURITY.md](./SECURITY.md).

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
