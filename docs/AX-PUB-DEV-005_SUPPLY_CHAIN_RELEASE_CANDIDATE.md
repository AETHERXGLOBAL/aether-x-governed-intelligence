# AX-PUB-DEV-005 — Supply-Chain & Release Candidate

**Artifact ID:** `AX-PUB-DEV-005`  
**Version:** `1.0`  
**Status:** `DEV-GATE-03 CANDIDATE · RELEASE CANDIDATE NOT YET ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`  
**Program:** `AX-PUB-DEV-001`  
**Builds on:** `AX-PUB-DEV-004 — DEV-GATE-02 CLOSED`  
**Engineering release-candidate descriptor:** `AX-PUB-RC-001 v0.1.0-rc1`  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-005.json`

## 1. Purpose

DEV-GATE-03 tests whether the bounded repository-local SDK candidate can be transformed into a **traceable, deterministic, supply-chain-verifiable engineering release candidate** without publishing a package or creating unsupported distribution commitments.

The candidate chain is:

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
```

`SUPPLY-CHAIN CANDIDATE ≠ SDK RELEASE`  
`ATTESTED ARTIFACT ≠ SUPPORTED SDK`

## 2. Explicit Non-Goals

DEV-GATE-03 does **not** establish or authorize:

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
SDK PUBLICATION: NOT AUTHORIZED
```

## 3. Engineering Release Candidate — AX-PUB-RC-001

`AX-PUB-RC-001` is a non-published engineering artifact identifier.

```text
Artifact: AX-PUB-RC-001
Version: 0.1.0-rc1
Bundle: AX-PUB-RC-001.zip
State: DEV-GATE-03 CANDIDATE
```

The identifier exists so the build, digest, SBOM, attestation and verification evidence can refer to one bounded object. It is not an approved registry/package identity.

## 4. Deterministic Build Contract

The canonical builder is:

```text
tools/build_release_candidate.py
```

The builder uses only Python standard-library capabilities and a fixed source inventory declared by `release-candidate/AX-PUB-RC-001.json`.

The build is designed to be deterministic by controlling:

- source inventory and ordering;
- archive entry ordering;
- archive timestamps through `SOURCE_DATE_EPOCH`;
- file permission metadata;
- generated JSON key ordering;
- ZIP compression mode.

The CI candidate must build twice from the same checkout and compare the resulting bundle bytes directly.

Determinism here means identical bytes under the declared build procedure for the same public source state. It is not a broader reproducible-build certification.

## 5. Build Digest & Manifest

The canonical bundle receives a SHA-256 digest recorded in:

```text
AX-PUB-RC-001.sha256
```

A generated build manifest records:

- source paths;
- source SHA-256 digests;
- source sizes;
- source date epoch;
- declared runtime-dependency boundary;
- package/registry/licence/publication states.

The build manifest does not create release authority.

## 6. SPDX 2.3 SBOM

The build creates:

```text
AX-PUB-RC-001.spdx.json
```

The candidate SBOM uses `SPDX 2.3` document structure and describes the bounded engineering candidate.

Software licence fields are deliberately represented as `NOASSERTION` because no public SDK reuse licence has been decided. The SPDX document data licence does not grant a licence to the bundled software.

`SBOM ≠ SOFTWARE LICENCE`  
`SBOM ≠ SECURITY CERTIFICATION`

## 7. GitHub Artifact Attestations

The candidate workflow is designed to generate GitHub artifact attestations for:

1. build provenance for `AX-PUB-RC-001.zip`;
2. the associated SPDX SBOM.

The workflow uses GitHub OIDC-backed attestation permissions only inside the bounded CI job:

```text
contents: read
id-token: write
attestations: write
```

This provides verifiable provenance for the CI artifact. It does not imply AETHER X has obtained an external supply-chain or security certification.

## 8. Attestation Verification

The workflow must verify the generated attestations using GitHub CLI.

Build provenance verification:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence
```

SPDX predicate verification:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence \
  --predicate-type https://spdx.dev/Document/v2.3
```

`gh attestation verify` success is evidence for the specific GitHub-generated attestation. It is not a general security approval.

## 9. Extracted-Bundle Verification

The CI artifact must be extracted into a clean directory and execute the bounded candidate validation directly from the extracted bundle:

```bash
python -m unittest discover -s sdk-candidate/python/tests -v
python sdk-candidate/python/run_candidate_conformance.py
```

The expected candidate conformance marker remains:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

This tests that the engineering bundle contains a usable copy of the declared public candidate rather than merely packaging files that were tested elsewhere.

## 10. Public / Private Boundary

The release-candidate source set must remain entirely inside the public repository.

It must not require:

- private AETHER X repositories;
- private package indexes;
- private endpoints;
- private credentials;
- unpublished product source;
- unpublished research;
- customer data;
- hidden production schemas.

The declared third-party runtime dependency list for the current candidate is empty.

## 11. CI-Only Artifact Boundary

The workflow may upload the generated engineering files as a temporary GitHub Actions artifact for review.

```text
ARTIFACT UPLOAD SCOPE: CI_ONLY
RETENTION: 7 DAYS
```

The CI artifact must not be represented as a GitHub Release asset, PyPI package, GitHub Packages package or another public distribution channel.

`CI ARTIFACT ≠ PUBLIC PACKAGE`

## 12. Vulnerability / Security Reporting Path

The public repository's `SECURITY.md` remains the public reporting boundary for security issues.

DEV-GATE-03 may strengthen release-integrity and provenance evidence, but it does not establish a new security certification or expose private security implementation details.

## 13. Protected Future Publication Design

A later publication design should preserve:

- least-privilege release permissions;
- protected release events;
- short-lived identity/token mechanisms where appropriate;
- immutable release-version treatment;
- verifiable origin;
- explicit package identity;
- licence/IP authority;
- supported compatibility policy;
- maintenance ownership.

DEV-GATE-03 candidate work intentionally stops before registry publishing.

## 14. DEV-GATE-03 Exit Criteria

Gate-03 may be promoted to `RELEASE-CANDIDATE VALIDATED` only after direct CI evidence establishes all applicable criteria:

- [ ] fixed public source inventory validated;
- [ ] deterministic canonical build succeeds;
- [ ] second build is byte-identical;
- [ ] SHA-256 digest is generated and validated;
- [ ] build manifest is generated and validated;
- [ ] SPDX 2.3 SBOM is generated and validated;
- [ ] build-provenance attestation is generated;
- [ ] SBOM attestation is generated;
- [ ] build-provenance attestation is verified with `gh attestation verify`;
- [ ] SPDX attestation is verified with `gh attestation verify`;
- [ ] extracted-bundle unit tests pass;
- [ ] extracted-bundle candidate conformance passes;
- [ ] public/private dependency boundary passes;
- [ ] no package-distribution metadata is present;
- [ ] no registry publication occurs;
- [ ] candidate state is recorded in public artifact governance;
- [ ] verification evidence is recorded before closure.

Until these checks have direct evidence:

```text
DEV-GATE-03: CANDIDATE
RELEASE CANDIDATE: NOT YET ESTABLISHED
```

## 15. Current Candidate State

```text
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
DEV-GATE-03: CANDIDATE / UNDER VALIDATION
SDK CANDIDATE: ESTABLISHED
RELEASE CANDIDATE: NOT YET ESTABLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION NOT AUTHORIZED
```

The next gate after verified DEV-GATE-03 closure is:

```text
DEV-GATE-04 — External Evaluation Readiness
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
