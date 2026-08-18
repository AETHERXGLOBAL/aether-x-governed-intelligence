# AETHER X Governed Intelligence — Feedback & Triage

`DEV-GATE-04 CANDIDATE · PUBLIC FEEDBACK PROCESS · NO SUPPORT SLA`

This process defines how reproducible public developer/evaluator feedback should be classified and handled without creating a support, maintenance or response-time commitment.

## 1. Appropriate Public Feedback

Use the repository's **External evaluation feedback** issue form for non-sensitive findings such as:

- reproducibility defect;
- documentation friction;
- contract/specification ambiguity;
- candidate API behavior defect;
- compatibility observation;
- conformance/test discrepancy;
- feature request / future-direction suggestion.

## 2. Do Not Use Public Issues For

Do not place the following in a public issue:

- credentials or secrets;
- private keys or tokens;
- personal/customer/confidential data;
- suspected exploitable vulnerability details;
- private AETHER X implementation information;
- non-public partner/customer information.

Security-sensitive reports must follow `SECURITY.md`.

## 3. Required Reproduction Information

A useful evaluator report should include:

```text
CATEGORY
REPOSITORY COMMIT / REF
OPERATING SYSTEM
PYTHON VERSION
COMMAND / PATH EXERCISED
EXPECTED RESULT
ACTUAL RESULT
MINIMAL REPRODUCTION STEPS
RELEVANT PUBLIC OUTPUT / ERROR
```

Attach only public-safe material.

## 4. Triage States

Public feedback may be classified using the following operational states:

- `RECEIVED` — report exists; no technical conclusion yet;
- `NEEDS_REPRODUCTION` — additional public-safe reproduction detail is needed;
- `REPRODUCED` — reported behavior was independently reproduced on the public surface;
- `DOCUMENTATION_GAP` — behavior is consistent but public guidance is insufficient/ambiguous;
- `CONTRACT_REVIEW` — report may affect specification/contract semantics;
- `CANDIDATE_DEFECT` — bounded SDK-candidate behavior appears inconsistent with declared behavior;
- `COMPATIBILITY_REVIEW` — report may affect declared candidate/runtime compatibility;
- `OUT_OF_SCOPE` — request concerns an unsupported/private/product surface;
- `NOT_REPRODUCIBLE` — current public evidence did not reproduce the report;
- `SECURITY_REDIRECT` — sensitive handling is required outside public issue discussion;
- `RESOLVED` — public disposition and any applicable change/evidence are recorded.

These are triage states, not customer-support statuses.

## 5. Severity Does Not Create Authority

A technically important report can trigger review, correction, deprecation proposal or withdrawal proposal.

It does not itself authorize:

- package publication;
- product changes in private repositories;
- a public security claim;
- a supported-SDK commitment;
- a compatibility guarantee.

Material changes still follow repository governance and evidence controls.

## 6. Feature Requests

Feature requests are treated as inputs, not commitments.

A request may be:

```text
OUT_OF_SCOPE
RESEARCH INPUT
FUTURE DIRECTION
CANDIDATE FOR DESIGN
DECLINED
```

No roadmap promise should be inferred from issue acknowledgement.

## 7. Compatibility Reports

If a report concerns a runtime outside the declared Python 3.10–3.13 candidate matrix, it may be useful research input but must not be represented as expansion of verified support without direct evidence and governance update.

## 8. Response-Time Boundary

This public process creates no guaranteed:

- first-response time;
- resolution time;
- maintenance window;
- security-response SLA;
- release schedule.

A future support model requires separate approval.

## 9. Closure Evidence

Where a report results in a material public change, closure should link, as applicable, to:

- the affected artifact/change;
- tests or conformance updates;
- compatibility classification;
- migration/deprecation note;
- CI evidence;
- manifest/governance update.

This preserves:

```text
FEEDBACK
→ REPRODUCTION
→ CLASSIFICATION
→ CHANGE / NO-CHANGE DECISION
→ VERIFICATION
→ RECORDED OUTCOME
```

---

`PUBLIC ISSUE ≠ SUPPORT CONTRACT`  
`FEATURE REQUEST ≠ ROADMAP COMMITMENT`  
`REPRODUCED DEFECT ≠ PRODUCT DEFECT`  
`SDK PUBLICATION NOT AUTHORIZED`
