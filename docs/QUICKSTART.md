# AETHER X Governed Intelligence — Public Quickstart

`PUBLIC ENGINEERING GUIDE · CONTROLLED DISCLOSURE · NON-PRODUCTION`

This is the shortest supported path for an engineer to inspect, run and evaluate the current public AETHER X governed-intelligence engineering surface.

For the exact moving maturity state, use [`PUBLIC_ENGINEERING_STATE.md`](./PUBLIC_ENGINEERING_STATE.md).

## Current status

```text
DEV-GATE-00  CLOSED
DEV-GATE-01  CLOSED
DEV-GATE-02  CLOSED
DEV-GATE-03  CLOSED
DEV-GATE-04  CLOSED

DEV-GATE-05  ACTIVE
  05A  CLOSED
  05B  CLOSED
  05C  ACTIVE
  05D  NOT AUTHORIZED
```

Current installable engineering candidate:

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Import:       aetherxglobal.governed_intelligence
Runtime:      CPython 3.11–3.14 verified at package level
```

Current release-readiness aggregation:

```text
AX-PUB-RELPACK-001: CI-VALIDATED / BLOCKED
AX-PUB-CI-016: DIRECT VALIDATION EVIDENCE
HARD DIMENSIONS: 13
ESTABLISHED: 4
BLOCKED: 9
READY FOR DEV-GATE-05D AUTHORITY REVIEW: NO
```

`INSTALLABLE CANDIDATE ≠ SUPPORTED SDK`  
`RELEASE READINESS AGGREGATION PASS ≠ RELEASE READINESS`  
`SDK PUBLICATION NOT AUTHORIZED`

---

## 1. Clone the public engineering repository

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
```

The public reference paths are self-contained and do not require a private AETHER X repository, private endpoint or private credential.

---

## 2. Run the three public reference paths

### Evidence / Authority / Verification

```bash
python3 reference-implementations/eav-contract-validator/validator.py \
  reference-implementations/eav-contract-validator/examples/valid_bundle.json
```

Expected marker:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

### Point-in-Time Knowledge / Provenance

```bash
python3 reference-implementations/point-in-time-knowledge-validator/validator.py \
  reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json
```

Expected marker:

```text
AX_PTK_REFERENCE_VALIDATION_PASS
```

### Governed Agent Authority / Tool Use

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Expected marker:

```text
AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS
```

`REFERENCE VALIDATOR PASS ≠ PRODUCTION AUTHORIZATION`

---

## 3. Run public conformance

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
python3 conformance/AX-PUB-TEST-002/run_conformance.py
python3 tools/check_public_conformance_boundary.py
```

Published success markers include:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

These are bounded synthetic conformance checks, not production certification.

---

## 4. Durable closed-gate evidence

The moving Quickstart preserves the exact closure markers consumed by the fail-closed governance checkers for earlier gates:

```text
DEV-GATE-01: CLOSED
AX-PUB-CI-004
VERIFIED RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13

DEV-GATE-02: CLOSED
SDK CANDIDATE: ESTABLISHED
AX-PUB-CI-005
OBJECTIVE: DEV-GATE-05 — SDK RELEASE DECISION
SDK PUBLICATION: NOT AUTHORIZED

DEV-GATE-03: CLOSED
RELEASE CANDIDATE: VALIDATED / NON-PUBLISHED
AX-PUB-CI-006

DEV-GATE-04: CLOSED
EXTERNAL EVALUATION READINESS: ESTABLISHED
AX-PUB-CI-007
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
```

These markers preserve historical gate closure while the active engineering objective advances. They do not override the more specific current Gate-05 state below.

---

## 5. Inspect the installable SDK candidate

Candidate source:

[`sdk-release-candidate/python`](../sdk-release-candidate/python/)

The current candidate exposes:

```python
from aetherxglobal.governed_intelligence import (
    validate,
    validate_eav,
    validate_point_in_time,
    validate_agent_authority,
    supported_contracts,
)
```

The candidate is deliberately scoped to **offline governed-intelligence validation**. It does not expose network services, credentials, production authorization, tool execution, brokerage execution or private product integration.

Exact validated candidate identity:

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

Direct evidence: [`AX-PUB-CI-009`](../evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md).

---

## 6. Understand distribution validation

`DEV-GATE-05C` has directly validated the exact candidate through a loopback-only Python Simple Repository API-compatible index. The exact candidate was discovered with pip index semantics, installed into a clean environment and verified on CPython 3.11–3.14.

Direct evidence: [`AX-PUB-CI-010`](../evidence/AX-PUB-CI-010_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE_VALIDATION.md).

```text
LOCAL INDEX VALIDATION: VERIFIED / LOCAL ONLY
TESTPYPI VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED
PYPI VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED
REGISTRY OWNERSHIP: NOT ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

`LOCAL INDEX PASS ≠ TESTPYPI PASS`

---

## 7. Inspect the public API contract candidate

The current candidate public API is explicitly governed by:

- [`AX-PUB-API-001`](./AX-PUB-API-001_PYTHON_SDK_PUBLIC_API_CONTRACT.md) — candidate public API contract;
- [`AX-PUB-CI-012`](../evidence/AX-PUB-CI-012_SDK_PUBLIC_API_CONTRACT_VALIDATION.md) — direct CPython 3.11–3.14 validation evidence.

The contract covers:

```text
TOP-LEVEL EXPORT INVENTORY
CALLABLE PARAMETER SEMANTICS
FROZEN RESULT-TYPE FIELD ORDER
ERROR CATEGORY VALUES
SUPPORTED CONTRACT INVENTORY
FAIL-CLOSED UNSUPPORTED CONTRACT / VERSION BEHAVIOR
OFFLINE / NO-EXECUTION PRODUCT BOUNDARY
```

```text
API CONTRACT CANDIDATE: VALIDATED
STABLE 1.0 GUARANTEE: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

---

## 8. Inspect support and security productization contracts

The future production-supported SDK has two explicit **pre-activation** operating contracts:

- [`AX-PUB-SUP-001`](./AX-PUB-SUP-001_SDK_SUPPORT_COMPATIBILITY_MAINTENANCE_CONTRACT.md) — support, compatibility and maintenance contract candidate;
- [`AX-PUB-SEC-001`](./AX-PUB-SEC-001_SDK_SECURITY_OPERATIONS_READINESS_CONTRACT.md) — security-operations readiness contract candidate;
- [`AX-PUB-CI-013`](../evidence/AX-PUB-CI-013_SDK_SUPPORT_SECURITY_CONTRACT_VALIDATION.md) — direct validation evidence across CPython 3.11–3.14 plus closed Gate-03 identity preservation.

Current state:

```text
SUPPORT CONTRACT CANDIDATE: VALIDATED / NOT ACTIVATED
TARGET NORMAL DEPRECATION WINDOW: LATER OF 90 DAYS OR ONE SUPPORTED MINOR / NOT ACTIVE
SUPPORT COMMITMENT: NOT ESTABLISHED
COMMERCIAL SLA: NOT ESTABLISHED

SECURITY OPERATIONS CONTRACT CANDIDATE: VALIDATED / NOT READY
DEDICATED SECURITY CHANNEL: NOT ESTABLISHED
SECURITY RESPONSE OWNER: NOT ESTABLISHED
SECURITY RESPONSE SLA: NOT ESTABLISHED
BUG BOUNTY: NOT ESTABLISHED
SECURITY OPERATIONS READY: NO

SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

The candidate target window is a future activation condition, not a current promise.

`CONTRACT VALIDATION ≠ CONTRACT ACTIVATION`

---

## 9. Inspect the external-evaluator handoff

The current installable evaluator handoff is governed by:

- [`AX-PUB-EVAL-PACK-001`](./AX-PUB-EVAL-PACK-001_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF.md);
- [`AX-PUB-CI-014`](../evidence/AX-PUB-CI-014_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF_VALIDATION.md);
- [`AX-PUB-CI-015`](../evidence/AX-PUB-CI-015_EVALUATOR_HANDOFF_PROMOTED_MATERIALIZATION.md).

Current state:

```text
HANDOFF PACK: CI-VALIDATED / DETERMINISTIC
LOCAL REHEARSAL: CPYTHON 3.11–3.14 VERIFIED
FINAL EXTERNAL INDEX: REQUIRED
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

`HANDOFF CI-VALIDATED ≠ HUMAN EXTERNAL EVALUATION`

---

## 10. Inspect the release-readiness evidence aggregation

The current hard-gate aggregation is governed by:

- [`AX-PUB-RELPACK-001`](./AX-PUB-RELPACK-001_SDK_RELEASE_READINESS_EVIDENCE_PACK.md);
- [`AX-PUB-CI-016`](../evidence/AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md).

Validated current result:

```text
REQUIRED HARD DIMENSIONS: 13
ESTABLISHED: 4
BLOCKED: 9
READY FOR DEV-GATE-05D AUTHORITY REVIEW: NO
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

The four established dimensions are engineering evidence only:

```text
ENGINEERING_CANDIDATE_IDENTITY
PUBLIC_API_CONTRACT
EXACT_ARTIFACT_RUNTIME_VALIDATION
SUPPLY_CHAIN_PROVENANCE_SBOM
```

The nine remaining blockers cover external registry validation, independent human evaluation, release controls, registry ownership/Trusted Publisher, licence/IP clearance, support activation, security operations, release-owner accountability and explicit release authority.

A green aggregation workflow means the report correctly reflects those blockers.

`AGGREGATION PASS ≠ RELEASE READINESS`

---

## 11. Machine-readable current state

Canonical moving compatibility/governance index:

```text
AX-PUB-MANIFEST-001 v1.26
AX-PUB-POL-001 v1.6
```

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) for machine-readable artifact relationships and current gate state.

The manifest records:

```text
AX-PUB-CI-011 — first live release-control baseline
AX-PUB-API-001 + AX-PUB-CI-012 — validated API contract candidate
AX-PUB-SUP-001 + AX-PUB-SEC-001 + AX-PUB-CI-013 — validated pre-activation support/security contracts
AX-PUB-EVAL-PACK-001 + AX-PUB-CI-014 + AX-PUB-CI-015 — CI-validated evaluator handoff
AX-PUB-RELPACK-001 + AX-PUB-CI-016 — CI-validated blocked release-readiness aggregation
```

---

## 12. Production SDK target

The program target is not merely to place a package on a registry. The target is an official production-supported developer product:

```text
OFFICIAL SOURCE
→ CONTROLLED CHANGE
→ VERIFIED BUILD
→ TESTED WHEEL / SDIST
→ RELEASE PROVENANCE
→ CONTROLLED REGISTRY PUBLICATION
→ pip install
→ DOCUMENTED PUBLIC API
→ COMPATIBILITY / DEPRECATION CONTRACT
→ SECURITY / MAINTENANCE PROCESS
→ SUPPORTED DECLARED PRODUCTION SCOPE
```

The exact Definition of Done is in [`PRODUCTION_SDK_DEFINITION_OF_DONE.md`](./PRODUCTION_SDK_DEFINITION_OF_DONE.md).

Release-control requirements are in [`RELEASE_CONTROL_PLANE.md`](./RELEASE_CONTROL_PLANE.md).

Live release-control audit semantics and the current baseline are in [`RELEASE_CONTROL_AUDIT.md`](./RELEASE_CONTROL_AUDIT.md).

---

## 13. Recommended reading order

```text
README.md
→ QUICKSTART.md
→ PUBLIC_ENGINEERING_STATE.md
→ AX-PUB-ARCH-001
→ AX-PUB-SPEC-002 / 003 / 004
→ AX-PUB-DEV-007 / 008 / 009
→ AX-PUB-CI-008 / 009 / 010
→ AX-PUB-API-001 / AX-PUB-CI-012
→ AX-PUB-SUP-001 / AX-PUB-SEC-001 / AX-PUB-CI-013
→ AX-PUB-EVAL-PACK-001 / AX-PUB-CI-014 / AX-PUB-CI-015
→ AX-PUB-RELPACK-001 / AX-PUB-CI-016
→ AX-PUB-CI-011 / RELEASE_CONTROL_AUDIT.md
→ PRODUCTION_SDK_DEFINITION_OF_DONE.md
→ RELEASE_CONTROL_PLANE.md
→ LIMITATIONS_AND_UNSUPPORTED_USES.md
```

---

## Claim boundary

```text
PUBLIC ENGINEERING ≠ PRODUCT IMPLEMENTATION
REFERENCE CODE ≠ PRODUCTION CODE
CI PASS ≠ EXTERNAL CERTIFICATION
INSTALLABLE CANDIDATE ≠ SUPPORTED SDK
VALIDATED API CONTRACT CANDIDATE ≠ STABLE 1.0 GUARANTEE
VALIDATED SUPPORT CONTRACT ≠ SUPPORT COMMITMENT ACTIVATED
VALIDATED SECURITY CONTRACT ≠ SECURITY OPERATIONS READY
TARGET DEPRECATION WINDOW ≠ CURRENT SUPPORT PROMISE
EVALUATOR HANDOFF CI PASS ≠ HUMAN EXTERNAL EVALUATION
RELEASE READINESS AGGREGATION PASS ≠ RELEASE READINESS
READY FOR DEV-GATE-05D AUTHORITY REVIEW ≠ DEV-GATE-05D AUTHORITY
LIVE RELEASE-CONTROL AUDIT ≠ RELEASE-CONTROL READY
LOCAL INDEX PASS ≠ EXTERNAL REGISTRY VALIDATION
TARGET LICENCE ≠ LICENCE GRANT
SDK PUBLICATION NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
