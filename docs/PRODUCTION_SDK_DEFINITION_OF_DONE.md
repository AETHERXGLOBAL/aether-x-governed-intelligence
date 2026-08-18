# AETHER X Governed Intelligence — Production SDK Definition of Done

**Document state:** `PRODUCTIZATION TARGET · NOT CURRENT CAPABILITY`  
**Applies to:** first official AETHER X Governed Intelligence Python SDK release  
**Current release authority:** `NOT AUTHORIZED`

## Purpose

This document defines the minimum evidence required before AETHER X may represent its Python SDK as an **official production-supported developer product**.

The target statement is:

> A developer can install the official AETHER X Governed Intelligence SDK from PyPI using `pip`, verify its release origin and provenance, rely on a documented public API and compatibility contract, use it inside its declared production scope, receive security and maintenance guidance, and upgrade through a governed release process.

No single CI pass, package upload, release tag, contract file or licence file is sufficient to establish this state.

Current contract candidates that make this target machine-checkable are:

- `AX-PUB-API-001` — public API contract candidate;
- `AX-PUB-SUP-001` — support / compatibility / maintenance contract candidate;
- `AX-PUB-SEC-001` — security-operations readiness contract candidate.

Their validation evidence is `AX-PUB-CI-012` and `AX-PUB-CI-013`. Validation does not activate support, security operations or release authority.

---

## 1. Product scope

The first production-supported SDK scope is deliberately narrow:

```text
OFFLINE GOVERNED-INTELLIGENCE VALIDATION
```

Included target surface:

- `AX-PUB-SPEC-002` validation;
- `AX-PUB-SPEC-003` validation;
- `AX-PUB-SPEC-004` validation;
- explicit developer-facing result/finding types;
- deterministic fail-closed behavior for declared validation contracts;
- supported-contract and version discovery;
- local machine-readable operation.

Excluded from the first production-supported scope unless separately approved and evidenced:

- remote AETHER X services;
- credentials or authentication;
- production authorization decisions;
- tool invocation;
- agent execution;
- brokerage, financial or infrastructure execution;
- autonomous external side effects;
- private AETHER X product integrations.

`PRODUCTION-SUPPORTED VALIDATION SDK ≠ PRODUCTION AUTHORIZATION OR EXECUTION PLATFORM`

---

## 2. Installation and distribution

Before production-supported status:

- the exact distribution name is owned/controlled on PyPI;
- publication occurs through the approved release workflow;
- an exact released version installs with standard pip index semantics;
- wheel and sdist identities are recorded;
- the installed distribution is tested outside the source checkout;
- declared supported runtimes install and execute the exact released artifact;
- no undocumented private package index or private runtime dependency is required.

Target developer command:

```bash
pip install aetherxglobal-governed-intelligence
```

A pre-release candidate may use an exact version pin. A stable production release must identify the supported release line unambiguously.

---

## 3. Public API contract

Production-supported status requires an explicit API inventory.

At minimum:

- every supported top-level import is documented;
- public symbols are separated from internal implementation modules;
- supported behavior maps to a normative public contract or documented SDK extension;
- error/result semantics are documented;
- unsupported inputs fail deterministically where the contract requires fail-closed behavior;
- accidental importability does not create a support commitment;
- compatibility tests detect unintended public-surface changes.

The first candidate surface is based on:

```python
from aetherxglobal.governed_intelligence import (
    validate,
    validate_eav,
    validate_point_in_time,
    validate_agent_authority,
    supported_contracts,
)
```

Current binding:

```text
PUBLIC API CONTRACT: AX-PUB-API-001 v0.1
VALIDATION EVIDENCE: AX-PUB-CI-012
VALIDATED RUNTIMES: CPython 3.11–3.14
STABLE 1.0 GUARANTEE: NOT ESTABLISHED
SUPPORT COMMITMENT: NOT ESTABLISHED
```

This list is not promoted to a stable `1.0.0` compatibility guarantee merely by appearing here or by passing candidate CI.

---

## 4. Runtime, compatibility and support contract

Current target runtime line:

```text
CPython 3.11
CPython 3.12
CPython 3.13
CPython 3.14
```

Production-supported status requires:

- package-level CI for every declared runtime;
- documented `Requires-Python` metadata aligned with actual support;
- versioning rules documented for the supported release line;
- a deprecation policy;
- migration guidance for material changes;
- an end-of-support rule;
- a defined response when an upstream Python version reaches end of life;
- compatibility evidence for the exact artifact being released.

The pre-activation model is defined by:

[`AX-PUB-SUP-001 — SDK Support, Compatibility & Maintenance Contract Candidate`](./AX-PUB-SUP-001_SDK_SUPPORT_COMPATIBILITY_MAINTENANCE_CONTRACT.md)

Current candidate target under normal conditions, **after explicit activation only**:

```text
NORMAL REMOVAL REQUIRES PRIOR DEPRECATION
TARGET NOTICE: 90 DAYS
TARGET INTERVENING RELEASE: ONE SUPPORTED MINOR
TARGET RULE: LATER OF 90 DAYS OR ONE INTERVENING SUPPORTED MINOR
```

Current actual state:

```text
SUPPORT CONTRACT CANDIDATE: VALIDATED
SUPPORT COMMITMENT: NOT ESTABLISHED
PRODUCTION SUPPORT: NOT ACTIVATED
COMMERCIAL SLA: NOT ESTABLISHED
```

`TESTED ON A RUNTIME ≠ PERMANENT SUPPORT COMMITMENT`  
`TARGET DEPRECATION WINDOW ≠ CURRENT SUPPORT PROMISE`

---

## 5. Software supply-chain requirements

The release path must establish all of the following:

- release-sensitive source changes are governed through protected change control;
- build happens in controlled CI, not on a maintainer workstation;
- release-sensitive Actions dependencies are pinned to reviewed immutable revisions;
- workflow permissions use least privilege;
- wheel and sdist are built once and treated as immutable release inputs;
- the exact release artifacts are installed and tested before publication;
- cryptographic digests are recorded;
- provenance/attestation is generated and retained;
- SBOM evidence is produced where required by the release contract;
- publication uses PyPI Trusted Publishing / OIDC rather than a long-lived primary upload token;
- production publication is bound to an approved GitHub Environment or equivalent protected release boundary;
- published artifacts are verified after registry publication;
- final release evidence links source commit, workflow identity, artifact identity and registry result.

Attestation, SBOM and Trusted Publishing are controls; none alone is a security certification.

Closed historical release-candidate evidence must not be silently rewritten by later productization work. `AX-PUB-CI-013` directly revalidated the Gate-03 deterministic candidate identity while validating the support/security contract candidates.

---

## 6. Repository and release-control requirements

Before any production publication:

- protected release-relevant changes require a pull request;
- required release validation checks are enforced;
- at least one independent approval is required for material release changes;
- stale approval handling is configured where supported;
- force-push and deletion of protected release branches/tags are blocked or equivalently controlled;
- release tags or release inputs are restricted to the approved release path;
- the production publishing environment is protected;
- production publication cannot be silently triggered from untrusted pull-request code;
- release-control state is independently audited immediately before final release authority.

Current observed `main` protection is insufficient and remains a blocker until a later evidence record proves otherwise.

See [`RELEASE_CONTROL_PLANE.md`](./RELEASE_CONTROL_PLANE.md) and [`RELEASE_CONTROL_AUDIT.md`](./RELEASE_CONTROL_AUDIT.md).

---

## 7. Licensing and IP requirements

Before the SDK is offered for general reuse:

- AETHER X must confirm it has the right to distribute and license every shipped file;
- copyright ownership/permission must be documented for the release inventory;
- third-party notices and obligations must be resolved;
- the selected SDK licence must be explicitly authorized;
- package metadata must match the actual granted licence;
- repository-wide content must not be implicitly relicensed by an SDK-only decision;
- trademarks and brand assets remain outside a software copyright licence unless separately authorized.

Current target direction is `Apache-2.0`; **no SDK licence is currently granted**.

---

## 8. Security and vulnerability operations

Production-supported status requires a functioning security process, including:

- a documented private vulnerability-reporting path;
- ownership for triage and remediation;
- severity classification;
- a supported method for security releases;
- documented treatment of compromised release credentials or workflows;
- dependency/update policy appropriate to the final package;
- release revocation/yank guidance when a published artifact is unsafe;
- consumer guidance for identifying fixed versions.

The pre-activation operating model is defined by:

[`AX-PUB-SEC-001 — SDK Security Operations Readiness Contract Candidate`](./AX-PUB-SEC-001_SDK_SECURITY_OPERATIONS_READINESS_CONTRACT.md)

Current actual state:

```text
SECURITY OPERATIONS CONTRACT CANDIDATE: VALIDATED
DEDICATED SECURITY CHANNEL: NOT ESTABLISHED
SECURITY RESPONSE OWNER: NOT ESTABLISHED
SECURITY RESPONSE SLA: NOT ESTABLISHED
BUG BOUNTY: NOT ESTABLISHED
SECURITY OPERATIONS READY: NO
```

A security policy or contract document without an operating owner, private intake path and executable remediation/release process does not satisfy this gate.

`VALIDATED SECURITY CONTRACT ≠ SECURITY OPERATIONS READY`

---

## 9. External evaluation

Before the first public production-supported release, require at least one independent human technical evaluation of the exact installable candidate/release path.

The record must include:

- evaluator identity or bounded evaluator record;
- exact version and artifact digest;
- runtime/environment;
- installation path;
- exercised public APIs;
- observed failures or limitations;
- machine-readable result where required by Gate-05;
- disposition of every material finding.

No unresolved critical finding is permitted. High-severity findings require remediation or explicit authorized risk acceptance with rationale.

External evaluation does not imply endorsement or adoption.

---

## 10. Documentation requirements

A production-supported SDK release must provide, at minimum:

- installation instructions;
- supported Python versions;
- public API reference;
- minimal runnable examples;
- supported/unsupported use cases;
- compatibility and deprecation policy;
- migration guidance;
- security reporting instructions;
- release-origin/provenance verification guidance;
- maintenance/support boundary;
- changelog/release notes;
- known material limitations.

The documentation and package metadata must describe the same release state.

---

## 11. Maintenance contract

The first supported `0.x` release line may remain pre-1.0, but support commitments must be explicit.

The current candidate direction is encoded in `AX-PUB-SUP-001` rather than left as prose-only policy:

- no commercial SLA is established;
- the latest supported minor is the target primary maintained line after activation;
- the immediately previous minor has a **target** security/correctness window of 90 days after a successor minor, where technically feasible;
- normal planned removals have a target rule of the later of 90 days or one intervening supported minor after activation;
- material planned removals should include migration guidance;
- support scope excludes private product integration and production execution systems unless separately contracted.

These targets become a support commitment only when final release authority explicitly adopts/activates the contract.

---

## 12. Final evidence pack

`DEV-GATE-05D` must not authorize publication without an evidence pack containing at least:

```text
REPOSITORY + SOURCE COMMIT
EXACT DISTRIBUTION NAME
EXACT VERSION
WHEEL + SDIST DIGESTS
PUBLIC API INVENTORY + AX-PUB-API-001 STATE
SUPPORTED PYTHON MATRIX
CONFORMANCE RESULTS
BUILD / PROVENANCE EVIDENCE
SBOM / RELEASE INVENTORY EVIDENCE
RELEASE-CONTROL AUDIT
REGISTRY OWNERSHIP / TRUSTED PUBLISHER STATE
LICENCE + IP CLEARANCE
EXTERNAL EVALUATION RESULT
AX-PUB-SUP-001 ACTIVATION STATE
AX-PUB-SEC-001 READINESS STATE
SECURITY + SUPPORT BOUNDARY
MATERIAL LIMITATIONS
RELEASE OWNER
EXPLICIT RELEASE AUTHORITY
```

---

## 13. Promotion states

The following state transitions are intentionally distinct:

```text
INSTALLABLE CANDIDATE
    ↓
DISTRIBUTION-VALIDATED CANDIDATE
    ↓
API CONTRACT VALIDATED CANDIDATE
    ↓
SUPPORT / SECURITY CONTRACTS VALIDATED CANDIDATE
    ↓
EXTERNALLY EVALUATED CANDIDATE
    ↓
RELEASE-CONTROL READY
    ↓
LICENCE / IP CLEARED
    ↓
SUPPORT ACTIVATED + SECURITY OPERATIONS READY
    ↓
DEV-GATE-05D AUTHORIZED
    ↓
OFFICIAL PUBLISHED SDK
    ↓
PRODUCTION-SUPPORTED DECLARED SCOPE
```

No stage may be inferred from a later-looking filename, CI result or package version.

---

## Current disposition

```text
PRODUCTION SDK DEFINITION OF DONE: DEFINED
PUBLIC API CONTRACT CANDIDATE: VALIDATED
SUPPORT CONTRACT CANDIDATE: VALIDATED / NOT ACTIVATED
SECURITY OPERATIONS CONTRACT CANDIDATE: VALIDATED / NOT READY
SUPPORT COMMITMENT: NOT ESTABLISHED
SECURITY OPERATIONS READY: NO
PRODUCTION SDK: NOT ESTABLISHED
PYPI DISTRIBUTION: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
