# AX-PUB-DEV-008 — Installable Package Candidate

**Artifact ID:** `AX-PUB-DEV-008`  
**Version:** `0.1`  
**Status:** `DEV-GATE-05B CLOSED · DEV-GATE-05C ACTIVE · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Parent decision:** `AX-PUB-DEV-007 — SDK Release Decision Baseline`  
**Governing gate:** `AX-PUB-GATE-001`

## 1. Purpose

This artifact defines and records closure of the bounded installable Python package candidate for `DEV-GATE-05B`.

Closure is supported by direct published-baseline validation recorded in [`AX-PUB-CI-009`](../evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md).

```text
DEV-GATE-05A RELEASE DECISION BASELINE       [CLOSED]
→ DEV-GATE-05B INSTALLABLE PACKAGE CANDIDATE [CLOSED]
→ DEV-GATE-05C DISTRIBUTION / EXTERNAL VALIDATION [ACTIVE]
→ DEV-GATE-05D FINAL RELEASE AUTHORITY       [NOT AUTHORIZED]
```

`DEV-GATE-05B CLOSED ≠ SUPPORTED SDK`  
`SDK PUBLICATION NOT AUTHORIZED`

## 2. Verified Candidate Identity

```text
Distribution candidate: aetherxglobal-governed-intelligence
Version candidate:      0.1.0rc1
Import namespace:       aetherxglobal.governed_intelligence
Namespace model:        PEP 420 implicit company namespace
Verified runtime:       CPython 3.11 / 3.12 / 3.13 / 3.14
Runtime dependencies:   0 third-party packages
Canonical registry:     PyPI — ownership NOT ESTABLISHED
Staging registry:       TestPyPI — publication NOT AUTHORIZED
```

The package identity remains a Gate-05 candidate. Repository presence and package validation do not establish registry ownership.

## 3. Public Capability Boundary

The validated candidate exposes **offline validation only** for:

```text
AX-PUB-SPEC-002
AX-PUB-SPEC-003
AX-PUB-SPEC-004
```

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

## 4. Namespace Architecture

The company-level Python namespace is an implicit **PEP 420 namespace**.

The distribution intentionally omits:

```text
src/aetherxglobal/__init__.py
```

and provides:

```text
src/aetherxglobal/governed_intelligence/
```

This preserves room for future independently versioned AETHER X Python SDK distributions under the `aetherxglobal.*` namespace.

## 5. Reference-Implementation Traceability

The packaged validator sources preserve the exact Git blob identities of the current public reference validators:

```text
AX-PUB-REF-001 → 10b31f990cdeb0a2285081d4b4a8cc2457564c69
AX-PUB-REF-002 → f4344dfb70685b490e716e33f8f2fd2da1f0ca50
AX-PUB-REF-003 → 6c8f4d325ef3d3f2041909f8bba7d554ced4366e
```

The package facade changes delivery/import mechanics without silently rewriting the reference-validation semantics.

## 6. Verified Build Contract

Gate-05B validation used:

- PEP 517 build semantics;
- PEP 621 project metadata;
- `src/` layout;
- Hatchling `1.31.0`;
- Python `build` `1.5.0`;
- canonical `SOURCE_DATE_EPOCH = 1787076737`;
- wheel and sdist outputs;
- zero third-party runtime dependencies.

No software licence metadata was attached.

Direct validation established:

1. two wheel + sdist builds from the same source;
2. byte-identical wheel rebuilds;
3. byte-identical sdist rebuilds;
4. wheel rebuild from the generated sdist;
5. byte identity between the sdist-rebuilt wheel and the direct wheel;
6. exact SHA-256 identities;
7. exact-wheel tests across all declared runtimes;
8. inherited Gate-03, Gate-04, Gate-05A and Manifest preservation.

## 7. Exact Validated Distribution Identity

### Wheel

```text
Filename:
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl

SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac
```

### Source distribution

```text
Filename:
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz

SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

These hashes identify the validated **CI candidate artifacts only**.

## 8. Installed-Artifact Validation

The exact same wheel was installed with:

```text
--no-index --no-deps
```

and passed package tests on:

```text
CPython 3.11
CPython 3.12
CPython 3.13
CPython 3.14
```

The installed package was also validated outside the repository source path.

## 9. CI Artifact Evidence

The successful direct verification run retained the candidate distributions as a seven-day GitHub Actions artifact:

```text
Artifact ID:     9337474216
Artifact name:   ax-pub-dev-008-3267c66681e417bf5eb0f8a384e8c2d992d266c0
Artifact digest: sha256:9b2e050d59146e2b768cb5f9468b2035c078aa1abbb4e0fd0ac4148e8d58d4a2
Retention:       7 days
```

`CI ARTIFACT ≠ PUBLIC PACKAGE`

## 10. Direct Closure Evidence

Closure evidence is recorded in:

**[`AX-PUB-CI-009 — Installable Package Candidate Validation Evidence`](../evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md)**

```text
PUBLISHED BASELINE:       774abcce340c3fbaf3481ab5244ee1d41b88243c
VERIFICATION HEAD:        63477bb11124aebbad4034587a366d5ef882b3c2
VERIFICATION MERGE:       3267c66681e417bf5eb0f8a384e8c2d992d266c0
VERIFICATION PR:          #36 — CLOSED WITHOUT MERGE
GATE-05B WORKFLOW RUN:    32171606094 / #19 — SUCCESS
GATE-05B JOB:             95823835258 — SUCCESS
MANIFEST WORKFLOW RUN:    32171606079 / #168 — SUCCESS
VERIFIED RUNTIMES:        CPython 3.11 / 3.12 / 3.13 / 3.14
```

## 11. Licence / IP Boundary

Gate-05A selected Apache-2.0 as the target SDK licence direction, but **no licence is granted** by Gate-05B closure.

```text
TARGET SDK LICENCE: Apache-2.0
LICENCE GRANTED: NO
IP / COPYRIGHT CLEARANCE: REQUIRED
REPOSITORY-WIDE RELICENSING: NO
```

## 12. What Gate-05B Closure Establishes

Gate-05B closure establishes only that the bounded installable package candidate has direct evidence for:

- deterministic package construction;
- exact wheel/sdist identities;
- self-contained sdist-to-wheel rebuild;
- PEP 420 namespace behavior;
- zero runtime third-party dependencies;
- CPython 3.11–3.14 installed-package behavior;
- preservation of the declared public/private and inherited governance boundaries.

## 13. What Gate-05B Closure Does Not Establish

It does **not** establish:

- PyPI/TestPyPI ownership;
- package-name reservation;
- a public software licence grant;
- registry publication;
- Trusted Publishing configuration;
- protected production publishing controls;
- human external evaluation;
- external adoption;
- production API/authentication/authorization;
- a supported SDK;
- a support SLA;
- DEV-GATE-05 closure;
- final SDK release authority.

Those remain later Gate-05 responsibilities.

## 14. Current Next Phase

```text
DEV-GATE-05:  ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: CLOSED
DEV-GATE-05C: ACTIVE — DISTRIBUTION & EXTERNAL VALIDATION
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

Gate-05C must now resolve distribution identity/ownership and external validation without turning technical readiness into a release claim.

---

`DETERMINISTIC PACKAGE ≠ PUBLIC RELEASE`  
`PACKAGE CANDIDATE ≠ SUPPORTED SDK`  
`DEV-GATE-05B CLOSED ≠ DEV-GATE-05 CLOSED`  
`SDK PUBLICATION NOT AUTHORIZED`

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
