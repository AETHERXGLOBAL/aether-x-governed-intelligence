# AETHER X — Installable External Evaluator Guide — Current Correction Candidate

**Scope:** bounded evaluator handoff for `AXGI-REV-001` correction only.  
**Correction revision:** `3e8be5b097df0049dbf4cad134fbc6706269ca9c`  
**Status:** `CURRENT CANDIDATE EVIDENCE — NOT RELEASE AUTHORITY`

## Current package identity

- Distribution: `aetherxglobal-governed-intelligence`
- Version: `0.1.0rc1`
- Wheel: `aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl`
- Wheel SHA-256: `277910189daaad2167d5d321a7881b72455483ec886574aea5f5ba4f1e1f3f1c`
- sdist: `aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz`
- sdist SHA-256: `c9eeab1060689e918c91b882c985ab9630a84d5ded0da7424decde4779616291`

Verify the payload against the manifest and `CURRENT_CANDIDATE_IDENTITY.json` before use. The packaged `AX-PUB-EVAL-REPORT-002.template.json` is bound to these current digests.

## Historical evidence boundary

`AX-PUB-DEV-008 / AX-PUB-CI-009` and `AX-PUB-EVAL-PACK-001 / AX-PUB-CI-014` remain immutable historical closed-state evidence. Their earlier wheel, sdist, validator and validation-subject digests are **not** redefined by this current candidate. `HISTORICAL_EVALUATOR_GUIDE.md` is retained inside the handoff only to preserve that historical context.

## Evaluation boundary

This handoff supports local/CI rehearsal only. `LOCAL REHEARSAL ≠ FINAL EXTERNAL-INDEX EVALUATION`.

A final external evaluator must acquire the candidate from the authorized external index and record `external_index_used` in the final `AX-PUB-EVAL-REPORT-002` record. Local CI artifacts do not establish registry publication, human external evaluation, adoption, support, release authority, or production status.

`SDK PUBLICATION NOT AUTHORIZED`
