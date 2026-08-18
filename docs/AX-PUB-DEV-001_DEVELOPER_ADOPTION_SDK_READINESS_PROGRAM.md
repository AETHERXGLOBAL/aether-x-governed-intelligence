# AX-PUB-DEV-001 — Developer Adoption & SDK Readiness Program

**Artifact ID:** `AX-PUB-DEV-001`  
**Version:** `1.0`  
**Status:** `PUBLIC ENGINEERING PROGRAM · UNDER DEVELOPMENT · DEV-GATE-00 CLOSED · DEV-GATE-01 CLOSED · DEV-GATE-02 CLOSED · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Governing readiness gate:** `AX-PUB-GATE-001`

## 1. Purpose

This program defines how AETHER X may evolve its public governed-intelligence engineering from material that can be inspected and reproduced into a developer surface that can eventually be built upon under explicit compatibility, security, licensing, maintenance and release controls.

The target is not rapid package publication. The target is a durable developer contract.

```text
PUBLIC ENGINEERING
→ DEVELOPER CONTRACT
→ REPRODUCIBLE EXPERIENCE
→ SDK CANDIDATE
→ SECURITY / SUPPLY-CHAIN EVIDENCE
→ EXTERNAL EVALUATION
→ RELEASE AUTHORITY
→ SUPPORTED DEVELOPER SURFACE
```

This program does not authorize the final step.

`DEVELOPER ADOPTION PROGRAM ≠ SDK RELEASE`  
`SDK CANDIDATE ≠ SUPPORTED SDK`  
`PUBLIC REFERENCE CODE ≠ REUSE LICENCE`

## 2. Strategic Objective

The program is intended to make the public engineering surface progressively easier to understand, validate, integrate and extend while preserving AETHER X boundaries around evidence, authority, verification and controlled execution.

The desired developer experience is:

```text
DISCOVER
→ UNDERSTAND
→ INSTALL / RUN
→ VALIDATE
→ INTEGRATE
→ OBSERVE
→ UPGRADE SAFELY
→ VERIFY RELEASE ORIGIN
```

The program must not create an implicit production commitment, product integration claim, security certification, open-source licence or support obligation before those items are separately authorized.

## 3. Current Baseline

The repository now provides:

- conceptual governed-intelligence specifications;
- machine-readable JSON Schema contracts;
- bounded Python reference validators;
- synthetic conformance kits;
- public CI evidence for declared paths;
- machine-readable artifact manifest and compatibility policy;
- commit-anchored reproducibility snapshots;
- a formal non-product public engineering release;
- `AX-PUB-GATE-001` as the controlling SDK publication gate;
- `AX-PUB-DEV-002` as the closed DEV-GATE-00 developer contract baseline;
- `AX-PUB-DEV-003` as the closed DEV-GATE-01 reproducible developer experience;
- directly observed Gate-01 runtime-matrix evidence recorded by `AX-PUB-CI-004`;
- `AX-PUB-DEV-004` as the closed DEV-GATE-02 bounded repository-local SDK candidate;
- directly observed Gate-02 SDK-candidate and governance evidence recorded by `AX-PUB-CI-005`.

The public reference developer path uses the Python standard library only. `AX-PUB-CI-004` directly validates the declared Gate-01 reference experience across Python 3.10, 3.11, 3.12 and 3.13. `AX-PUB-CI-005` directly validates the bounded Gate-02 candidate across the same declared candidate runtime matrix.

This establishes a bounded SDK candidate only. No supported or published SDK exists.

## 4. Non-Negotiable Boundaries

1. `AX-PUB-GATE-001` remains authoritative for SDK publication readiness.
2. No package may be represented as an officially supported AETHER X SDK while the gate disposition is `SDK PUBLICATION NOT AUTHORIZED`.
3. No package registry publication may occur before package identity, licensing/IP authority, release authority and distribution controls are explicitly approved.
4. No public SDK may depend on a private AETHER X repository, private endpoint, private credential, unpublished algorithm or unpublished research artifact.
5. Reference validators and schemas remain non-production unless a later artifact explicitly changes their public maturity with evidence.
6. Public compatibility does not imply integration with AETHER X Quantum, AX-OS, AIC, AETHER X Research or any other private initiative.
7. Public visibility does not create an open-source or commercial reuse licence.

## 5. Target Developer Platform Architecture

### Layer A — Governed Contract Core

The contract core should remain language-neutral and machine-readable.

It should define:

- stable schema identifiers and versions;
- normative field semantics;
- authority and evidence invariants;
- deterministic validation expectations where applicable;
- canonical error categories;
- compatibility and deprecation rules;
- conformance vectors.

If a network API is later approved, its externally supported HTTP surface should be described by a machine-readable API contract such as OpenAPI. An API specification must not be created merely to imply that a production service exists.

### Layer B — Developer Experience

The public developer path includes:

- one canonical Quickstart;
- minimal runnable examples;
- deterministic success and failure behavior;
- contract/reference documentation;
- conformance paths;
- a public/private dependency-boundary checker;
- a clean-environment developer-experience runner;
- a directly verified Python 3.10–3.13 reference-experience matrix.

DEV-GATE-01 closure establishes reproducibility of this bounded public reference experience. It does not create SDK support commitments.

### Layer C — SDK Candidate

DEV-GATE-02 establishes a bounded repository-local Python SDK candidate because the current public reference implementations and Quickstart already use Python and the candidate can remain aligned with the language-neutral contract surface.

The established candidate:

- exposes explicit typed result abstractions;
- maps only to the three declared public contract paths;
- preserves original reference findings;
- maps selected findings into the declared `AXDEV-*` taxonomy;
- fails explicitly for unsupported contracts and versions;
- exposes no production execution, credential, network or product API;
- remains non-distributable and without an approved package identity.

The verified candidate runtime matrix is Python 3.10–3.13 under `AX-PUB-CI-005`. This is a bounded candidate compatibility result, not a general package-support policy.

A future second language should be demand-driven after the language-neutral contract and compatibility surface are stable. Multi-language expansion must not multiply inconsistent semantics.

### Layer D — Conformance & Compatibility

Every supported SDK behavior should be traceable to a public contract and testable behavior.

The target chain is:

```text
SPECIFICATION
→ MACHINE-READABLE CONTRACT
→ SDK BEHAVIOR
→ CONFORMANCE CASE
→ CI RESULT
→ RELEASE EVIDENCE
```

Required mechanisms should include:

- semantic versioning once a public API is declared;
- pre-release versioning while the supported API remains unstable;
- compatibility matrices;
- breaking-change detection;
- regression suites;
- deterministic conformance vectors where applicable;
- deprecation and migration policy before stable release.

### Layer E — Security & Software Supply Chain

Before public package distribution, release engineering should establish:

- least-privilege CI permissions;
- protected release workflows;
- dependency and licence inventory;
- SBOM generation for distributable artifacts where applicable;
- build provenance / artifact attestations;
- verifiable release-origin instructions for consumers;
- dependency vulnerability review and update policy;
- secret scanning and secret-free public builds;
- reproducible or otherwise traceable build procedures appropriate to the package;
- explicit incident and vulnerability-reporting boundary.

Security evidence must not be described as a certification unless an actual certification exists.

### Layer F — Observability & Operability

If the future developer surface includes runtime services, remote calls or operational integrations, observability should use vendor-neutral telemetry conventions where justified.

Potential signals include:

- traces for request / operation paths;
- metrics for reliability and latency;
- structured logs for diagnosable events;
- correlation identifiers that preserve evidence and authority boundaries without leaking sensitive material.

Static libraries should not acquire unnecessary runtime telemetry merely to appear sophisticated.

### Layer G — Ecosystem & Integration Surface

Ecosystem work begins only after the core contract is stable enough to avoid exporting churn.

Possible later surfaces include:

- integration examples;
- adapters built against the public contract;
- partner-facing implementation guides;
- compatibility test packs;
- reference integration patterns;
- issue / discussion templates for developer feedback;
- public roadmap and deprecation communication where support authority exists.

No named partner, adoption result or integration may be claimed without evidence.

## 6. Program Gates

### DEV-GATE-00 — Contract Baseline

**Current state:** `CLOSED`

Closure is established by:

- [`AX-PUB-DEV-002 — Developer Contract Baseline`](./AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md);
- machine-readable companion `artifacts/AX-PUB-DEV-002.json`;
- [`AX-PUB-CI-003`](../evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md).

Closing this gate establishes only the public developer contract baseline. It does not establish an SDK candidate or SDK release.

### DEV-GATE-01 — Reproducible Developer Experience

**Current state:** `CLOSED`

Closure is established by:

- [`AX-PUB-DEV-003 — Reproducible Developer Experience`](./AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md);
- machine-readable companion `artifacts/AX-PUB-DEV-003.json`;
- canonical runner `tools/check_developer_experience.py`;
- closed-state checker `tools/check_developer_experience_state.py`;
- [`AX-PUB-CI-004`](../evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md).

The directly verified Gate-01 reference-experience runtime matrix is:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

Closing this gate establishes only a reproducible public reference developer experience. It does not establish an SDK candidate, supported package, production API or general Python support commitment.

### DEV-GATE-02 — SDK Candidate

**Current state:** `CLOSED`

Closure is established by:

- [`AX-PUB-DEV-004 — SDK Candidate Engineering Baseline`](./AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md);
- machine-readable companion `artifacts/AX-PUB-DEV-004.json`;
- repository-local candidate module `sdk-candidate/python/aetherx_sdk_candidate.py`;
- unit and candidate-conformance tests;
- public/private candidate boundary checker;
- closed-state governance checker;
- [`AX-PUB-CI-005`](../evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md).

The directly verified bounded candidate runtime matrix is:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

Passing this gate establishes `SDK CANDIDATE`, not `SUPPORTED SDK`.

### DEV-GATE-03 — Supply-Chain & Release Candidate

**Current state:** `ACTIVE ENGINEERING OBJECTIVE`

Exit requires:

- controlled build workflow;
- dependency inventory;
- SBOM where applicable;
- provenance / artifact attestation for candidate distributables;
- release integrity verification instructions;
- protected publication path design;
- vulnerability-reporting path;
- no private repository dependency.

Beginning DEV-GATE-03 does not authorize registry publication, approve a package identity, select a licence or create a supported release commitment.

### DEV-GATE-04 — External Evaluation Readiness

Exit requires:

- installation and integration instructions usable without internal assistance;
- known limitations and unsupported uses;
- migration/deprecation draft;
- feedback and issue triage process;
- testable compatibility claims only;
- no support promises beyond explicitly approved scope.

External evaluators may be invited only when appropriate. Their existence or results must not be invented.

### DEV-GATE-05 — SDK Release Decision

This gate is subordinate to `AX-PUB-GATE-001` and requires explicit release authority.

At minimum it must resolve:

- licensing / IP terms;
- package identity and registry;
- supported language/runtime versions;
- public API and compatibility commitment;
- security and credential boundary;
- maintenance owner and support window;
- release process and signing/provenance controls;
- conformance evidence;
- material limitations.

Only an explicit authorized decision may change the public state from `SDK PUBLICATION NOT AUTHORIZED`.

## 7. Proposed Engineering Quality Targets

The following are program targets, not claims of current achievement except where a separate artifact explicitly records verified evidence:

- clean-environment time-to-first-success measured and kept intentionally low;
- `100%` of declared supported SDK behaviors mapped to a normative contract or explicitly documented extension;
- `100%` of supported release candidates covered by the required conformance suite;
- `100%` of distributable release artifacts accompanied by required provenance and SBOM evidence once package distribution is authorized;
- zero private-repository runtime/build dependency in the public developer path;
- zero long-lived package-registry credential requirement where trusted short-lived publishing is available and approved;
- automated detection of declared breaking changes before release;
- explicit supported-runtime matrix and deprecation policy before stable `1.0.0`;
- release artifacts immutable once published; fixes require a new version.

Targets must be measured before they are represented as outcomes.

## 8. Versioning Strategy

Until a stable supported public API is explicitly approved, any SDK candidate should remain in a pre-stable version line such as `0.y.z`.

A future `1.0.0` would mean that AETHER X has explicitly declared the supported public API and the associated compatibility commitment. It must not be used as a maturity marketing label.

Versioning should distinguish:

```text
PATCH = backward-compatible bug fix
MINOR = backward-compatible capability addition
MAJOR = incompatible supported-API change
```

Pre-release identifiers should be used for release candidates where appropriate.

## 9. Package Distribution Strategy

No package name or registry is approved by this document.

For a future Python package, the preferred security direction is automated publishing from a protected GitHub Actions release workflow using short-lived OIDC-based trusted publishing rather than a long-lived registry API token, subject to the final release-security decision.

A production package should not be published directly from an engineer workstation as the normal release path.

## 10. External Standards Reference Baseline

The program should track current primary standards/documentation rather than copy their semantics into AETHER X governance.

Relevant external references at program initiation include:

- Semantic Versioning 2.0.0 — https://semver.org/
- OpenAPI Specification — https://spec.openapis.org/oas/
- SLSA v1.2 — https://slsa.dev/spec/v1.2/
- GitHub Artifact Attestations — https://docs.github.com/en/actions/concepts/security/artifact-attestations
- OpenSSF Scorecard — https://openssf.org/scorecard/
- OpenTelemetry — https://opentelemetry.io/docs/
- PyPI Trusted Publishing — https://docs.pypi.org/trusted-publishers/

Use of these references does not establish compliance, certification or conformance unless separately tested and evidenced.

## 11. Build / Buy / Adopt Principle

AETHER X should build the layers that encode its differentiated governed-intelligence semantics:

- evidence contracts;
- authority semantics;
- verification semantics;
- conformance logic;
- governed developer abstractions.

Commodity infrastructure should normally be adopted rather than reinvented when it meets requirements, including package standards, CI infrastructure, build provenance, SBOM formats, telemetry standards and registry mechanisms.

The objective is differentiated intelligence engineering, not proprietary reinvention of commodity developer infrastructure.

## 12. Failure Modes to Prevent

The program must actively prevent:

- publishing an SDK before licensing/IP authority exists;
- treating executable reference code as a support promise;
- freezing an unstable API too early;
- language proliferation before the contract is stable;
- documentation diverging from executable behavior;
- release artifacts with unclear origin;
- long-lived release credentials where safer mechanisms are available;
- private implementation leakage into the public developer surface;
- compatibility claims not backed by tests;
- ecosystem claims not backed by external evidence;
- security or standards language being presented as certification.

## 13. Current Program State

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-03 — SUPPLY-CHAIN & RELEASE CANDIDATE
DEVELOPER PLATFORM: NOT RELEASED
SDK CANDIDATE: ESTABLISHED
PUBLIC SDK: NOT PUBLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
AX-PUB-GATE-001: SDK PUBLICATION NOT AUTHORIZED
```

`AX-PUB-CI-003` records the directly observed validation evidence used to close DEV-GATE-00.

`AX-PUB-CI-004` records the directly observed clean-environment runtime-matrix and public-governance evidence used to close DEV-GATE-01.

`AX-PUB-CI-005` records the directly observed SDK-candidate runtime-matrix, candidate conformance, public-boundary and governance evidence used to close DEV-GATE-02.

The current program position is:

```text
CANDIDATE
```

This means a bounded repository-local SDK candidate is established for the declared public contract surface. It does not mean a package is published, supported, licensed for general reuse, production-ready or approved for registry distribution.

## 14. Promotion Principle

Developer adoption is evidence of usable engineering, not a marketing label.

Progress should be promoted only when the corresponding developer path is independently reproducible and its claims are supported by tests or release evidence.

```text
REFERENCE
→ CONTRACTED
→ REPRODUCIBLE
→ CANDIDATE
→ RELEASE-CANDIDATE VALIDATED
→ AUTHORIZED
→ SUPPORTED
```

Current position:

```text
CANDIDATE
```

The next promotion target is `RELEASE-CANDIDATE VALIDATED`, governed by DEV-GATE-03. No later state may be inferred from an earlier one.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
