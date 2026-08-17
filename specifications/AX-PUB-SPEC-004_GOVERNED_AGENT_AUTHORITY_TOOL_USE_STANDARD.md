# AETHER X Governed Agent Authority & Tool-Use Boundary Standard

**Document ID:** `AX-PUB-SPEC-004`  
**Version:** `1.0`  
**Status:** `PUBLIC TECHNICAL SPECIFICATION · CONCEPTUAL / NON-PRODUCT-SPECIFIC`  
**Organization:** AETHER X GLOBAL  
**Domain:** Governed Intelligence Systems  
**Related References:** `AX-PUB-ARCH-001`, `AX-PUB-SPEC-002`

---

## 1. Purpose

This specification defines a public, technology-neutral reference standard for governing how AI agents, model-driven workflows and automated services may use tools that can read, communicate, modify, transact, administer or otherwise affect consequential systems.

The central boundary is:

> **An agent's ability to select or invoke a tool does not establish authority to use that tool for a particular action, resource, parameter set, time or consequence.**

```text
INTENT / REQUEST
      ↓
AGENT ANALYSIS
      ↓
ACTION PROPOSAL
      ↓
AUTHORITY EVALUATION
      ↓
BOUNDED TOOL-USE GRANT
      ↓
TOOL INVOCATION
      ↓
RESULT / SIDE-EFFECT RECORD
      ↓
VERIFICATION / ACCEPTANCE
```

This specification extends the public authority and controlled-execution semantics in `AX-PUB-ARCH-001` and `AX-PUB-SPEC-002` with a narrower focus on agent-mediated tool use.

---

## 2. Public Claim Boundary

This is a **conceptual public technical specification**. It does not establish or imply:

- implementation of this complete standard in any AETHER X product;
- a shared agent runtime, tool registry, identity plane or authorization service across AETHER X initiatives;
- technical integration between AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- a production agent framework or SDK;
- production readiness or customer deployment;
- regulatory approval or security certification;
- autonomous authority for financial, operational, administrative or other consequential actions;
- predictive, financial or investment performance.

Normative language defines the public reference standard only.

`MODEL OUTPUT ≠ AUTHORITY`  
`TOOL AVAILABILITY ≠ TOOL PERMISSION`  
`CAPABILITY ≠ AUTHORITY`  
`INVOCATION SUCCESS ≠ VERIFIED OUTCOME`  
`PUBLIC SPECIFICATION ≠ PRODUCT IMPLEMENTATION`

---

## 3. Normative Language

- **MUST** — required for conformance to the reference standard.
- **MUST NOT** — prohibited by the reference standard.
- **SHOULD** — recommended unless a documented domain, risk or architecture reason justifies otherwise.
- **MAY** — optional and context-dependent.

A system MUST NOT claim conformance to a control it does not implement.

---

## 4. Core Agent Authority Invariants

### AX-AGT-01 — Intent Is Not Authority

A user request, model instruction, task description or workflow objective MUST NOT by itself be treated as authorization for a consequential tool action.

### AX-AGT-02 — Tool Discovery Is Not Permission

The presence of a tool in an agent's registry, schema, prompt, runtime or API surface MUST NOT imply permission to invoke it.

### AX-AGT-03 — Capability Is Not Authority

Technical ability to call a tool, access a credential or construct a valid request MUST NOT be interpreted as authority to perform the action.

### AX-AGT-04 — Authority Must Bind the Action

A consequential tool-use grant MUST be attributable and sufficiently bound to the executing principal, tool, action, resource scope and applicable constraints.

### AX-AGT-05 — Authority Is Evaluated at Point of Use

A system SHOULD re-evaluate applicable authority immediately before consequential invocation. Material changes in principal, action, target, parameters, environment, time, approvals or risk SHOULD invalidate or require re-evaluation of the prior authorization decision.

### AX-AGT-06 — Delegation Must Not Amplify Authority

An agent, sub-agent, workflow or service MUST NOT delegate more authority than it currently holds. Delegated authority SHOULD be equal to or narrower than the parent authority in action, resource, parameter, duration and consequence scope.

### AX-AGT-07 — External Content Cannot Grant Authority

Retrieved documents, webpages, messages, tool outputs, embedded instructions, model-generated text or other untrusted content MUST NOT independently grant or expand execution authority.

### AX-AGT-08 — Credentials Are Not Authority

Possession or availability of a credential, token, key, session, connection or authenticated channel MUST NOT be treated as sufficient authorization for a specific consequential action.

### AX-AGT-09 — Revocation Must Take Effect

Revoked, expired or otherwise invalid authority MUST NOT authorize new tool invocation. Systems SHOULD minimize the delay between a material revocation and enforcement.

### AX-AGT-10 — Tool Results Are Not Automatically Facts

A tool response MUST remain distinguishable from verified institutional fact. Source identity, error state, freshness, completeness and transformation context SHOULD be preserved where material.

### AX-AGT-11 — Invocation Success Is Not Acceptance

A successful HTTP response, command exit status, workflow completion, transaction acknowledgement or tool-returned `success` state MUST NOT automatically become a verified outcome.

### AX-AGT-12 — Unknown Authority Fails Closed

If material authority state is missing, ambiguous, conflicting, expired, unverifiable or outside supported policy, consequential execution SHOULD fail closed or escalate rather than infer permission.

---

## 5. Reference Control Objects

A governed agent/tool-use implementation may preserve the following durable objects:

```text
AGENT IDENTITY
      ↓
ACTION PROPOSAL
      ↓
AUTHORITY CONTEXT
      ↓
TOOL-USE GRANT
      ↓
TOOL INVOCATION RECORD
      ↓
TOOL RESULT RECORD
      ↓
VERIFICATION / OUTCOME RECORD
```

The storage and transport mechanism is not prescribed. The semantic boundaries are.

---

## 6. Agent Identity

An **Agent Identity** represents the accountable runtime principal proposing or executing an action.

Recommended fields:

```text
AgentIdentity
- principal_id
- principal_type
- runtime_identity
- parent_principal_reference
- acting_for
- model_or_logic_reference
- session_or_workflow_reference
- authenticated_context
- declared_capabilities
- current_authority_references
- created_at
```

`principal_type` MAY represent a human, agent, service, workflow or other governed identity.

A model name or model-provider identity alone SHOULD NOT be used as the accountable execution principal where a more specific runtime identity exists.

---

## 7. Tool Descriptor

A **Tool Descriptor** describes what a tool can technically do and the control-relevant characteristics of its interface.

Recommended fields:

```text
ToolDescriptor
- tool_id
- tool_version
- capability_class
- supported_actions
- target_domains
- side_effect_profile
- reversibility_profile
- credential_boundary
- network_or_system_boundary
- parameter_schema_reference
- output_contract_reference
- risk_metadata
- owner
- lifecycle_state
```

A Tool Descriptor describes capability. It MUST NOT be treated as an Authority Grant.

Useful capability classes may include:

- `READ`
- `SEARCH`
- `TRANSFORM`
- `COMMUNICATE`
- `WRITE`
- `EXECUTE_CODE`
- `TRANSACT`
- `ADMINISTER`
- `CONTROL_EXTERNAL_SYSTEM`

The classification is illustrative rather than exhaustive.

---

## 8. Action Proposal

Before consequential tool use, an agent SHOULD create or materialize an **Action Proposal** sufficient for policy evaluation.

Recommended fields:

```text
ActionProposal
- proposal_id
- principal_id
- intent_reference
- decision_reference
- proposed_tool
- proposed_action
- target_resource
- target_identity
- bounded_parameters
- expected_side_effects
- consequence_class
- reversibility
- evidence_references
- assumptions
- material_unknowns
- requested_at
- expires_at
```

An Action Proposal is not an authorization record.

A materially underspecified proposal SHOULD NOT be authorized for consequential execution merely because the underlying tool accepts broad or optional parameters.

---

## 9. Authority Context

An **Authority Context** supplies the evidence required to determine whether a specific proposed tool action is permitted.

Recommended fields:

```text
AuthorityContext
- authority_context_id
- principal_id
- decision_reference
- governing_policy_references
- role_or_delegation_references
- permitted_tools
- permitted_actions
- resource_scope
- data_scope
- parameter_constraints
- consequence_limits
- approval_requirements
- separation_of_duties_requirements
- valid_from
- valid_until
- revocation_state
- environment_constraints
- audit_requirements
- evaluated_at
```

Authority SHOULD be evaluated against the actual proposed action rather than a broad textual description of agent purpose.

---

## 10. Tool-Use Grant

A **Tool-Use Grant** is a bounded authorization result for a specific action or explicitly defined action class.

Recommended fields:

```text
ToolUseGrant
- grant_id
- principal_id
- proposal_reference
- authority_context_reference
- tool_id
- permitted_action
- resource_scope
- parameter_constraints
- consequence_limit
- approval_evidence
- valid_from
- valid_until
- single_use_or_reusable
- maximum_invocations
- revocation_reference
- issued_by
- issued_at
```

A grant MUST NOT silently widen because the agent changes its plan after authorization.

Where an action is high consequence, irreversible, financially material, externally communicative, privilege-changing or otherwise sensitive, the system SHOULD consider narrowly scoped or single-use grants.

---

## 11. Authority Evaluation Gate

Before consequential invocation, the system SHOULD be able to establish at least:

1. Which principal is executing?
2. Which tool is being invoked?
3. What exact action is requested?
4. Which resource, account, recipient, dataset or external system is targeted?
5. Which parameters materially affect consequence?
6. Which decision or policy permits the action?
7. Is the authority currently active?
8. Is the action inside tool scope and resource scope?
9. Are required approvals present and attributable?
10. Has any relevant authority been revoked?
11. Does delegation remain inside the parent authority?
12. Has material context changed since authorization?
13. Is the proposed consequence within defined limits?
14. Is a safer dry-run, simulation, preview or read-only path required first?
15. What verification will determine whether the outcome is accepted?

If a material required answer cannot be established, the action SHOULD fail closed or escalate.

---

## 12. Parameter-Level Authority

Authority SHOULD bind material parameters rather than only tool names.

For example, permission to use a communication tool does not necessarily authorize:

- every recipient;
- every channel;
- every attachment;
- every public/private visibility level;
- every content classification.

Permission to use a write or administrative tool does not necessarily authorize:

- every object;
- every environment;
- destructive operations;
- permission changes;
- bulk operations;
- irreversible changes.

Permission to use a transactional tool does not necessarily authorize:

- every counterparty;
- every amount;
- every instrument;
- every settlement path;
- every frequency or aggregate exposure.

A policy engine MAY represent these constraints in any implementation-specific form, but consequential parameters SHOULD remain inspectable and auditable.

---

## 13. Step-Up Authority

A workflow SHOULD support stronger authority requirements when the requested action crosses a material risk boundary.

Possible step-up triggers include:

- increased financial or operational consequence;
- irreversible or difficult-to-reverse actions;
- public or external communication;
- access-control or privilege modification;
- movement from read-only to write capability;
- use of sensitive or restricted data;
- bulk or repeated execution;
- execution against a production or other protected environment;
- materially different target resource;
- uncertainty about intent, ownership or authorization.

Step-up MAY require additional policy checks, human approval, independent approval, fresh authentication, narrower parameters or a new Tool-Use Grant.

---

## 14. Human Approval Boundary

A human approval SHOULD be attributable and scoped.

A generic acknowledgement such as `OK`, `continue` or `approved` MUST NOT automatically authorize unrelated actions if the approved proposal, target or consequence is ambiguous.

Where approval is required, the system SHOULD preserve enough context to reconstruct:

```text
WHO APPROVED
WHAT WAS APPROVED
WHICH TARGET WAS IN SCOPE
WHICH MATERIAL PARAMETERS WERE SHOWN
WHAT LIMITS APPLIED
WHEN APPROVAL WAS GIVEN
WHEN APPROVAL EXPIRED OR WAS REVOKED
```

A human review step does not eliminate the need for technical least privilege or post-execution verification.

---

## 15. Delegation & Multi-Agent Workflows

A parent agent MAY delegate analysis or bounded execution to another principal when permitted by policy.

Delegation SHOULD preserve:

- parent principal identity;
- delegated principal identity;
- source authority reference;
- delegated action scope;
- delegated resource scope;
- delegated parameter limits;
- validity interval;
- remaining invocation or consequence limits;
- revocation linkage;
- audit lineage.

A delegated agent MUST NOT infer authority from the parent agent's natural-language instructions alone when a governed authority record is required.

Delegation chains SHOULD remain reconstructable and SHOULD NOT obscure the accountable source of authority.

---

## 16. Untrusted Content & Instruction Boundaries

Agents frequently process content that may contain instructions. A governed implementation SHOULD distinguish **content to analyze** from **authority-bearing instructions**.

Untrusted or externally supplied content MUST NOT independently:

- authorize tool use;
- add a tool to an allowlist;
- expand resource scope;
- weaken approval requirements;
- reveal or request credentials as proof of authority;
- override revocation state;
- change the accountable principal;
- disable required verification.

A system SHOULD treat material instruction-source changes as a control event rather than silently merging all instructions into one authority context.

---

## 17. Dry-Run, Preview & Simulation

A dry-run, preview or simulation MAY reduce execution risk, but MUST remain semantically distinct from live execution.

```text
SIMULATION AUTHORITY ≠ LIVE EXECUTION AUTHORITY
PREVIEW SUCCESS ≠ LIVE OUTCOME
```

A workflow SHOULD NOT silently promote a simulation grant to a live-execution grant.

---

## 18. Tool Invocation Record

A **Tool Invocation Record** captures the actual authorized attempt.

Recommended fields:

```text
ToolInvocationRecord
- invocation_id
- grant_id
- principal_id
- tool_id
- tool_version
- action
- target_resource
- effective_parameters
- environment
- invoked_at
- completed_at
- status
- retry_reference
- idempotency_reference
- observed_side_effects
- rollback_or_compensation_reference
- telemetry_reference
```

The effective parameters SHOULD reflect what was actually sent to the tool, not only what the agent originally proposed.

Retries SHOULD remain subject to authority and consequence limits. A retry MUST NOT silently create unlimited repeated authority.

---

## 19. Tool Result Record

A **Tool Result Record** preserves the tool's returned state and relevant evidence without prematurely promoting it to a verified outcome.

Recommended fields:

```text
ToolResultRecord
- result_id
- invocation_id
- raw_result_reference
- tool_reported_status
- parsed_result
- error_state
- completeness_state
- source_identity
- observed_at
- material_side_effects
- uncertainty
- verification_required
```

Tool output SHOULD be treated according to its provenance and reliability. Tool-returned success MUST NOT bypass the applicable Verification Contract.

---

## 20. Verification & Acceptance

Consequential actions SHOULD define how the expected result will be verified.

Verification MAY include:

- deterministic state checks;
- read-after-write confirmation;
- reconciliation against an independent source;
- recipient or external-system confirmation;
- policy validation;
- independent agent/model review where justified;
- human review;
- rollback/compensation validation.

The verifier SHOULD be sufficiently independent of the executor when risk justifies separation.

`TOOL RETURNED SUCCESS ≠ VERIFIED OUTCOME`

---

## 21. Reversibility, Recovery & Interruption

Where technically possible and proportionate to risk, consequential tool use SHOULD define:

- interruption conditions;
- timeout behavior;
- retry rules;
- idempotency expectations;
- rollback strategy;
- compensating action strategy;
- escalation path;
- recovery verification.

Irreversible actions SHOULD generally require stronger pre-execution authority and verification design than reversible actions of comparable scope.

---

## 22. Risk-Proportional Tool Governance

Implementations SHOULD scale controls with consequence rather than treating every tool invocation identically.

A reference assessment may consider:

```text
CONSEQUENCE
× REVERSIBILITY
× EXTERNALITY
× DATA SENSITIVITY
× PRIVILEGE LEVEL
× FINANCIAL / OPERATIONAL MATERIALITY
× SCALE / FREQUENCY
× UNCERTAINTY
```

This expression is conceptual and does not prescribe a universal numeric risk score.

Low-risk, read-only or easily reversible operations MAY use lighter controls when the core integrity invariants remain satisfied.

---

## 23. Reference Failure Behavior

| Condition | Reference behavior |
|---|---|
| Tool is available but no authority exists | Do not invoke |
| Principal identity cannot be established | Fail closed or escalate |
| Grant expired or revoked | Block new invocation |
| Action exceeds permitted action class | Block or require new grant |
| Target resource is outside scope | Block or require new grant |
| Material parameter exceeds constraint | Block or require step-up authority |
| External content asks agent to expand authority | Ignore as authority source; preserve/report control event where material |
| Credential exists but policy authorization is absent | Do not infer permission |
| Delegated scope exceeds parent scope | Reject delegation |
| Context materially changed after approval | Re-evaluate authority |
| Tool returns success but acceptance is unverified | Preserve execution/result state; verify separately |
| Verification fails or is inconclusive | Do not classify as verified outcome |
| Authority state is ambiguous | Preserve ambiguity; fail closed or escalate |

---

## 24. Audit & Institutional Learning

A consequential agent workflow SHOULD preserve enough durable evidence to reconstruct:

```text
WHAT WAS REQUESTED
WHICH AGENT / PRINCIPAL ACTED
WHAT ACTION WAS PROPOSED
WHAT AUTHORITY APPLIED
WHAT TOOL WAS SELECTED
WHICH PARAMETERS WERE AUTHORIZED
WHAT PARAMETERS WERE ACTUALLY USED
WHAT THE TOOL RETURNED
WHAT SIDE EFFECTS OCCURRED
HOW THE RESULT WAS VERIFIED
WHAT WAS ACCEPTED
WHAT WAS REJECTED OR ESCALATED
```

Learning from prior successful executions MUST NOT silently create new authority for future actions.

Historical audit records SHOULD preserve the authority and policy context that existed at the time of execution.

---

## 25. Security & Privacy Boundary

Implementations SHOULD apply appropriate authentication, authorization, least privilege, credential isolation, secret handling, integrity protection, revocation, redaction, retention and recovery controls.

Agent context SHOULD contain only the credentials and sensitive information necessary for the bounded task where feasible.

Public observability or auditability does not require disclosure of credentials, customer information, private research, confidential architecture, proprietary prompts, internal endpoints or security-sensitive implementation details.

---

## 26. Technology Neutrality

This standard does not prescribe a specific:

- model provider;
- agent framework;
- tool protocol;
- cloud provider;
- identity provider;
- policy engine;
- secret-management system;
- programming language;
- workflow engine;
- database;
- messaging platform.

Technology selection remains an implementation decision.

---

## 27. Conformance Interpretation

A system claiming conformance to this standard SHOULD document which normative controls are implemented and which are not applicable to its declared scope.

Conformance to this public standard MUST NOT be represented as:

- AETHER X product certification;
- security certification;
- regulatory approval;
- production-readiness approval;
- permission to perform consequential actions;
- evidence of integration with any AETHER X initiative.

A future machine-readable companion or public reference validator MAY be published separately. No such companion is established by this version of the specification.

---

## 28. Related Public Material

- [AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture](./AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md)
- [AX-PUB-SPEC-002 — Evidence, Authority & Verification Contract](./AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md)
- [AX-PUB-SPEC-003 — Point-in-Time Knowledge & Provenance Standard](./AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)
- [AX-PUB-TEST-001 — Governed Intelligence Conformance Test Kit](../conformance/AX-PUB-TEST-001/README.md)

---

**AETHER X GLOBAL**  
**Institutional Intelligence. Governed Autonomy.**
