<p align="center">
  <img src="https://raw.githubusercontent.com/AETHERXGLOBAL/.github/main/profile/assets/aether-x-premium-banner.png" alt="AETHER X GLOBAL" width="100%" />
</p>

# AETHER X Governed Intelligence

**Public reference architecture, machine-readable contracts, bounded reference implementations, conformance evidence and developer-readiness engineering for governed intelligence systems by AETHER X GLOBAL.**

`PUBLIC ENGINEERING REPOSITORY · CONTROLLED DISCLOSURE · NON-PRODUCTION`

> **Institutional Intelligence. Governed Autonomy.**  
> **Build Intelligence That Can Be Trusted to Act.**

---

## Engineering Thesis

AETHER X treats intelligence as a governed system, not a model response.

```text
INTENT
  ↓
DATA / KNOWLEDGE
  ↓
EVIDENCE
  ↓
ANALYSIS / REASONING
  ↓
DECISION
  ↓
AUTHORITY
  ↓
CONTROLLED EXECUTION
  ↓
VERIFICATION
  ↓
VERIFIED OUTCOME
  ↓
AUDIT / LEARNING
```

Core engineering separations:

`OUTPUT ≠ FACT`  
`RECOMMENDATION ≠ DECISION`  
`CAPABILITY ≠ AUTHORITY`  
`TOOL AVAILABILITY ≠ TOOL PERMISSION`  
`EXECUTION COMPLETE ≠ VERIFIED`

These separations are architectural constraints, not marketing language.

---

## What Is Public Here

This repository intentionally exposes a bounded technical surface for inspection, reproducibility and engineering evaluation:

- governed-intelligence reference architecture;
- evidence, authority and verification specifications;
- point-in-time knowledge and provenance contracts;
- governed agent authority and tool-use boundaries;
- JSON Schemas;
- Python reference validators;
- synthetic conformance kits;
- deterministic build and supply-chain evidence;
- public CI evidence;
- an installable Python SDK **candidate**;
- local-index distribution validation;
- external-evaluation contracts and tooling.

Private product code, confidential research, credentials, internal endpoints, proprietary algorithms and unpublished implementation architecture remain outside this repository.

---

## Current Engineering State

The current public developer program is deliberately gated.

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

Current verified engineering facts:

```text
INSTALLABLE PACKAGE CANDIDATE: ESTABLISHED
DISTRIBUTION CANDIDATE: aetherxglobal-governed-intelligence
IMPORT NAMESPACE: aetherxglobal.governed_intelligence
VERSION CANDIDATE: 0.1.0rc1
VERIFIED PACKAGE RUNTIME MATRIX: Python 3.11–3.14
LOCAL SIMPLE-INDEX DISTRIBUTION VALIDATION: VERIFIED / LOCAL ONLY
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

The detailed current-state page is **[Public Engineering State](./docs/PUBLIC_ENGINEERING_STATE.md)**.

---

## Recent Verified Engineering Additions

The current Stable Public Evaluation Baseline includes two independently reviewed, bounded offline interoperability/trust-admissibility proofs:

- **[Offline in-toto / SLSA Attestation Semantic Importer](./reference-implementations/offline-attestation-importer/README.md)** — accepts caller-supplied attestation bytes, parses in-toto Statement v1, classifies supported SLSA predicate forms, preserves exact-byte identities and maps imported material only to AETHER `SOURCE_DATA`. Signature, trust and policy determinations are injected interfaces. It implements no cryptography, trust store, network access, registry access, AETHER Decision, Authority, Execution, Verification or Verified Outcome.
- **[Offline AuthZEN Decision Admissibility Proof](./reference-implementations/offline-authzen-admissibility/README.md)** — evaluates one already-supplied AuthZEN single Access Evaluation through the bounded chain `RECEIVED → REQUEST_BOUND → RESPONSE_INTEGRITY_VERIFIED → PDP_TRUSTED → DECISION_ADMISSIBLE`. It is fail-closed, preserves exact request/response identities, and implements no PDP, network client, policy engine, cryptography, AETHER Decision, Authority, grant, capability or execution permission.

Their corresponding design records are [AX-INTEROP-IMPORT-PROFILE-001](./docs/AX-INTEROP-IMPORT-PROFILE-001.md) and [AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001](./docs/AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001.md).

`DECISION_ADMISSIBLE ≠ AETHER_DECISION ≠ AETHER_AUTHORITY ≠ EXECUTION_PERMISSION`

`CURRENT MAIN BASELINE ≠ FORMAL PUBLIC ENGINEERING RELEASE`

The fixed formal public engineering release remains `public-engineering-vnext-1.0`; these verified additions do not create a new release, Gate transition, Production approval, Security GO or Risk Acceptance.

---

## Developer Entry Points

1. **[Quickstart](./docs/QUICKSTART.md)** — run the bounded public reference path.
2. **[Developer Adoption & SDK Readiness Program](./docs/AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md)** — understand the gate model.
3. **[External Evaluator Guide](./docs/EXTERNAL_EVALUATOR_GUIDE.md)** — evaluate the bounded public surface.
4. **[Installable External Evaluator Guide](./docs/INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md)** — evaluate the exact installable candidate when an authorized distribution path exists.
5. **[Limitations & Unsupported Uses](./docs/LIMITATIONS_AND_UNSUPPORTED_USES.md)** — read before interpreting capability.

---

## Public Technical Series

| Layer | Public artifact | State |
|---|---|---|
| Reference architecture | `AX-PUB-ARCH-001` | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Evidence / Authority / Verification | `AX-PUB-SPEC-002` | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Point-in-Time Knowledge & Provenance | `AX-PUB-SPEC-003` | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Agent Authority & Tool Use | `AX-PUB-SPEC-004` | `CONCEPTUAL / NON-PRODUCT-SPECIFIC` |
| Machine-readable contracts | `AX-PUB-SCHEMA-001/002/003` | `PUBLIC / MACHINE-READABLE` |
| Reference validators | `AX-PUB-REF-001/002/003` | `CI-TESTED / EDUCATIONAL / NON-PRODUCTION` |
| Conformance | `AX-PUB-TEST-001/002` | `BOUNDED / SYNTHETIC / NON-PRODUCTION` |
| Public artifact governance | `AX-PUB-MANIFEST-001` | `CURRENT MACHINE-READABLE BASELINE` |
| Public engineering release | `AX-PUB-REL-001` | `FORMAL PUBLIC ENGINEERING RELEASE / NON-PRODUCT` |
| Developer program | `AX-PUB-DEV-001` | `ACTIVE / UNDER DEVELOPMENT` |
| Installable candidate | `AX-PUB-DEV-008` | `DEV-GATE-05B CLOSED` |
| Distribution validation | `AX-PUB-DEV-009` + `AX-PUB-CI-010` | `05C ACTIVE · LOCAL INDEX VERIFIED` |

---

## Evidence Chain

The public technical surface is designed to remain traceable:

```text
SPECIFICATION
→ MACHINE-READABLE CONTRACT
→ REFERENCE / SDK BEHAVIOR
→ CONFORMANCE CASE
→ CI RESULT
→ EVIDENCE RECORD
→ GOVERNED MATURITY STATE
```

Three core public paths are:

```text
AX-PUB-SPEC-002 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001 → AX-PUB-TEST-001
AX-PUB-SPEC-003 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002 → AX-PUB-TEST-001
AX-PUB-SPEC-004 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003 → AX-PUB-TEST-002
```

Recent developer evidence:

- `AX-PUB-CI-008` — DEV-GATE-05A release-decision baseline validation;
- `AX-PUB-CI-009` — deterministic installable-package candidate validation;
- `AX-PUB-CI-010` — local-index distribution validation across Python 3.11–3.14.

---

## Installable Candidate Identity

The current engineering candidate is intentionally pre-release and non-published:

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Import:       aetherxglobal.governed_intelligence
```

Validated artifact identities:

```text
Wheel SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

sdist SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

`LOCAL INDEX PASS ≠ TESTPYPI PASS`  
`INSTALLABLE CANDIDATE ≠ SUPPORTED SDK`

---

## Licensing & Reuse Boundary

No general open-source licence or general reuse/distribution permission is granted by publication of this repository at this time.

Public availability is for inspection, technical review and reproducibility, subject to applicable GitHub terms and applicable law. Broader reuse, redistribution, adaptation, sublicensing or commercial use requires separate authorization unless otherwise permitted by law.

The current SDK release-direction record identifies **Apache-2.0 as a target direction only after IP/copyright clearance**. No licence has been granted.

`PUBLIC VISIBILITY ≠ OPEN-SOURCE LICENCE`

---

## What This Repository Does Not Establish

This repository does **not** establish or imply:

- production deployment;
- customer deployment;
- a production API;
- a supported public SDK;
- PyPI or TestPyPI ownership/publication;
- package-name reservation;
- human external evaluation;
- external developer adoption;
- security certification;
- regulatory approval;
- integration with private AETHER X products;
- unrestricted autonomous authority.

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`CI PASS ≠ PRODUCT IMPLEMENTATION`  
`HUMAN EVALUATION ≠ CI`  
`SDK PUBLICATION NOT AUTHORIZED`

---

## Public Engineering Release

The fixed public engineering release remains:

**`public-engineering-vnext-1.0` — AETHER X Governed Intelligence — Public Engineering vNext 1.0**

See **[AX-PUB-REL-001](./evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)** and **[AX-PUB-SNAP-002](./snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)**.

---

## Security

See **[SECURITY.md](./SECURITY.md)** for the public security and disclosure boundary.

---

**AETHER X GLOBAL — A Governed Intelligence Systems Company**  
**Institutional Intelligence. Governed Autonomy.**