# AX-PUB-CI-008 — SDK Release Decision Baseline Validation Evidence

**Artifact ID:** `AX-PUB-CI-008`  
**Version:** `1.0`  
**Scope:** `DEV-GATE-05A — Release Decision Baseline`  
**Evidence state:** `DIRECT CI VALIDATION OF PUBLISHED CANDIDATE BASELINE · GATE NOT YET CLOSED AT TIME OF EVIDENCE CAPTURE`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This record captures direct GitHub Actions evidence for the published `DEV-GATE-05A` decision-baseline candidate while preserving the distinction between engineering validation, gate closure and SDK publication authority.

```text
DIRECT CI VALIDATION
≠ DEV-GATE-05A CLOSURE
≠ DEV-GATE-05 CLOSURE
≠ SDK RELEASE AUTHORITY
≠ SDK PUBLICATION
```

## 2. Published Candidate Baseline

The Gate-05A candidate baseline was squash-merged to `main` at:

```text
fa1e2d132071ddff195fb998d0d27a6b5b9d4e40
```

The published baseline contains:

- `AX-PUB-DEV-007 — SDK Release Decision Baseline`;
- machine-readable `artifacts/AX-PUB-DEV-007.json`;
- fail-closed `tools/check_sdk_release_decision_baseline.py`;
- the default-branch read-only Gate-05A CI workflow.

At the time of publication, the candidate remained explicitly bounded by:

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: DECISION BASELINE CANDIDATE
SDK PUBLICATION: NOT AUTHORIZED
RELEASE AUTHORIZED: FALSE
```

## 3. Verification Method

A verification-only branch was created from the exact published candidate baseline.

The only verification change was one disposable machine-readable field:

```text
verification_trigger = VERIFY_PUBLISHED_BASELINE_ONLY
```

It did not change:

- release scope;
- licensing direction;
- package identity candidate;
- runtime target;
- security controls;
- support boundary;
- Gate state;
- publication disposition;
- release authority.

Verification head:

```text
7877abceda8fa6a372300fceb1ae0c124853d2b6
```

Synthetic pull-request merge commit used by GitHub Actions:

```text
15e4f0cf3fc221e5494d9e6c3a0597fb721a3e1e
```

Verification PR:

```text
#31 — CI verification: published DEV-GATE-05A baseline
```

The PR was closed **without merge** after successful evidence capture. The verification branch was then reset to the exact published `main` candidate baseline.

## 4. Primary Gate-05A Workflow Evidence

```text
Workflow: Validate SDK Release Decision Baseline
Run ID: 32168696722
Run number: 10
Conclusion: SUCCESS
```

All declared Gate-05A runtime jobs completed successfully:

| Runtime | Job ID | Decision invariants | SDK candidate tests | Conformance | Public/private boundary | Gate-04 preservation |
|---|---:|---|---|---|---|---|
| Python 3.11 | `95814358240` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` |
| Python 3.12 | `95814357868` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` |
| Python 3.13 | `95814357940` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` |
| Python 3.14 | `95814358020` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` | `SUCCESS` |

Each runtime job directly completed:

1. checkout with persistent credentials disabled;
2. setup and confirmation of the declared Python runtime;
3. parse of `AX-PUB-DEV-007.json`;
4. compilation of the Gate-05A checker;
5. validation of Gate-05A fail-closed decision invariants;
6. compilation of the bounded repository-local SDK candidate;
7. SDK candidate unit tests;
8. SDK candidate example execution;
9. candidate conformance execution;
10. SDK candidate public/private boundary validation;
11. revalidation of the closed Gate-04 state.

Observed success markers include:

```text
AX_SDK_RELEASE_DECISION_BASELINE_PASS
AX_SDK_CANDIDATE_EXAMPLE_PASS
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
AX_SDK_CANDIDATE_BOUNDARY_PASS
AX_DEV_GATE_04_CLOSED_STATE_PASS
```

The Python 3.14 job directly reported CPython `3.14.7` and completed all declared checks successfully.

## 5. Workflow Security Observation

The Gate-05A jobs ran with GitHub token permissions limited to:

```text
Contents: read
Metadata: read
```

The workflow used immutable full-commit pins for the release-sensitive setup actions:

```text
actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5
actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405
```

No package publication, registry credential, OIDC publication permission, secret-dependent release action or SDK release authority was exercised by this validation run.

## 6. Public Artifact Governance Evidence

The same verification head also passed the public artifact-governance workflow:

```text
Workflow: Validate Public Artifact Manifest
Run ID: 32168696655
Run number: 159
Conclusion: SUCCESS
```

This establishes that the Gate-05A verification trigger did not invalidate the existing public artifact-governance baseline.

## 7. What Was Validated

The evidence supports the following bounded statement:

> The published DEV-GATE-05A candidate baseline preserves its declared fail-closed release-decision invariants and the pre-existing bounded SDK-candidate behavior across CPython 3.11, 3.12, 3.13 and 3.14, while the closed DEV-GATE-04 governance and public/private boundary remain valid.

## 8. What Was Not Validated

This evidence does **not** establish:

- an installable wheel or sdist;
- PyPI or TestPyPI package ownership;
- a software reuse licence;
- IP/copyright clearance;
- human external evaluation;
- external developer adoption;
- production authentication or authorization;
- production API or service integration;
- branch/ruleset release protection;
- protected PyPI release environment;
- a supported SDK;
- SDK release authority;
- SDK publication.

## 9. Gate Boundary

At evidence capture:

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: DECISION BASELINE CANDIDATE
DEV-GATE-05B: NOT ESTABLISHED
DEV-GATE-05C: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

`AX-PUB-CI-008` may support a later explicit Gate-05A closure decision. The existence of this evidence file does not itself close any Gate.

---

`CI VALIDATION ≠ RELEASE AUTHORITY`  
`DEV-GATE-05A VALIDATED ≠ DEV-GATE-05 CLOSED`  
`SDK PUBLICATION NOT AUTHORIZED`
