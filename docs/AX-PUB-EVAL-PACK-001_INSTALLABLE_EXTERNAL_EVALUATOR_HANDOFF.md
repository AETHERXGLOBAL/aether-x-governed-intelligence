# AX-PUB-EVAL-PACK-001 — Installable External Evaluator Handoff Pack

**Artifact ID:** `AX-PUB-EVAL-PACK-001`  
**Version:** `0.1`  
**State:** `DEV-GATE-05C · CI-VALIDATED HANDOFF · HUMAN EXTERNAL EVALUATION NOT ESTABLISHED`  
**Distribution candidate:** `aetherxglobal-governed-intelligence`  
**Version candidate:** `0.1.0rc1`  
**Publication boundary:** `SDK PUBLICATION NOT AUTHORIZED`

## Purpose

`AX-PUB-EVAL-PACK-001` is the bounded, deterministic engineering handoff used to prepare an independent evaluator to review the exact installable SDK candidate.

It packages the public evaluator guide, final-report template/checker, current API/support/security candidate contracts, public limitations, and exact wheel/sdist identities for local rehearsal.

The operational evaluator instructions remain in:

[`INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md`](./INSTALLABLE_EXTERNAL_EVALUATOR_GUIDE.md)

Machine-readable source state:

[`artifacts/AX-PUB-EVAL-PACK-001.json`](../artifacts/AX-PUB-EVAL-PACK-001.json)

Builder:

[`tools/build_installable_evaluator_handoff.py`](../tools/build_installable_evaluator_handoff.py)

Integrity checker:

[`tools/check_installable_evaluator_handoff.py`](../tools/check_installable_evaluator_handoff.py)

## Validation chain

```text
AX-PUB-CI-014
→ validated the pre-promotion handoff subject
→ deterministic ZIP + exact package identity
→ local rehearsal CPython 3.11–3.14

AX-PUB-CI-015
→ re-materialized the promoted CI-validated source state
→ deterministic promoted ZIP
→ exact package payload preserved
→ local rehearsal CPython 3.11–3.14
```

Current promoted deterministic ZIP identity:

```text
2a7c85422421428af7e51c6b4ec86a1dc7ec10f8995585d9886b38e6f0e3f085
```

## Final evaluation firewall

A `FINAL` `AX-PUB-EVAL-REPORT-002` remains a separate human evidence object.

Final Gate-05C human evaluation requires, among other conditions:

```text
INDEPENDENT HUMAN EVALUATOR
AUTHORIZED EXTERNAL INDEX ACQUISITION
external_index_used = true
EXACT CANDIDATE IDENTITY
COMPLETE FINDING DISPOSITION
NO UNRESOLVED CRITICAL FINDING
```

A local handoff ZIP, GitHub Actions artifact, repository checkout, local web server or direct wheel path cannot satisfy the external-index requirement.

## Current disposition

```text
HANDOFF PACK: CI-VALIDATED
DETERMINISTIC PROMOTED PACK: VERIFIED
LOCAL REHEARSAL: CPYTHON 3.11–3.14 PASS
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
INDEPENDENT EVALUATOR RESULT: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
RELEASE CONTROL READY: NO
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

`HANDOFF PACK PASS ≠ HUMAN EXTERNAL EVALUATION`  
`LOCAL REHEARSAL ≠ EXTERNAL-INDEX VALIDATION`  
`ACTIONS ARTIFACT ≠ TESTPYPI OR PYPI PUBLICATION`  
`HANDOFF PACK PASS ≠ SUPPORTED SDK`  
`HANDOFF PACK PASS ≠ RELEASE AUTHORITY`
