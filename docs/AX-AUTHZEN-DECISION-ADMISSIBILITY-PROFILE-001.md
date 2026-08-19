# AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001

**Version:** `0.1`  
**Status:** `DESIGN_CANDIDATE / NON-BINDING / OFFLINE / READ-ONLY / NO_RUNTIME_IMPLEMENTATION`  
**Baseline:** `256594c364ca3e76eb7d6d95cd93d56e9773e36f`  
**Parent research:** `AX-AUTHORIZATION-INTEROP-RESEARCH-002 @ 51c9f0d5697af8f52e32a27e1a1330b006876791` — Independent Technical Oversight research result `PASS`.

## 1. Objective

Define only the semantic admissibility boundary for an AuthZEN Authorization API 1.0 request/response pair that has already been supplied offline.

This profile does **not** implement AuthZEN networking, a PDP, cryptography, trust-store management, an authorization engine, or runtime enforcement.

Its single purpose is to prevent an external PDP decision from collapsing AETHER's semantic and authority boundaries.

Required separation:

```text
RECEIVED
  != REQUEST_BOUND
  != RESPONSE_INTEGRITY_VERIFIED
  != PDP_TRUSTED
  != DECISION_ADMISSIBLE
  != AETHER_DECISION
  != AETHER_AUTHORITY
  != EXECUTION_PERMISSION
```

Also preserved:

```text
Evidence != Decision
Decision != Authority
Authority != Capability
External Decision != AETHER Authority
Unknown != Pass
Execution != Verified Outcome
```

## 2. Preserve / do not touch

The existing `AX-PUB-SCHEMA-003 Agent Tool-Use Authority Envelope` remains unchanged.

In particular, this design does not redefine or mutate:

- `action_proposal`;
- `authority_context`;
- `tool_use_grant`;
- `tool_invocation`;
- `tool_result`;
- current Point-in-Time/provenance semantics.

AuthZEN is treated only as an external decision-interoperability source. It does not replace AETHER's authority model.

## 3. Default classification

The exact AuthZEN request, exact AuthZEN response, raw boolean `decision`, PDP identity claims, policy claims, timestamps, and response context enter AETHER first as:

```text
target = evidence_record
classification = SOURCE_DATA
semantic_role = EXTERNAL_AUTHORIZATION_DECISION_SOURCE_DATA
promotion = NONE
```

Therefore:

```text
raw decision=true  != AETHER Decision
raw decision=false != trusted terminal deny until admissibility
```

An unverified or untrusted response has no trusted ALLOW/DENY semantics. It is `INADMISSIBLE/UNKNOWN -> NO_PROCEED`.

## 4. Stage contract

### 4.1 `RECEIVED`

Meaning: the offline input pair is preserved as source data and satisfies minimum structure. The AuthZEN response must carry a boolean decision.

Results: `PASS / FAIL`.

`RECEIVED=PASS` proves neither request binding nor response integrity nor PDP trust.

### 4.2 `REQUEST_BOUND`

Meaning: the exact external request is deterministically bound, under an explicit binding-profile identity/version, to the intended existing AETHER action proposal.

A PASS requires explicit binding of:

| External dimension | Required AETHER binding |
|---|---|
| `Subject` | `action_proposal.principal_id` |
| `Resource` | `action_proposal.target_resource` and material target identity |
| `Action` | `action_proposal.proposed_action` |
| Tool dimension | `action_proposal.proposed_tool` through an explicit profiled request/context or correlation binding; never inferred from Action alone |
| `Context` | `action_proposal.bounded_parameters` plus every profile-defined enforcement-relevant context dimension |
| Decision use | `action_proposal.proposal_id` |

Results: `PASS / FAIL / UNKNOWN`.

A deterministic mismatch is `FAIL`. A required dimension that cannot be established without inference is `UNKNOWN`. Both mean `NO_PROCEED` for an allow path.

### 4.3 `RESPONSE_INTEGRITY_VERIFIED`

Meaning: explicit external verification evidence establishes integrity/correlation for the exact response and exact bound request.

Results: `PASS / FAIL / UNKNOWN / NOT_EVALUATED`.

A PASS requires a defined verification-method identity and evidence tied to the exact response identity plus exact request identity or explicit request/response correlation.

This profile implements no cryptography and defines no transport security mechanism.

### 4.4 `PDP_TRUSTED`

Meaning: the verified PDP identity is admitted for this purpose by an explicit applicable point-in-time AETHER trust policy.

Results: `PASS / FAIL / UNKNOWN / NOT_EVALUATED`.

A PASS requires:

- `RESPONSE_INTEGRITY_VERIFIED=PASS`;
- verified PDP identity;
- trust-policy identity;
- immutable trust-policy version or digest;
- purpose/scope match;
- known trust-policy evaluation time.

Missing PDP identity, trust-policy identity/version/digest, or evaluation time is `UNKNOWN`; none may be inferred from endpoint names, local configuration, raw response content, or observation time.

### 4.5 `DECISION_ADMISSIBLE`

Meaning: the external AuthZEN decision is admissible **only as bounded external authorization decision evidence** for exactly the bound action proposal.

Results:

- `ADMISSIBLE_ALLOW`
- `ADMISSIBLE_DENY`
- `FAIL`
- `UNKNOWN`
- `NOT_EVALUATED`

Any admissible result requires all of:

- `RECEIVED=PASS`;
- `REQUEST_BOUND=PASS`;
- `RESPONSE_INTEGRITY_VERIFIED=PASS`;
- `PDP_TRUSTED=PASS`;
- exact raw boolean decision preserved;
- PDP policy identity;
- immutable PDP policy version/digest;
- PDP evaluation time;
- explicit freshness/validity policy PASS;
- replay check PASS for this exact decision use;
- all enforcement-relevant request/response context classified and understood.

#### Admissible deny

Only after admissibility is established:

```text
decision=false -> ADMISSIBLE_DENY -> terminal NO_PROCEED for this adapter path
```

The adapter cannot flip it to allow.

`ADMISSIBLE_DENY` still does not auto-create an AETHER Decision record.

#### Admissible allow

Only after all admissibility requirements pass:

```text
decision=true -> ADMISSIBLE_ALLOW
```

But:

```text
ADMISSIBLE_ALLOW
  != AETHER_DECISION
  != AETHER_AUTHORITY
  != CAPABILITY
  != authority_context
  != tool_use_grant
  != EXECUTION_PERMISSION
  != AETHER Verification
  != Verified Outcome
```

### 4.6 `AETHER_DECISION`

The adapter may not create this stage.

A separate AETHER decision process may consume admissible external decision evidence under its own requirements.

Default from this profile: `NOT_CREATED`.

### 4.7 `AETHER_AUTHORITY`

The adapter may not create `authority_context`, `tool_use_grant`, delegation, approval, or capability.

Default from this profile: `NOT_CREATED`.

### 4.8 `EXECUTION_PERMISSION`

The adapter may not grant invocation or external side-effect permission.

A separate execution gate must evaluate existing AETHER authority, capability, tool, resource, parameter, validity, and revocation constraints.

Default from this profile: `NOT_GRANTED`.

## 5. Exact identity and Point-in-Time rules

When original bytes exist, preserve separate SHA-256 identities for:

- exact received request bytes;
- exact received response bytes.

If only parsed objects are supplied, exact-byte identity is `UNAVAILABLE`; no reserialization digest may be silently presented as received-byte identity.

`observed_at` is an AETHER observation timestamp and is distinct from PDP evaluation time.

```text
observed_at != PDP evaluation time
```

A missing PDP evaluation time remains missing and makes admissibility `UNKNOWN`; neither current time nor observation time may replace it.

The design similarly forbids inference of missing PDP identity, PDP policy identity/version/digest, or AETHER trust-policy identity/version.

## 6. Response context

Raw AuthZEN response context is preserved as external source data.

Only a field explicitly profiled with defined enforcement semantics may affect admissibility or enforcement.

Unprofiled response context must not become, by implication:

- obligation;
- approval;
- delegation;
- authority;
- capability;
- tool-use grant;
- AETHER Decision metadata.

If a field is unrecognized or its enforcement relevance is unknown, an external allow cannot be admitted:

```text
UNKNOWN enforcement relevance -> DECISION_ADMISSIBLE=UNKNOWN/FAIL -> NO_PROCEED
```

A context field may be ignored only if the active reviewed profile explicitly classifies it as non-enforcement informational data.

## 7. Replay and freshness

A previously valid allow is not automatically reusable.

An admissible allow requires:

- exact request identity;
- exact response identity when available;
- exact bound proposal reference;
- PDP evaluation time;
- explicit freshness/validity policy identity/version;
- replay check PASS for this use.

Rules:

```text
reused for different proposal/material request -> FAIL -> NO_PROCEED
replay status unavailable                    -> UNKNOWN -> NO_PROCEED
stale/outside permitted validity             -> FAIL -> NO_PROCEED
```

No replay database or runtime store is designed here; this is only the semantic evidence requirement.

## 8. Negative semantic cases

The design requires at least the following cases before any implementation can be authorized:

| ID | Condition | Required result | Forbidden |
|---|---|---|---|
| NEG-AZ-001 | malformed request/response or non-boolean decision | `RECEIVED=FAIL`; later stages not reached | trusted allow/deny |
| NEG-AZ-002 | raw `decision=true` before checks | SOURCE_DATA; `NO_PROCEED` | AETHER Decision/Authority/grant/capability/execution |
| NEG-AZ-003 | raw `decision=false` before checks | SOURCE_DATA; `NO_PROCEED` | trusted terminal deny claim |
| NEG-AZ-004 | Subject mismatch | `REQUEST_BOUND=FAIL` | admissible allow |
| NEG-AZ-005 | Resource mismatch | `REQUEST_BOUND=FAIL` | admissible allow |
| NEG-AZ-006 | Action mismatch | `REQUEST_BOUND=FAIL` | admissible allow |
| NEG-AZ-007 | tool binding missing | `REQUEST_BOUND=UNKNOWN` | infer tool from Action/Resource |
| NEG-AZ-008 | Context/parameter mismatch | `REQUEST_BOUND=FAIL` | admissible allow |
| NEG-AZ-009 | response integrity/correlation unknown | `RESPONSE_INTEGRITY_VERIFIED=UNKNOWN`; no later PASS | trusted allow/deny |
| NEG-AZ-010 | verified PDP identity missing | `PDP_TRUSTED=UNKNOWN` | infer PDP identity |
| NEG-AZ-011 | trust-policy identity/version/digest missing | `PDP_TRUSTED=UNKNOWN` | PDP trust PASS |
| NEG-AZ-012 | PDP evaluated policy identity/version absent | `DECISION_ADMISSIBLE=UNKNOWN` | admissible allow/deny |
| NEG-AZ-013 | PDP evaluation time absent | `DECISION_ADMISSIBLE=UNKNOWN` | substitute observation/current time |
| NEG-AZ-014 | `observed_at` substituted for evaluation time | FAIL/UNKNOWN | point-in-time PDP provenance claim |
| NEG-AZ-015 | decision replayed for different proposal/material request | `DECISION_ADMISSIBLE=FAIL` | admissible allow |
| NEG-AZ-016 | replay evidence unavailable | `DECISION_ADMISSIBLE=UNKNOWN` | assume freshness/single use |
| NEG-AZ-017 | stale allow | `DECISION_ADMISSIBLE=FAIL` | admissible allow |
| NEG-AZ-018 | unprofiled response context | SOURCE_DATA only; unknown enforcement relevance => `UNKNOWN` | obligation/approval/delegation/authority inference |
| NEG-AZ-019 | unknown enforcement-relevant request/response context | binding/admissibility `UNKNOWN` | fail-open |
| NEG-AZ-020 | all checks pass and raw decision=false | `ADMISSIBLE_DENY`; terminal `NO_PROCEED` | adapter flips to allow/execution |
| NEG-AZ-021 | all checks pass and raw decision=true | `ADMISSIBLE_ALLOW`; AETHER Decision/Authority not created; execution not granted | any semantic promotion |
| NEG-AZ-022 | PDP would be trusted but response integrity not PASS | PDP trust not evaluated; no admissibility PASS | trusted decision use |

## 9. Out of scope

No:

- network client;
- PDP;
- Cedar;
- OpenFGA;
- OAuth;
- WIMSE;
- transaction-token work;
- crypto subsystem;
- trust-store management;
- schema mutation;
- SDK/runtime integration;
- Gate/Release/Production action;
- risk acceptance.

## 10. Design review boundary

This document and the companion JSON artifact are **design candidates only**.

They do not authorize implementation.

Any implementation would touch the `Decision != Authority` trust boundary and therefore requires Independent Technical Oversight re-review of the exact design revision first.

`DESIGNED != IMPLEMENTED != VERIFIED != ACCEPTED`.
