# AX-PUB-SUP-001 — SDK Support, Compatibility & Maintenance Contract Candidate

**Artifact ID:** `AX-PUB-SUP-001`  
**Version:** `0.1`  
**State:** `DEV-GATE-05C SUPPORT CONTRACT CANDIDATE`  
**Applies to:** future official AETHER X Governed Intelligence Python SDK release line  
**Support commitment established:** `NO`  
**Production support activated:** `NO`  
**SDK publication:** `NOT AUTHORIZED`

## 1. Purpose

A production SDK is not defined by package installation alone. A production consumer must know what is supported, what may change, how long compatibility is intended to last, how deprecation works, and which behaviors are outside the support boundary.

This artifact defines that operating contract **before activation** so AETHER X can validate the model before making a binding public support commitment.

```text
PACKAGE EXISTS
≠ SUPPORTED SDK

PUBLIC API CONTRACT
+ VERSIONING RULES
+ DEPRECATION RULES
+ MAINTENANCE MODEL
+ SECURITY OPERATIONS
+ RELEASE AUTHORITY
= SUPPORTABLE SDK
```

---

## 2. Bound SDK candidate

```text
Distribution: aetherxglobal-governed-intelligence
Version candidate: 0.1.0rc1
Import namespace: aetherxglobal.governed_intelligence
Public API contract: AX-PUB-API-001
API validation evidence: AX-PUB-CI-012
Candidate runtime matrix: CPython 3.11–3.14
```

The current candidate remains pre-1.0 and non-published.

---

## 3. Support scope candidate

The first production-supported scope is intended to cover only the declared offline validation SDK surface:

- declared public imports under `aetherxglobal.governed_intelligence`;
- declared contract validation for `AX-PUB-SPEC-002/003/004`;
- documented result and finding semantics;
- canonical package installation after registry authorization;
- documented supported Python runtime matrix;
- correctness/security maintenance inside the activated support policy;
- migration/deprecation guidance.

Not included without a separate contract:

- private AETHER X product integrations;
- remote AETHER X service availability;
- production authorization decisions;
- agent or tool execution;
- brokerage or financial execution;
- customer-specific integration;
- commercial response-time SLA.

---

## 4. Versioning model after activation

Once a supported release line is explicitly authorized, the target model is Semantic Versioning for the declared SDK public API.

### PATCH

Intended for correctness, security and documentation fixes that do not intentionally break the declared public API.

### MINOR

May add compatible public functionality and may introduce deprecations. Under normal conditions, a public API already declared deprecated is not removed within the same major line until the activated deprecation rule permits removal.

### MAJOR

May contain incompatible public API changes, but requires explicit migration guidance and a release record identifying the break.

### PRE-1.0

The current `0.1.0rc1` state remains candidate engineering. Breaking changes remain possible, but they must be explicitly classified and accompanied by migration guidance where a safe migration exists.

`PRE-1.0 ≠ UNCONTROLLED CHANGE`

---

## 5. Candidate deprecation rule

Normal target after activation:

```text
REMOVAL ELIGIBILITY
= later of:
  90 days after deprecation notice
  OR
  one intervening supported minor release
```

This 90-day/one-minor rule is a **candidate commitment**, not a currently active promise.

Emergency withdrawal may use a shorter path only for material:

- security risk;
- legal constraint;
- correctness failure;
- governance/safety issue.

An emergency exception must preserve a public-safe rationale and migration/mitigation guidance where possible.

---

## 6. Candidate maintenance model

Target model after activation:

```text
PRIMARY MAINTAINED LINE:
latest supported minor within current supported major

PREVIOUS MINOR:
security/correctness fixes targeted for up to 90 days after successor minor

LONG-TERM SUPPORT LINE:
not established
```

The 90-day previous-minor window is not active until final release authority adopts this contract.

Upstream Python lifecycle changes do not create automatic permanent support. The supported runtime matrix must be reviewed and changed explicitly, with migration notice when material.

---

## 7. Breaking-change classification

Compatibility-sensitive changes include, at minimum:

- removing/renaming a declared public export;
- incompatible callable signature change;
- removing/reordering exported dataclass constructor fields;
- changing an existing `ErrorCategory` value;
- changing an existing contract descriptor identity;
- changing fail-closed unsupported contract/version behavior;
- introducing network/execution side effects into an API declared offline-only.

The machine-readable public API contract remains the primary SDK-surface inventory.

---

## 8. Migration obligation

A material incompatible change should record:

```text
CHANGE ID
OLD VERSION / BEHAVIOR
NEW VERSION / BEHAVIOR
COMPATIBILITY CLASS
REASON
MIGRATION ACTION
AFFECTED API / CONTRACT
EFFECTIVE RELEASE
VALIDATION EVIDENCE
```

Where no safe migration exists, the record must say so explicitly.

---

## 9. End-of-support discipline

Before a supported release line can be ended, AETHER X must publish an explicit end-of-support state for that line.

This candidate does not yet commit to a fixed EOS notice period.

A final support contract must define the notice model before the first supported production release is authorized.

---

## 10. Activation requirements

This contract must remain inactive until all required evidence exists:

```text
AX-PUB-API-001 VALIDATED AND BOUND TO RELEASE
RELEASE CONTROL READINESS ESTABLISHED
REGISTRY OWNERSHIP ESTABLISHED
PYPI TRUSTED PUBLISHER ESTABLISHED
IP / COPYRIGHT CLEARANCE ESTABLISHED
PUBLIC SDK LICENCE GRANTED
DEDICATED SECURITY INTAKE ESTABLISHED
SECURITY RESPONSE OWNER ASSIGNED
INDEPENDENT HUMAN EXTERNAL EVALUATION COMPLETE
FINAL RELEASE EVIDENCE PACK COMPLETE
EXPLICIT DEV-GATE-05D RELEASE AUTHORITY
```

No subset of these requirements silently activates production support.

---

## 11. Current disposition

```text
SUPPORT CONTRACT CANDIDATE: DEFINED
SUPPORT COMMITMENT: NOT ESTABLISHED
PRODUCTION SUPPORT: NOT ACTIVATED
STABLE 1.0 SEMVER COMMITMENT: NOT ESTABLISHED
COMMERCIAL SLA: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
