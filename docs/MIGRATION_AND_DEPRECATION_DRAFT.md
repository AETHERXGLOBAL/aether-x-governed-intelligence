# AETHER X Governed Intelligence — Migration & Deprecation Draft

`DEV-GATE-04 CANDIDATE · DRAFT PROCESS · NOT A SUPPORT COMMITMENT`

This document defines a draft mechanism for communicating future candidate/API changes before a supported SDK or stable public API is authorized.

It does not establish a fixed support window, notice period, stable `1.0.0` API or backward-compatibility guarantee.

## 1. Purpose

A developer surface becomes difficult to adopt if change semantics are unclear.

The current objective is therefore to make future change classification understandable **before** AETHER X makes any stable support commitment.

## 2. Current Status

```text
SDK CANDIDATE VERSION: 0.1.0-candidate
SUPPORTED SDK: NOT ESTABLISHED
PUBLIC API 1.0.0: NOT DECLARED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

## 3. Change Classification

Candidate changes should be classified as one of:

### CLARIFICATION
Documentation or wording changes that do not intentionally change declared candidate behavior.

### ADDITIVE CANDIDATE CHANGE
New optional behavior, contract mapping or result metadata intended not to invalidate existing declared candidate behavior.

### BEHAVIORAL CORRECTION
A correction where existing candidate behavior is inconsistent with the governing public contract or declared semantics.

### INCOMPATIBLE CANDIDATE CHANGE
A change that removes, renames or materially changes a declared candidate interface, error category, contract mapping or result shape in a way that requires evaluator/integrator action.

### WITHDRAWAL
Removal of a previously exposed candidate path because it is unsafe, invalid, superseded or no longer intended for progression.

## 4. Draft Migration Record

For an incompatible candidate change, the public change record should identify:

```text
CHANGE ID
AFFECTED ARTIFACT / INTERFACE
OLD BEHAVIOR
NEW BEHAVIOR
COMPATIBILITY CLASSIFICATION
WHY THE CHANGE IS REQUIRED
MIGRATION ACTION
AFFECTED EXAMPLES / TESTS
EFFECTIVE CANDIDATE VERSION
EVIDENCE / CI RESULT
```

Where no safe migration exists, the record should say so explicitly rather than inventing compatibility.

## 5. Candidate Deprecation States

Before a stable supported API exists, the following states may be used for public candidate surfaces:

```text
CURRENT
DEPRECATION_PROPOSED
DEPRECATED_CANDIDATE
SUPERSEDED
WITHDRAWN
```

These states describe public candidate engineering only.

`DEPRECATED_CANDIDATE` does not imply a guaranteed support period.

## 6. Removal Discipline

A candidate interface should not be silently removed from the public surface when external evaluators could reasonably have relied on its published existence.

A removal should normally include:

- explicit change classification;
- migration guidance where available;
- updated examples/tests;
- manifest/governance update;
- compatibility impact statement;
- CI evidence for the new state.

Emergency withdrawal may occur when a material security, correctness, legal or governance issue makes continued exposure inappropriate. The reason should be documented to the degree safe for public disclosure.

## 7. Versioning Boundary

The candidate remains pre-stable.

A future supported `1.0.0` would require an explicit declaration of the supported public API and compatibility commitment under the SDK release decision gate.

`1.0.0` must not be used as a maturity marketing label.

## 8. No Fixed Support Window Yet

This draft deliberately does **not** promise:

- a number of months/years of support;
- a minimum deprecation notice period;
- long-term support releases;
- security-fix timelines;
- migration assistance;
- backward compatibility across all pre-stable versions.

Those commitments require an approved maintenance/support model.

## 9. Relationship to AX-PUB-POL-001

`AX-PUB-POL-001` remains the current public artifact compatibility/versioning policy.

This draft adds developer-facing migration/deprecation preparation for Gate-04. It does not replace the policy or create supported-SDK semantics.

## 10. Gate-04 Boundary

Gate-04 may validate that this draft is clear, consistent and externally usable.

Gate-04 cannot convert this draft into a support contract.

---

`MIGRATION DRAFT ≠ SUPPORT PROMISE`  
`DEPRECATION PROCESS ≠ FIXED SUPPORT WINDOW`  
`PRE-STABLE CANDIDATE ≠ STABLE PUBLIC API`  
`SDK PUBLICATION NOT AUTHORIZED`
