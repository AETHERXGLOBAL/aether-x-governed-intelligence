# AETHER X Public Artifact Compatibility & Versioning Policy

**Policy ID:** `AX-PUB-POL-001`  
**Version:** `1.6`  
**Status:** `PUBLIC ENGINEERING POLICY · ACTIVE FOR THIS REPOSITORY`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This policy defines how public AETHER X governed-intelligence artifacts are identified, versioned, related, validated, snapshotted, released and promoted toward supported developer surfaces inside this repository.

It applies to public reference architecture, specifications, machine-readable schemas, non-production reference implementations, public conformance artifacts, CI evidence records, reproducibility snapshots, public engineering release records and publication-readiness gates.

It is **not** a product-release, SDK-compatibility or production-API policy.

## 2. Artifact Identity

Public technical artifacts use stable identifiers such as:

```text
AX-PUB-ARCH-001
AX-PUB-SPEC-002
AX-PUB-SCHEMA-001
AX-PUB-REF-001
AX-PUB-TEST-001
AX-PUB-CI-001
AX-PUB-SNAP-001
AX-PUB-REL-001
AX-PUB-GATE-001
```

The artifact ID identifies the public artifact family. The version identifies a published revision within that family.

A materially different contract may require a new ID rather than overloading an existing artifact identity.

## 3. Version Format

Current versioned public artifacts use:

```text
MAJOR.MINOR
```

### MAJOR

Increase `MAJOR` for materially incompatible changes, such as changing the meaning of a normative state, removing a required machine-readable field without a compatible path, or changing a core control boundary in a way that invalidates important prior assumptions.

### MINOR

Increase `MINOR` for additive or clarifying changes intended to preserve prior contract meaning, including:

- additive optional fields;
- clarifying normative text;
- new validation for already-declared behavior;
- new independently identified public artifacts;
- new public evidence records;
- new snapshots, release records or readiness gates;
- documentation or metadata changes that alter the published current-state description.

A version increment does not establish product adoption or implementation by any AETHER X initiative.

## 4. Compatibility Is Explicit, Not Inferred

Compatibility between current artifacts is recorded in:

[`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json)

A reviewer should not infer compatibility because artifacts share a repository, naming pattern or corporate doctrine.

Current public evidence paths include:

```text
AX-PUB-SPEC-002 v1.0
→ AX-PUB-SCHEMA-001 v1.0
→ AX-PUB-REF-001 v1.0
→ AX-PUB-TEST-001 v1.0
```

```text
AX-PUB-SPEC-003 v1.0
→ AX-PUB-SCHEMA-002 v1.0
→ AX-PUB-REF-002 v1.0
→ AX-PUB-TEST-001 v1.0
```

```text
AX-PUB-SPEC-004 v1.0
→ AX-PUB-SCHEMA-003 v1.0
→ AX-PUB-REF-003 v1.0
→ AX-PUB-TEST-002 v1.0
```

Compatibility does not establish internal product adoption.

## 5. Compatibility States

The public manifest may use:

- `CURRENT`
- `COMPATIBLE`
- `SUPERSEDED`
- `DEPRECATED`
- `WITHDRAWN`

These states describe public repository artifacts only. They do not describe internal product maturity.

## 6. Artifact Responsibilities

### Reference Architecture
Defines technology-neutral system-level structure and control boundaries.

### Specification
Defines normative or conceptual semantics.

### JSON Schema
Defines selected machine-readable structure, required fields, primitive types, enums and timestamp formats.

### Reference Validator
Implements selected deterministic cross-record, authority or temporal semantics.

### Conformance Test Kit
Defines synthetic public cases, expected behavior and selected required findings.

### CI Evidence Record
Preserves directly observed public validation evidence with explicit scope and claim boundaries.

### Public Engineering Snapshot
Preserves a fixed commit-anchored public-review state with recorded Git object identities.

### Public Engineering Release Record
Preserves the identity of an intentionally published Git tag / GitHub Release and separates that publication event from product-release semantics.

### Publication Readiness Gate
Defines evidence and authority conditions that must be satisfied before a new supported public developer surface is represented as approved for publication.

Therefore:

`SCHEMA VALID ≠ SEMANTICALLY VALID`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`  
`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC CI PASS ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`PUBLIC REFERENCE IMPLEMENTATION ≠ SUPPORTED SDK`

## 7. Change Discipline

A material public change should preserve a traceable answer to:

1. Which artifact changed?
2. Which version changed?
3. Is the change compatible or incompatible?
4. Which dependent public artifacts are affected?
5. Were examples/tests updated where applicable?
6. What public validation or reproducible evidence applies?
7. Does the change alter a public claim boundary?
8. Does the change create a new support, compatibility, licensing or publication commitment?

Changes should fail closed when artifact paths, versions, declared relationships, evidence references, snapshot references, release references or readiness-gate references become internally inconsistent.

A public workflow MUST NOT be represented as a successfully verified CI run unless the run itself is directly evidenced.

## 8. Main Branch & Reproducibility Snapshots

The `main` branch represents the **current moving public engineering state** and may advance.

For fixed external review, AETHER X publishes commit-anchored Public Engineering Snapshots.

### Current snapshot

[`AX-PUB-SNAP-002 — Governed Intelligence Public vNext`](../snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)

Immutable technical-review anchor:

```text
6dfdec04a4d8375bc2da0bb6a3830ff07eeb1711
```

Machine-readable record:

[`AX-PUB-SNAP-002.json`](../snapshots/AX-PUB-SNAP-002.json)

Closure evidence:

[`AX-PUB-CI-002`](../evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)

### Historical snapshot

[`AX-PUB-SNAP-001 — Governed Intelligence Public v1.0`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)

A snapshot is not automatically a Git tag, GitHub Release, product release or SDK release.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 9. Formal Public Engineering Releases

AETHER X may package an intentionally published public engineering state using a Git tag and GitHub Release.

The first formal public engineering release is:

```text
Tag: public-engineering-vnext-1.0
Title: AETHER X Governed Intelligence — Public Engineering vNext 1.0
Tag target: 4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6
```

Release publication evidence is recorded in:

[`AX-PUB-REL-001`](../evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)

The release tag target and `AX-PUB-SNAP-002` anchor are intentionally distinct identifiers with distinct roles:

- the release tag fixes the repository state used to package the public engineering release;
- the snapshot anchor fixes the technical-review state and Git-blob inventory recorded by `AX-PUB-SNAP-002`.

A public engineering release does **not** establish a product release, production deployment, SDK/API stability, customer availability or internal product adoption.

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

## 10. Developer SDK Publication Readiness

The current public SDK publication gate is:

[`AX-PUB-GATE-001 — Developer SDK Publication Readiness Gate`](./AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)

Current disposition:

```text
SDK PUBLICATION: NOT AUTHORIZED
```

This disposition applies only to the public repository and does not describe private product maturity.

An official supported SDK must not be inferred from reference implementations, machine-readable schemas, conformance evidence, CI results or a public engineering release.

Promotion to an SDK publication state requires explicit evidence and authority across the gate dimensions, including licence/IP terms, interface compatibility, package identity/distribution, security/credential boundaries, failure semantics, SDK-specific conformance, supply-chain controls, documentation and maintenance/support commitments.

`PUBLIC REFERENCE IMPLEMENTATION ≠ SUPPORTED SDK`  
`PUBLIC ENGINEERING RELEASE ≠ SDK RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## 11. Snapshot, Release & Gate Immutability

A published snapshot must not be silently redefined. A later public state uses a new snapshot identifier or version.

A published release tag must not be silently moved to a different commit. A later public engineering release should use a new tag and release identity.

A readiness gate state must not be promoted without the evidence and authority required by the gate. A later change to the gate itself must remain version-traceable.

The publication of `AX-PUB-SNAP-002` does not alter the historical contents or meaning of `AX-PUB-SNAP-001`.

## 12. No Product Adoption Inference

A public artifact relationship, CI result, conformance result, snapshot, public engineering release or readiness gate does **not** establish:

- implementation by AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- a shared company-wide runtime, agent framework, authorization plane or data model;
- a production API or SDK;
- production readiness;
- customer deployment;
- regulatory or security certification.

Product adoption requires separate implementation evidence and explicit disclosure authority.

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`  
`PUBLIC CONFORMANCE ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## 13. Current Public Compatibility Set

The authoritative moving compatibility list is the machine-readable artifact manifest.

At policy version `1.6`, the current public paths are:

```text
AX-PUB-ARCH-001 v1.0

AX-PUB-SPEC-002 v1.0
→ AX-PUB-SCHEMA-001 v1.0
→ AX-PUB-REF-001 v1.0
→ AX-PUB-TEST-001 v1.0

AX-PUB-SPEC-003 v1.0
→ AX-PUB-SCHEMA-002 v1.0
→ AX-PUB-REF-002 v1.0
→ AX-PUB-TEST-001 v1.0

AX-PUB-SPEC-004 v1.0
→ AX-PUB-SCHEMA-003 v1.0
→ AX-PUB-REF-003 v1.0
→ AX-PUB-TEST-002 v1.0
```

The current fixed technical-review state is preserved by `AX-PUB-SNAP-002`. The formal public engineering publication is recorded by `AX-PUB-REL-001` and tag `public-engineering-vnext-1.0`. Future supported SDK publication is governed separately by `AX-PUB-GATE-001` and is currently **not authorized**.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
