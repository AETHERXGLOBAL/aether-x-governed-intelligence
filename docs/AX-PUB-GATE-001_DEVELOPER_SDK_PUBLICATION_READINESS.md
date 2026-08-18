# AX-PUB-GATE-001 — Developer SDK Publication Readiness Gate

**Artifact ID:** `AX-PUB-GATE-001`  
**Version:** `1.0`  
**Status:** `PUBLIC ENGINEERING GOVERNANCE GATE · ACTIVE · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This gate defines the minimum public-engineering conditions that should be satisfied before AETHER X represents any developer package, library, SDK or production-oriented integration surface from this repository as an officially supported public SDK.

It exists to prevent a common category error:

```text
PUBLIC REFERENCE IMPLEMENTATION
≠
SUPPORTED SDK
```

The current repository now includes a bounded SDK candidate, a validated non-published engineering release candidate and an external-evaluation-ready public surface. Those facts still do **not** by themselves authorize SDK publication.

## 2. Current Disposition

```text
SDK PUBLICATION: NOT AUTHORIZED
```

This disposition is based only on the current public repository state. It does not describe private product maturity or private implementation capability.

Current developer-program position:

```text
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
DEV-GATE-03: CLOSED
DEV-GATE-04: CLOSED
CURRENT ENGINEERING / DECISION OBJECTIVE: DEV-GATE-05 — SDK RELEASE DECISION
EXTERNAL EVALUATION READINESS: ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

At present, the public repository still does not establish all of the following as approved supported commitments:

- an approved public software licence governing SDK reuse/distribution;
- a stable supported SDK/API compatibility contract;
- an approved package namespace and distribution channel;
- a public support/maintenance commitment;
- a production authentication, authorization or credential-handling contract;
- a production security or deployment support boundary;
- explicit SDK release authority.

The absence of those public commitments is intentional and must not be silently filled by inference.

## 3. Gate Principle

An SDK is not just executable code. Publication of an SDK creates expectations about compatibility, security, packaging, maintenance, support and release accountability.

Therefore:

```text
REFERENCE CODE
+
CI
+
DOCUMENTATION
+
SDK CANDIDATE
+
VALIDATED RELEASE CANDIDATE
+
EXTERNAL-EVALUATION READINESS
≠
SUPPORTED SDK
```

SDK publication should occur only after the required evidence **and authority** for the intended public support boundary exist.

## 4. Readiness Dimensions — Current Assessment

### GATE-01 — Public Authority & IP / Licence

Required before SDK publication:

- explicit authority to publish the SDK as a supported developer artifact;
- an approved software licence or other explicit reuse/distribution terms;
- confirmation that the published package does not disclose restricted source, research, data, credentials or intellectual property.

**Current public state:** `NOT SATISFIED / NO PUBLIC SDK LICENCE DECISION RECORDED`

Public repository visibility alone does not grant a reuse licence.

### GATE-02 — Contract & Compatibility Stability

Required before SDK publication:

- a declared supported public interface surface;
- versioning rules for that interface;
- defined compatibility expectations across supported versions;
- deprecation and breaking-change handling.

**Current public state:** `PARTIAL / BOUNDED CANDIDATE CONTRACT + PYTHON 3.10–3.13 EVIDENCE EXISTS; SUPPORTED SDK API / COMPATIBILITY COMMITMENT NOT APPROVED`

The public engineering now includes:

- `AX-PUB-DEV-002` developer contract baseline;
- `AX-PUB-DEV-004` bounded repository-local SDK candidate;
- direct Python 3.10–3.13 candidate CI evidence through `AX-PUB-CI-005`;
- a migration/deprecation draft established by the Gate-04 readiness surface.

These are candidate/readiness controls, not a stable supported SDK API contract.

### GATE-03 — Package Identity & Distribution

Required before SDK publication:

- approved package name / namespace;
- approved distribution channel;
- package versioning and release ownership;
- reproducible build/package process;
- integrity/provenance expectations for distributed artifacts.

**Current public state:** `PARTIAL / ENGINEERING RELEASE-CANDIDATE BUILD, SBOM AND PROVENANCE ARE VERIFIED; PACKAGE IDENTITY + REGISTRY ARE NOT APPROVED`

`AX-PUB-DEV-005`, `AX-PUB-RC-001` and `AX-PUB-CI-006 v1.1` establish a deterministic, attested, non-published engineering release candidate. They do not establish an approved package name or registry distribution surface.

### GATE-04 — Security, Credentials & Authority Boundary

Required before an SDK can mediate consequential operations:

- explicit authentication boundary;
- credential storage and transmission boundary;
- authorization/authority evaluation semantics;
- least-privilege and revocation behavior;
- failure behavior when identity or authority cannot be established;
- clear separation between reference validation and production authorization.

**Current public state:** `PARTIAL / REFERENCE AUTHORITY SEMANTICS AND PUBLIC BOUNDARY CONTROLS EXIST; PRODUCTION CREDENTIAL / AUTHORIZATION BOUNDARY NOT ESTABLISHED`

`AX-PUB-SPEC-004`, `AX-PUB-SCHEMA-003`, `AX-PUB-REF-003` and the SDK candidate expose bounded authority-validation semantics. They do not establish a production authorization plane or production credential contract.

### GATE-05 — Error & Failure Semantics

Required before SDK publication:

- stable error model;
- deterministic failure categories where appropriate;
- retry/idempotency expectations where applicable;
- timeout/cancellation behavior where applicable;
- fail-closed behavior for authority or evidence failures.

**Current public state:** `PARTIAL / AXDEV CANDIDATE ERROR TAXONOMY AND FAIL-CLOSED REFERENCE BEHAVIOR EXIST; SUPPORTED SDK RETRY / TIMEOUT / CANCELLATION CONTRACT NOT APPROVED`

The bounded candidate's error taxonomy is evidence for candidate engineering, not a stable support commitment.

### GATE-06 — Conformance & Regression Evidence

Required before SDK publication:

- automated tests for the supported SDK surface;
- compatibility/regression coverage;
- public conformance cases for normative behavior where appropriate;
- release-gated CI.

**Current public state:** `PARTIAL / BOUNDED SDK-CANDIDATE UNIT + CONFORMANCE TESTS AND PYTHON 3.10–3.13 CI EXIST; SUPPORTED RELEASE-GATED SDK CONFORMANCE COMMITMENT NOT APPROVED`

`AX-PUB-CI-005` and later readiness checks directly exercise the bounded candidate. This does not yet define the release gate for a supported distributed package.

### GATE-07 — Dependency & Supply-Chain Boundary

Required before SDK publication:

- dependency inventory and update policy;
- supported runtime versions;
- package integrity/provenance expectations;
- secret-free, private-repository-free public build path;
- clear policy for third-party components and licences.

**Current public state:** `PARTIAL / DETERMINISTIC RELEASE-CANDIDATE BUILD + SPDX SBOM + BUILD PROVENANCE ARE VERIFIED; DISTRIBUTED-PACKAGE DEPENDENCY / UPDATE / PUBLISHING POLICY NOT APPROVED`

The bounded engineering candidate currently declares no third-party runtime dependency and has verified public/private build boundaries. A future distributed package still requires an approved dependency/update and publication policy.

### GATE-08 — Documentation & Developer Contract

Required before SDK publication:

- installation instructions;
- supported usage examples;
- explicit unsupported uses;
- compatibility/version selection guidance;
- security and authority warnings;
- migration guidance for breaking changes.

**Current public state:** `PARTIAL / SELF-SERVICE EVALUATOR GUIDE + LIMITATIONS + MIGRATION DRAFT + STRUCTURED FEEDBACK PATH EXIST; SUPPORTED PACKAGE INSTALLATION / SDK DOCUMENTATION CONTRACT NOT APPROVED`

`AX-PUB-DEV-006` and `AX-PUB-CI-007` establish external-evaluation readiness for the repository-local candidate surface. They do not establish a supported package installation contract.

### GATE-09 — Maintenance & Support Boundary

Required before SDK publication:

- responsible maintainer/owner boundary;
- supported version window;
- vulnerability/security reporting path;
- deprecation/end-of-support process;
- public statement of support expectations.

**Current public state:** `NOT SATISFIED AS A SUPPORTED-SDK COMMITMENT`

A public security-reporting path, feedback/triage process and migration/deprecation draft now exist. However, no supported-version window, response SLA, maintenance commitment, end-of-support contract or supported SDK owner obligation has been approved.

### GATE-10 — Release Authority

A supported SDK publication requires an explicit release decision after the preceding dimensions are reviewed for the intended scope.

A Git tag, GitHub Release, SDK candidate, release candidate, external-evaluation readiness state or successful CI workflow does not implicitly grant this authority.

**Current public state:** `NO SDK RELEASE AUTHORITY RECORDED`

## 5. Promotion Rule

The public SDK state may advance only through an explicit recorded decision such as:

```text
NOT AUTHORIZED
→ CANDIDATE
→ RELEASE-CANDIDATE VALIDATED
→ APPROVED FOR PUBLIC SDK RELEASE
```

Developer-program gates may establish engineering readiness without changing the publication disposition.

No state should be promoted because of marketing pressure, repository activity, a successful demo, a successful CI run, or the mere existence of executable candidate code.

## 6. Evidence Required for Promotion

A future SDK publication decision should identify, at minimum:

- the exact package/interface scope;
- approved licence/distribution terms;
- supported versions and compatibility policy;
- security and authority boundary;
- test/conformance evidence;
- supply-chain and dependency boundary;
- documentation/support boundary;
- release authority and date;
- material limitations.

Unknowns remain unknown until evidenced.

## 7. External-Evaluation Boundary

`DEV-GATE-04 CLOSED` means the bounded public surface is ready for external technical evaluation under its declared constraints.

It does **not** establish:

- that a human external evaluator has participated;
- that an external developer or partner adopted the candidate;
- that an integration exists;
- that a support relationship exists;
- that the SDK is approved for publication.

`EXTERNAL EVALUATION READINESS ≠ EXTERNAL EVALUATION OCCURRED ≠ EXTERNAL ADOPTION`

## 8. Private-Project Boundary

This gate does not require inspection or disclosure of any private AETHER X project repository.

It does not establish implementation by AETHER X Quantum, AX-OS, AIC, AETHER X Research or any other private initiative.

Private source code, unpublished research, credentials, confidential architecture, internal endpoints, customer information and unpublished intellectual property remain outside the public disclosure boundary.

## 9. Current Assessment Refresh — 2026-08-18

This refresh updates only the **current evidence assessment** of the existing Gate dimensions after DEV-GATE-00 through DEV-GATE-04 progression.

It does not change:

- Artifact ID `AX-PUB-GATE-001`;
- Version `1.0`;
- the Gate criteria;
- publication authority;
- licence/IP authority;
- package identity;
- registry authorization;
- supported SDK status.

Current disposition remains:

```text
SDK PUBLICATION NOT AUTHORIZED
```

## 10. Claim Boundary

`PUBLIC REFERENCE IMPLEMENTATION ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SUPPORTED SDK`  
`RELEASE-CANDIDATE VALIDATED ≠ SDK RELEASE`  
`EXTERNAL-EVALUATION READY ≠ SDK RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ SDK RELEASE`  
`JSON SCHEMA ≠ PRODUCTION API`  
`REFERENCE AUTHORITY VALIDATOR ≠ PRODUCTION AUTHORIZATION`  
`DEV-GATE-05 ACTIVE ≠ SDK PUBLICATION AUTHORIZED`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

This gate is a public engineering control for future publication decisions, not an announcement that an SDK will be released.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
