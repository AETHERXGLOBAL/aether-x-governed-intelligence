# AETHER X Gate-03 Release-Candidate Engineering

`NON-PUBLISHED ENGINEERING ARTIFACT · SUPPLY-CHAIN VALIDATION ONLY`

This directory defines the bounded release-candidate engineering surface for `DEV-GATE-03 — Supply-Chain & Release Candidate`.

The current descriptor is:

```text
AX-PUB-RC-001
version: 0.1.0-rc1
state: DEV-GATE-03 CANDIDATE
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

The Gate-03 workflow may build, inspect, attest and temporarily upload a CI artifact for supply-chain validation. It must not publish to PyPI, GitHub Packages or another package registry.

## Supply-Chain Controls Under Test

- deterministic source selection;
- deterministic ZIP construction;
- SHA-256 build digest;
- machine-readable build manifest;
- SPDX 2.3 SBOM document with software licence fields left `NOASSERTION`;
- GitHub build-provenance attestation;
- GitHub SBOM attestation;
- `gh attestation verify` verification;
- extracted-bundle unit/conformance execution;
- public-only dependency boundary;
- CI-only artifact retention.

The SBOM describes the engineering bundle. It does not grant an open-source, commercial or other reuse licence.

## Local Build

From repository root:

```bash
SOURCE_DATE_EPOCH=315532800 python3 tools/build_release_candidate.py --output-dir dist
```

The build creates:

```text
dist/AX-PUB-RC-001.zip
dist/AX-PUB-RC-001.sha256
dist/AX-PUB-RC-001_BUILD_MANIFEST.json
dist/AX-PUB-RC-001.spdx.json
```

Validate the built state:

```bash
python3 tools/check_supply_chain_release_candidate.py --dist dist
```

## Attestation Verification

When a GitHub Actions run has generated attestations for the candidate artifact, the intended verification commands are:

```bash
gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence

gh attestation verify dist/AX-PUB-RC-001.zip \
  -R AETHERXGLOBAL/aether-x-governed-intelligence \
  --predicate-type https://spdx.dev/Document/v2.3
```

These commands verify artifact provenance or the associated SBOM attestation. Verification does not convert the artifact into a supported or published SDK.

`ATTESTED BUILD ≠ SUPPORTED SDK`  
`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`  
`SBOM ≠ REUSE LICENCE`  
`SDK PUBLICATION NOT AUTHORIZED`
