# AETHER X Evidence, Authority & Verification Contract

**Document ID:** `AX-PUB-SPEC-002`  
**Version:** `1.0`  
**Status:** `PUBLIC TECHNICAL SPECIFICATION · CONCEPTUAL / NON-PRODUCT-SPECIFIC`  
**Organization:** AETHER X GLOBAL  
**Domain:** Governed Intelligence Systems  
**Related Reference:** `AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`

---

## 1. Purpose

This specification defines a public, technology-neutral reference contract for connecting **evidence, recommendation, decision, authority, execution and verification** inside consequential intelligence workflows.

> **A system being able to produce an answer or perform an action does not mean that the answer is established, the recommendation is approved, the action is authorized, or the outcome is verified.**

```text
EVIDENCE
→ ANALYSIS
→ RECOMMENDATION
→ DECISION
→ AUTHORITY
→ EXECUTION
→ VERIFICATION
→ VERIFIED OUTCOME
```

The specification complements `AX-PUB-ARCH-001` by defining control objects, integrity invariants and state-transition boundaries that may be used to implement that architecture.

---

## 2. Public Claim Boundary

This is a **conceptual public technical specification**. It does not establish or imply:

- implementation of the complete contract in any AETHER X product;
- a shared runtime, data model or control plane across AETHER X initiatives;
- technical integration between AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- production readiness or customer deployment;
- regulatory approval or security certification;
- autonomous authority to execute consequential actions;
- predictive, financial or investment performance.

Normative language defines the reference contract, not the maturity of any product.

`OUTPUT ≠ FACT`  
`RECOMMENDATION ≠ DECISION`  
`CAPABILITY ≠ AUTHORITY`  
`EXECUTION COMPLETE ≠ VERIFIED`  
`ARCHITECTURE ≠ IMPLEMENTATION`

---

## 3. Normative Language

- **MUST** — required for conformance to the reference contract.
- **MUST NOT** — prohibited by the reference contract.
- **SHOULD** — recommended unless a documented domain, risk or architecture reason justifies otherwise.
- **MAY** — optional and context-dependent.

A project may adopt only the portions appropriate to its domain and maturity, but must not claim conformance to an element it does not implement.

---

## 4. Core Integrity Invariants

### AX-EAV-01 — Evidence Before Confidence

A material claim MUST remain distinguishable from the evidence supporting it. Insufficient, stale, conflicting or unavailable evidence SHOULD preserve uncertainty or trigger abstention/escalation rather than manufactured certainty.

### AX-EAV-02 — Output Is Not Fact

Model output, agent output, generated analysis or retrieved text MUST NOT become institutional fact merely because a system produced it.

### AX-EAV-03 — Recommendation Is Not Decision

A recommendation MUST NOT become a decision without explicit decision authority appropriate to scope and consequence.

### AX-EAV-04 — Capability Is Not Authority

Technical ability to perform an action MUST NOT be treated as permission to perform it.

### AX-EAV-05 — Authority Must Be Bounded

Authority for consequential action MUST be attributable and scoped. Where appropriate it SHOULD be time-limited, revocable and auditable.

### AX-EAV-06 — Execution Is Not Acceptance

Successful invocation of a tool, API, workflow or transaction MUST NOT automatically mean the required outcome was achieved.

### AX-EAV-07 — Verification Before Verified Outcome

A result MUST NOT be classified as a `VERIFIED OUTCOME` until applicable verification criteria have passed.

### AX-EAV-08 — Unknowns Remain Unknown

A material unresolved unknown MUST NOT be silently converted into an assumption, fact, decision or verified result.

---

## 5. Reference Control Objects

The reference model uses six primary durable objects:

```text
EVIDENCE RECORD
      ↓
DECISION RECORD
      ↓
AUTHORITY GRANT
      ↓
EXECUTION RECORD
      ↓
VERIFICATION RECORD
      ↓
VERIFIED OUTCOME RECORD
```

They may be represented as database records, events, signed documents, structured messages or workflow state. The storage mechanism is not prescribed; the semantic boundaries are.

---

## 6. Evidence Record

An **Evidence Record** preserves the traceable basis for a material claim, analysis or decision.

Recommended fields:

```text
EvidenceRecord
- evidence_id
- claim_or_question_id
- classification
- source_identity
- source_type
- provenance
- observed_at
- effective_at
- evidence_cutoff_at
- transformation_or_method
- supporting_content_reference
- conflicting_evidence_reference
- assumptions
- limitations
- freshness_state
- confidence_rationale
- created_by
- created_at
- supersedes / superseded_by
```

Useful classifications include `FACT`, `SOURCE_DATA`, `ASSUMPTION`, `ESTIMATE`, `HYPOTHESIS`, `INFERENCE`, `FORECAST`, `SCENARIO`, `PROFESSIONAL_OPINION`, `RECOMMENDATION`, `DECISION`, `VERIFIED_OUTCOME`, `UNKNOWN`, and `SUPERSEDED`.

A classification MUST NOT be promoted merely because it is persuasive or repeated.

Material conflicting evidence SHOULD be retained or linked rather than removed because it weakens a preferred conclusion.

---

## 7. Decision Record

A **Decision Record** captures an explicit decision made by an authorized decision-maker or governed decision mechanism.

Recommended fields:

```text
DecisionRecord
- decision_id
- decision_question
- decision_owner
- decision_scope
- recommendation_reference
- evidence_references
- alternatives_considered
- material_assumptions
- material_unknowns
- decision
- conditions
- effective_at
- expires_at
- rationale
- created_at
- supersedes / superseded_by
```

A recommendation, report, research result, model answer or agent proposal MUST NOT become a Decision Record without explicit decision authority.

Approval MUST remain inside the defined decision scope and MUST NOT be silently extended to unrelated actions, systems, resources or future decisions.

---

## 8. Authority Grant

An **Authority Grant** defines permission to perform a bounded consequential action.

Recommended fields:

```text
AuthorityGrant
- authority_id
- principal
- delegated_by
- decision_reference
- permitted_action
- resource_scope
- data_scope
- tool_scope
- parameter_constraints
- financial_or_operational_limits
- approval_requirements
- valid_from
- valid_until
- revocation_state
- separation_of_duties_requirements
- audit_requirements
- created_at
```

The principal MAY be a person, service, agent or workflow identity. The model that generated a recommendation does not automatically become the execution principal.

A consequential workflow SHOULD grant the minimum authority required. Expired or revoked authority MUST NOT authorize new execution.

---

## 9. Execution Record

An **Execution Record** captures what the system actually attempted or changed under an Authority Grant.

Recommended fields:

```text
ExecutionRecord
- execution_id
- authority_reference
- decision_reference
- principal
- tool_or_workflow
- action
- bounded_inputs
- parameter_set
- started_at
- completed_at
- preconditions
- observed_side_effects
- result_state
- error_state
- rollback_or_compensation_state
- telemetry_reference
- evidence_artifacts
```

Before consequential execution, the implementation MUST verify that authority is valid for the principal, action, resource, current time, requested parameters and required approvals.

Execution states such as `SUCCEEDED`, `FAILED`, `PARTIAL`, `CANCELLED`, `TIMED_OUT`, `ROLLED_BACK` or `UNKNOWN` describe execution behavior only; they do not imply acceptance.

---

## 10. Verification Record

A **Verification Record** determines whether an execution or produced artifact satisfies defined acceptance criteria.

Recommended fields:

```text
VerificationRecord
- verification_id
- subject_reference
- verification_contract_reference
- acceptance_criteria
- verification_method
- verifier_identity
- verifier_independence_boundary
- required_evidence
- observed_evidence
- result
- exceptions
- residual_risk
- verified_at
```

Verification SHOULD distinguish at least:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`
- `NOT_PERFORMED`

`INCONCLUSIVE` MUST NOT be treated as `PASS`.

Verifier independence SHOULD increase with risk. Possible mechanisms include deterministic tests, reconciliation, independent model/agent review, rule validation, hidden evaluation, human review or external-system confirmation.

---

## 11. Verified Outcome Record

A **Verified Outcome Record** represents the accepted result after required verification has passed.

Recommended fields:

```text
VerifiedOutcomeRecord
- outcome_id
- decision_reference
- execution_reference
- verification_reference
- accepted_result
- acceptance_scope
- measured_metrics
- residual_risk
- limitations
- follow_up_actions
- learning_reference
- accepted_at
```

A verified outcome is contextual. Passing one verification contract MUST NOT be interpreted as universal correctness, permanent validity or broader commercial success beyond the accepted scope.

---

## 12. Reference State Transition Model

```text
PROPOSED
  ↓
EVIDENCE ASSEMBLED
  ↓
RECOMMENDED
  ↓
DECIDED
  ↓
AUTHORIZED
  ↓
EXECUTION ATTEMPTED
  ↓
EXECUTION COMPLETE
  ↓
VERIFICATION COMPLETE
  ↓
VERIFIED OUTCOME
```

Invalid collapses include:

```text
MODEL OUTPUT → FACT
RECOMMENDATION → EXECUTION
TECHNICAL CAPABILITY → AUTHORITY
EXECUTION SUCCEEDED → VERIFIED OUTCOME
RESEARCH RESULT → PRODUCTION CLAIM
```

---

## 13. Decision-to-Execution Gate

Before consequential execution, the system SHOULD be able to answer:

1. What decision authorized the action?
2. What evidence informed that decision?
3. Who or what owns decision authority?
4. Which principal may execute?
5. What exact action is permitted?
6. Which resources/data are in scope?
7. What limits apply?
8. When does authority expire?
9. Can it be revoked?
10. What verification determines acceptance?
11. What happens if execution fails or partially completes?

If a material required answer is unavailable, execution SHOULD fail closed or escalate according to applicable risk policy.

---

## 14. Verification-to-Acceptance Gate

Before a result becomes a verified outcome, the system SHOULD establish:

1. applicable acceptance criteria;
2. whether criteria were defined before execution;
3. evidence actually observed;
4. verifier identity;
5. required verifier independence;
6. recorded exceptions/deviations;
7. residual risk;
8. explicit verification result;
9. accepted scope;
10. conditions requiring re-verification.

---

## 15. Risk-Proportional Control

As consequence increases, implementations SHOULD consider stronger evidence requirements, narrower authority, shorter authority duration, separation of duties, stronger verification independence, deterministic reconciliation, recovery design and more durable audit evidence.

Low-risk, reversible workflows MAY use lighter controls where integrity requirements remain satisfied.

---

## 16. Failure Behavior

| Condition | Reference behavior |
|---|---|
| Material evidence missing | Preserve `UNKNOWN`, abstain or escalate |
| Evidence materially stale | Re-verify where required |
| Recommendation has no decision authority | Do not execute |
| Authority expired or revoked | Block new execution |
| Requested action exceeds scope | Block or require new authorization |
| Execution partially completes | Record partial state; do not infer acceptance |
| Verification fails | Do not create `VERIFIED_OUTCOME` |
| Verification inconclusive | Preserve `INCONCLUSIVE`; escalate or re-test |
| Audit evidence incomplete | Preserve incomplete state; never fabricate traceability |

---

## 17. Audit & Institutional Learning

A consequential workflow SHOULD preserve enough durable state to reconstruct:

```text
WHAT WAS REQUESTED
WHAT WAS KNOWN
WHAT WAS INFERRED
WHAT WAS RECOMMENDED
WHAT WAS DECIDED
WHO OR WHAT HAD AUTHORITY
WHAT WAS EXECUTED
WHAT ACTUALLY HAPPENED
HOW IT WAS VERIFIED
WHAT WAS ACCEPTED
WHAT SHOULD CHANGE NEXT
```

New evidence MUST NOT silently rewrite the historical record of what was known at the time of an earlier decision.

---

## 18. Security & Privacy Boundary

Implementations SHOULD apply appropriate authentication, authorization, least privilege, integrity protection, retention, encryption, redaction, revocation and recovery controls to contract records themselves.

Public auditability does not require disclosure of confidential evidence, credentials, customer information, security-sensitive data or proprietary implementation.

---

## 19. Technology Neutrality

This contract does not prescribe a model provider, agent framework, cloud, database, policy engine, identity provider, event bus, programming language or verification framework.

Technology selection remains an implementation decision.

---

## 20. Machine-Readable Example

A minimal conceptual bundle may resemble:

```json
{
  "evidence_records": [{"evidence_id": "ev-1", "classification": "SOURCE_DATA"}],
  "decision_records": [{"decision_id": "dec-1", "evidence_refs": ["ev-1"]}],
  "authority_grants": [{"authority_id": "auth-1", "decision_id": "dec-1", "status": "ACTIVE"}],
  "execution_records": [{"execution_id": "exec-1", "authority_id": "auth-1"}],
  "verification_records": [{"verification_id": "ver-1", "execution_id": "exec-1", "verdict": "PASS"}],
  "verified_outcomes": [{"outcome_id": "out-1", "verification_id": "ver-1", "outcome_state": "VERIFIED"}]
}
```

The example is illustrative, not a universal schema.

---

## 21. Reference Implementation

Selected invariants from this specification are implemented in the public, non-production [AX-PUB-REF-001 — EAV Contract Validator](../reference-implementations/eav-contract-validator/README.md).

A validator pass demonstrates only that the tested bundle satisfied the implemented reference checks. It is not a security approval or production-readiness determination.

---

## 22. Related Public Material

- [AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture](./AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md)
- [AX-PUB-SPEC-003 — Point-in-Time Knowledge & Provenance Standard](./AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)
- [AX-PUB-REF-001 — EAV Contract Validator](../reference-implementations/eav-contract-validator/README.md)

---

**AETHER X GLOBAL**  
**Institutional Intelligence. Governed Autonomy.**
