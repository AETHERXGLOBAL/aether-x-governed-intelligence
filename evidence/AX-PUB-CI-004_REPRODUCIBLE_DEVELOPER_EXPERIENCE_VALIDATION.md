# AX-PUB-CI-004 — Reproducible Developer Experience Validation Evidence

**Evidence ID:** `AX-PUB-CI-004`  
**Version:** `1.0`  
**Status:** `PUBLIC CI EVIDENCE · VERIFIED`  
**Scope:** `AX-PUB-DEV-003 / DEV-GATE-01 CANDIDATE RUNTIME MATRIX`

## 1. Purpose

This record preserves directly observed GitHub Actions evidence that the corrected DEV-GATE-01 reproducible developer-experience candidate completed successfully across the declared Python runtime matrix while the public artifact-governance workflow also passed.

## 2. Verification Context

```text
Repository:
AETHERXGLOBAL/aether-x-governed-intelligence

Verification PR:
#11 — ci: verify DEV-GATE-01 runtime matrix v2

PR intent:
VERIFICATION ONLY / DO NOT MERGE

Base branch:
main

Validated base commit:
91907334ea993c8111b77b6fce83c360c7db95f1

Verification head commit:
8cb092ead19a5a116d51b939845da193ce91c984
```

The verification branch adds only a disposable machine-readable trigger field to the Gate-01 candidate artifact. That field is not part of the published main-branch state and is not intended to merge.

## 3. Developer Experience Workflow

```text
Workflow:
Validate Developer Experience

Workflow run ID:
32136562796

Run number:
10

Conclusion:
SUCCESS
```

All four declared candidate runtime jobs completed successfully:

| Runtime job | Job ID | Conclusion |
|---|---:|---|
| Python 3.10 | `95709172551` | `SUCCESS` |
| Python 3.11 | `95709172573` | `SUCCESS` |
| Python 3.12 | `95709172521` | `SUCCESS` |
| Python 3.13 | `95709172476` | `SUCCESS` |

For each runtime job, the following workflow steps were directly observed as successful:

1. checkout public repository;
2. set up the declared Python runtime;
3. confirm runtime;
4. parse Gate-01 machine-readable state;
5. compile public developer checks;
6. validate clean-environment developer experience;
7. validate machine-readable developer-experience report;
8. re-validate the closed developer contract baseline;
9. re-validate the public-only boundary.

The Gate-01 runner evaluates nine declared checks: three valid reference examples, three intentionally invalid reference fixtures, two public conformance suites and one separate public-only boundary check.

## 4. Public Artifact Governance Workflow

```text
Workflow:
Validate Public Artifact Manifest

Workflow run ID:
32136562828

Run number:
118

Conclusion:
SUCCESS
```

This separately confirms that the candidate developer-experience artifact remained consistent with the registered public artifact governance state for the verification head.

## 5. Runtime Matrix Meaning

The directly validated Gate-01 reference-experience matrix is:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

This evidence supports compatibility of the declared **public reference developer experience** with those runtime lines for the validated repository state.

It does not create a general future Python support promise, SDK support window or package compatibility guarantee. Those commitments belong to later SDK-candidate and release decisions.

## 6. Corrective History Boundary

An earlier DEV-GATE-01 verification attempt exposed a contract error in the Gate-01 runner: the runner incorrectly expected the public-only boundary marker to be emitted by `AX-PUB-TEST-001` rather than by the separate public-boundary checker.

The candidate was **not promoted** after that failure. The check model was corrected so public conformance and the public-only boundary are evaluated as separate controls, producing nine total Gate-01 checks. This record applies only to the corrected successful verification represented by PR #11 and workflow run #10.

## 7. Claim Boundary

This evidence establishes only that the declared public developer-experience checks completed successfully across Python 3.10–3.13 for the referenced verification state and that the public artifact manifest workflow also passed.

It does **not** establish:

- an SDK candidate;
- a supported SDK;
- package publication;
- a production API or service;
- production readiness;
- external developer adoption;
- customer or partner integration;
- security or regulatory certification;
- an open-source or commercial reuse licence;
- implementation inside AETHER X private products or research systems.

`DEV-GATE-01 CI PASS ≠ SDK CANDIDATE`  
`RUNTIME MATRIX PASS ≠ SDK SUPPORT COMMITMENT`  
`REPRODUCIBLE REFERENCE EXPERIENCE ≠ PRODUCTION READINESS`

## 8. Gate Use

This evidence satisfies the directly observed clean-environment runtime-matrix evidence requirement for DEV-GATE-01 candidate promotion.

DEV-GATE-01 closure still requires publication of the closed machine-readable state and successful final closed-state repository verification.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
