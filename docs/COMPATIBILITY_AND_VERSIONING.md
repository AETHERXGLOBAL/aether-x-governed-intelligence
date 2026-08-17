# AETHER X Public Artifact Compatibility & Versioning Policy

**Policy ID:** `AX-PUB-POL-001`  
**Version:** `1.3`  
**Status:** `PUBLIC ENGINEERING POLICY · ACTIVE FOR THIS REPOSITORY`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This policy defines how public AETHER X governed-intelligence artifacts are identified, versioned, related and changed inside this repository.

It applies to public reference architecture, specifications, machine-readable schemas, non-production reference implementations and public conformance-test artifacts.

It is **not** a product-release, SDK-compatibility or production-API policy.

## 2. Artifact Identity

Each public technical artifact has a stable artifact identifier such as:

```text
AX-PUB-ARCH-001
AX-PUB-SPEC-002
AX-PUB-SPEC-004
AX-PUB-SCHEMA-001
AX-PUB-REF-001
AX-PUB-TEST-001
```

The artifact ID identifies the conceptual artifact family. The version identifies a published revision within that family.

A change to the artifact title or file path does not by itself create a new artifact ID. A materially different contract may require a new ID rather than overloading an existing one.

## 3. Version Format

Current public artifacts use:

```text
MAJOR.MINOR
```

Example:

```text
1.0
1.1
2.0
```

### MAJOR

Increase `MAJOR` when a change is materially incompatible with the prior public contract, such as:

- changing the meaning of an existing normative state;
- removing or renaming a required machine-readable field without a compatible transition path;
- changing a validator rule so an important previously conforming reference case becomes invalid for a new semantic reason;
- changing a core control boundary in a way that requires consumers to reconsider their implementation assumptions.

### MINOR

Increase `MINOR` for additive or clarifying public changes that are intended to preserve the prior contract meaning, such as:

- adding optional fields;
- adding non-breaking examples;
- adding clarifying normative text that does not reverse an earlier requirement;
- adding validation for behavior already required by the associated specification;
- adding a new independently identified artifact to the current public compatibility set;
- adding new artifact metadata, conformance evidence or documentation.

A version increment does not itself establish production adoption or implementation by any AETHER X initiative.

## 4. Compatibility Is Explicit, Not Inferred

Compatibility between artifacts is recorded in the canonical machine-readable manifest:

[`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json)

A reviewer should not infer compatibility solely because two artifacts are present on the same branch or share similar names.

The intended relationship is explicit, for example:

```text
AX-PUB-SPEC-002 v1.0
        ↓ defined structurally by
AX-PUB-SCHEMA-001 v1.0
        ↓ selected semantics demonstrated by
AX-PUB-REF-001 v1.0
        ↓ selected behavior exercised by
AX-PUB-TEST-001 v1.0
```

and:

```text
AX-PUB-SPEC-003 v1.0
        ↓ defined structurally by
AX-PUB-SCHEMA-002 v1.0
        ↓ selected semantics demonstrated by
AX-PUB-REF-002 v1.0
        ↓ selected behavior exercised by
AX-PUB-TEST-001 v1.0
```

and:

```text
AX-PUB-SPEC-004 v1.0
        ↓ defined structurally by
AX-PUB-SCHEMA-003 v1.0
        ↓ selected semantics demonstrated by
AX-PUB-REF-003 v1.0
        ↓ selected behavior exercised by
AX-PUB-TEST-002 v1.0
```

`AX-PUB-SCHEMA-003`, `AX-PUB-REF-003` and `AX-PUB-TEST-002` are separately identified public artifacts. Their publication does not alter the normative text of `AX-PUB-SPEC-004 v1.0`, and their compatibility does not establish product adoption.

## 5. Compatibility States

The public manifest may use the following relationship states:

- `CURRENT` — current public artifact in the declared compatibility set.
- `COMPATIBLE` — intended to operate with the referenced artifact version for the published reference scope.
- `SUPERSEDED` — replaced by a newer public artifact/version; retained for historical traceability where appropriate.
- `DEPRECATED` — still published for transition or historical review but should not be selected for new reference work.
- `WITHDRAWN` — no longer presented as an active public reference artifact.

These states describe public repository artifacts only. They do not describe internal product maturity.

## 6. Artifact Responsibilities

A compatibility declaration does not mean related artifacts perform the same role.

### Reference Architecture

Defines a technology-neutral system-level reference structure and control boundaries.

### Specification

Defines normative or conceptual semantics.

### JSON Schema

Defines selected machine-readable structure, required fields, primitive types, enums and timestamp formats.

### Reference Validator

Implements selected deterministic cross-record, authority or temporal semantics that are not fully expressible through the published schema alone.

### Conformance Test Kit

Defines synthetic public cases, expected behavior and selected required findings for published reference validators. A conformance result applies only to the declared public artifacts and test vectors.

Therefore:

`SCHEMA VALID ≠ SEMANTICALLY VALID`

`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`

## 7. Change Discipline

A material change should preserve a traceable answer to:

1. Which artifact changed?
2. Which version changed?
3. Is the change compatible or incompatible?
4. Which dependent public artifacts are affected?
5. Were examples/tests updated where applicable?
6. What public validation or reproducible evidence applies?
7. Does the change alter any public claim boundary?

Changes should fail closed when the artifact manifest, referenced paths or declared compatibility relationships become internally inconsistent.

A public workflow existing in the repository MUST NOT be represented as a successfully verified CI run unless the run itself is directly evidenced.

## 8. Main Branch, Snapshots & Reproducibility

The `main` branch represents the **current public engineering state** and may advance.

For a fixed public-review state, AETHER X may publish a **Public Engineering Snapshot**. A snapshot records an immutable Git commit anchor, a declared artifact inventory, Git blob identities for material files and selected public CI evidence.

The current snapshot is:

[`AX-PUB-SNAP-001 — Governed Intelligence Public v1.0`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)

with anchor:

```text
f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

Its machine-readable record is [`snapshots/AX-PUB-SNAP-001.json`](../snapshots/AX-PUB-SNAP-001.json).

A public snapshot is not automatically a Git tag, GitHub Release, product release or SDK release. Until AETHER X separately adopts and publishes a formal Git tag / GitHub Release policy, the commit SHA remains the authoritative immutable identifier for reproducible review.

A branch name alone is not a permanent reproducibility identifier.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 9. Deprecation and Supersession

When a public artifact is superseded or deprecated, AETHER X should preserve enough public information to identify:

- the prior artifact/version;
- the successor, if one exists;
- the compatibility impact;
- the reason or scope of the transition where public disclosure is appropriate.

Historical material should not be silently rewritten in a way that obscures which public contract existed at an earlier point in time.

Published snapshots should preserve their original anchor and recorded inventory. A later snapshot should use a new snapshot identifier or version rather than silently redefining an earlier reproducibility record.

## 10. No Product Adoption Inference

A public artifact relationship, conformance result or snapshot does **not** establish:

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

The authoritative machine-readable compatibility list is the artifact manifest. At policy version `1.3`, the intended current paths are:

```text
AX-PUB-ARCH-001 v1.0

AX-PUB-SPEC-002 v1.0
→ AX-PUB-SCHEMA-001 v1.0
→ AX-PUB-REF-001 v1.0
↘
  AX-PUB-TEST-001 v1.0

AX-PUB-SPEC-003 v1.0
→ AX-PUB-SCHEMA-002 v1.0
→ AX-PUB-REF-002 v1.0
↘
  AX-PUB-TEST-001 v1.0

AX-PUB-SPEC-004 v1.0
→ AX-PUB-SCHEMA-003 v1.0
→ AX-PUB-REF-003 v1.0
→ AX-PUB-TEST-002 v1.0
```

The agent-authority artifacts are public reference artifacts only. They do not establish a shared agent runtime, authorization plane, credential boundary, product SDK, or implementation inside any AETHER X initiative.

The current reproducibility snapshot is separately recorded by `AX-PUB-SNAP-001` and must not be inferred from the moving `main` branch.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
