# AX-PUB-CI-013 — SDK Support & Security Contract Validation Evidence

**Evidence ID:** `AX-PUB-CI-013`  
**State:** `DIRECT CI EVIDENCE / CANDIDATE CONTRACT VALIDATION`  
**Scope:** `DEV-GATE-05C SUPPORT / COMPATIBILITY / MAINTENANCE + SECURITY-OPERATIONS CONTRACT CANDIDATES`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## Reviewed change

```text
Pull request: #50
Reviewed head: b7c0f25eacfa534ae38d71b495fbd2d963d679a5
Merged main commit: 9cced38d62723f05d6bb8142cb9525c89e93a4c9
```

Validated candidate artifacts:

```text
AX-PUB-SUP-001 v0.1
AX-PUB-SEC-001 v0.1
Bound API contract: AX-PUB-API-001 v0.1
Bound SDK candidate: aetherxglobal-governed-intelligence 0.1.0rc1
```

## Primary validation workflow

```text
Workflow: Validate SDK Support & Security Contracts
Workflow run ID: 32194756205
Workflow run number: 5
Conclusion: SUCCESS
```

Runtime jobs:

```text
CPython 3.11 — job 95896362054 — SUCCESS
CPython 3.12 — job 95896362020 — SUCCESS
CPython 3.13 — job 95896362021 — SUCCESS
CPython 3.14 — job 95896362076 — SUCCESS
```

Each runtime job directly validated:

- machine-readable support contract parsing;
- machine-readable security-operations contract parsing;
- binding to `AX-PUB-API-001` and SDK candidate `0.1.0rc1`;
- support commitment remains unactivated;
- stable `1.0` compatibility guarantee remains unestablished;
- target deprecation rule remains candidate-only;
- security operations remain not ready;
- provisional security intake remains non-dedicated and without SLA;
- release-control baseline remains not ready;
- SDK publication remains not authorized.

## Cross-gate immutability validation

```text
Job: Preserve closed Gate-03 release-candidate identity
Job ID: 95896362012
Canonical runtime: CPython 3.13
Conclusion: SUCCESS
```

The job rebuilt `AX-PUB-RC-001` from its declared immutable source inventory using the verified source epoch and re-ran the closed Gate-03 supply-chain checker.

Verified Gate-03 identity remained:

```text
AX-PUB-RC-001 verified build digest:
8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21

Verified source date epoch:
1787064230
```

This check was added after an adverse intermediate result showed that changing a source file included in the closed Gate-03 bundle would alter the deterministic bundle digest. The final reviewed state restores the exact immutable Gate-03 source identity and prevents support/security productization work from silently rewriting closed evidence.

## Governance companion workflows

On the same reviewed head:

```text
Validate Public Artifact Manifest
Run ID: 32194756195
Run number: 190
Conclusion: SUCCESS

Validate External Evaluation Readiness
Run ID: 32194756191
Run number: 35
Conclusion: SUCCESS
```

## What is established

```text
SUPPORT / COMPATIBILITY / MAINTENANCE CONTRACT CANDIDATE: VALIDATED
SECURITY-OPERATIONS READINESS CONTRACT CANDIDATE: VALIDATED
CANDIDATE CONTRACT VALIDATION: CPYTHON 3.11–3.14 PASS
CLOSED GATE-03 RELEASE-CANDIDATE IDENTITY: PRESERVED
```

## What is not established

```text
SUPPORT COMMITMENT: NOT ESTABLISHED
PRODUCTION SUPPORT: NOT ACTIVATED
STABLE 1.0 API GUARANTEE: NOT ESTABLISHED
COMMERCIAL SLA: NOT ESTABLISHED
DEDICATED SECURITY CHANNEL: NOT ESTABLISHED
SECURITY RESPONSE OWNER: NOT ESTABLISHED BY THIS EVIDENCE
SECURITY RESPONSE SLA: NOT ESTABLISHED
BUG BOUNTY: NOT ESTABLISHED
SECURITY OPERATIONS READY: NO
RELEASE CONTROL READY: NO
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

## Claim boundary

`CONTRACT VALIDATION ≠ CONTRACT ACTIVATION`  
`TARGET SUPPORT WINDOW ≠ CURRENT SUPPORT PROMISE`  
`SECURITY-OPERATIONS CONTRACT ≠ SECURITY-OPERATIONS READINESS`  
`CROSS-GATE IMMUTABILITY PASS ≠ RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
