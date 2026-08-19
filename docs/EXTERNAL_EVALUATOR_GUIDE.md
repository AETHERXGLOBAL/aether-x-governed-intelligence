# AETHER X Governed Intelligence — External Evaluator Guide

`DEV-GATE-04 ESTABLISHED · SELF-SERVICE PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This guide is for technically competent external reviewers who want to evaluate the bounded public developer surface without internal AETHER X assistance.

It does not create a support relationship, SDK publication, software reuse licence, product integration claim or production-readiness claim.

The current public engineering program now has two distinct evaluator paths:

```text
REPOSITORY-LOCAL EVALUATION
= inspect and run the bounded public engineering surface directly from a repository checkout

INSTALLABLE PACKAGE EVALUATION
= inspect the exact Gate-05B installable package candidate under the Gate-05C evaluator handoff
```

This guide covers the **repository-local evaluation path**. For the current installable package candidate and Gate-05C handoff requirements, use [`INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md`](./INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md).

`REPOSITORY-LOCAL EVALUATION ≠ FINAL GATE-05C HUMAN EVALUATION`

## 1. What You Are Evaluating

You are evaluating a public governed-intelligence engineering surface consisting of:

- three public contract/specification paths;
- machine-readable JSON Schema structures;
- bounded reference validators;
- synthetic conformance kits;
- a repository-local Python SDK candidate;
- an installable Python package candidate governed separately under the current Gate-05 program;
- deterministic release-candidate engineering controls;
- public CI/governance evidence.

You are **not** evaluating a production AETHER X product, customer deployment, live service, broker connection, private agent runtime or internal product implementation.

The current installable package candidate is an engineering candidate only. Its existence does not establish supported-SDK status, public registry publication, production readiness or release authority.

## 2. Prerequisites

Required:

- Git;
- Python `3.11`, `3.12`, `3.13` or `3.14` for the current directly verified installable-candidate runtime matrix;
- a local shell capable of running the commands below.

No third-party Python package is required for the bounded repository-local evaluation path.

No AETHER X credential, private repository, private package index or private endpoint is required.

## 3. Clean Checkout

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
python3 --version
```

For current evaluation, use CPython `3.11–3.14`, which is the directly verified runtime matrix for the current installable candidate. A runtime outside that matrix may still allow repository inspection, but AETHER X does not claim it as part of the current verified installable-candidate runtime surface.

## 4. One-Command Repository-Local Evaluation Path

Run:

```bash
python3 tools/run_external_evaluation.py --json-out external-evaluation-report.json
```

Then validate the generated report:

```bash
python3 tools/check_external_evaluation_report.py external-evaluation-report.json
```

Expected success markers:

```text
AX_EXTERNAL_EVALUATION_RUN_PASS
AX_EXTERNAL_EVALUATION_REPORT_PASS
```

The runner exercises only public repository material.

A successful repository-local run is useful external engineering evidence, but it is not a substitute for the separately governed final Gate-05C installable-package human evaluation.

## 5. Manual Evaluation Path

If you want to inspect each repository-local layer separately, run:

```bash
python3 tools/check_developer_experience.py
python3 -m unittest discover -s sdk-candidate/python/tests -v
python3 sdk-candidate/python/example.py
python3 sdk-candidate/python/run_candidate_conformance.py
python3 tools/check_sdk_candidate_boundary.py
python3 tools/check_sdk_candidate_state.py
python3 tools/check_supply_chain_release_candidate.py
python3 tools/check_artifact_manifest.py
```

A successful run establishes only that the bounded public checks passed in your environment.

## 6. Repository-Local Integration Example

The repository-local SDK candidate remains available for direct checkout-based evaluation. A separate **installable package candidate** has also been established under Gate-05B; do not confuse the two evaluation paths.

To exercise the repository-local facade directly from the checkout:

```bash
PYTHONPATH="$PWD/sdk-candidate/python" python3 - <<'PY'
import json
from pathlib import Path

from aetherx_sdk_candidate import supported_contracts, validate_eav

print(supported_contracts())

payload = json.loads(
    Path("reference-implementations/eav-contract-validator/examples/valid_bundle.json").read_text()
)
result = validate_eav(payload)
print(result.as_dict())
assert result.valid is True
PY
```

This example evaluates the repository-local facade only.

For the exact installable package candidate, including its governed artifact identity, runtime matrix and external-index evaluation requirements, use [`INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md`](./INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md).

`REPOSITORY-LOCAL IMPORT ≠ APPROVED PACKAGE DISTRIBUTION`  
`INSTALLABLE CANDIDATE ≠ SUPPORTED SDK`

## 7. Contract Surface

The bounded public candidate surface currently maps only to:

```text
AX-PUB-SPEC-002 v1.0 — Evidence / Authority / Verification
AX-PUB-SPEC-003 v1.0 — Point-in-Time Knowledge / Provenance
AX-PUB-SPEC-004 v1.0 — Governed Agent Authority / Tool Use
```

Use `supported_contracts()` to inspect the bounded inventory programmatically.

Unsupported contract IDs and unsupported versions must fail explicitly through the candidate result model rather than being silently accepted.

## 8. Failure-Path Evaluation

Do not evaluate only the happy path.

The public repository includes invalid examples and conformance cases intended to exercise fail-closed behavior. Use the reference implementation example directories and public conformance kits to inspect how invalid evidence, provenance or authority states are reported.

## 9. Release-Candidate Reproducibility

The validated Gate-03 engineering bundle can be rebuilt from the declared source state using:

```bash
SOURCE_DATE_EPOCH=1787064230 \
python3 tools/build_release_candidate.py --output-dir dist
```

Then:

```bash
python3 tools/check_supply_chain_release_candidate.py --dist dist
```

For the currently validated Gate-03 state, the bundle identity is:

```text
AX-PUB-RC-001.zip
SHA-256: 8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21
```

This is a non-published engineering release candidate, not a package release.

## 10. What to Read Before Drawing Conclusions

Read:

- [`PUBLIC_ENGINEERING_STATE.md`](./PUBLIC_ENGINEERING_STATE.md)
- [`INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md`](./INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md)
- [`LIMITATIONS_AND_UNSUPPORTED_USES.md`](./LIMITATIONS_AND_UNSUPPORTED_USES.md)
- [`MIGRATION_AND_DEPRECATION_DRAFT.md`](./MIGRATION_AND_DEPRECATION_DRAFT.md)
- [`FEEDBACK_AND_TRIAGE.md`](./FEEDBACK_AND_TRIAGE.md)
- [`AX-PUB-GATE-001`](./AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)
- [`SECURITY.md`](../SECURITY.md)

## 11. How to Report Findings

Use the repository's **External evaluation feedback** issue form for reproducible, non-sensitive findings.

Do **not** place security-sensitive information, credentials, secrets, private data or suspected exploitable details into a public issue. Follow `SECURITY.md` for sensitive reports.

No response-time or support SLA is created by the public feedback process.

## 12. Evaluation Result Boundary

A successful repository-local run may support a statement such as:

> The evaluator reproduced the declared bounded public repository checks in the stated environment.

It must not be generalized into claims of:

- production readiness;
- security certification;
- standards certification;
- product implementation;
- customer adoption;
- supported SDK status;
- AETHER X product integration;
- commercial reuse permission;
- final Gate-05C human evaluation;
- external registry validation;
- SDK publication authority.

`EVALUATION PASS ≠ PRODUCTION APPROVAL`  
`EVALUATION PASS ≠ EXTERNAL ENDORSEMENT`  
`REPOSITORY-LOCAL EVALUATION ≠ FINAL GATE-05C HUMAN EVALUATION`  
`EXTERNAL EVALUATION READINESS ≠ EXTERNAL ADOPTION`  
`INSTALLABLE CANDIDATE ≠ SUPPORTED SDK`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
