# AX-PUB-DEV-004 — SDK Candidate Engineering Baseline

**Artifact ID:** `AX-PUB-DEV-004`  
**Version:** `1.0`  
**Status:** `DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED · SDK PUBLICATION NOT AUTHORIZED`  
**Program:** `AX-PUB-DEV-001`  
**Builds on:** `AX-PUB-DEV-002`, `AX-PUB-DEV-003`  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-004.json`  
**Closure evidence:** `AX-PUB-CI-005`

## 1. Purpose

DEV-GATE-02 evaluates whether the closed public contract baseline and reproducible developer experience can support a **bounded developer-facing SDK candidate** without prematurely creating package, registry, support, licence or production commitments.

The established candidate preserves the smallest surface that represents the three declared public contract paths:

```text
PUBLIC CONTRACT
→ REPOSITORY-LOCAL PYTHON FACADE
→ EXPLICIT RESULT MODEL
→ AXDEV ERROR CATEGORY
→ REFERENCE FINDING PRESERVED
→ UNIT / CONFORMANCE TEST
→ VERIFIED CANDIDATE RUNTIME MATRIX
```

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`DEV-GATE-02 CLOSED ≠ SDK RELEASE`

## 2. Candidate Packaging Boundary

No package identity or distribution channel is approved by DEV-GATE-02 closure.

The established candidate remains repository-local at:

```text
sdk-candidate/python/aetherx_sdk_candidate.py
```

The technical module name is a repository-local candidate identifier only. It is **not** an approved package-registry name.

The candidate intentionally contains no:

```text
pyproject.toml
setup.py
setup.cfg
registry publication workflow
package signing claim
installation support contract
reuse licence
```

Package/distribution identity remains unresolved under `AX-PUB-GATE-001`.

## 3. Candidate Public Surface

The candidate API is validation-only:

```python
supported_contracts()
validate(contract_id, payload, version="1.0")
validate_eav(payload, version="1.0")
validate_point_in_time(payload, version="1.0")
validate_agent_authority(payload, version="1.0")
```

The candidate data model exposes:

```text
ErrorCategory
CandidateFinding
ValidationResult
```

It exposes no execution, tool invocation, brokerage, credential, authorization-granting, publication or network API.

## 4. Candidate Contract Mapping

| Candidate operation | Contract | Version | Structural/reference path |
|---|---|---:|---|
| `validate_eav` | `AX-PUB-SPEC-002` | `1.0` | `AX-PUB-SCHEMA-001 → AX-PUB-REF-001` |
| `validate_point_in_time` | `AX-PUB-SPEC-003` | `1.0` | `AX-PUB-SCHEMA-002 → AX-PUB-REF-002` |
| `validate_agent_authority` | `AX-PUB-SPEC-004` | `1.0` | `AX-PUB-SCHEMA-003 → AX-PUB-REF-003` |
| `validate` | one of the three declared contracts | `1.0` | dispatches only to registered public reference paths |

An unknown contract is represented as `AXDEV-UNSUPPORTED-OPERATION`.

An unsupported declared contract version is represented as `AXDEV-VERSION-UNSUPPORTED`.

No silent version coercion is permitted.

## 5. Candidate Error Model

DEV-GATE-00 established semantic `AXDEV-*` categories but did not bind them to an SDK surface. DEV-GATE-02 establishes a deterministic candidate mapping while preserving every original reference-validator finding code.

Each `CandidateFinding` contains:

```text
category
source_code
path
message
```

The candidate taxonomy is:

```text
AXDEV-CONTRACT-INVALID
AXDEV-VERSION-UNSUPPORTED
AXDEV-EVIDENCE-INSUFFICIENT
AXDEV-AUTHORITY-UNESTABLISHED
AXDEV-AUTHORITY-INACTIVE
AXDEV-AUTHORITY-SCOPE-VIOLATION
AXDEV-TEMPORAL-CUTOFF-VIOLATION
AXDEV-PROVENANCE-INCOMPLETE
AXDEV-CONFLICT-UNRESOLVED
AXDEV-VERIFICATION-FAILED
AXDEV-VERIFICATION-INCONCLUSIVE
AXDEV-EXECUTION-NOT-VERIFIED
AXDEV-UNSUPPORTED-OPERATION
```

Not every category must be emitted by the current bounded validators. The taxonomy defines the candidate semantic namespace; mapping is asserted only where current public reference findings support it.

Unmapped current reference-validator findings conservatively map to:

```text
AXDEV-CONTRACT-INVALID
```

This fallback prevents invented semantic specificity while retaining the original source finding.

## 6. Current Deterministic Mapping Rules

The candidate maps selected public reference findings as follows:

- missing invocation/grant/authority linkage where authority cannot be established → `AXDEV-AUTHORITY-UNESTABLISHED`;
- expired/revoked/not-yet-valid authority execution conditions → `AXDEV-AUTHORITY-INACTIVE`;
- principal/action/tool/resource/parameter/invocation-limit violations → `AXDEV-AUTHORITY-SCOPE-VIOLATION`;
- point-in-time future-data/cutoff violations → `AXDEV-TEMPORAL-CUTOFF-VIOLATION`;
- missing/invalid source, supersession or transformation references → `AXDEV-PROVENANCE-INCOMPLETE`;
- an attempted verified outcome without applicable passing verification → `AXDEV-EXECUTION-NOT-VERIFIED`;
- unsupported candidate contract version → `AXDEV-VERSION-UNSUPPORTED`;
- unsupported contract operation → `AXDEV-UNSUPPORTED-OPERATION`;
- all other current public reference findings → `AXDEV-CONTRACT-INVALID`.

This is an SDK-candidate mapping, not a production exception model or wire protocol.

## 7. Result Semantics

`ValidationResult.valid = true` means only that the selected public reference validator returned no findings for the supplied payload under the declared candidate contract version.

It does not mean:

```text
PRODUCT APPROVED
PRODUCTION READY
SECURE
AUTHORIZED TO ACT
REGULATORILY COMPLIANT
DATA QUALITY CERTIFIED
VERIFIED BUSINESS OUTCOME
```

The result preserves:

- contract ID;
- contract version;
- reference validator ID;
- candidate version;
- mapped findings;
- original source finding codes.

## 8. Verified Candidate Compatibility Matrix

Candidate facade version:

```text
0.1.0-candidate
```

This is a repository-local engineering version only. It is not a registry release and does not activate a supported Semantic Versioning commitment.

`AX-PUB-CI-005` directly records successful SDK-candidate CI across:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

This is the verified runtime matrix for the bounded repository-local Gate-02 candidate. It does not create a general SDK runtime-support commitment for any future published package.

## 9. Test & Conformance Surface

Unit tests:

```bash
python3 -m unittest discover -s sdk-candidate/python/tests -v
```

Candidate conformance:

```bash
python3 sdk-candidate/python/run_candidate_conformance.py
```

Expected candidate marker:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

Candidate boundary checker:

```bash
python3 tools/check_sdk_candidate_boundary.py
```

Expected marker:

```text
AX_SDK_CANDIDATE_BOUNDARY_PASS
```

Governance-state checker:

```bash
python3 tools/check_sdk_candidate_state.py
```

Closed-state marker:

```text
AX_DEV_GATE_02_CLOSED_STATE_PASS
```

Direct candidate-validation evidence is recorded by:

```text
AX-PUB-CI-005
Validate SDK Candidate run 32144445255 / #3 — SUCCESS
Validate Public Artifact Manifest run 32144445221 / #125 — SUCCESS
```

## 10. Public / Private Boundary

The SDK candidate remains self-contained within the public repository and uses only declared public reference artifacts and standard-library runtime dependencies for this gate.

It does not require:

- private AETHER X repositories;
- private package indexes;
- private endpoints;
- private credentials;
- private product algorithms;
- unpublished research;
- customer data;
- hidden production schemas.

No private product implementation is implied by the candidate facade.

## 11. DEV-GATE-02 Exit Criteria

The promotion to `SDK CANDIDATE ESTABLISHED` is supported by:

- [x] bounded repository-local candidate implementation exists;
- [x] no package-registry publication metadata is introduced;
- [x] candidate surface maps only to declared public contracts;
- [x] explicit candidate result model exists;
- [x] stable candidate `AXDEV-*` mapping policy is documented;
- [x] unsupported contract/version behavior fails explicitly;
- [x] unit-test suite exists;
- [x] SDK-candidate conformance runner exists;
- [x] public/private candidate boundary checker exists;
- [x] candidate runtime matrix is declared;
- [x] all declared SDK-candidate runtime jobs completed successfully in `AX-PUB-CI-005`;
- [x] candidate conformance was directly observed in CI;
- [x] candidate boundary was directly observed in CI;
- [x] machine-readable candidate state is promoted to established;
- [x] the published closed state is subject to final repository validation before closure is treated as operationally complete.

Current governed state:

```text
DEV-GATE-02 CLOSED
SDK CANDIDATE ESTABLISHED
SDK PUBLICATION NOT AUTHORIZED
```

## 12. Promotion Boundary

DEV-GATE-02 closure establishes only:

```text
BOUNDED SDK CANDIDATE ESTABLISHED
```

It does not establish:

```text
SUPPORTED SDK
PUBLISHED PACKAGE
APPROVED PACKAGE NAME
REGISTRY AVAILABILITY
PUBLIC REUSE LICENCE
PRODUCTION API
SUPPORT SLA
SECURITY CERTIFICATION
PRODUCT INTEGRATION
```

The next gate is:

```text
DEV-GATE-03 — Supply-Chain & Release Candidate
```

`SDK CANDIDATE ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SDK RELEASE`  
`VERIFIED CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
