# AETHER X Gate-03 Release-Candidate Engineering

`VALIDATED NON-PUBLISHED ENGINEERING ARTIFACT · CI-ONLY DISTRIBUTION BOUNDARY`

This directory defines the bounded release-candidate engineering surface for `DEV-GATE-03 — Supply-Chain & Release Candidate`.

The current descriptor is:

```text
AX-PUB-RC-001
version: 0.1.0-rc1
state: DEV-GATE-03 VALIDATED
verified SHA-256: 8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
verified SOURCE_DATE_EPOCH: 1787064230
closure evidence: AX-PUB-CI-006 v1.1
```

The candidate is built as a deterministic CI-only archive named:

```text
AX-PUB-RC-001.zip
```

The artifact ID is an engineering identifier. It is **not** an approved public package name.

## Current Boundaries

```text
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
PUBLIC SDK: NOT PUBLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

Gate-03 closure validates the bounded engineering artifact and its supply-chain evidence. It does not publish to PyPI, GitHub Packages or another package registry and does not create a supported SDK contract.

## Verified Supply-Chain Controls

`AX-PUB-CI-006 v1.1` records successful validation of:

- fixed public source selection;
- deterministic ZIP construction;
- SHA-256 build digest;
- machine-readable build manifest;
- SPDX 2.3 SBOM with software licence fields left `NOASSERTION`;
- GitHub build-provenance attestation;
- GitHub SBOM attestation;
- `gh attestation verify` verification;
- extracted-bundle unit/conformance execution;
- public-only dependency boundary;
- CI-only artifact retention.

The SBOM describes the engineering bundle. It does not grant an open-source, commercial or other reuse licence.

## Reproduce the Validated Build

From repository root, while the declared source set remains unchanged:

```bash
SOURCE_DATE_EPOCH=1787064230 \
python3 tools/build_release_candidate.py --output-dir dist
```

The build creates:

```text
dist/AX-PUB-RC-001.zip
dist/AX-PUB-RC-001.sha256
dist/AX-PUB-RC-001_BUILD_MANIFEST.json
dist/AX-PUB-RC-001.spdx.json
```

Validate the closed state and built artifact:

```bash
python3 tools/check_supply_chain_release_candidate.py
python3 tools/check_supply_chain_release_candidate.py --dist dist
```

For the validated source state, the bundle digest must be:

```text
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

## Attestation Verification

When a GitHub Actions run has generated attestations for the candidate artifact, verification uses:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence

gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence \
  --predicate-type https://spdx.dev/Document/v2.3
```

These commands verify artifact provenance or the associated SBOM attestation. Verification does not convert the artifact into a supported or published SDK.

`RELEASE-CANDIDATE VALIDATED ≠ SUPPORTED SDK`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`  
`SBOM ≠ REUSE LICENCE`  
`SDK PUBLICATION NOT AUTHORIZED`
