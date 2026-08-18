# AX-PUB-DEV-005 — Supply-Chain & Release Candidate

**Artifact ID:** `AX-PUB-DEV-005`  
**Version:** `1.0`  
**Status:** `DEV-GATE-03 CLOSED · RELEASE-CANDIDATE VALIDATED · SDK PUBLICATION NOT AUTHORIZED`  
**Program:** `AX-PUB-DEV-001`  
**Builds on:** `AX-PUB-DEV-004 — DEV-GATE-02 CLOSED`  
**Engineering release-candidate descriptor:** `AX-PUB-RC-001 v0.1.0-rc1`  
**Closure evidence:** [`AX-PUB-CI-006 v1.1`](../evidence/AX-PUB-CI-006_SUPPLY_CHAIN_RELEASE_CANDIDATE_VALIDATION.md)  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-005.json`

## 1. Purpose

DEV-GATE-03 determines whether the bounded repository-local SDK candidate can be transformed into a **traceable, deterministic, supply-chain-verifiable engineering release candidate** without publishing a package or creating unsupported distribution commitments.

The validated chain is:

```text
DEV-GATE-02 SDK CANDIDATE
→ FIXED PUBLIC SOURCE SET
→ DETERMINISTIC BUILD
→ SHA-256 DIGEST
→ BUILD MANIFEST
→ SPDX 2.3 SBOM
→ BUILD-PROVENANCE ATTESTATION
→ SBOM ATTESTATION
→ ATTESTATION VERIFICATION
→ EXTRACTED-BUNDLE TEST / CONFORMANCE
→ CI-ONLY ARTIFACT
→ RELEASE-CANDIDATE VALIDATED
```

`RELEASE-CANDIDATE VALIDATED ≠ SDK RELEASE`  
`ATTESTED ARTIFACT ≠ SUPPORTED SDK`

## 2. Explicit Non-Goals

DEV-GATE-03 closure does **not** establish or authorize:

- a public package name;
- a PyPI, GitHub Packages or other registry publication;
- a public SDK licence or reuse permission;
- a supported SDK installation contract;
- production service availability;
- a production API;
- customer or partner adoption;
- product integration inside AETHER X Quantum, AX-OS, AIC or Research;
- security certification or standards certification;
- release authority under `AX-PUB-GATE-001`.

Current publication boundary:

```text
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
PUBLIC SDK: NOT PUBLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

## 3. Validated Engineering Release Candidate — AX-PUB-RC-001

`AX-PUB-RC-001` remains a non-published engineering artifact identifier.

```text
Artifact: AX-PUB-RC-001
Version: 0.1.0-rc1
Bundle: AX-PUB-RC-001.zip
State: DEV-GATE-03 VALIDATED
Canonical build runtime: Python 3.13
Verified SOURCE_DATE_EPOCH: 1787064230
Verified bundle SHA-256:
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

The identifier exists so build, digest, SBOM, attestation and verification evidence can refer to one bounded object. It is not an approved registry/package identity.

The outer GitHub Actions artifact archive is a separate object and has a separate digest. `AX-PUB-CI-006 v1.1` records this distinction explicitly.

## 4. Deterministic Build Contract

The canonical builder is:

```text
tools/build_release_candidate.py
```

The builder uses Python standard-library capabilities and the fixed source inventory declared by `release-candidate/AX-PUB-RC-001.json`.

The build controls:

- source inventory and ordering;
- archive entry ordering;
- archive timestamps through `SOURCE_DATE_EPOCH`;
- file permission metadata;
- generated JSON key ordering;
- ZIP compression mode.

The Gate-03 CI path builds twice and compares the resulting bundle bytes directly.

For the validated candidate, the workflow reuses the evidence-bound `SOURCE_DATE_EPOCH` so later governance-only commits can verify the same artifact bytes rather than silently redefine the candidate.

`DETERMINISTIC BUILD RESULT ≠ GENERAL REPRODUCIBLE-BUILD CERTIFICATION`

## 5. Build Digest & Manifest

The canonical bundle receives a SHA-256 digest recorded in:

```text
AX-PUB-RC-001.sha256
```

The verified digest is:

```text
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

The generated build manifest records:

- source paths;
- source SHA-256 digests;
- source sizes;
- source date epoch;
- declared runtime-dependency boundary;
- package/registry/licence/publication states.

The validated build manifest records `21` public source files and zero declared third-party runtime dependencies for the bounded candidate.

## 6. SPDX 2.3 SBOM

The build creates:

```text
AX-PUB-RC-001.spdx.json
```

The candidate SBOM uses `SPDX 2.3` structure and describes the bounded engineering candidate.

Software licence fields remain:

```text
licenseConcluded: NOASSERTION
licenseDeclared: NOASSERTION
```

No public SDK reuse licence has been decided. The SPDX document data licence does not grant a licence to the bundled software.

`SBOM ≠ SOFTWARE LICENCE`  
`SBOM ≠ SECURITY CERTIFICATION`

## 7. GitHub Artifact Attestations

`AX-PUB-CI-006 v1.1` records successful generation and verification of:

1. GitHub build-provenance attestation for `AX-PUB-RC-001.zip`;
2. SPDX SBOM attestation for the same subject artifact.

The workflow uses bounded GitHub Actions permissions:

```text
contents: read
id-token: write
attestations: write
```

The evidence does not claim an external supply-chain or security certification.

## 8. Attestation Verification

Verification uses GitHub CLI:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence
```

and for the SPDX predicate:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence \
  --predicate-type https://spdx.dev/Document/v2.3
```

`gh attestation verify` success is evidence for the specific GitHub-generated attestation. It is not a general security approval.

## 9. Extracted-Bundle Verification

The CI-created ZIP was extracted into a separate directory and exercised from the extracted artifact itself.

The verified results recorded by `AX-PUB-CI-006` are:

```text
UNIT TESTS: 9 PASS
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

This establishes bounded usability of the declared candidate payload after packaging. It does not establish a supported installation contract or production fitness.

## 10. Public / Private Boundary

The release-candidate source set remains entirely inside the public repository.

It does not require:

- private AETHER X repositories;
- private package indexes;
- private endpoints;
- private credentials;
- unpublished product source;
- unpublished research;
- customer data;
- hidden production schemas.

The declared third-party runtime dependency list for this candidate is empty.

## 11. CI-Only Artifact Boundary

The workflow may upload generated engineering files as a temporary GitHub Actions artifact for review.

```text
ARTIFACT UPLOAD SCOPE: CI_ONLY
RETENTION: 7 DAYS
```

The CI artifact is not a GitHub Release asset, PyPI package, GitHub Packages package or another public distribution channel.

`CI ARTIFACT ≠ PUBLIC PACKAGE`

## 12. Vulnerability / Security Reporting Path

The public repository's `SECURITY.md` remains the public reporting boundary for security issues.

Gate-03 strengthens release-integrity and provenance evidence. It does not establish a security certification or expose private security implementation details.

## 13. Protected Future Publication Design

A later publication decision must separately resolve and preserve:

- least-privilege release permissions;
- protected release events;
- short-lived identity/token mechanisms where appropriate;
- immutable release-version treatment;
- verifiable origin;
- explicit package identity;
- licence/IP authority;
- supported compatibility policy;
- maintenance ownership.

DEV-GATE-03 intentionally stops before registry publishing.

## 14. DEV-GATE-03 Exit Criteria

Direct evidence in `AX-PUB-CI-006 v1.1` establishes the applicable exit criteria:

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
- [x] candidate state is recorded in public artifact governance;
- [x] verification evidence was recorded before closure.

## 15. Closure State

```text
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
DEV-GATE-03: CLOSED
SDK CANDIDATE: ESTABLISHED
RELEASE CANDIDATE: VALIDATED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
PUBLIC SDK: NOT PUBLISHED
SDK PUBLICATION NOT AUTHORIZED
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-04 — EXTERNAL EVALUATION READINESS
```

Closure evidence:

```text
AX-PUB-CI-006 v1.1
Supply-chain workflow run: 32150126557 / #7 / SUCCESS
Manifest workflow run: 32150126711 / #135 / SUCCESS
```

`DEV-GATE-03 CLOSED` means only that the bounded non-published engineering release candidate has verified supply-chain/release-integrity evidence under this public program.

It does not authorize SDK publication.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
