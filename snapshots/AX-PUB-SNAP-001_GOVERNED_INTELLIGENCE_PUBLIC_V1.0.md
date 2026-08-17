# AETHER X Governed Intelligence — Public Snapshot v1.0

**Snapshot ID:** `AX-PUB-SNAP-001`  
**Snapshot Version:** `1.0`  
**Status:** `PUBLIC ENGINEERING SNAPSHOT · REPRODUCIBILITY ANCHOR · NON-PRODUCT`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Anchor Commit:** `f839d4ac0a0b69dcbb682e900f02aad7e24524eb`  
**Anchor Commit Time:** `2026-08-17T21:37:23Z`

## Purpose

This snapshot records a fixed public engineering state for reproducible external review of the AETHER X governed-intelligence technical series.

It exists so an engineer, researcher, institutional reviewer or diligence team can answer:

```text
WHICH PUBLIC ARTIFACT VERSIONS WERE REVIEWED?
AT WHICH EXACT REPOSITORY STATE?
WHICH FILE CONTENTS BELONG TO THAT STATE?
WHICH PUBLIC CI EVIDENCE WAS AVAILABLE?
```

The immutable reproducibility anchor is the Git commit SHA above. Individual material files are additionally recorded by their Git blob SHA in [`AX-PUB-SNAP-001.json`](./AX-PUB-SNAP-001.json).

## Snapshot Inventory

| Artifact | Version | Snapshot role |
|---|---:|---|
| `AX-PUB-ARCH-001` | `1.0` | Governed Intelligence Reference Architecture |
| `AX-PUB-SPEC-002` | `1.0` | Evidence, Authority & Verification Contract |
| `AX-PUB-SPEC-003` | `1.0` | Point-in-Time Knowledge & Provenance Standard |
| `AX-PUB-SCHEMA-001` | `1.0` | Governed EAV machine-readable structural contract |
| `AX-PUB-SCHEMA-002` | `1.0` | Point-in-Time Knowledge machine-readable envelope |
| `AX-PUB-REF-001` | `1.0` | EAV Contract Validator |
| `AX-PUB-REF-002` | `1.0` | Point-in-Time Knowledge Validator |
| `AX-PUB-POL-001` | `1.0` | Public Artifact Compatibility & Versioning Policy |
| `AX-PUB-MANIFEST-001` | `1.0` | Machine-readable public compatibility manifest |

Supporting material in the snapshot includes the Public Quickstart and repository README.

## Reproduce the Snapshot

Clone the repository and check out the immutable anchor:

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
git checkout f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

Confirm the commit:

```bash
git rev-parse HEAD
```

Expected value:

```text
f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

The machine-readable snapshot record contains Git blob SHAs for the material files. A reviewer can verify any recorded path with:

```bash
git rev-parse f839d4ac0a0b69dcbb682e900f02aad7e24524eb:<path>
```

and compare the result with the corresponding `git_blob_sha` in [`AX-PUB-SNAP-001.json`](./AX-PUB-SNAP-001.json).

## Validation Evidence

The snapshot manifest records public GitHub Actions evidence available for the technical series.

The exact anchor commit `f839d4ac...` passed the **Validate Public Artifact Manifest** workflow, which checked artifact paths, versions, schema identity, compatibility relationships and developer-entry-point integrity.

The snapshot also records the successful workflow runs that exercised the EAV and Point-in-Time schema/reference layers. Those component workflow runs occurred on earlier commits in the same development sequence; the snapshot manifest records their exact head commits and scopes rather than implying that each workflow was rerun on the final snapshot anchor.

This distinction is intentional:

`RECORDED CI EVIDENCE ≠ CLAIM THAT EVERY WORKFLOW RAN ON THE SNAPSHOT COMMIT`

## Snapshot vs. Release

This record is **not** a GitHub Release and **not** a Git tag.

The currently available integration can create and validate repository content but does not expose a write operation for Git tags or GitHub Releases. Therefore AETHER X uses the commit SHA as the authoritative reproducibility anchor for this snapshot.

If a formal tag or GitHub Release is later created, it should point to the exact snapshot anchor or explicitly identify a successor snapshot. A tag must not silently redefine the content represented by `AX-PUB-SNAP-001`.

## Claim Boundary

This snapshot establishes only a fixed, inspectable state of selected public engineering material.

It does **not** establish or imply:

- implementation inside AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- production readiness;
- production API or SDK stability;
- customer deployment;
- security certification;
- regulatory compliance;
- production-scale financial-data capability;
- product-to-product integration;
- scientific, predictive, financial or investment performance.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

## Canonical Records

- [Machine-readable snapshot record](./AX-PUB-SNAP-001.json)
- [Public artifact compatibility manifest](../artifacts/AX-PUB-MANIFEST-001.json)
- [Compatibility & Versioning Policy](../docs/COMPATIBILITY_AND_VERSIONING.md)
- [Public Quickstart](../docs/QUICKSTART.md)

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
