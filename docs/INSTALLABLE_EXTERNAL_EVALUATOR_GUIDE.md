# AETHER X Governed Intelligence — Installable Package External Evaluator Guide

`AX-PUB-EVAL-PACK-001 · DEV-GATE-05C CANDIDATE · INDEPENDENT HUMAN EVALUATION HANDOFF · SDK PUBLICATION NOT AUTHORIZED`

## Purpose

This guide is for an independent technical evaluator reviewing the exact Gate-05B installable package candidate during `DEV-GATE-05C`.

It separates two activities that must not be confused:

```text
LOCAL REHEARSAL
= inspect the exact candidate and exercise it without external-registry evidence

FINAL GATE-05C HUMAN EVALUATION
= acquire the exact candidate from an explicitly authorized external index,
  perform independent technical evaluation, and return a FINAL
  AX-PUB-EVAL-REPORT-002 record
```

You are **not** being asked to endorse AETHER X, adopt the SDK, test a production service, grant a software licence, or evaluate any private AETHER X product.

`EVALUATOR HANDOFF PACK ≠ HUMAN EVALUATION COMPLETED`

---

## 1. Exact Candidate

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Import:       aetherxglobal.governed_intelligence

Wheel:
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

Source distribution:
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz
SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99

Declared evaluation runtimes:
CPython 3.11 / 3.12 / 3.13 / 3.14
```

Do not evaluate a package with a different digest and report it as this candidate.

---

## 2. Handoff Pack

The engineering handoff candidate is:

```text
AX-PUB-EVAL-PACK-001 v0.1
```

A CI-produced handoff ZIP may contain:

- this guide;
- the blank `AX-PUB-EVAL-REPORT-002` template;
- the final-report checker;
- the current public API/support/security contract records;
- current public limitations;
- an exact locally rebuilt wheel and sdist for **rehearsal and identity inspection**;
- a machine-readable pack manifest with SHA-256 identities.

The Actions artifact containing this handoff pack is a short-lived engineering transport only.

```text
CI ARTIFACT ≠ TESTPYPI PUBLICATION
CI ARTIFACT ≠ PYPI PUBLICATION
LOCAL WHEEL IN HANDOFF PACK ≠ FINAL EXTERNAL-INDEX INSTALLATION
```

---

## 3. Verify the Handoff Pack Before Use

After extracting `AX-PUB-EVAL-PACK-001.zip`, inspect the generated pack manifest and verify the payload hashes.

Example using Python only:

```bash
python3 - <<'PY'
import hashlib, json
from pathlib import Path

root = Path('.')
manifest = json.loads((root / 'AX-PUB-EVAL-PACK-001.manifest.json').read_text())
for item in manifest['files']:
    path = root / item['path']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == item['sha256'], (item['path'], digest, item['sha256'])
print('AX_EVALUATOR_HANDOFF_PAYLOAD_HASHES_PASS')
PY
```

The candidate wheel and sdist must match the exact hashes in Section 1.

---

## 4. Local Rehearsal — Not Final Gate-05C Evidence

The handoff pack may include the exact candidate wheel so an evaluator can understand the API and evaluation steps before an authorized external index exists.

Example:

```bash
python3 -m venv .venv-rehearsal
. .venv-rehearsal/bin/activate
python -m pip install --disable-pip-version-check --no-deps \
  payload/aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
python - <<'PY'
import aetherxglobal.governed_intelligence as sdk
print(sdk.__version__)
print(sdk.supported_contracts())
assert sdk.__version__ == '0.1.0rc1'
PY
```

On Windows, activate the virtual environment using the platform-appropriate command.

Local rehearsal is useful for evaluator preparation, but it **must not** be recorded as a `FINAL` Gate-05C human evaluation because it did not acquire the package from the authorized external distribution path.

```text
LOCAL REHEARSAL ≠ FINAL EXTERNAL-INDEX EVALUATION
```

---

## 5. Final Installation Source Requirement

Gate-05C closure requires an explicitly authorized controlled external distribution path. Until AETHER X separately provides that authorized index location, **do not infer that TestPyPI or PyPI publication exists**.

When an authorized evaluation index is supplied, the evaluator should acquire the exact candidate from that index rather than from the handoff ZIP.

Recommended acquisition pattern:

```bash
python3 -m venv .venv-final
. .venv-final/bin/activate
mkdir -p external-dist

python -m pip download \
  --index-url '<AUTHORIZED_EXTERNAL_INDEX_URL>' \
  --no-deps \
  --only-binary=:all: \
  --dest external-dist \
  'aetherxglobal-governed-intelligence==0.1.0rc1'
```

Then verify the downloaded wheel SHA-256 equals:

```text
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac
```

Install only after exact identity verification:

```bash
python -m pip install --disable-pip-version-check --no-deps \
  external-dist/aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
```

Record the exact index URL/domain and set:

```json
"external_index_used": true
```

only when the candidate was actually acquired through that authorized external index.

Do not set the field to `true` for a handoff ZIP, GitHub Actions artifact, repository checkout, local web server, direct wheel path or other non-external-registry source.

---

## 6. Evaluation Objectives

Evaluate, at minimum:

1. acquisition from the supplied authorized external index for a final record;
2. exact package/version/hash identity;
3. import of `aetherxglobal.governed_intelligence`;
4. declared contract inventory;
5. valid-input behavior;
6. fail-closed invalid-input behavior;
7. unsupported contract/version behavior;
8. clarity and usefulness of errors/findings;
9. absence of unexpected network/credential requirements for the declared offline scope;
10. documentation clarity and material limitations;
11. consistency of the observed public API with `AX-PUB-API-001`;
12. any material installation, packaging, compatibility or security concern observable within the public scope.

You may perform additional non-destructive technical review within the public package/repository scope.

---

## 7. Public API Scope

The candidate public surface is governed by `AX-PUB-API-001` and currently covers the bounded offline validation surface for:

```text
AX-PUB-SPEC-002 v1.0 — Evidence / Authority / Verification
AX-PUB-SPEC-003 v1.0 — Point-in-Time Knowledge / Provenance
AX-PUB-SPEC-004 v1.0 — Governed Agent Authority / Tool Use
```

Relevant top-level functions include:

```python
validate
validate_eav
validate_point_in_time
validate_agent_authority
supported_contracts
```

A candidate API contract does not establish a stable `1.0` compatibility guarantee.

---

## 8. Required Evaluation Record

Start from:

```text
AX-PUB-EVAL-REPORT-002.template.json
```

For a final report, change:

```json
"record_state": "FINAL"
```

and record:

- evaluator identity or bounded evaluator identifier;
- `independent_of_implementation: true` only when accurate;
- start/completion timestamps;
- operating system/platform;
- Python runtime;
- installation source;
- `external_index_used: true` only when accurate;
- exact wheel/sdist identity;
- each check and result;
- findings with severity and reproduction detail;
- overall result;
- issue/finding disposition state.

Validate the completed report with:

```bash
python3 check_installable_external_evaluation_report.py evaluator-report.json
```

A report with placeholder evaluator identity, missing artifact identity, `record_state=TEMPLATE`, or `external_index_used=false` is **not** final Gate-05C human external-evaluation evidence.

---

## 9. Finding Severity and Disposition

Severity values:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

Allowed dispositions are defined by the report checker.

An unresolved `CRITICAL` finding blocks Gate-05C closure. A `HIGH` finding must be fixed or have explicit authorized risk acceptance (or another checker-accepted non-open disposition) before a final report can satisfy the current evidence contract.

Do not mark issue disposition complete while material findings remain unresolved under the checker rules.

---

## 10. Sensitive Findings

Do not publish secrets, credentials, personal data, confidential architecture or exploitable security details in a public issue.

The current public security reporting path remains provisional. A final production-supported SDK requires the separate `AX-PUB-SEC-001` security-operations readiness conditions to be satisfied.

---

## 11. What the Evaluator Is Not Testing

Unless separately and explicitly authorized, this evaluation does not cover:

- production AETHER X services;
- private repositories;
- production authorization decisions;
- brokerage/trading execution;
- tool invocation or autonomous external side effects;
- private AETHER X product integrations;
- customer deployments;
- commercial support or SLA delivery.

---

## 12. Claim Boundary

A successful evaluation may establish only that the named independent evaluator acquired and evaluated the exact declared candidate through the recorded path and environment, with the documented findings and dispositions.

It does not establish:

- security certification;
- standards certification;
- production readiness;
- product integration;
- customer adoption;
- endorsement;
- support SLA;
- software reuse permission;
- stable `1.0` API status;
- SDK publication authority.

`EVALUATION ≠ ENDORSEMENT`  
`EVALUATION ≠ ADOPTION`  
`EVALUATION PASS ≠ SUPPORTED SDK`  
`EVALUATION PASS ≠ RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
