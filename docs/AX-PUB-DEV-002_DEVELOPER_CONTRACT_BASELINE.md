# AX-PUB-DEV-002 — Developer Contract Baseline

**Artifact ID:** `AX-PUB-DEV-002`  
**Version:** `1.0`  
**Status:** `PUBLIC DEVELOPER CONTRACT BASELINE · DEV-GATE-00 CANDIDATE · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Program:** `AX-PUB-DEV-001`  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-002.json`

## 1. Purpose

This artifact defines the initial public developer-facing contract baseline for the AETHER X Developer Adoption & SDK Readiness Program.

It answers the questions that must be stable before SDK candidate code is allowed to become the primary public interface:

```text
WHAT CAN A DEVELOPER RELY ON?
WHAT IS EXPLICITLY OUT OF SCOPE?
WHICH PUBLIC CONTRACTS ARE CANONICAL?
HOW ARE FAILURES CLASSIFIED?
WHAT MAY CHANGE COMPATIBLY?
WHAT MUST FAIL CLOSED?
WHAT MUST REMAIN OUTSIDE THE PUBLIC BUILD / RUNTIME PATH?
```

This baseline does not publish an SDK, package, production API, support commitment or reuse licence.

`DEVELOPER CONTRACT BASELINE ≠ SUPPORTED SDK`  
`CONTRACTED PUBLIC SEMANTICS ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC VISIBILITY ≠ REUSE LICENCE`

## 2. Developer Problem Definition

The public engineering repository currently contains specifications, schemas, reference validators and conformance kits that can be inspected and reproduced. The developer-adoption problem is to make the supported public meaning of those artifacts explicit enough that an external engineer can build a compatible implementation without relying on private AETHER X knowledge.

The initial developer problem is therefore:

> **Given a declared AETHER X public governed-intelligence contract and version, a developer should be able to identify the applicable machine-readable structure, evaluate declared deterministic constraints, understand failure categories, run public conformance cases and determine whether their implementation remains inside the published public contract boundary.**

This is a contract-and-conformance problem first. It is not yet a production service-integration problem.

## 3. Initial Developer-Facing Scope

The initial contract baseline consists of three public technical paths.

### Path A — Evidence / Authority / Verification

```text
AX-PUB-SPEC-002 v1.0
→ AX-PUB-SCHEMA-001 v1.0
→ AX-PUB-REF-001 v1.0
→ AX-PUB-TEST-001 v1.0
```

Developer-facing meaning:

- preserve evidence, decision, authority, execution and verification as distinct control states;
- do not promote recommendation to decision or capability to authority;
- do not promote execution success to verified outcome;
- preserve unknown, failed, partial and inconclusive states where applicable.

### Path B — Point-in-Time Knowledge / Provenance

```text
AX-PUB-SPEC-003 v1.0
→ AX-PUB-SCHEMA-002 v1.0
→ AX-PUB-REF-002 v1.0
→ AX-PUB-TEST-001 v1.0
```

Developer-facing meaning:

- preserve observation/effective/cutoff semantics where material;
- prevent future leakage in point-in-time reconstruction;
- retain provenance, revision and supersession boundaries;
- preserve missing, unavailable, conflicted and unknown states rather than manufacturing defaults.

### Path C — Governed Agent Authority / Tool Use

```text
AX-PUB-SPEC-004 v1.0
→ AX-PUB-SCHEMA-003 v1.0
→ AX-PUB-REF-003 v1.0
→ AX-PUB-TEST-002 v1.0
```

Developer-facing meaning:

- tool availability is not permission;
- credentials are not authority;
- authority must bind principal, action, tool/resource scope, material parameters and applicable time/approval constraints;
- materially unknown or invalid authority fails closed for consequential execution;
- tool-returned success does not establish verified acceptance.

## 4. Canonical Contract Inventory

The authoritative machine-readable inventory for this baseline is `artifacts/AX-PUB-DEV-002.json`.

The canonical developer-contract roles are:

| Role | Public artifact | Contract role |
|---|---|---|
| EAV semantics | `AX-PUB-SPEC-002 v1.0` | Normative/conceptual control semantics |
| EAV structure | `AX-PUB-SCHEMA-001 v1.0` | Selected machine-readable structure |
| EAV executable reference | `AX-PUB-REF-001 v1.0` | Bounded deterministic reference behavior |
| PIT/provenance semantics | `AX-PUB-SPEC-003 v1.0` | Normative/conceptual temporal and provenance semantics |
| PIT/provenance structure | `AX-PUB-SCHEMA-002 v1.0` | Selected machine-readable structure |
| PIT executable reference | `AX-PUB-REF-002 v1.0` | Bounded deterministic reference behavior |
| Agent authority semantics | `AX-PUB-SPEC-004 v1.0` | Normative/conceptual authority/tool-use semantics |
| Agent authority structure | `AX-PUB-SCHEMA-003 v1.0` | Selected machine-readable structure |
| Agent authority executable reference | `AX-PUB-REF-003 v1.0` | Bounded deterministic reference behavior |
| Shared conformance | `AX-PUB-TEST-001 v1.0` | EAV + PIT synthetic conformance |
| Agent authority conformance | `AX-PUB-TEST-002 v1.0` | Agent-authority synthetic conformance |

No developer should infer additional contract surface merely because another file exists in the repository.

## 5. Normative Precedence for the Developer Baseline

For the initial developer contract surface, interpretation follows this order:

```text
PUBLIC SPECIFICATION
→ MACHINE-READABLE SCHEMA
→ DECLARED REFERENCE VALIDATOR BEHAVIOR
→ CONFORMANCE EXPECTATION
```

A schema establishes selected structure, not the entire semantic contract.

A reference validator demonstrates selected deterministic semantics, not every possible requirement in the specification.

A conformance case demonstrates declared expected behavior for that case; it does not enlarge the normative scope beyond the specification and registered machine-readable contract.

If an apparent conflict exists, the implementation must not silently invent precedence. The discrepancy should be treated as a contract defect requiring explicit resolution and versioned publication.

## 6. Explicit Non-Goals

DEV-GATE-00 does **not** establish:

- a production HTTP API;
- a hosted AETHER X developer service;
- a shared AETHER X runtime;
- a production authorization plane;
- credentials, authentication or account provisioning;
- live brokerage, financial execution or product execution authority;
- product-to-product integration across AETHER X initiatives;
- a package name or registry;
- a supported Python SDK;
- a stable `1.0.0` SDK API;
- an open-source or commercial reuse licence;
- customer support, SLA, uptime or maintenance commitments;
- security, regulatory or standards certification;
- product adoption by AETHER X Quantum, AX-OS, AIC or AETHER X Research.

## 7. Baseline Error Taxonomy

The developer surface needs stable failure meaning before it needs stable exception classes. The following taxonomy defines semantic categories for future SDK candidate mapping.

### `AXDEV-CONTRACT-INVALID`

The submitted structure is not valid for the declared public contract or required structural information is absent.

Typical source: JSON Schema or required contract structure.

### `AXDEV-VERSION-UNSUPPORTED`

The caller requests a contract/artifact version that is not declared supported by the active developer contract inventory.

Behavior: fail explicitly; do not silently reinterpret as another version.

### `AXDEV-EVIDENCE-INSUFFICIENT`

Material evidence required for the declared evaluation is missing, stale, unavailable or otherwise insufficient.

Behavior: preserve uncertainty, abstain or escalate according to the applicable reference contract; never manufacture evidence.

### `AXDEV-AUTHORITY-UNESTABLISHED`

Required authority cannot be established because it is missing, ambiguous, unverifiable or not attributable.

Behavior: fail closed for consequential action.

### `AXDEV-AUTHORITY-INACTIVE`

The applicable authority is expired, revoked, not yet valid or otherwise inactive.

Behavior: block new consequential execution.

### `AXDEV-AUTHORITY-SCOPE-VIOLATION`

The principal, tool, action, resource, data scope, material parameter, approval or consequence exceeds the applicable authority boundary.

Behavior: fail closed or require new authority; never silently widen scope.

### `AXDEV-TEMPORAL-CUTOFF-VIOLATION`

A point-in-time evaluation would use information unavailable after the declared knowledge cutoff or otherwise violate the declared temporal policy.

Behavior: exclude the information or explicitly enter a separately labelled hindsight/revised-history mode; do not claim point-in-time reproducibility.

### `AXDEV-PROVENANCE-INCOMPLETE`

Required source, version, transformation or lineage information is unavailable for a claim that depends on recoverable provenance.

Behavior: preserve incomplete lineage and avoid a false reproducibility claim.

### `AXDEV-CONFLICT-UNRESOLVED`

Material source or evidence conflict remains unresolved under the declared policy.

Behavior: preserve conflict/uncertainty unless a documented resolution rule applies.

### `AXDEV-VERIFICATION-FAILED`

Applicable verification criteria were evaluated and failed.

Behavior: do not create or represent a verified outcome.

### `AXDEV-VERIFICATION-INCONCLUSIVE`

Verification was performed but cannot establish pass/fail with the required confidence or evidence.

Behavior: preserve `INCONCLUSIVE`; do not treat as pass.

### `AXDEV-EXECUTION-NOT-VERIFIED`

Execution or tool invocation may have completed or returned success, but applicable verification/acceptance has not established the required outcome.

Behavior: preserve execution state separately from verified outcome state.

### `AXDEV-UNSUPPORTED-OPERATION`

The requested behavior is outside the declared developer contract surface.

Behavior: fail explicitly rather than infer product/runtime capability.

These identifiers are **developer-contract taxonomy identifiers**, not yet public Python exception class names, HTTP status codes or wire-protocol error codes. SDK-specific mapping belongs to DEV-GATE-02.

## 8. Fail-Closed Rules

A future SDK candidate built against this baseline must preserve at least the following fail-closed principles where consequential behavior is involved:

```text
UNKNOWN AUTHORITY → NO CONSEQUENTIAL EXECUTION
EXPIRED / REVOKED AUTHORITY → NO NEW EXECUTION
OUT-OF-SCOPE ACTION → NO EXECUTION
FUTURE DATA IN PIT MODE → NO PIT-CONFORMANT RESULT
FAILED VERIFICATION → NO VERIFIED OUTCOME
INCONCLUSIVE VERIFICATION → NO VERIFIED OUTCOME
UNKNOWN CONTRACT VERSION → NO SILENT VERSION COERCION
```

The public developer surface may expose analysis/validation results for these conditions; it does not thereby gain authority to execute real-world actions.

## 9. Compatibility Baseline

Compatibility remains governed by `AX-PUB-POL-001` and the public artifact manifest.

For the developer contract baseline:

- existing artifact IDs and versions identify the declared contract surface;
- additive clarification must not silently change prior normative meaning;
- incompatible semantic changes require versioned treatment under the public compatibility policy;
- a materially different contract may require a new artifact identity;
- unknown versions fail explicitly;
- compatibility between artifacts is recorded, not inferred;
- SDK-level Semantic Versioning is **not yet active** because no supported SDK API exists.

A future SDK candidate may use a pre-stable `0.y.z` line, but that is governed later by DEV-GATE-02 and does not alter this artifact-versioning policy.

## 10. Public / Private Dependency Boundary

The initial developer contract surface MUST remain independently usable for inspection, validation and conformance without any private AETHER X repository.

It must not require:

- private source code;
- private Git submodules;
- private package indexes;
- private endpoints;
- private credentials;
- unpublished schemas;
- proprietary product algorithms;
- unpublished research records;
- customer or licensed private datasets.

Public examples must remain synthetic or otherwise explicitly authorized for publication.

A future public SDK candidate must preserve this boundary unless a later explicitly authorized public contract changes it.

## 11. Product and Initiative Boundary

This baseline is intentionally non-product-specific.

It does not establish implementation or technical integration inside:

- AETHER X Quantum;
- AX-OS;
- AETHER Intelligence Core (AIC);
- AETHER X Research;
- any future private AETHER X initiative.

Product adoption requires separate implementation evidence and explicit public-disclosure authority.

## 12. DEV-GATE-00 Exit Criteria

DEV-GATE-00 may be closed only when the public repository establishes all of the following:

- [x] developer-facing problem definition;
- [x] bounded initial developer-facing scope;
- [x] canonical public contract inventory;
- [x] explicit non-goals;
- [x] baseline semantic error taxonomy;
- [x] compatibility principles;
- [x] fail-closed behavior for material unsupported/unknown states;
- [x] public/private dependency boundary;
- [x] machine-readable companion for the baseline;
- [ ] repository-level automated validation of this baseline and its manifest registration;
- [ ] successful directly observed CI evidence for that validation state.

Until the final two items are evidenced, the gate remains `CANDIDATE / NOT CLOSED`.

## 13. Promotion Boundary

Closing DEV-GATE-00 means only:

```text
PUBLIC DEVELOPER CONTRACT BASELINE ESTABLISHED
```

It does **not** mean:

```text
SDK CANDIDATE ESTABLISHED
SDK PUBLISHED
PACKAGE PUBLISHED
PRODUCTION API AVAILABLE
SUPPORT COMMITMENT ACTIVE
LICENCE GRANTED
```

The next gate after verified closure is:

```text
DEV-GATE-01 — REPRODUCIBLE DEVELOPER EXPERIENCE
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
