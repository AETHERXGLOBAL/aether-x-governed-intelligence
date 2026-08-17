# AETHER X Public Artifact Compatibility & Versioning Policy

**Policy ID:** `AX-PUB-POL-001`  
**Version:** `1.4`  
**Status:** `PUBLIC ENGINEERING POLICY · ACTIVE FOR THIS REPOSITORY`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This policy defines how public AETHER X governed-intelligence artifacts are identified, versioned, related, validated and changed inside this repository.

It applies to public reference architecture, specifications, machine-readable schemas, non-production reference implementations, public conformance-test artifacts, validation-evidence records and reproducibility snapshots.

It is **not** a product-release, SDK-compatibility or production-API policy.

## 2. Artifact Identity

Each public technical artifact has a stable identifier such as:

```text
AX-PUB-ARCH-001
AX-PUB-SPEC-002
AX-PUB-SCHEMA-001
AX-PUB-REF-001
AX-PUB-TEST-001
AX-PUB-CI-001
AX-PUB-SNAP-001
```

The artifact ID identifies the conceptual artifact family. The version identifies a published revision within that family.

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
- new snapshots or snapshot semantics;
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

Therefore:

`SCHEMA VALID ≠ SEMANTICALLY VALID`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`  
`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC CI PASS ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 7. Change Discipline

A material public change should preserve a traceable answer to:

1. Which artifact changed?
2. Which version changed?
3. Is the change compatible or incompatible?
4. Which dependent public artifacts are affected?
5. Were examples/tests updated where applicable?
6. What public validation or reproducible evidence applies?
7. Does the change alter a public claim boundary?

Changes should fail closed when artifact paths, versions, declared relationships, evidence references or snapshot references become internally inconsistent.

A public workflow MUST NOT be represented as a successfully verified CI run unless the run itself is directly evidenced.

## 8. Main Branch & Reproducibility Snapshots

The `main` branch represents the **current moving public engineering state** and may advance.

For fixed external review, AETHER X publishes commit-anchored Public Engineering Snapshots.

### Current snapshot

[`AX-PUB-SNAP-002 — Governed Intelligence Public vNext`](../snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)

Immutable anchor:

```text
6dfdec04a4d8375bc2da0bb6a3830ff07eeb1711
```

Machine-readable record:

[`AX-PUB-SNAP-002.json`](../snapshots/AX-PUB-SNAP-002.json)

Closure evidence:

[`AX-PUB-CI-002`](../evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)

### Historical snapshot

[`AX-PUB-SNAP-001 — Governed Intelligence Public v1.0`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)

A snapshot is not automatically a Git tag, GitHub Release, product release or SDK release. Until a formal tag/release is actually created, the recorded full commit SHA is the authoritative immutable review identifier.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 9. Snapshot Immutability & Supersession

A published snapshot must not be silently redefined. A later public state uses a new snapshot identifier or version.

The publication of `AX-PUB-SNAP-002` does not alter the historical contents or meaning of `AX-PUB-SNAP-001`.

Snapshot validation evidence may be published separately from the immutable anchor inventory, provided the evidence record clearly identifies the validated snapshot and verification state.

## 10. No Product Adoption Inference

A public artifact relationship, CI result, conformance result or snapshot does **not** establish:

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

## 11. Current Public Compatibility Set

The authoritative moving compatibility list is the machine-readable artifact manifest.

At policy version `1.4`, the current public paths are:

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

The current fixed review state is separately preserved by `AX-PUB-SNAP-002`.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
