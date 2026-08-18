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

`INSTALLABLE CANDIDATE ≠ SUPPORTED SDK`  
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

## 4. Inspect the installable SDK candidate

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

## 5. Understand distribution validation

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

## 6. Machine-readable current state

Canonical moving compatibility/governance index:

```text
AX-PUB-MANIFEST-001 v1.22
AX-PUB-POL-001 v1.6
```

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) for machine-readable artifact relationships and current gate state.

---

## 7. Production SDK target

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

---

## 8. Recommended reading order

```text
README.md
→ QUICKSTART.md
→ PUBLIC_ENGINEERING_STATE.md
→ AX-PUB-ARCH-001
→ AX-PUB-SPEC-002 / 003 / 004
→ AX-PUB-DEV-007 / 008 / 009
→ AX-PUB-CI-008 / 009 / 010
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
LOCAL INDEX PASS ≠ EXTERNAL REGISTRY VALIDATION
TARGET LICENCE ≠ LICENCE GRANT
SDK PUBLICATION NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
