# AX-PUB-DEV-007 — SDK Release Decision Baseline

**Artifact ID:** `AX-PUB-DEV-007`  
**Version:** `0.1`  
**Status:** `DEV-GATE-05A CLOSED · DEV-GATE-05B ACTIVE · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Governing gate:** `AX-PUB-GATE-001`

## 1. Purpose

This artifact establishes the bounded release strategy and engineering decision baseline for `DEV-GATE-05 — SDK Release Decision`.

`DEV-GATE-05A` is now closed on direct CI evidence recorded in `AX-PUB-CI-008`. The current engineering objective is `DEV-GATE-05B — Installable Package Candidate`.

This does **not** authorize package publication.

The objective is to convert the validated repository-local SDK candidate into a release-capable package candidate without silently creating production, support, licensing, security or compatibility commitments.

```text
GATE-04 READINESS
→ RELEASE STRATEGY                  [DEV-GATE-05A CLOSED]
→ PACKAGE CANDIDATE                 [DEV-GATE-05B ACTIVE]
→ DISTRIBUTION VALIDATION
→ HUMAN EXTERNAL EVALUATION
→ RELEASE EVIDENCE PACK
→ EXPLICIT RELEASE AUTHORITY
→ PUBLICATION
```

`DEV-GATE-05A CLOSED ≠ DEV-GATE-05 CLOSED`  
`DEV-GATE-05 ACTIVE ≠ SDK RELEASE AUTHORIZED`

## 2. Decision Summary

The following technical strategy is selected for Gate-05 engineering.

### DEC-05-01 — Release scope

The first public SDK scope is **offline governed-intelligence validation only**.

Included:

- validation of the three declared public contract paths;
- stable developer-facing result and finding types;
- deterministic fail-closed validation semantics;
- contract inventory and version inspection;
- local machine-readable validation only.

Explicitly excluded from the first release scope:

- network API calls;
- remote services;
- credentials or secrets;
- authentication;
- production authorization decisions;
- tool invocation;
- brokerage, financial, infrastructure or real-world execution;
- background agents;
- telemetry that is not required for local validation;
- private AETHER X repositories or endpoints.

This keeps the first SDK surface small, auditable and low-blast-radius.

### DEC-05-02 — Open SDK / Controlled Core

Selected licensing direction for the **SDK distribution only**:

```text
TARGET SDK LICENCE: Apache License 2.0
CURRENT LICENCE STATE: NO SDK REUSE LICENCE GRANTED YET
LICENCE ATTACHMENT: BLOCKED UNTIL IP / COPYRIGHT AUTHORITY IS CONFIRMED
```

Rationale:

- permissive enterprise adoption;
- explicit copyright permissions;
- explicit patent grant and patent-termination mechanism;
- broad ecosystem compatibility;
- no implied trademark licence;
- lower developer friction than a custom source-available licence.

The selected direction does **not** relicense the whole repository.

Unless a later explicit decision says otherwise:

- repository-wide public specifications remain under their existing no-general-reuse boundary;
- private AETHER X code remains private;
- AETHER X names, logos and marks are outside the software licence grant;
- only files intentionally included in the released SDK distribution may receive the SDK licence.

No Apache-2.0 `LICENSE` file is to be attached to the candidate package until legal/IP authority confirms AETHER X has the right to grant that licence over every distributed file.

### DEC-05-03 — Distribution and import identity

The selected **candidate** distribution identity is:

```text
PyPI distribution candidate: aetherxglobal-governed-intelligence
Python import namespace:      aetherxglobal.governed_intelligence
```

Reasoning:

- `AetherX` already exists as an unrelated PyPI project and must not be used as the AETHER X GLOBAL package identity;
- the `aetherxglobal` prefix aligns with the GitHub organization and creates a scalable company namespace;
- the domain suffix keeps this SDK separate from future product-specific or unrelated AETHER X packages.

Before any registry reservation or publication, the exact normalized PyPI name must be checked directly against PyPI at the time of action. Search-engine absence is not sufficient evidence of availability.

Canonical registry decision:

```text
STAGING / DISTRIBUTION VALIDATION: TestPyPI
PUBLIC CANONICAL PYTHON REGISTRY: PyPI
SOURCE / RELEASE EVIDENCE: GitHub
```

A GitHub Release is not a substitute for the canonical Python package index.

### DEC-05-04 — Runtime support

Target supported runtime set for the first package candidate:

```text
CPython 3.11
CPython 3.12
CPython 3.13
CPython 3.14
```

Python 3.10 remains historical Gate-01/Gate-02 validation evidence but is **not** selected for the new supported SDK contract because its upstream support ends in October 2026.

Python 3.15 is not selected while it remains pre-release.

A support claim may be made only after direct package-level CI validates the exact wheel/sdist installation path on the declared runtime set.

### DEC-05-05 — Versioning

The package must use PEP 440-compatible versions.

Gate-05 package-candidate sequence:

```text
0.1.0rc1  → first distributable release candidate
0.1.0rcN  → corrected release candidates when required
0.1.0     → only after DEV-GATE-05 closure and explicit release authority
```

`0.1.0rc1` is not equivalent to the existing repository-local string `0.1.0-candidate`.

The public SDK API must be explicit. Accidental internal imports must not become supported merely because Python can import them.

For the `0.x` lifecycle:

- patch releases preserve the declared public surface except for security/correctness fixes that cannot safely remain compatible;
- minor releases may evolve the API but require migration notes for material changes;
- deprecation should precede planned removal where practical;
- `1.0.0` is reserved for a separately approved stable compatibility contract.

### DEC-05-06 — Package architecture

The release candidate must use a standard `src/` package layout and must not rely on repository-relative imports at runtime.

Target structure:

```text
sdk-release-candidate/python/
├── pyproject.toml
├── README.md
├── src/
│   └── aetherxglobal/
│       └── governed_intelligence/
│           ├── __init__.py
│           ├── _contracts/
│           ├── _validators/
│           └── ...
└── tests/
```

The package must be self-contained from the installed wheel.

Runtime dependency target for `0.1.0`:

```text
THIRD-PARTY RUNTIME DEPENDENCIES: 0
```

Build tooling is separate from runtime dependency policy.

Selected build-system direction:

- PEP 517 / PEP 621 via `pyproject.toml`;
- `hatchling` as the initial build-backend candidate;
- build tooling must be version-constrained in the release workflow;
- the exact wheel and sdist produced by the controlled build must be the artifacts that are tested and later published.

If reproducibility or package-data requirements show that another standards-compliant backend is materially better, changing the backend requires a recorded Gate-05 engineering decision and fresh build evidence.

### DEC-05-07 — Supply-chain and publication security

The public release workflow must satisfy all of the following before production publication:

1. GitHub Actions `permissions` are minimum-required.
2. Third-party and GitHub-maintained actions used in release-sensitive jobs are pinned to reviewed full commit SHAs.
3. Package build occurs in CI, not on a maintainer laptop.
4. The built wheel and sdist are immutable inputs to subsequent test and publish jobs.
5. The exact built distributions are installed and tested before publication.
6. GitHub provenance attestation is generated for release artifacts.
7. An SBOM is generated and associated with release evidence where technically appropriate.
8. PyPI publication uses **Trusted Publishing / OIDC**; long-lived PyPI API tokens are not the primary release credential.
9. PyPI digital attestations are retained as release provenance.
10. Production PyPI publication runs only through a protected GitHub environment.
11. Release publication requires human approval independent of the job that built the artifact when platform controls allow it.
12. A release workflow must never use `pull_request_target` with untrusted code in the publication path.

Target release flow:

```text
TAG / AUTHORIZED RELEASE INPUT
→ BUILD ONCE
→ HASH / MANIFEST / SBOM
→ UNIT + CONFORMANCE TEST EXACT DISTRIBUTIONS
→ INSTALL TEST ON DECLARED PYTHON MATRIX
→ TESTPYPI VALIDATION
→ EXTERNAL EVALUATION EVIDENCE
→ PROTECTED APPROVAL
→ PYPI TRUSTED PUBLISHING
→ VERIFY PYPI + GITHUB PROVENANCE
→ RECORD RELEASE EVIDENCE
```

### DEC-05-08 — Main-branch and release-control hard gate

Before public SDK publication, the repository must have a branch/ruleset control that prevents uncontrolled direct release-state changes.

Minimum target controls:

- pull request required for protected release-relevant paths;
- at least one independent approval for material release changes;
- required status checks for Gate-05 release validation;
- stale approvals invalidated after material changes where supported;
- release tags protected or otherwise restricted to authorized release flow;
- production package publication restricted to a protected `pypi` environment;
- self-approval of production publication disabled where supported.

The current `main` branch protection state is not sufficient for final release and is a **hard release blocker**.

### DEC-05-09 — External evaluation before public 0.1.0

Gate-04 established readiness for human external evaluation; it did not establish that evaluation occurred.

Before `0.1.0` publication, require at least one independent external technical evaluation of the installable release-candidate path with:

- evaluator identity or bounded evaluation record;
- candidate version and artifact digest;
- environment/runtime used;
- machine-readable evaluation result;
- defects and limitations found;
- disposition of any material findings.

No unresolved critical issue may remain. Any high-severity issue must either be fixed or explicitly accepted by authorized release authority with a documented rationale.

### DEC-05-10 — Maintenance and support boundary

For the initial `0.x` public SDK:

- no commercial SLA is implied;
- the latest minor series is the primary maintained line;
- the immediately previous minor receives security/correctness fixes for up to 90 days after a successor minor is released when a fix is technically feasible;
- planned breaking removals should receive migration guidance;
- security reporting continues through the repository security process;
- support does not include private product integration, deployment consulting or production authorization systems.

A later commercial or enterprise support contract requires a separate decision.

### DEC-05-11 — Contribution boundary

The first release does not require open contribution rights to all repository content.

If external code contributions to the SDK are accepted, contribution terms must be explicit before merge. The preferred low-friction direction is:

- SDK contributions under the same Apache-2.0 terms;
- contributor representation that the contribution may legally be submitted;
- a DCO-style sign-off or equivalent contribution control unless a later legal decision requires a CLA.

No contributor policy is considered active merely because this direction is recorded.

### DEC-05-12 — Final release authority

This decision baseline authorizes Gate-05 engineering work only.

It does not authorize:

- attaching a public software licence before IP clearance;
- reserving or publishing a PyPI project;
- publishing to TestPyPI if doing so creates an unwanted public package identity before package-name review;
- publishing `0.1.0`;
- claiming external adoption;
- claiming a supported production integration surface.

Final publication requires a separate explicit release decision tied to the exact release evidence pack.

## 3. Gate-05 Work Breakdown

### DEV-GATE-05A — Release Decision Baseline

**Current state:** `CLOSED`

Goal: establish the release strategy, boundaries and hard gates.

Closure is established by:

- this artifact;
- machine-readable companion `artifacts/AX-PUB-DEV-007.json`;
- fail-closed checker `tools/check_sdk_release_decision_baseline.py`;
- direct CI evidence [`AX-PUB-CI-008`](../evidence/AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md) across CPython 3.11–3.14.

Closing Gate-05A establishes only the SDK release-decision baseline. It does not grant a software licence, establish package ownership, establish an installable supported SDK, close DEV-GATE-05 or authorize publication.

### DEV-GATE-05B — Installable Package Candidate

**Current state:** `ACTIVE ENGINEERING OBJECTIVE`

Goal: create a self-contained wheel/sdist candidate.

Required evidence includes:

- `pyproject.toml`;
- installable `src/` package;
- exact public API declaration;
- zero-runtime-dependency evidence;
- package-level tests from installed distributions;
- source inventory and package-data verification.

### DEV-GATE-05C — Distribution & External Validation

**Current state:** `NOT ESTABLISHED`

Goal: validate the exact distribution path without production release authority.

Required evidence includes:

- package-name availability check;
- TestPyPI or equivalent controlled distribution validation after authorization;
- install-from-index verification;
- at least one human external evaluation;
- issue disposition.

### DEV-GATE-05D — Final Release Authority

**Current state:** `NOT AUTHORIZED`

Goal: make the explicit publish / do-not-publish decision.

Required evidence pack must identify:

- exact package name;
- exact version;
- exact wheel/sdist digests;
- licence/IP clearance;
- supported Python versions;
- conformance evidence;
- supply-chain provenance;
- security boundary;
- support boundary;
- external evaluation result;
- material limitations;
- release owner;
- explicit authorization.

Only Gate-05D may change the publication disposition.

## 4. Current Disposition

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: ACTIVE ENGINEERING OBJECTIVE
DEV-GATE-05C: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

## 5. Gate-05A Closure Evidence

Direct closure evidence is recorded in:

**[`AX-PUB-CI-008 — SDK Release Decision Baseline Validation Evidence`](../evidence/AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md)**

Verified baseline and CI identity:

```text
PUBLISHED CANDIDATE BASE: fa1e2d132071ddff195fb998d0d27a6b5b9d4e40
VERIFICATION HEAD:        7877abceda8fa6a372300fceb1ae0c124853d2b6
VERIFICATION PR:          #31 — CLOSED WITHOUT MERGE
GATE-05A WORKFLOW RUN:    32168696722 — SUCCESS
MANIFEST WORKFLOW RUN:    32168696655 — SUCCESS
VERIFIED RUNTIMES:        CPython 3.11 / 3.12 / 3.13 / 3.14
```

The verification-only PR used one disposable trigger and was closed without merge after evidence capture. The branch was reset to the exact published candidate baseline.

`DIRECT CI EVIDENCE ≠ SDK RELEASE AUTHORITY`

## 6. Claim Boundary

`OPEN-SOURCE DIRECTION ≠ LICENCE GRANTED`  
`PACKAGE NAME CANDIDATE ≠ REGISTRY OWNERSHIP`  
`PYTHON TARGET MATRIX ≠ VERIFIED PACKAGE SUPPORT`  
`TESTPYPI ≠ PRODUCTION RELEASE`  
`PEP 740 ATTESTATION ≠ SECURITY CERTIFICATION`  
`EXTERNAL EVALUATION ≠ EXTERNAL ADOPTION`  
`DEV-GATE-05A CLOSED ≠ DEV-GATE-05 CLOSED`  
`DEV-GATE-05B ACTIVE ≠ INSTALLABLE PACKAGE VALIDATED`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
