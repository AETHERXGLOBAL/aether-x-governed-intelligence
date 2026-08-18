# AX-PUB-DEV-008 — Installable Package Candidate

**Artifact ID:** `AX-PUB-DEV-008`  
**Version:** `0.1`  
**Status:** `DEV-GATE-05B ENGINEERING CANDIDATE · DIRECT PUBLISHED-BASELINE VALIDATION NOT YET ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Parent decision:** `AX-PUB-DEV-007 — SDK Release Decision Baseline`  
**Governing gate:** `AX-PUB-GATE-001`

## 1. Purpose

This artifact defines the bounded installable Python package candidate for `DEV-GATE-05B`.

It exists to prove that the repository-local SDK candidate can be transformed into a reproducible, self-contained Python distribution while preserving the AETHER X public/private, authority, security, licensing and publication boundaries established by earlier Gates.

```text
DEV-GATE-05A RELEASE DECISION BASELINE       [CLOSED]
→ DEV-GATE-05B INSTALLABLE PACKAGE CANDIDATE [THIS ARTIFACT]
→ DEV-GATE-05C DISTRIBUTION / EXTERNAL VALIDATION
→ DEV-GATE-05D FINAL RELEASE AUTHORITY
```

`INSTALLABLE PACKAGE CANDIDATE ≠ SUPPORTED SDK`  
`SDK PUBLICATION NOT AUTHORIZED`

## 2. Candidate Identity

```text
Distribution candidate: aetherxglobal-governed-intelligence
Version candidate:      0.1.0rc1
Import namespace:       aetherxglobal.governed_intelligence
Namespace model:        PEP 420 implicit company namespace
Target runtime:         CPython 3.11 / 3.12 / 3.13 / 3.14
Runtime dependencies:   0 third-party packages
Canonical registry:     PyPI — ownership NOT ESTABLISHED
Staging registry:       TestPyPI — publication NOT AUTHORIZED
```

The package identity is still a Gate-05 candidate. Repository presence does not establish registry ownership.

## 3. Public Capability Boundary

The candidate exposes **offline validation only** for the three declared public contract paths:

```text
AX-PUB-SPEC-002
AX-PUB-SPEC-003
AX-PUB-SPEC-004
```

It may expose developer-facing result/finding types, contract inventory and deterministic validation behavior.

It does not expose:

- a network API client;
- remote AETHER X services;
- credentials;
- authentication;
- production authorization;
- tool invocation;
- brokerage or financial execution;
- infrastructure execution;
- background agent execution;
- private product integration;
- any private AETHER X repository or endpoint dependency.

## 4. Namespace Decision

The company-level Python namespace is an implicit **PEP 420 namespace**.

The distribution intentionally omits:

```text
src/aetherxglobal/__init__.py
```

and provides:

```text
src/aetherxglobal/governed_intelligence/
```

This avoids forcing future AETHER X Python SDKs into a monolithic distribution and reduces namespace collision between independently versioned company packages.

## 5. Reference-Implementation Traceability

The packaged validator sources preserve the exact Git blob identities of the three current public reference validators:

```text
AX-PUB-REF-001 → 10b31f990cdeb0a2285081d4b4a8cc2457564c69
AX-PUB-REF-002 → f4344dfb70685b490e716e33f8f2fd2da1f0ca50
AX-PUB-REF-003 → 6c8f4d325ef3d3f2041909f8bba7d554ced4366e
```

The package facade changes how the validators are delivered and imported; it does not silently rewrite the reference-validation semantics.

## 6. Build Contract

Gate-05B uses:

- PEP 517 build semantics;
- PEP 621 project metadata;
- `src/` layout;
- Hatchling `1.31.0` as the fixed Gate-05B build-backend candidate;
- Python `build` `1.5.0` as the fixed Gate-05B CI frontend candidate;
- canonical `SOURCE_DATE_EPOCH = 1787076737`, anchored to the DEV-GATE-05A closure commit timestamp;
- wheel and sdist outputs;
- zero third-party runtime dependencies.

No software licence metadata is attached before IP/copyright clearance.

## 7. Reproducibility Contract

A Gate-05B validation run must:

1. build wheel and sdist from the same source twice;
2. prove the two wheel outputs are byte-identical;
3. prove the two sdist outputs are byte-identical;
4. rebuild a wheel from the generated sdist;
5. prove that wheel is byte-identical to the original wheel;
6. record SHA-256 digests for the exact candidate distributions;
7. preserve build metadata sufficient to identify source commit, build epoch and build tool versions.

Failure of any step means the installable package candidate is not validated.

## 8. Installed-Artifact Validation Contract

The exact first-build wheel—not a separately rebuilt wheel per runtime—must be installed using local-file installation with runtime dependency resolution disabled:

```text
--no-index --no-deps
```

The same wheel must pass the package tests on:

```text
CPython 3.11
CPython 3.12
CPython 3.13
CPython 3.14
```

The installed package must also be importable and inspectable from outside the repository source path.

This distinguishes source-tree success from real distribution behavior.

## 9. Distribution Inventory Contract

The candidate wheel must establish, at minimum:

- normalized distribution identity;
- version `0.1.0rc1`;
- `Requires-Python >=3.11,<3.15`;
- no `Requires-Dist` runtime dependencies;
- no top-level `aetherxglobal/__init__.py`;
- the declared `aetherxglobal.governed_intelligence` package;
- the three traced validator modules;
- no software licence file or metadata before clearance.

The sdist must contain enough public source to rebuild the same wheel without private repositories or private runtime dependencies.

## 10. CI Artifact Boundary

Successful candidate wheel/sdist outputs, SHA-256 records and build metadata may be retained as **short-lived GitHub Actions CI evidence** for 7 days.

This is not a GitHub Release, package registry publication or software distribution decision.

```text
CI ARTIFACT ≠ PUBLIC PACKAGE
CI RETENTION ≠ SUPPORT COMMITMENT
```

## 11. Licence / IP Boundary

Gate-05A selected Apache-2.0 as the target SDK licence direction, but no licence is granted by this artifact.

Before attaching a licence to a release distribution, AETHER X must confirm authority over the complete final distribution inventory and explicitly approve the licence grant.

```text
TARGET SDK LICENCE: Apache-2.0
LICENCE GRANTED: NO
IP / COPYRIGHT CLEARANCE: REQUIRED
REPOSITORY-WIDE RELICENSING: NO
```

## 12. Gate-05B Closure Requirements

`DEV-GATE-05B` may close only after direct validation of the **published candidate baseline** establishes:

- package-boundary pass;
- exact validator-source identity;
- PEP 420 namespace pass;
- deterministic double build;
- byte-identical sdist-to-wheel rebuild;
- valid wheel/sdist inventory;
- exact candidate SHA-256 digests;
- installed-package tests on CPython 3.11–3.14;
- installed-package operation outside repository source paths;
- short-lived CI artifact evidence;
- preserved Gate-03, Gate-04 and Gate-05A governance;
- `SDK PUBLICATION NOT AUTHORIZED` throughout.

Pre-merge PR success is engineering evidence only. Gate closure requires the same published-baseline verification discipline used by prior AETHER X developer-program gates.

## 13. What Gate-05B Does Not Establish

Even after successful closure, Gate-05B will not by itself establish:

- PyPI/TestPyPI ownership;
- a public software licence grant;
- registry publication;
- human external evaluation;
- external adoption;
- production API/authentication/authorization;
- protected production publishing controls;
- a supported SDK;
- DEV-GATE-05 closure;
- final SDK release authority.

Those remain later Gate-05 responsibilities.

---

`DETERMINISTIC PACKAGE ≠ PUBLIC RELEASE`  
`PACKAGE CANDIDATE ≠ SUPPORTED SDK`  
`DEV-GATE-05B ≠ DEV-GATE-05D`  
`SDK PUBLICATION NOT AUTHORIZED`

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
