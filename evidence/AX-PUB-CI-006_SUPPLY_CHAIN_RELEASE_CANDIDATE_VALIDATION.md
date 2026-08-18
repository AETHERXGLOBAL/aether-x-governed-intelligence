# AX-PUB-CI-006 — Supply-Chain Release-Candidate Validation Evidence

**Artifact ID:** `AX-PUB-CI-006`  
**Version:** `1.1`  
**Type:** `PUBLIC CI VALIDATION EVIDENCE`  
**Scope:** `DEV-GATE-03 — Supply-Chain & Release Candidate`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Status:** `VERIFIED CANDIDATE VALIDATION · GATE NOT YET CLOSED · NON-PRODUCTION`  
**Candidate artifact:** `AX-PUB-RC-001 v0.1.0-rc1`  
**Developer program:** `AX-PUB-DEV-001`  
**Gate artifact:** `AX-PUB-DEV-005`  
**Publication gate:** `AX-PUB-GATE-001 — SDK PUBLICATION NOT AUTHORIZED`

## 0. Correction Record — v1.1

Version `1.0` incorrectly recorded the engineering-bundle SHA-256 as `698ad1fed52cb4b27726d60298021697a58609dc0c2f5253b7e7a40553534da6`.

Direct GitHub Actions job output for run `32150126557` and an independent SHA-256 calculation over the downloaded inner `AX-PUB-RC-001.zip` both establish the correct engineering-bundle digest as:

```text
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

The outer GitHub Actions artifact archive has a separate digest:

```text
907bea9c870fd578bf812bae3d94131ca74752b9ee1b070dbb424d7617270858
```

These values identify different objects and must not be conflated. No Gate-03 maturity or publication claim is changed by this correction.

## 1. Purpose

This record captures the directly observed GitHub Actions evidence for the **published DEV-GATE-03 candidate baseline**.

The evidence supports a later governed decision on whether DEV-GATE-03 may be promoted to `RELEASE-CANDIDATE VALIDATED`. This file does **not** perform that promotion and does not close the gate by itself.

`VALIDATION EVIDENCE ≠ GATE CLOSURE`  
`RELEASE-CANDIDATE VALIDATION ≠ SDK PUBLICATION`

## 2. Verified Repository State

```text
Published candidate base commit:
d91c7a5071f26f1726a9c3449daea6df30ef8f22

Verification head commit:
2a0b0e201d5fe97744825012b66508d1eaef03e5

Verification pull request:
#18 — ci: verify published DEV-GATE-03 candidate state

PR disposition:
CLOSED WITHOUT MERGE
```

The verification-only pull request changed only a disposable `_verification_trigger` field in `artifacts/AX-PUB-DEV-005.json`.

`AX-PUB-DEV-005.json` is not part of the declared `AX-PUB-RC-001` source-file inventory, so the verification trigger did not alter the bounded engineering bundle payload.

## 3. Supply-Chain Validation Workflow

```text
Workflow: Validate Supply-Chain Release Candidate
Run ID: 32150126557
Run number: 7
Job ID: 95753629882
Conclusion: SUCCESS
Canonical SOURCE_DATE_EPOCH: 1787064230
```

The following controls completed successfully in the same job:

```text
Re-validate closed DEV-GATE-02 state
Validate DEV-GATE-03 candidate state before build
Build canonical release candidate
Build release candidate again
Verify deterministic rebuild
Validate built release-candidate state
Extract engineering bundle
Run extracted SDK candidate unit tests
Run extracted SDK candidate conformance
Generate build provenance attestation
Generate SPDX SBOM attestation
Verify build provenance attestation
Verify SPDX SBOM attestation
Upload CI-only engineering artifact
```

## 4. Public Artifact Governance

```text
Workflow: Validate Public Artifact Manifest
Run ID: 32150126711
Run number: 135
Conclusion: SUCCESS
```

This independently confirmed the public artifact graph, closed earlier gates, DEV-GATE-03 candidate registration and public/private governance boundaries for the verification state.

## 5. Deterministic Engineering Bundle

The verified engineering artifact is:

```text
Artifact ID: AX-PUB-RC-001
Candidate version: 0.1.0-rc1
Bundle filename: AX-PUB-RC-001.zip
Canonical build runtime: Python 3.13
Canonical SOURCE_DATE_EPOCH: 1787064230
```

The canonical build and second build were byte-compared in CI.

The verified engineering-bundle SHA-256 is:

```text
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

The build manifest records a fixed inventory of `21` declared public source files and no third-party runtime dependencies for the bounded candidate build.

`DETERMINISTIC BUILD RESULT ≠ GENERAL REPRODUCIBLE-BUILD CERTIFICATION`

## 6. SPDX SBOM

The candidate build generated:

```text
AX-PUB-RC-001.spdx.json
SPDX version: SPDX-2.3
```

The software package entry preserves:

```text
licenseConcluded: NOASSERTION
licenseDeclared: NOASSERTION
```

This is intentional because no public SDK software licence has been decided.

`SPDX DOCUMENT DATA LICENCE ≠ SOFTWARE REUSE LICENCE`  
`SBOM ≠ SECURITY CERTIFICATION`

## 7. GitHub Artifact Attestations

The same workflow successfully generated and verified:

- a GitHub build-provenance attestation for `AX-PUB-RC-001.zip`;
- an SPDX SBOM attestation for the same subject artifact.

Verification was performed in CI with `gh attestation verify`, including the SPDX predicate-type constraint for the SBOM verification.

The connector did not expose stable attestation IDs through the repository attestation endpoint used during this review. Therefore this evidence record does **not** invent or assert attestation IDs; it records only the generation and verification results directly observed in the successful workflow.

`ATTESTATION VERIFICATION SUCCESS ≠ SECURITY CERTIFICATION`

## 8. Extracted-Bundle Validation

The CI-created ZIP was extracted into a separate directory and the candidate was exercised from the extracted artifact itself.

The extracted SDK-candidate unit suite completed successfully:

```text
9 tests
PASS
```

The extracted candidate conformance completed with:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

This demonstrates bounded usability of the declared candidate payload after packaging. It does not establish a supported installation contract or production fitness.

## 9. CI-Only Artifact Record

The successful workflow uploaded a temporary GitHub Actions artifact:

```text
Artifact ID: 9329383928
Name: AX-PUB-RC-001-ci-only
Outer Actions artifact SHA-256: 907bea9c870fd578bf812bae3d94131ca74752b9ee1b070dbb424d7617270858
Retention policy: 7 days
Scope: CI_ONLY
```

The Actions artifact is temporary verification material. It is not a GitHub Release asset, registry package or supported SDK distribution.

`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`

## 10. Candidate-Exit Evidence Assessment

The directly observed evidence supports the following DEV-GATE-03 candidate criteria:

- [x] fixed public source inventory validated;
- [x] deterministic canonical build succeeds;
- [x] second build is byte-identical;
- [x] SHA-256 digest is generated and validated;
- [x] build manifest is generated and validated;
- [x] SPDX 2.3 SBOM is generated and validated;
- [x] build-provenance attestation is generated;
- [x] SBOM attestation is generated;
- [x] build-provenance attestation is verified with `gh attestation verify`;
- [x] SPDX attestation is verified with `gh attestation verify`;
- [x] extracted-bundle unit tests pass;
- [x] extracted-bundle candidate conformance passes;
- [x] public/private dependency boundary passes;
- [x] no package-distribution metadata is present;
- [x] no registry publication occurs;
- [x] candidate state remains bounded by `SDK PUBLICATION NOT AUTHORIZED`.

This evidence is sufficient to support a **separate governed closure review** for DEV-GATE-03.

It does not itself change the public gate state.

## 11. Claim Boundary

`AX-PUB-CI-006 ≠ DEV-GATE-03 CLOSURE`  
`RELEASE-CANDIDATE VALIDATION EVIDENCE ≠ SUPPORTED SDK`  
`BUILD PROVENANCE ≠ SECURITY CERTIFICATION`  
`SPDX SBOM ≠ SOFTWARE REUSE LICENCE`  
`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`  
`PACKAGE IDENTITY: NOT APPROVED`  
`PACKAGE REGISTRY: NOT AUTHORIZED`  
`PUBLIC SDK LICENCE: NOT DECIDED`  
`SDK PUBLICATION NOT AUTHORIZED`

The next state, if separately approved by repository governance after closed-state CI, is:

```text
DEV-GATE-03 CLOSED
RELEASE-CANDIDATE VALIDATED
DEV-GATE-04 — External Evaluation Readiness
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
