# AETHER X Governed Intelligence — Migration & Deprecation Draft

`DEV-GATE-05C CANDIDATE · NOT A SUPPORT COMMITMENT`

This document defines the developer-facing migration and deprecation process for the current installable SDK candidate and the future supported release line.

It does **not** activate a support commitment, stable `1.0.0` guarantee, fixed support window, software licence, registry publication, or release authority.

## 1. Current state

```text
DISTRIBUTION CANDIDATE: aetherxglobal-governed-intelligence
VERSION CANDIDATE: 0.1.0rc1
IMPORT: aetherxglobal.governed_intelligence
PUBLIC API CONTRACT: AX-PUB-API-001 / CANDIDATE
API VALIDATION EVIDENCE: AX-PUB-CI-012
SUPPORTED SDK: NOT ESTABLISHED
PUBLIC API 1.0.0: NOT DECLARED
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SDK PUBLICATION: NOT AUTHORIZED
```

The current machine-readable support-policy candidate is `AX-PUB-SUP-001`.

`AX-PUB-SUP-001` defines a **target** normal-removal rule of the later of 90 days or one intervening supported minor release after activation. That target is not active today and is not a present support promise.

---

## 2. Change classification

Candidate or future supported-SDK changes are classified as one of:

### CLARIFICATION
Documentation or wording changes that do not intentionally alter declared behavior.

### ADDITIVE CHANGE
New optional behavior, contract mapping or result metadata intended to preserve existing declared behavior.

### BEHAVIORAL CORRECTION
A correction where implementation behavior is inconsistent with the governing public contract or declared SDK semantics.

### INCOMPATIBLE CHANGE
A removal, rename or material semantic change to a declared public interface, error category, contract mapping or result shape that requires integrator action.

### WITHDRAWAL
Removal or emergency disablement of a path because continuing it is unsafe, legally impermissible, materially incorrect, or inconsistent with governing safety/authority requirements.

---

## 3. Required migration record

For an incompatible change, the change record should identify:

```text
CHANGE ID
AFFECTED SDK VERSION / PUBLIC API
OLD BEHAVIOR
NEW BEHAVIOR
COMPATIBILITY CLASSIFICATION
RATIONALE
MIGRATION ACTION
AFFECTED EXAMPLES / TESTS
EFFECTIVE VERSION
VALIDATION EVIDENCE
SUPPORT / DEPRECATION STATE
```

Where no safe migration exists, the record must say so rather than invent compatibility.

---

## 4. Candidate deprecation states

Before a supported stable line exists:

```text
CURRENT
DEPRECATION_PROPOSED
DEPRECATED_CANDIDATE
SUPERSEDED
WITHDRAWN
```

These are engineering states, not promises of a minimum support period.

`PRE-STABLE CANDIDATE ≠ STABLE PUBLIC API`

---

## 5. Target supported-line deprecation model

If and only if final release authority explicitly activates `AX-PUB-SUP-001`, the intended normal-removal discipline is:

```text
DECLARE DEPRECATION
→ DOCUMENT REPLACEMENT / MIGRATION
→ PRESERVE COMPATIBILITY DURING NOTICE WINDOW
→ LATER OF:
     90 DAYS
     OR ONE INTERVENING SUPPORTED MINOR RELEASE
→ ELIGIBLE FOR NORMAL REMOVAL
```

Emergency withdrawal may bypass the normal target window only for material security, legal, correctness, governance, or safety reasons and should preserve a public-safe rationale where disclosure is appropriate.

`TARGET WINDOW ≠ CURRENT SUPPORT COMMITMENT`

---

## 6. Removal discipline

A published candidate interface should not be silently removed when an evaluator or integrator could reasonably have relied on its declared existence.

A normal removal should include, as applicable:

- change classification;
- migration guidance;
- updated examples/tests;
- public API contract update;
- manifest/governance update;
- compatibility impact statement;
- CI evidence for the new state.

A future supported release must additionally follow the activated support contract.

---

## 7. Versioning boundary

The current candidate remains pre-stable at `0.1.0rc1`.

A future stable or supported version requires explicit release authority and support-policy activation. Version numbering alone does not create maturity.

`1.0.0` must not be used as a marketing maturity label.

---

## 8. No Fixed Support Window Yet

The repository currently does **not** promise:

- a binding number of months/years of support;
- an active minimum deprecation notice period;
- a long-term-support release;
- security response or fix-time SLA;
- migration assistance SLA;
- backward compatibility across all pre-stable versions.

The 90-day / one-minor values in `AX-PUB-SUP-001` remain an activation candidate only.

---

## 9. Relationship to other contracts

- `AX-PUB-API-001` defines the current candidate public API inventory.
- `AX-PUB-SUP-001` defines the candidate future support/compatibility/maintenance model.
- `AX-PUB-SEC-001` defines the candidate security-operations readiness model.
- `AX-PUB-POL-001` remains the repository-wide public artifact compatibility/versioning policy.

These artifacts are distinct because repository artifact compatibility is not the same thing as an SDK support commitment.

---

## 10. Publication boundary

```text
MIGRATION PROCESS DEFINED: YES / CANDIDATE
SUPPORT COMMITMENT ACTIVATED: NO
STABLE 1.0 API GUARANTEE: NO
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION NOT AUTHORIZED
```

---

`MIGRATION DRAFT ≠ SUPPORT PROMISE`  
`TARGET DEPRECATION WINDOW ≠ ACTIVE DEPRECATION GUARANTEE`  
`PRE-STABLE CANDIDATE ≠ STABLE PUBLIC API`  
`SDK PUBLICATION NOT AUTHORIZED`
