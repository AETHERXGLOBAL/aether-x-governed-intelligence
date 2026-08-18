# AX-PUB-CI-003 — Developer Contract Baseline Validation Evidence

**Evidence ID:** `AX-PUB-CI-003`  
**Version:** `1.0`  
**Status:** `PUBLIC CI EVIDENCE · VERIFIED`  
**Scope:** `AX-PUB-DEV-002 / DEV-GATE-00 CONTRACT BASELINE CANDIDATE`

## 1. Purpose

This record preserves directly observed GitHub Actions evidence that the public developer contract baseline candidate and its repository governance checks completed successfully before DEV-GATE-00 closure.

## 2. Verification Context

```text
Repository:
AETHERXGLOBAL/aether-x-governed-intelligence

Verification PR:
#8 — ci: verify DEV-GATE-00 developer contract baseline

PR disposition:
CLOSED WITHOUT MERGE

Base branch:
main

Base commit validated by the verification branch plus disposable trigger files:
8e821f9debc27ce8924e1480852b047a8ecf6f02

Verification head commit:
ae72355968f64997242b770457634fe4f3bf021c

Workflow:
Validate Public Artifact Manifest

Workflow run ID:
32134148610

Run number:
97

Conclusion:
SUCCESS
```

The verification branch differed from the base only by disposable verification-trigger files and was reset to `main` after the PR was closed. The verification PR was not merged.

## 3. Directly Observed Successful Checks

The GitHub Actions job `validate-public-artifact-manifest` completed with conclusion `success`.

The following steps were directly observed as successful:

1. `Checkout public repository`
2. `Parse public machine-readable artifacts`
3. `Compile public integrity checkers`
4. `Validate artifact paths versions and compatibility`
5. `Validate developer contract baseline`
6. `Validate public-only conformance boundary`

This establishes successful CI execution for the declared DEV-GATE-00 candidate repository checks.

## 4. What Was Validated

The developer baseline checker verifies, within its declared public scope:

- `AX-PUB-DEV-002` document identity and version markers;
- the machine-readable `artifacts/AX-PUB-DEV-002.json` companion;
- the three declared contract paths;
- the baseline semantic error taxonomy;
- the public/private dependency boundary flags;
- SDK publication remaining unauthorized;
- package identity remaining unapproved;
- registry publication remaining unauthorized;
- SDK Semantic Versioning remaining inactive at DEV-GATE-00;
- public licence decision remaining unresolved;
- registration of `AX-PUB-DEV-002` in the public artifact manifest.

The manifest workflow also validates the broader registered public artifact and public-only conformance boundaries.

## 5. Claim Boundary

This evidence supports only the claim that the declared public DEV-GATE-00 candidate checks completed successfully in the referenced GitHub Actions run.

It does **not** establish:

- a supported SDK;
- package publication;
- product implementation;
- production API availability;
- production authorization;
- security certification;
- regulatory approval;
- external developer adoption;
- customer deployment;
- an open-source or commercial reuse licence.

`CI PASS ≠ SDK RELEASE`  
`DEV-GATE-00 VALIDATION ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC CONTRACT BASELINE ≠ PRODUCTION API`

## 6. Gate Use

This evidence satisfies the directly observed CI-evidence requirement declared by `AX-PUB-DEV-002` for DEV-GATE-00 closure.

A separate final repository-state validation should verify the **closed** gate state after closure metadata is published.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
