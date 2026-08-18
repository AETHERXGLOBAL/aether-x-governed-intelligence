# AX-PUB-CI-014 — Installable External Evaluator Handoff Validation Evidence

**Evidence ID:** `AX-PUB-CI-014`  
**State:** `DIRECT CI EVIDENCE / EVALUATOR HANDOFF VALIDATION`  
**Scope:** `DEV-GATE-05C INSTALLABLE INDEPENDENT-HUMAN EVALUATOR HANDOFF PREPARATION`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## Reviewed change

```text
Candidate bootstrap PR: #53
Bootstrap merge commit: f25e8c5db41232e29efe201bd202231994a59cdc

Validation PR: #54
Validation head: 8817b4540a8dee4ab0b1e1ad1fcb21c4826d710f
GitHub pull-request merge-test commit: 09a5e6f1d396f23ccd26969559fe5210e6bd7b10
Validation merge commit on main: 584c317c04da4219c8952f67d641ef2edb19c967
```

Validated handoff artifact:

```text
AX-PUB-EVAL-PACK-001 v0.1
State under test: DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CANDIDATE
Candidate distribution: aetherxglobal-governed-intelligence
Candidate version: 0.1.0rc1
```

## Primary workflow

```text
Workflow: Validate Installable External Evaluator Handoff
Workflow run ID: 32196714529
Workflow run number: 7
Job: Deterministic evaluator handoff / CPython 3.11-3.14 rehearsal
Job ID: 95902129022
Conclusion: SUCCESS
```

Companion governance validation on the same reviewed head:

```text
Workflow: Validate Public Artifact Manifest
Run ID: 32196714599
Run number: 199
Conclusion: SUCCESS
```

## Deterministic handoff identity

The handoff builder rebuilt the exact candidate twice from reviewed source and produced byte-identical handoff ZIPs.

```text
AX-PUB-EVAL-PACK-001.zip SHA-256:
5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2
```

Both builds directly re-established the exact Gate-05B package identities:

```text
Wheel:
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl
SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

sdist:
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz
SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

The built pack contained a machine-readable file inventory and direct per-file SHA-256 checks. Bundle validation reported:

```text
files=10
external_registry=false
human_evaluation=false
publication=NOT_AUTHORIZED
```

## Local rehearsal runtime validation

The exact wheel carried by the handoff pack was installed into fresh virtual environments and imported successfully on:

```text
CPython 3.11 — PASS
CPython 3.12 — PASS
CPython 3.13 — PASS
CPython 3.14 — PASS
```

For every runtime, CI verified:

- package version `0.1.0rc1`;
- import namespace `aetherxglobal.governed_intelligence`;
- declared supported contract IDs exactly `AX-PUB-SPEC-002`, `AX-PUB-SPEC-003`, `AX-PUB-SPEC-004`;
- the blank `AX-PUB-EVAL-REPORT-002` template remained valid only under `--allow-template`;
- template validation preserved `human_evaluation=false`.

This is **local rehearsal validation**, not final human external evaluation.

## Final human-evaluation firewall

The handoff contract continues to require a `FINAL` report to establish all applicable human evidence conditions, including:

```text
record_state = FINAL
independent_of_implementation = true
external_index_used = true
issue_disposition_complete = true
unresolved_critical_findings = 0
```

The guide explicitly requires that `external_index_used=true` be set only when the exact candidate is actually acquired through a separately authorized external index. A GitHub Actions artifact, repository checkout, local web server, handoff ZIP or direct wheel path does not satisfy this field.

## Short-lived Actions artifact

The workflow preserved the deterministic handoff output as a seven-day GitHub Actions artifact:

```text
Artifact ID: 9346099991
Artifact name: ax-pub-eval-pack-001-09a5e6f1d396f23ccd26969559fe5210e6bd7b10
Artifact size: 52700 bytes
Artifact SHA-256:
9aab68064bf93319056dfb3d75135ab75559a26bad78ff8b949e7297c9e68961
```

This Actions artifact is engineering transport/evidence only. It is not TestPyPI/PyPI publication and is not the external-index acquisition source required for a final Gate-05C human evaluation.

## What is established

```text
EVALUATOR HANDOFF PACK DEFINITION: ESTABLISHED
DETERMINISTIC HANDOFF BUILD: VERIFIED
HANDOFF BUNDLE INTEGRITY: VERIFIED
EXACT WHEEL / SDIST IDENTITY: VERIFIED
LOCAL REHEARSAL: CPYTHON 3.11–3.14 PASS
FINAL REPORT TEMPLATE CONTRACT: VALIDATED AS TEMPLATE
HANDOFF PACK CI VALIDATION: SUCCESS
```

## What is not established

```text
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED
TESTPYPI PUBLICATION: NOT AUTHORIZED / NOT ESTABLISHED
PYPI PUBLICATION: NOT AUTHORIZED / NOT ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
INDEPENDENT EVALUATOR RESULT: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
ENDORSEMENT: NOT ESTABLISHED
RELEASE-CONTROL READINESS: NOT ESTABLISHED
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

## Claim boundary

`HANDOFF PACK PASS ≠ HUMAN EXTERNAL EVALUATION`  
`LOCAL REHEARSAL PASS ≠ EXTERNAL-INDEX VALIDATION`  
`CI ARTIFACT ≠ TESTPYPI OR PYPI PUBLICATION`  
`EVALUATION READINESS ≠ ENDORSEMENT OR ADOPTION`  
`HANDOFF PACK PASS ≠ SUPPORTED SDK`  
`HANDOFF PACK PASS ≠ RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
