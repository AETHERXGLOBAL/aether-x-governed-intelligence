# AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001

**Version:** `0.1`  
**Status:** `DESIGN_CANDIDATE / NON-BINDING / OFFLINE / READ-ONLY / SINGLE_ACCESS_EVALUATION_ONLY / NO_RUNTIME_IMPLEMENTATION`  
**Baseline:** `256594c364ca3e76eb7d6d95cd93d56e9773e36f`  
**Parent research:** `AX-AUTHORIZATION-INTEROP-RESEARCH-002 @ 51c9f0d5697af8f52e32a27e1a1330b006876791` — Independent Technical Oversight research result `PASS`.  
**Correction basis:** Independent Technical Oversight review of `d823e163f227d471e5e7ba25d8933aa2372fa3e6` — `CORRECTION / BOUNDED DESIGN CORRECTION ONLY`.

## 1. Objective

Define only the semantic admissibility boundary for **one AuthZEN Authorization API 1.0 single Access Evaluation** request/response pair that has already been supplied offline.

This profile does **not** implement AuthZEN networking, a PDP, cryptography, trust-store management, an authorization engine, runtime enforcement, canonical-object identity, Access Evaluations/boxcarring, or Search APIs.

Its single purpose is to prevent an external PDP decision — and the provenance asserted around that decision — from collapsing AETHER's semantic and authority boundaries.

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
Asserted Provenance != Verified Provenance
External Decision != AETHER Authority
Unknown != Pass
Execution != Verified Outcome
```

## 2. Preserve / do not touch

The existing `AX-PUB-SCHEMA-003 Agent Tool-Use Authority Envelope` remains unchanged.

This design does not redefine or mutate:

- `action_proposal`;
- `authority_context`;
- `tool_use_grant`;
- `tool_invocation`;
- `tool_result`;
- current Point-in-Time/provenance semantics.

AuthZEN remains only an external decision-interoperability source. It does not replace AETHER's authority model.

`NEG-AZ-001` through `NEG-AZ-022` remain preserved. The correction adds cases after them; it does not reinterpret the original cases.

## 3. v0.1 API surface

**Supported:** one AuthZEN **single Access Evaluation API** request/response pair.

**Unsupported / out of scope in v0.1:**

- AuthZEN `Access Evaluations` / boxcarring;
- AuthZEN Search APIs.

If an unsupported surface is encountered, it may be preserved as raw `SOURCE_DATA`, but this profile assigns it no decision-admissibility semantics:

```text
UNSUPPORTED -> DECISION_ADMISSIBLE=NOT_EVALUATED/UNKNOWN -> NO_PROCEED
```

No single-evaluation result may be synthesized from a boxed or search response.

## 4. Default classification

The exact AuthZEN request, exact AuthZEN response, raw boolean `decision`, PDP identity claims, policy claims, timestamps, freshness claims/results, replay claims/results, trust claims/results, and response context enter AETHER first as:

```text
target = evidence_record
classification = SOURCE_DATA
semantic_role = EXTERNAL_AUTHORIZATION_DECISION_SOURCE_DATA
promotion = NONE
```

A value being present, asserted, or caller-supplied does not establish any PASS.

Therefore:

```text
raw decision=true   != AETHER Decision
raw decision=false  != trusted terminal deny until admissibility
pdp_id supplied     != PDP_TRUSTED
policy_id supplied  != policy provenance verified
timestamp supplied  != PDP evaluation time verified
freshness_pass=true != freshness verified
replay_pass=true    != replay verified
```

An unverified or untrusted response has no trusted ALLOW/DENY semantics. It is `INADMISSIBLE/UNKNOWN -> NO_PROCEED`.

## 5. Immutable identity and object-only input

### 5.1 Original immutable identity

When original bytes exist, preserve separate SHA-256 identities for:

- exact received request bytes;
- exact received response bytes.

These identities are the v0.1 immutable request/response identities used by admissibility.

### 5.2 Parsed-object-only input

Parsed-object-only request/response input is allowed for import as `SOURCE_DATA`.

If original immutable request or response identity is unavailable:

```text
SOURCE_DATA import = allowed
DECISION_ADMISSIBLE = not reachable
NO_PROCEED
```

More specifically:

- without original immutable request identity, `REQUEST_BOUND` cannot PASS;
- without original immutable response identity, `RESPONSE_INTEGRITY_VERIFIED` cannot PASS;
- without both, neither `ADMISSIBLE_ALLOW` nor `ADMISSIBLE_DENY` may be produced.

### 5.3 No identity substitution

A digest of locally reserialized JSON must **not** be presented as received-byte/original immutable identity.

No canonical-object identity, JSON canonicalization, semantic hash, or equivalent new identity mechanism is defined by this profile.

```text
parsed equivalence != original immutable identity
reserialization hash != received-byte identity
```

## 6. Stage contract

### 6.1 `RECEIVED`

Meaning: one offline single Access Evaluation request/response pair is preserved as source data and satisfies minimum structure. The response must carry a boolean decision.

Parsed-object-only input is permitted at this stage.

Results: `PASS / FAIL`.

`RECEIVED=PASS` proves neither immutable identity, request binding, response integrity, PDP trust, nor provenance validity.

### 6.2 `REQUEST_BOUND`

Meaning: the **exact immutable request identity** is deterministically bound, under an explicit binding-profile identity/version, to the intended existing AETHER action proposal.

A PASS requires:

| External dimension | Required AETHER binding |
|---|---|
| immutable request identity | original request identity available and preserved |
| `Subject` | `action_proposal.principal_id` |
| `Resource` | `action_proposal.target_resource` and material target identity |
| `Action` | `action_proposal.proposed_action` |
| Tool dimension | `action_proposal.proposed_tool` through explicit profiled request/context or correlation binding; never inferred from Action alone |
| `Context` | `action_proposal.bounded_parameters` plus every profile-defined enforcement-relevant context dimension |
| Decision use | `action_proposal.proposal_id` |
| Binding contract | explicit binding profile identity/version |

Results: `PASS / FAIL / UNKNOWN`.

A deterministic mismatch is `FAIL`. A required dimension or immutable request identity that cannot be established without inference is `UNKNOWN`. Both mean `NO_PROCEED` for an allow path.

### 6.3 `RESPONSE_INTEGRITY_VERIFIED`

Meaning: explicit **attributable external verification evidence** establishes integrity/correlation for the exact immutable response identity and exact bound request identity.

Results: `PASS / FAIL / UNKNOWN / NOT_EVALUATED`.

A PASS requires:

- `RECEIVED=PASS`;
- `REQUEST_BOUND=PASS`;
- original immutable response identity;
- verification source/identity;
- verification-method identity;
- verification result;
- verification/check time where applicable;
- binding of that verification result to the exact response identity;
- binding to the exact request identity and exact bound proposal.

This profile implements no cryptography and defines no transport-security mechanism.

If only a parsed response object exists, the response remains `SOURCE_DATA` and this stage cannot PASS.

### 6.4 `PDP_TRUSTED`

Meaning: a **verified PDP identity attributable to this exact decision use** is admitted for this purpose by an explicit applicable point-in-time AETHER trust policy.

Results: `PASS / FAIL / UNKNOWN / NOT_EVALUATED`.

A PASS requires:

- `RESPONSE_INTEGRITY_VERIFIED=PASS`;
- verified PDP identity;
- attributable identity-source/verification identity;
- identity verification method/result;
- binding of PDP identity evidence to the exact request identity;
- binding to the exact response identity;
- binding to the exact proposal and intended purpose;
- trust-policy identity;
- immutable trust-policy version or digest;
- purpose/scope match;
- known trust-policy evaluation/check time;
- trust result bound to that same verified PDP identity and decision use.

A PDP identity merely present in the response, local configuration, endpoint name, or caller input remains `SOURCE_DATA`.

Missing, asserted-only, unbound, or unverified provenance means:

```text
PDP_TRUSTED=UNKNOWN/NOT_EVALUATED -> NO_PROCEED
```

### 6.5 `DECISION_ADMISSIBLE`

Meaning: the external AuthZEN decision is admissible **only as bounded external authorization decision evidence** for exactly the bound AETHER action proposal.

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
- original immutable request identity;
- original immutable response identity;
- exact raw boolean decision preserved;
- verified PDP policy identity + immutable version/digest attributable to this exact PDP evaluation;
- verified PDP evaluation time attributable to this exact PDP evaluation;
- freshness result PASS with attributable checker identity, policy identity/version/digest, check time, and exact request/response/proposal bindings;
- replay result PASS with attributable checker identity, policy identity/version/digest, check time, and exact request/response/proposal bindings;
- all enforcement-relevant request/response context classified and understood.

No asserted/supplied provenance field or bare boolean may satisfy an admissibility prerequisite.

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

### 6.6 `AETHER_DECISION`

The adapter may not create this stage.

A separate AETHER decision process may consume admissible external decision evidence under its own requirements.

Default: `NOT_CREATED`.

### 6.7 `AETHER_AUTHORITY`

The adapter may not create `authority_context`, `tool_use_grant`, delegation, approval, or capability.

Default: `NOT_CREATED`.

### 6.8 `EXECUTION_PERMISSION`

The adapter may not grant invocation or external side-effect permission.

A separate execution gate must evaluate existing AETHER authority, capability, tool, resource, parameter, validity, and revocation constraints.

Default: `NOT_GRANTED`.

## 7. Admissibility provenance contract

### 7.1 Common rule

Each provenance item used to reach a PASS is preserved as `SOURCE_DATA` first.

For PDP identity, PDP policy identity/version/digest, PDP evaluation time, freshness, and replay, PASS requires provenance that is:

1. attributable to a source identity;
2. attributable to a verification/checker identity where applicable;
3. evaluated under a named verification/check method;
4. associated with a verification/check result;
5. bound to the exact immutable request identity;
6. bound to the exact immutable response identity;
7. bound to the exact AETHER `action_proposal.proposal_id`;
8. bound to the intended purpose/use;
9. evaluated under an applicable policy identity with immutable version or digest;
10. accompanied by evaluation/check time where the check is time-sensitive.

If a required provenance item is missing, unbound, asserted-only, or unverified:

```text
dependent stage = UNKNOWN / NOT_EVALUATED
NO_PROCEED
```

### 7.2 PDP policy provenance

A supplied policy URI/name/version/digest is a claim, not proof that the exact PDP evaluation used that policy.

Admissibility requires attributable evidence tying the exact policy instance to:

- exact request identity;
- exact response identity;
- exact proposal;
- exact PDP evaluation;
- applicable verification identity/method/result.

### 7.3 PDP evaluation time

The PDP evaluation time first enters as source data.

It becomes usable for admissibility only when attributable evidence links that timestamp to the exact PDP evaluation/request/response/proposal.

```text
caller timestamp != verified PDP evaluation time
observed_at != verified PDP evaluation time
current time != verified PDP evaluation time
```

### 7.4 Freshness

A freshness PASS requires:

- freshness checker/verifier identity;
- freshness policy identity;
- immutable policy version/digest;
- check time;
- verified PDP evaluation time;
- exact request identity;
- exact response identity;
- exact proposal reference;
- result PASS under that exact policy.

A bare `freshness_pass=true` is only a claim.

### 7.5 Replay

A replay PASS requires:

- replay checker/verifier identity;
- replay policy identity;
- immutable policy version/digest;
- check time;
- exact request identity;
- exact response identity;
- exact proposal reference;
- intended use;
- result PASS under that exact policy.

A bare `replay_pass=true` is only a claim.

## 8. Point-in-Time separation

`observed_at` is an AETHER observation timestamp and remains distinct from:

- PDP evaluation time;
- PDP identity verification time;
- trust-policy evaluation time;
- PDP-policy attribution check time;
- freshness check time;
- replay check time.

No one timestamp substitutes for another merely because it is available.

Missing verified time provenance remains `UNKNOWN`.

## 9. Response context

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

## 10. Replay and freshness

A previously valid allow is not automatically reusable.

The replay/freshness outcome itself must be supported by attributable evidence as defined above.

Rules:

```text
reused for different proposal/material request -> FAIL -> NO_PROCEED
replay evidence unavailable/unbound            -> UNKNOWN -> NO_PROCEED
freshness evidence unavailable/unbound         -> UNKNOWN -> NO_PROCEED
stale/outside permitted validity               -> FAIL -> NO_PROCEED
bare replay/freshness boolean                   -> SOURCE_DATA only -> NO_PROCEED
```

No replay database or runtime store is designed here; only the semantic evidence contract is defined.

## 11. Negative semantic cases

`NEG-AZ-001` through `NEG-AZ-022` are preserved. Correction cases begin at `NEG-AZ-023`.

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
| NEG-AZ-023 | PDP identity supplied/asserted without attributable verification bound to exact request/response/proposal | `PDP_TRUSTED=UNKNOWN`; `NO_PROCEED` | trust PASS from supplied identity |
| NEG-AZ-024 | PDP policy identity/version/digest supplied but no evidence proves exact evaluation used it | `DECISION_ADMISSIBLE=UNKNOWN`; `NO_PROCEED` | admissibility from policy assertion |
| NEG-AZ-025 | caller supplies evaluation timestamp without attributable evidence tying it to exact PDP evaluation | `DECISION_ADMISSIBLE=UNKNOWN`; `NO_PROCEED` | treat caller time as verified PDP evaluation time |
| NEG-AZ-026 | bare `freshness_pass=true` without checker/policy/check-time/exact bindings | `DECISION_ADMISSIBLE=UNKNOWN`; `NO_PROCEED` | freshness PASS from bare boolean |
| NEG-AZ-027 | bare `replay_pass=true` without checker/policy/check-time/exact bindings | `DECISION_ADMISSIBLE=UNKNOWN`; `NO_PROCEED` | replay PASS from bare boolean |
| NEG-AZ-028 | otherwise-valid provenance is bound to a different request/response/proposal/purpose | dependent stage FAIL/UNKNOWN; `NO_PROCEED` | cross-decision provenance reuse |
| NEG-AZ-029 | parsed request/response objects supplied without original immutable identities | SOURCE_DATA import allowed; required upstream PASS unavailable; `DECISION_ADMISSIBLE=UNKNOWN/NOT_EVALUATED`; `NO_PROCEED` | admissible allow/deny |
| NEG-AZ-030 | locally reserialized object hash is substituted for original immutable identity | identity remains `UNAVAILABLE`; `NO_PROCEED` | reserialization hash as received-byte identity |
| NEG-AZ-031 | AuthZEN Access Evaluations/boxcarring input | `UNSUPPORTED`; raw SOURCE_DATA only; `DECISION_ADMISSIBLE=NOT_EVALUATED`; `NO_PROCEED` | apply single-evaluation admissibility semantics |
| NEG-AZ-032 | AuthZEN Search API input/result | `UNSUPPORTED`; raw SOURCE_DATA only; `DECISION_ADMISSIBLE=NOT_EVALUATED`; `NO_PROCEED` | treat search result as access decision/authority |

## 12. Out of scope

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
- canonical-object identity mechanism;
- Access Evaluations/boxcarring semantics;
- Search API semantics;
- schema mutation;
- SDK/runtime integration;
- Gate/Release/Production action;
- risk acceptance.

## 13. Design review boundary

This document and the companion JSON artifact are **design candidates only**.

They do not authorize implementation.

Any implementation would touch the `Decision != Authority` trust boundary and therefore requires Independent Technical Oversight re-review of the exact corrected design revision first.

`DESIGNED != IMPLEMENTED != VERIFIED != ACCEPTED`.
