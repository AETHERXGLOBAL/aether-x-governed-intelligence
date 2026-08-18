# AETHER X Governed Intelligence — External Evaluator Guide

`DEV-GATE-04 CANDIDATE · SELF-SERVICE PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This guide is for technically competent external reviewers who want to evaluate the bounded public developer surface without internal AETHER X assistance.

It does not create a support relationship, SDK publication, software reuse licence, product integration claim or production-readiness claim.

## 1. What You Are Evaluating

You are evaluating a public, repository-local governed-intelligence engineering surface consisting of:

- three public contract/specification paths;
- machine-readable JSON Schema structures;
- bounded reference validators;
- synthetic conformance kits;
- a repository-local Python SDK candidate;
- deterministic release-candidate engineering controls;
- public CI/governance evidence.

You are **not** evaluating a production AETHER X product, customer deployment, live service, broker connection, private agent runtime or internal product implementation.

## 2. Prerequisites

Required:

- Git;
- Python `3.10`, `3.11`, `3.12` or `3.13` for the directly verified candidate matrix;
- a local shell capable of running the commands below.

No third-party Python package is required for the bounded public candidate path.

No AETHER X credential, private repository, private package index or private endpoint is required.

## 3. Clean Checkout

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
python3 --version
```

If your Python runtime is outside `3.10–3.13`, you may inspect the repository, but AETHER X does not claim that runtime as part of the current directly verified candidate matrix.

## 4. One-Command Evaluation Path

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

## 5. Manual Evaluation Path

If you want to inspect each layer separately, run:

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

The candidate is not an installable package. To exercise the repository-local facade directly from the checkout:

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

This is an evaluation/integration example for the repository-local candidate only.

`REPOSITORY-LOCAL IMPORT ≠ APPROVED PACKAGE DISTRIBUTION`

## 7. Contract Surface

The candidate currently maps only to:

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

A successful external run may support a statement such as:

> The evaluator reproduced the declared bounded public checks in the stated environment.

It must not be generalized into claims of:

- production readiness;
- security certification;
- standards certification;
- product implementation;
- customer adoption;
- supported SDK status;
- AETHER X product integration;
- commercial reuse permission.

`EVALUATION PASS ≠ PRODUCTION APPROVAL`  
`EVALUATION PASS ≠ EXTERNAL ENDORSEMENT`  
`EXTERNAL EVALUATION READINESS ≠ EXTERNAL ADOPTION`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
