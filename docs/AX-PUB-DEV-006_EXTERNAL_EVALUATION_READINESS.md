# AX-PUB-DEV-006 — External Evaluation Readiness

**Artifact ID:** `AX-PUB-DEV-006`  
**Version:** `1.0`  
**Status:** `DEV-GATE-04 CANDIDATE · EXTERNAL EVALUATION READINESS NOT YET ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Governing program:** `AX-PUB-DEV-001`  
**Governing publication gate:** `AX-PUB-GATE-001`

## 1. Purpose

DEV-GATE-04 exists to make the bounded public developer surface understandable, runnable and evaluable by a technically competent person who has no internal AETHER X context.

The gate does **not** prove that an external evaluator has participated, adopted the candidate, integrated it into a product or endorsed AETHER X.

```text
EXTERNAL EVALUATION READINESS
≠
EXTERNAL EVALUATION OCCURRED
≠
EXTERNAL ADOPTION
≠
SUPPORTED SDK
```

## 2. Gate-04 Candidate Surface

The candidate readiness surface consists of:

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

An evaluator should be able to answer, using public repository material only:

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

If any of these require internal assistance, the Gate-04 readiness candidate is incomplete.

## 4. Testable Compatibility Boundary

The current bounded candidate has direct CI evidence on:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

That evidence applies to the declared repository-local public candidate and its tests. It is not a general Python support policy and does not imply package-distribution support.

Gate-04 must not claim compatibility outside the directly tested matrix.

## 5. Repository-Local Integration Boundary

The evaluator guide may demonstrate importing the candidate from the checked-out repository. It must not instruct users to:

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

The public readiness surface must clearly disclose, at minimum:

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

Gate-04 requires a draft migration/deprecation mechanism, not a support promise.

The draft must separate:

```text
CURRENT CANDIDATE BEHAVIOR
→ PROPOSED CHANGE
→ COMPATIBILITY CLASSIFICATION
→ MIGRATION NOTE
→ DEPRECATION STATE IF AUTHORIZED
→ LATER REMOVAL / REPLACEMENT ONLY UNDER APPROVED POLICY
```

No fixed support window, notice period or stable `1.0.0` commitment is created by Gate-04.

## 8. Feedback & Triage Requirement

External feedback must be classifiable without implying support SLA.

At minimum, the process distinguishes:

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

## 10. Gate-04 Exit Criteria

Gate-04 may be proposed for closure only when all of the following are directly evidenced:

- self-service setup/run/integration instructions require no internal AETHER X information;
- limitations and unsupported uses are explicit;
- migration/deprecation draft exists and creates no unsupported support commitment;
- feedback/triage process and structured issue intake exist;
- all declared compatibility claims are testable and bounded to direct evidence;
- the evaluation runner succeeds in clean CI across the declared Python 3.10–3.13 matrix;
- the generated evaluation report passes machine validation;
- the Gate-04 governance checker passes;
- prior Gate-00/01/02/03 controls remain valid;
- `SDK PUBLICATION NOT AUTHORIZED` remains unchanged unless separately decided under `AX-PUB-GATE-001`.

## 11. Evidence State

Current state while this document is a candidate:

```text
DEV-GATE-04: CANDIDATE
EXTERNAL EVALUATION READINESS: NOT YET ESTABLISHED
EXTERNAL EVALUATION OCCURRED: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

A later CI evidence record may support Gate-04 closure. The existence of this document alone does not.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
