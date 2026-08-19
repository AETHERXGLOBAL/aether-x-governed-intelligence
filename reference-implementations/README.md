# AETHER X Public Reference Implementations

`PUBLIC ENGINEERING MATERIAL · EDUCATIONAL / NON-PRODUCTION`

This directory contains bounded executable companions to selected AETHER X public technical specifications and machine-readable schemas, plus independently reviewed offline interoperability/trust-admissibility reference proofs that are part of the current Stable Public Evaluation Baseline.

`CURRENT MAIN BASELINE ≠ FORMAL PUBLIC ENGINEERING RELEASE`

## Current Reference Implementations

| ID / type | Reference implementation / proof | Related public artifacts | Public state |
|---|---|---|---|
| `AX-PUB-REF-001` | [EAV Contract Validator](./eav-contract-validator/README.md) | `AX-PUB-SPEC-002` · `AX-PUB-SCHEMA-001` | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | [Point-in-Time Knowledge Validator](./point-in-time-knowledge-validator/README.md) | `AX-PUB-SPEC-003` · `AX-PUB-SCHEMA-002` | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-003` | [Agent Tool-Use Authority Validator](./agent-tool-authority-validator/README.md) | `AX-PUB-SPEC-004` · `AX-PUB-SCHEMA-003` | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| Bounded offline proof | [Attestation Semantic Importer](./offline-attestation-importer/README.md) | `AX-INTEROP-IMPORT-PROFILE-001` · in-toto Statement v1 · supported SLSA predicate forms | `INDEPENDENTLY VERIFIED · OFFLINE · READ-ONLY · IMPORT-ONLY · NON-PRODUCTION` |
| Bounded offline proof | [AuthZEN Decision Admissibility](./offline-authzen-admissibility/README.md) | `AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001` · AuthZEN single Access Evaluation | `INDEPENDENTLY VERIFIED · OFFLINE · READ-ONLY · SINGLE ACCESS EVALUATION ONLY · NON-PRODUCTION` |

## Reference Responsibilities

### AX-PUB-REF-001

Demonstrates selected evidence / decision / authority / execution / verification invariants, including bounded authority and the requirement that a `VERIFIED` outcome be backed by `PASS` verification.

### AX-PUB-REF-002

Demonstrates selected point-in-time knowledge / provenance invariants, including:

- no-future-leakage relative to a declared knowledge cutoff;
- source and transformation lineage references;
- revision/supersession references;
- explicit missing states for absent values;
- reproducibility-cutoff consistency.

### AX-PUB-REF-003

Demonstrates selected agent/tool-use authority invariants from the public Agent Tool-Use Authority Envelope, including proposal/grant/context linkage, bounded parameters, invocation scope and explicit verification-required state.

`CAPABILITY ≠ AUTHORITY`

`TOOL AVAILABILITY ≠ TOOL PERMISSION`

### Offline Attestation Semantic Importer

Accepts only caller-supplied attestation bytes and demonstrates bounded semantic import of in-toto Statement v1 plus supported SLSA predicate classification. Exact received-byte identities are preserved; signature verification, trust evaluation and predicate-policy evaluation are injected interfaces. Imported material remains AETHER `SOURCE_DATA`.

It implements no cryptography, trust store, certificate/key discovery, network/registry access, AETHER Decision, Authority, Execution, Verification, Acceptance or Verified Outcome.

### Offline AuthZEN Decision Admissibility

Accepts one already-supplied AuthZEN single Access Evaluation request/response pair and demonstrates only:

`RECEIVED → REQUEST_BOUND → RESPONSE_INTEGRITY_VERIFIED → PDP_TRUSTED → DECISION_ADMISSIBLE`

It preserves exact request/response identities when bytes are available, fails closed when required provenance/binding evidence is missing or invalid, and uses injected interfaces for response integrity, PDP identity/trust, policy provenance, freshness and replay.

It implements no PDP, policy engine, trust store, network client, cryptography, AETHER Decision, `authority_context`, `tool_use_grant`, capability, execution permission, AETHER Verification or Verified Outcome.

`DECISION_ADMISSIBLE ≠ AETHER_DECISION ≠ AETHER_AUTHORITY ≠ EXECUTION_PERMISSION`

## Claim Boundary

These implementations and proofs are intentionally small and dependency-light. They are designed to make public engineering semantics inspectable, not to imitate or expose proprietary platform code.

They do **not** establish:

- production readiness;
- product integration;
- implementation inside AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- secure production authorization enforcement;
- production data-quality guarantees;
- ownership or availability of financial-data sources;
- regulatory compliance or certification;
- customer deployment;
- predictive or investment performance;
- a new formal public engineering release, Gate transition, Security GO or Risk Acceptance.

The fixed formal public engineering release remains `public-engineering-vnext-1.0`; the current `main` baseline may contain later independently verified engineering additions without changing that historical release.

`REFERENCE IMPLEMENTATION ≠ PRODUCT IMPLEMENTATION`

`CI PASS ≠ PRODUCTION APPROVAL`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
