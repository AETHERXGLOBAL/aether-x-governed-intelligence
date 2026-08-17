# AETHER X Public Artifact Compatibility & Versioning Policy

**Policy ID:** `AX-PUB-POL-001`  
**Version:** `1.0`  
**Status:** `PUBLIC ENGINEERING POLICY · ACTIVE FOR THIS REPOSITORY`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This policy defines how public AETHER X governed-intelligence artifacts are identified, versioned, related and changed inside this repository.

It applies to public reference architecture, specifications, machine-readable schemas and non-production reference implementations.

It is **not** a product-release, SDK-compatibility or production-API policy.

## 2. Artifact Identity

Each public technical artifact has a stable artifact identifier such as:

```text
AX-PUB-ARCH-001
AX-PUB-SPEC-002
AX-PUB-SCHEMA-001
AX-PUB-REF-001
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
- adding new artifact metadata or documentation.

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
```

and:

```text
AX-PUB-SPEC-003 v1.0
        ↓ defined structurally by
AX-PUB-SCHEMA-002 v1.0
        ↓ selected semantics demonstrated by
AX-PUB-REF-002 v1.0
```

## 5. Compatibility States

The public manifest may use the following relationship states:

- `CURRENT` — current public artifact in the declared compatibility set.
- `COMPATIBLE` — intended to operate with the referenced artifact version for the published reference scope.
- `SUPERSEDED` — replaced by a newer public artifact/version; retained for historical traceability where appropriate.
- `DEPRECATED` — still published for transition or historical review but should not be selected for new reference work.
- `WITHDRAWN` — no longer presented as an active public reference artifact.

These states describe public repository artifacts only. They do not describe internal product maturity.

## 6. Specification, Schema and Validator Responsibilities

A compatibility declaration does not mean the artifacts perform the same role.

### Specification

Defines normative or conceptual semantics.

### JSON Schema

Defines selected machine-readable structure, required fields, primitive types, enums and timestamp formats.

### Reference Validator

Implements selected deterministic cross-record or temporal semantics that are not fully expressible through the published schema alone.

Therefore:

`SCHEMA VALID ≠ SEMANTICALLY VALID`

`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`

## 7. Change Discipline

A material change should preserve a traceable answer to:

1. Which artifact changed?
2. Which version changed?
3. Is the change compatible or incompatible?
4. Which dependent public artifacts are affected?
5. Were examples/tests updated?
6. Did public CI validate the declared relationship?
7. Does the change alter any public claim boundary?

Changes should fail closed when the artifact manifest, referenced paths or declared compatibility relationships become internally inconsistent.

## 8. Main Branch and Reproducibility

The `main` branch represents the **current public engineering state** and may advance.

Until AETHER X separately adopts and publishes a formal tag/release policy, an external reviewer requiring reproducibility SHOULD pin a specific Git commit SHA.

A branch name alone is not a permanent reproducibility identifier.

## 9. Deprecation and Supersession

When a public artifact is superseded or deprecated, AETHER X should preserve enough public information to identify:

- the prior artifact/version;
- the successor, if one exists;
- the compatibility impact;
- the reason or scope of the transition where public disclosure is appropriate.

Historical material should not be silently rewritten in a way that obscures which public contract existed at an earlier point in time.

## 10. No Product Adoption Inference

A public artifact relationship does **not** establish:

- implementation by AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- a shared company-wide runtime or data model;
- a production API or SDK;
- production readiness;
- customer deployment;
- regulatory or security certification.

Product adoption requires separate implementation evidence and explicit disclosure authority.

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

## 11. Current Public Compatibility Set

The authoritative machine-readable list is the artifact manifest. At policy version `1.0`, the intended current paths are:

```text
AX-PUB-ARCH-001 v1.0

AX-PUB-SPEC-002 v1.0
→ AX-PUB-SCHEMA-001 v1.0
→ AX-PUB-REF-001 v1.0

AX-PUB-SPEC-003 v1.0
→ AX-PUB-SCHEMA-002 v1.0
→ AX-PUB-REF-002 v1.0
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**