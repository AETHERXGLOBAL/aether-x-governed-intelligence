# AX-PUB-CI-009 — Installable Package Candidate Validation Evidence

**Artifact ID:** `AX-PUB-CI-009`  
**Version:** `1.0`  
**Scope:** `DEV-GATE-05B — Installable Package Candidate`  
**Evidence state:** `DIRECT CI VALIDATION OF PUBLISHED CANDIDATE BASELINE · GATE NOT YET CLOSED AT TIME OF EVIDENCE CAPTURE`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This record captures direct GitHub Actions evidence for the published `DEV-GATE-05B` installable Python package candidate while preserving the separation between package validation, Gate closure, registry distribution, software licensing and SDK release authority.

```text
DETERMINISTIC PACKAGE VALIDATION
≠ DEV-GATE-05B CLOSURE
≠ DEV-GATE-05 CLOSURE
≠ SUPPORTED SDK
≠ SOFTWARE LICENCE GRANT
≠ REGISTRY RELEASE
≠ SDK PUBLICATION AUTHORITY
```

## 2. Published Candidate Baseline

The exact published Gate-05B baseline validated by this evidence is:

```text
774abcce340c3fbaf3481ab5244ee1d41b88243c
```

The published baseline contains:

- `AX-PUB-DEV-008 — Installable Package Candidate`;
- machine-readable `artifacts/AX-PUB-DEV-008.json`;
- the self-contained Python package candidate under `sdk-release-candidate/python/`;
- PEP 420 company namespace architecture;
- package/document fail-closed checkers;
- Gate-03 forward-compatible package-metadata guard;
- hardened Gate-05B deterministic-package CI.

At evidence capture, the public state remained:

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: ENGINEERING CANDIDATE / NOT YET CLOSED
DEV-GATE-05C: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
LICENCE GRANTED: NO
REGISTRY OWNERSHIP: NOT ESTABLISHED
```

## 3. Verification Method

A verification-only branch was created from the exact published baseline.

The only verification change was one disposable machine-readable field:

```text
verification_trigger = VERIFY_PUBLISHED_GATE_05B_BASELINE_ONLY
```

It did not change:

- package source;
- package metadata;
- package version;
- public API;
- runtime target;
- release scope;
- licensing direction;
- registry state;
- Gate state;
- support boundary;
- publication disposition;
- release authority.

Verification branch head:

```text
63477bb11124aebbad4034587a366d5ef882b3c2
```

GitHub pull-request synthetic merge commit used by the successful verification job:

```text
3267c66681e417bf5eb0f8a384e8c2d992d266c0
```

Verification PR:

```text
#36 — CI verification: published DEV-GATE-05B installable package baseline
```

The PR was closed **without merge** after successful evidence capture. The verification branch was then reset to the exact published baseline commit.

## 4. Primary Gate-05B Workflow Evidence

```text
Workflow: Validate SDK Release Candidate
Run ID: 32171606094
Run number: 19
Job ID: 95823835258
Conclusion: SUCCESS
```

The successful run directly validated the following sequence:

1. Gate-05B document integrity;
2. Gate-05B package and parent-Gate boundaries;
3. closed DEV-GATE-05A state;
4. closed DEV-GATE-03 supply-chain state;
5. closed DEV-GATE-04 external-evaluation-readiness state;
6. current public artifact-manifest governance;
7. exact Gate-05B build toolchain;
8. two independent wheel + sdist builds from the same source;
9. byte-identical comparison of both build outputs;
10. wheel rebuild from the generated sdist;
11. byte-identical comparison of the sdist-rebuilt wheel with the original wheel;
12. wheel/sdist metadata and inventory checks;
13. PEP 420 namespace validation;
14. zero third-party runtime dependency validation;
15. exact candidate SHA-256 recording;
16. installation of the exact same wheel on CPython 3.11, 3.12, 3.13 and 3.14;
17. installed-package tests on each declared runtime;
18. installed-package validation outside the repository source path;
19. removal of ephemeral build/test workspaces;
20. post-build revalidation of Gate-05B and the inherited governance chain;
21. preservation of the candidate distributions as a seven-day GitHub Actions CI artifact;
22. explicit preservation of `SDK PUBLICATION NOT AUTHORIZED`.

Observed success markers include:

```text
AX_SDK_RELEASE_CANDIDATE_DOC_PASS
AX_SDK_RELEASE_CANDIDATE_BOUNDARY_PASS
AX_SDK_BUILD_TOOLCHAIN_PASS build=1.5.0 hatchling=1.31.0
AX_SDK_DETERMINISTIC_DOUBLE_BUILD_PASS artifacts=2
AX_SDK_SDIST_SELF_CONTAINED_REBUILD_PASS wheel=byte-identical
AX_SDK_DISTRIBUTION_INVENTORY_PASS namespace=PEP420 runtime_dependencies=0 licence_granted=false
AX_SDK_INSTALLED_OUTSIDE_REPOSITORY_PASS namespace=aetherxglobal.governed_intelligence
AX_SDK_EPHEMERAL_WORKSPACE_CLEANUP_PASS
AX_DEV_GATE_03_CLOSED_STATE_PASS
AX_DEV_GATE_04_CLOSED_STATE_PASS
AX_SDK_RELEASE_DECISION_BASELINE_CLOSED_STATE_PASS
```

## 5. Exact Candidate Distribution Identity

The successful verification run produced the following exact candidate distributions.

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

The `SHA256SUMS` file preserved inside the GitHub Actions artifact records the same two digests.

These hashes identify the **validated CI candidate artifacts only**. They do not establish registry publication or a supported release.

## 6. Build Identity

The run-preserved `BUILD_INFO.json` records:

```text
Artifact ID:       AX-PUB-DEV-008-CI-BUILD
Source commit:     3267c66681e417bf5eb0f8a384e8c2d992d266c0
SOURCE_DATE_EPOCH: 1787076737
Builder Python:    3.14.7
Build frontend:    build 1.5.0
Build backend:     hatchling 1.31.0
Publication:       NOT AUTHORIZED
Registry release:  FALSE
```

The source commit above is the GitHub-generated synthetic merge commit for verification PR #36. The underlying published source baseline remains `774abcce340c3fbaf3481ab5244ee1d41b88243c`; the PR changed only the disposable verification trigger.

## 7. GitHub Actions Artifact Evidence

The successful run retained the candidate package outputs as a short-lived GitHub Actions artifact:

```text
Artifact ID:      9337474216
Artifact name:    ax-pub-dev-008-3267c66681e417bf5eb0f8a384e8c2d992d266c0
Artifact size:    36112 bytes
Retention:        7 days
Expires:          2026-08-25T18:33:22Z
Artifact digest:  sha256:9b2e050d59146e2b768cb5f9468b2035c078aa1abbb4e0fd0ac4148e8d58d4a2
```

The artifact contains:

```text
BUILD_INFO.json
SHA256SUMS
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz
```

`CI ARTIFACT ≠ GITHUB RELEASE ≠ PYPI RELEASE`

## 8. Runtime and Package Contract Established by This Evidence

The evidence supports the bounded statement that this exact Gate-05B package candidate:

- is self-contained as a Python wheel/sdist candidate;
- uses `aetherxglobal.governed_intelligence` under an implicit PEP 420 `aetherxglobal` namespace;
- declares no third-party runtime dependencies;
- preserves the exact current source identities of `AX-PUB-REF-001`, `AX-PUB-REF-002` and `AX-PUB-REF-003`;
- exposes offline validation only;
- exposes no network, credential, authentication, production authorization, tool-invocation or real-world execution capability;
- is reproducibly buildable under the declared Gate-05B build contract;
- produces byte-identical wheel/sdist outputs across repeated same-environment builds;
- produces a wheel from the sdist that is byte-identical to the directly built wheel;
- passes installed-package tests using the exact same wheel on CPython 3.11, 3.12, 3.13 and 3.14;
- remains compatible with the inherited closed Gate-03, Gate-04 and Gate-05A governance controls.

## 9. Public Artifact Governance Evidence

The same verification PR also passed the public artifact-governance workflow:

```text
Workflow: Validate Public Artifact Manifest
Run ID: 32171606079
Run number: 168
Conclusion: SUCCESS
```

This establishes that the disposable verification trigger did not invalidate the current public artifact-governance baseline.

## 10. What Was Not Established

This evidence does **not** establish:

- PyPI package ownership;
- TestPyPI package ownership;
- package-name reservation;
- a public software reuse licence;
- IP/copyright clearance;
- a PyPI or TestPyPI upload;
- Trusted Publishing configuration;
- a protected production publishing environment;
- protected release tags/rulesets sufficient for public release;
- human external technical evaluation;
- external developer adoption;
- production API/authentication/authorization;
- a supported SDK;
- a support SLA;
- DEV-GATE-05 closure;
- final SDK release authority;
- SDK publication.

## 11. Gate Boundary

At evidence capture:

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: ENGINEERING CANDIDATE
DEV-GATE-05C: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

`AX-PUB-CI-009` may support a later explicit `DEV-GATE-05B` closure decision. The existence of this evidence file does not itself close any Gate.

---

`DETERMINISTIC PACKAGE ≠ SUPPORTED SDK`  
`CI VALIDATION ≠ RELEASE AUTHORITY`  
`DEV-GATE-05B VALIDATED ≠ DEV-GATE-05 CLOSED`  
`SDK PUBLICATION NOT AUTHORIZED`
