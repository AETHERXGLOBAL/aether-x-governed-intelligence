<p align="center">
  <img src="https://raw.githubusercontent.com/AETHERXGLOBAL/.github/main/profile/assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

# AETHER X Governed Intelligence

**Public reference architecture, technical specifications, machine-readable contracts, bounded reference implementations and reproducible engineering evidence for governed intelligence systems by AETHER X GLOBAL.**

`PUBLIC ENGINEERING REPOSITORY · CONTROLLED DISCLOSURE`

> **Institutional Intelligence. Governed Autonomy.**  
> **Build Intelligence That Can Be Trusted to Act.**

---

## What This Repository Represents

AETHER X GLOBAL engineers the system layer around advanced intelligence: **evidence, knowledge state, authority, controlled execution, verification and institutional accountability**.

This repository is the bounded public engineering surface for that doctrine. It is intentionally designed to be inspectable by engineers, partners, researchers and technical diligence teams without implying that private AETHER X products share a single production runtime or that every published concept is implemented in a commercial system.

```text
KNOWLEDGE / EVIDENCE
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

`OUTPUT ≠ FACT` · `RECOMMENDATION ≠ DECISION` · `CAPABILITY ≠ AUTHORITY` · `TOOL AVAILABILITY ≠ TOOL PERMISSION` · `EXECUTION COMPLETE ≠ VERIFIED`

---

## Current Public Engineering State

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT

DEV-GATE-00  CLOSED   Developer Contract Baseline
DEV-GATE-01  CLOSED   Reproducible Developer Experience
DEV-GATE-02  CLOSED   SDK Candidate
DEV-GATE-03  CLOSED   Supply-Chain & Release Candidate
DEV-GATE-04  CLOSED   External Evaluation Readiness

DEV-GATE-05  ACTIVE   SDK Release Decision
  05A        CLOSED   Release Decision Baseline
  05B        CLOSED   Installable Package Candidate
  05C        ACTIVE   Distribution & External Validation
  05D        NOT AUTHORIZED   Final Release Authority
```

Current maturity boundary:

| Area | Current public state |
|---|---|
| Public reference architecture | `ESTABLISHED / CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Machine-readable public contracts | `ESTABLISHED` |
| Public reference validators | `CI-TESTED / NON-PRODUCTION` |
| Reproducible developer experience | `ESTABLISHED` |
| SDK candidate | `ESTABLISHED` |
| Installable wheel/sdist candidate | `ESTABLISHED / DETERMINISTIC` |
| Local index distribution validation | `VERIFIED / LOCAL ONLY` |
| External registry validation | `NOT ESTABLISHED / NOT AUTHORIZED` |
| Human external evaluation | `NOT ESTABLISHED` |
| External adoption | `NOT ESTABLISHED` |
| Registry ownership | `NOT ESTABLISHED` |
| Public SDK licence | `NOT GRANTED` |
| Supported SDK | `NOT ESTABLISHED` |
| SDK publication | `NOT AUTHORIZED` |

`LOCAL INDEX PASS ≠ TESTPYPI PASS`  
`HUMAN EVALUATION ≠ CI`  
`SDK CANDIDATE ≠ SUPPORTED SDK`

---

## Engineering Doctrine

AETHER X public engineering follows a small set of non-negotiable control principles:

1. **Evidence before confidence** — consequential claims remain traceable to evidence, provenance, assumptions and time.
2. **Authority before action** — technical capability does not imply permission to act.
3. **Fail closed at consequential boundaries** — ambiguity must not silently become authorization.
4. **Verification before acceptance** — successful execution is not equivalent to a verified outcome.
5. **Point-in-time integrity** — historical decisions must be reconstructable using the knowledge state available at the relevant time.
6. **Deterministic controls around probabilistic intelligence** — model output may inform a decision, but enforcement boundaries should be machine-verifiable where practical.
7. **Reproducibility over presentation** — engineering claims should be tied to code, contracts, hashes, CI or explicit bounded evidence.
8. **Research, design, implementation and production are different states** — they are not collapsed into one maturity claim.

---

## Public Technical Architecture

### 1. Governed Intelligence Reference Architecture

**[`AX-PUB-ARCH-001`](./specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md)**

A technology-neutral reference architecture describing how governed knowledge, evidence, decision, authority, execution and verification can be separated into explicit system boundaries.

### 2. Evidence, Authority & Verification Contract

**[`AX-PUB-SPEC-002`](./specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md)**  
**[`AX-PUB-SCHEMA-001`](./schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json)**  
**[`AX-PUB-REF-001`](./reference-implementations/eav-contract-validator/README.md)**

Defines a bounded public contract for connecting evidence, authority and verification without treating an analytical output as an execution permission.

### 3. Point-in-Time Knowledge & Provenance

**[`AX-PUB-SPEC-003`](./specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)**  
**[`AX-PUB-SCHEMA-002`](./schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json)**  
**[`AX-PUB-REF-002`](./reference-implementations/point-in-time-knowledge-validator/README.md)**

Defines public semantics for knowledge time, provenance, correction and historical reconstruction.

### 4. Governed Agent Authority & Tool Use

**[`AX-PUB-SPEC-004`](./specifications/AX-PUB-SPEC-004_GOVERNED_AGENT_AUTHORITY_TOOL_USE_STANDARD.md)**  
**[`AX-PUB-SCHEMA-003`](./schemas/AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json)**  
**[`AX-PUB-REF-003`](./reference-implementations/agent-tool-authority-validator/README.md)**

Defines a conceptual/non-production public boundary between an agent having access to a tool and the agent being authorized to invoke that tool for a specific action.

---

## Developer Entry Point

Start with:

**[Public Quickstart →](./docs/QUICKSTART.md)**

For external technical review:

**[External Evaluator Guide →](./docs/EXTERNAL_EVALUATOR_GUIDE.md)**

For the developer-program governance path:

**[`AX-PUB-DEV-001 — Developer Adoption & SDK Readiness Program`](./docs/AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md)**

The public developer path is intentionally bounded and offline. It does **not** expose private AETHER X services, credentials, production authorization systems, brokerage/execution connectivity or private product APIs.

---

## SDK Engineering Track

### Developer Contract

**[`AX-PUB-DEV-002`](./docs/AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md)** — `DEV-GATE-00 CLOSED`

Defines the public contract inventory, semantic errors, compatibility rules, fail-closed behavior and public/private dependency boundary.

Evidence: **[`AX-PUB-CI-003`](./evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md)**

### Reproducible Developer Experience

**[`AX-PUB-DEV-003`](./docs/AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md)** — `DEV-GATE-01 CLOSED`

Verified reference-runtime matrix:

```text
CPython 3.10 / 3.11 / 3.12 / 3.13
```

Evidence: **[`AX-PUB-CI-004`](./evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)**

### Repository-Local SDK Candidate

**[`AX-PUB-DEV-004`](./docs/AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md)** — `DEV-GATE-02 CLOSED`

A bounded repository-local Python candidate over the three declared public validation contracts.

Evidence: **[`AX-PUB-CI-005`](./evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md)**

### Supply-Chain Release Candidate

**[`AX-PUB-DEV-005`](./docs/AX-PUB-DEV-005_SUPPLY_CHAIN_RELEASE_CANDIDATE.md)** — `DEV-GATE-03 CLOSED`

Validated non-published engineering candidate:

```text
AX-PUB-RC-001 v0.1.0-rc1
Engineering bundle SHA-256:
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

The Gate-03 path includes deterministic rebuilds, SPDX 2.3 SBOM, provenance/attestation evidence and extracted-bundle validation.

Evidence: **[`AX-PUB-CI-006 v1.1`](./evidence/AX-PUB-CI-006_SUPPLY_CHAIN_RELEASE_CANDIDATE_VALIDATION.md)**

### External Evaluation Readiness

**[`AX-PUB-DEV-006`](./docs/AX-PUB-DEV-006_EXTERNAL_EVALUATION_READINESS.md)** — `DEV-GATE-04 CLOSED`

Self-service evaluation tooling and machine-readable evaluation contracts are established.

`EXTERNAL EVALUATION READINESS: ESTABLISHED`  
`HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED`  
`EXTERNAL ADOPTION: NOT ESTABLISHED`

Evidence: **[`AX-PUB-CI-007`](./evidence/AX-PUB-CI-007_EXTERNAL_EVALUATION_READINESS_VALIDATION.md)**

---

## DEV-GATE-05 — SDK Release Decision

### 05A — Release Decision Baseline

**[`AX-PUB-DEV-007`](./docs/AX-PUB-DEV-007_SDK_RELEASE_DECISION_BASELINE.md)** — `CLOSED`

Selected release direction:

```text
FIRST SDK SCOPE: offline governed-intelligence validation only
TARGET SDK LICENCE: Apache-2.0 / NOT YET GRANTED
CANONICAL REGISTRY DIRECTION: PyPI
CONTROLLED EXTERNAL VALIDATION DIRECTION: TestPyPI after explicit authority
TARGET RUNTIME MATRIX: CPython 3.11–3.14
SDK PUBLICATION: NOT AUTHORIZED
```

Evidence: **[`AX-PUB-CI-008`](./evidence/AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md)**

### 05B — Installable Package Candidate

**[`AX-PUB-DEV-008`](./docs/AX-PUB-DEV-008_INSTALLABLE_PACKAGE_CANDIDATE.md)** — `CLOSED`

Candidate distribution identity:

```text
Distribution candidate: aetherxglobal-governed-intelligence
Version candidate:      0.1.0rc1
Import namespace:       aetherxglobal.governed_intelligence
```

Exact validated package artifacts:

```text
Wheel:
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
SHA-256: bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

Source distribution:
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz
SHA-256: 2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

The candidate passed installed-package validation on CPython 3.11, 3.12, 3.13 and 3.14.

Evidence: **[`AX-PUB-CI-009`](./evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md)**

`CANDIDATE DISTRIBUTION IDENTITY ≠ REGISTRY OWNERSHIP`

### 05C — Distribution & External Validation

**[`AX-PUB-DEV-009`](./docs/AX-PUB-DEV-009_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE.md)** — `ACTIVE`

The exact Gate-05B candidate has been validated through a **loopback-only Python Simple Repository API-compatible index** using pip index discovery rather than a direct wheel path.

Verified local distribution matrix:

```text
CPython 3.11 / 3.12 / 3.13 / 3.14
LOCAL INDEX VALIDATION: VERIFIED / LOCAL ONLY
EXTERNAL REGISTRY WRITE: NOT AUTHORIZED
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
```

Evidence: **[`AX-PUB-CI-010`](./evidence/AX-PUB-CI-010_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE_VALIDATION.md)**

Remaining Gate-05C blockers include release-control protection, a protected publishing environment, separate authority for controlled external registry validation, actual independent human evaluation, finding disposition and later final release authority.

`LOCAL INDEX PASS ≠ TESTPYPI PASS`

---

## Machine-Readable Public Governance

**[`AX-PUB-MANIFEST-001 v1.22`](./artifacts/AX-PUB-MANIFEST-001.json)** is the current machine-readable public artifact and engineering-state manifest.

**[`AX-PUB-POL-001 v1.6`](./docs/COMPATIBILITY_AND_VERSIONING.md)** defines compatibility, release, snapshot and publication-readiness semantics.

The public validation-evidence chain currently extends through:

```text
AX-PUB-CI-003  Developer Contract Baseline
AX-PUB-CI-004  Reproducible Developer Experience
AX-PUB-CI-005  SDK Candidate
AX-PUB-CI-006  Supply-Chain Release Candidate
AX-PUB-CI-007  External Evaluation Readiness
AX-PUB-CI-008  SDK Release Decision Baseline
AX-PUB-CI-009  Installable Package Candidate
AX-PUB-CI-010  Local-Index Distribution Validation
```

---

## Formal Public Engineering Release

**`public-engineering-vnext-1.0` — AETHER X Governed Intelligence — Public Engineering vNext 1.0**

- tag target: `4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6`;
- fixed technical-review snapshot: **[`AX-PUB-SNAP-002`](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)**;
- release evidence: **[`AX-PUB-REL-001`](./evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)**.

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

---

## Licensing & Reuse Boundary

No open-source licence or general reuse/distribution permission is granted by publication of this repository at this time.

Public availability is provided for inspection, technical review and reproducibility, and for use of GitHub platform functionality subject to applicable GitHub terms. Broader reuse, redistribution, adaptation, sublicensing or commercial use requires separate authorization unless otherwise permitted by applicable law.

The **target** licence direction recorded for a future deliberately scoped SDK distribution is Apache-2.0, but that licence has **not** been granted and does not apply repository-wide.

`PUBLIC VISIBILITY ≠ OPEN-SOURCE LICENCE`  
`TARGET LICENCE DIRECTION ≠ LICENCE GRANTED`  
`SBOM ≠ SOFTWARE REUSE LICENCE`

---

## Private-System Boundary

This repository is intentionally self-contained. Public examples and conformance vectors are generic or synthetic.

No private AETHER X repository, private research program, unpublished algorithm, credential, internal endpoint or confidential implementation architecture is a required runtime dependency of the public engineering path.

Public specifications describe bounded engineering contracts. They do not disclose or establish confidential research mechanisms or private product internals.

---

## What This Repository Does Not Establish

Publication here does **not** establish or imply:

- production readiness;
- customer deployment;
- commercial traction;
- a production API;
- a supported or published SDK;
- PyPI/TestPyPI ownership;
- package-name reservation;
- a public software reuse licence;
- production authorization or autonomous execution authority;
- security certification;
- regulatory approval;
- independent human external evaluation;
- external developer adoption;
- integration between private AETHER X initiatives;
- public disclosure of confidential research or invention work.

`PUBLIC ENGINEERING ≠ PRODUCTION SYSTEM`  
`CI PASS ≠ CUSTOMER OUTCOME`  
`SDK CANDIDATE ≠ SUPPORTED SDK`  
`DEV-GATE-05C ACTIVE ≠ SDK PUBLICATION AUTHORIZED`

See **[SECURITY.md](./SECURITY.md)** for the public security boundary.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
