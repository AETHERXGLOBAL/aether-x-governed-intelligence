# AX-PUB-DEV-006 — External Evaluation Readiness

**Artifact ID:** `AX-PUB-DEV-006`  
**Version:** `1.0`  
**Status:** `DEV-GATE-04 CLOSED · EXTERNAL EVALUATION READINESS ESTABLISHED · HUMAN EXTERNAL EVALUATION NOT ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Governing program:** `AX-PUB-DEV-001`  
**Governing publication gate:** `AX-PUB-GATE-001`

## 1. Purpose

DEV-GATE-04 exists to make the bounded public developer surface understandable, runnable and evaluable by a technically competent person who has no internal AETHER X context.

Gate-04 closure establishes **readiness of that public evaluation surface**. It does **not** prove that a human external evaluator has participated, adopted the candidate, integrated it into a product or endorsed AETHER X.

```text
EXTERNAL EVALUATION READINESS
≠
EXTERNAL EVALUATION OCCURRED
≠
EXTERNAL ADOPTION
≠
SUPPORTED SDK
```

## 2. Established Readiness Surface

The closed Gate-04 readiness surface consists of:

- [`EXTERNAL_EVALUATOR_GUIDE.md`](./EXTERNAL_EVALUATOR_GUIDE.md) — clean, self-service evaluation and repository-local integration path;
- [`LIMITATIONS_AND_UNSUPPORTED_USES.md`](./LIMITATIONS_AND_UNSUPPORTED_USES.md) — explicit technical and claim boundaries;
- [`MIGRATION_AND_DEPRECATION_DRAFT.md`](./MIGRATION_AND_DEPRECATION_DRAFT.md) — draft change/migration semantics without support-window commitments;
- [`FEEDBACK_AND_TRIAGE.md`](./FEEDBACK_AND_TRIAGE.md) — public feedback classification and triage contract;
- `.github/ISSUE_TEMPLATE/external-evaluation.yml` — structured evaluator feedback intake;
- `tools/run_external_evaluation.py` — standard-library self-service evaluation runner;
- `tools/check_external_evaluation_report.py` — machine-checkable evaluation-report validator;
- `tools/check_external_evaluation_readiness.py` — Gate-04 documentation/governance consistency checker;
- `.github/workflows/validate-external-evaluation-readiness.yml` — clean GitHub Actions runtime-matrix verification.

## 3. Evaluator Contract

The public readiness surface is designed so a technically competent evaluator can answer, using public repository material only:

1. What is this public engineering surface?
2. What is the exact bounded SDK-candidate surface?
3. Which contract IDs and versions are currently handled?
4. How do I run the declared success/failure paths?
5. How do I exercise the repository-local integration facade?
6. What is explicitly unsupported?
7. Which compatibility statements are actually backed by CI evidence?
8. How do I report a reproducible defect or documentation gap?
9. Which changes would require migration or deprecation communication?
10. Which claims must **not** be inferred from a successful evaluation?

`AX-PUB-CI-007` directly validates the automated self-service readiness path. Human usability remains a separate empirical question until actual external evaluation is conducted and recorded.

## 4. Testable Compatibility Boundary

The bounded readiness path has direct CI evidence on:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

That evidence applies to the declared repository-local public candidate, its tests and the Gate-04 readiness runner/report contract. It is not a general Python support policy and does not imply package-distribution support.

Gate-04 does not claim compatibility outside the directly tested matrix.

## 5. Repository-Local Integration Boundary

The evaluator guide demonstrates importing the candidate from the checked-out repository. It does not instruct users to:

- `pip install` an AETHER X package that does not exist;
- depend on a private package index;
- call an unpublished AETHER X API or endpoint;
- use private credentials;
- treat the candidate as production or supported software.

The candidate surface remains:

```text
sdk-candidate/python/aetherx_sdk_candidate.py
```

and covers only the three declared public contract paths.

## 6. Known-Limitations Requirement

The public readiness surface explicitly discloses, at minimum:

- non-production maturity;
- repository-local / non-distributable status;
- no approved package identity or registry;
- no public software reuse licence;
- no network or product API;
- no credential or execution runtime;
- no product-to-product integration claim;
- synthetic/reference conformance scope;
- no security, regulatory or standards certification;
- no external adoption/evaluator claim until separately evidenced.

## 7. Migration & Deprecation Requirement

Gate-04 establishes a public migration/deprecation **draft mechanism**, not a support promise.

The draft separates:

```text
CURRENT CANDIDATE BEHAVIOR
→ PROPOSED CHANGE
→ COMPATIBILITY CLASSIFICATION
→ MIGRATION NOTE
→ DEPRECATION STATE IF AUTHORIZED
→ LATER REMOVAL / REPLACEMENT ONLY UNDER APPROVED POLICY
```

No fixed support window, notice period or stable `1.0.0` commitment is created by Gate-04 closure.

## 8. Feedback & Triage Requirement

External feedback is classifiable without implying support SLA.

The process distinguishes:

- reproducibility defect;
- contract/specification ambiguity;
- candidate API behavior defect;
- documentation friction;
- compatibility observation;
- feature request / future direction;
- security-sensitive report.

Security-sensitive material must follow `SECURITY.md` rather than a public issue.

## 9. Self-Service Evaluation Runner

The canonical readiness runner is:

```bash
python3 tools/run_external_evaluation.py --json-out external-evaluation-report.json
python3 tools/check_external_evaluation_report.py external-evaluation-report.json
```

The runner validates only the bounded public repository surface. It does not access private repositories, credentials, services or product environments.

The CI-generated report is **readiness evidence**, not evidence that a human external evaluator performed the run.

## 10. Gate-04 Exit Criteria — Evidence Disposition

The Gate-04 closure decision is supported by direct evidence that:

- self-service setup/run/integration instructions require no internal AETHER X information;
- limitations and unsupported uses are explicit;
- migration/deprecation draft exists and creates no unsupported support commitment;
- feedback/triage process and structured issue intake exist;
- all declared compatibility claims are bounded to the directly tested Python 3.10–3.13 matrix;
- the evaluation runner succeeded in clean GitHub Actions across Python 3.10, 3.11, 3.12 and 3.13;
- the generated machine-readable evaluation report passed validation on all four runtimes;
- the Gate-04 governance checker passed;
- prior Gate-00/01/02/03 controls remained valid;
- `SDK PUBLICATION NOT AUTHORIZED` remained unchanged.

Direct validation evidence is recorded in:

**[`AX-PUB-CI-007 — External Evaluation Readiness Validation Evidence`](../evidence/AX-PUB-CI-007_EXTERNAL_EVALUATION_READINESS_VALIDATION.md)**

## 11. Closed State

```text
DEV-GATE-04: CLOSED
EXTERNAL EVALUATION READINESS: ESTABLISHED
EXTERNAL EVALUATION OCCURRED: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
NEXT ENGINEERING GATE: DEV-GATE-05 — SDK RELEASE DECISION
```

This state means the public engineering surface is prepared for bounded external evaluation under its declared constraints. It does not create a claim that such human evaluation has already happened.

---

`READINESS ESTABLISHED ≠ EXTERNAL EVALUATION OCCURRED`  
`EXTERNAL EVALUATION READINESS ≠ EXTERNAL ADOPTION`  
`SUPPORTED SDK: NOT ESTABLISHED`  
`SDK PUBLICATION NOT AUTHORIZED`

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
