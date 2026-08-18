# AX-PUB-CI-015 — Evaluator Handoff Promoted Materialization Evidence

**Evidence ID:** `AX-PUB-CI-015`  
**State:** `DIRECT CI EVIDENCE / PROMOTED HANDOFF MATERIALIZATION`  
**Scope:** `AX-PUB-EVAL-PACK-001 CI-VALIDATED SOURCE STATE`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## Reviewed source

```text
Promotion PR: #56
Verified head commit: 51524fed7d7aee44254ec318e7897b988deb8498
Source artifact: AX-PUB-EVAL-PACK-001 v0.1
Source state: DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CI_VALIDATED
Prior validation evidence: AX-PUB-CI-014
```

## Direct workflow evidence

```text
Workflow: Validate Installable External Evaluator Handoff
Workflow run ID: 32197243557
Workflow run number: 11
Job ID: 95903654036
Conclusion: SUCCESS

Companion manifest validation:
Run ID: 32197243486
Run number: 201
Conclusion: SUCCESS
```

## Promoted deterministic handoff identity

The promoted source state was built twice and the resulting ZIPs were byte-identical.

```text
AX-PUB-EVAL-PACK-001.zip SHA-256:
2a7c85422421428af7e51c6b4ec86a1dc7ec10f8995585d9886b38e6f0e3f085
```

The exact package payload remained unchanged:

```text
Wheel SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

sdist SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

The handoff manifest state was:

```text
manifest_version: 1.1
source_state: CI_VALIDATED_HANDOFF_SOURCE
validation_evidence: AX-PUB-CI-014
final_external_index_required: true
human_external_evaluation_established: false
external_registry_validation_established: false
sdk_publication_authorized: false
```

## Local rehearsal

The promoted bundle was locally installed and verified again on:

```text
CPython 3.11 — PASS
CPython 3.12 — PASS
CPython 3.13 — PASS
CPython 3.14 — PASS
```

This remains a local rehearsal path. It is not final human external evaluation and does not satisfy the required authorized external-index acquisition step.

## Short-lived Actions artifact

```text
Artifact ID: 9346271842
Artifact name: ax-pub-eval-pack-001-19c8b7b10b67b99e267967a2585109c399acb131
Artifact size: 53072 bytes
Artifact SHA-256:
64cd6724dc90241d5df243b6c5e1a2c8bddcb298ef049bce3a2731f634a8e0e6
Retention: 7 days
```

The Actions artifact is short-lived CI transport. It is not TestPyPI/PyPI publication and is not an external package index.

## What this establishes

```text
PROMOTED HANDOFF SOURCE: DIRECTLY CI VALIDATED
PROMOTED HANDOFF ZIP: DETERMINISTIC
CURRENT PROMOTED ZIP IDENTITY: RECORDED
EXACT PACKAGE PAYLOAD: PRESERVED
LOCAL REHEARSAL: CPYTHON 3.11–3.14 PASS
```

## What this does not establish

```text
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED
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

`PROMOTED HANDOFF PASS ≠ HUMAN EXTERNAL EVALUATION`  
`LOCAL REHEARSAL ≠ EXTERNAL-INDEX VALIDATION`  
`ACTIONS ARTIFACT ≠ TESTPYPI OR PYPI PUBLICATION`  
`PROMOTED HANDOFF PASS ≠ SUPPORTED SDK`  
`PROMOTED HANDOFF PASS ≠ RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
