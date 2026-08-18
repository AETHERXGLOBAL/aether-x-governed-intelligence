# AX-PUB-CI-012 — SDK Public API Contract Validation Evidence

**Artifact ID:** `AX-PUB-CI-012`  
**Version:** `1.0`  
**Scope:** `AX-PUB-API-001 — Python SDK Public API Contract Candidate`  
**Evidence state:** `DIRECT CI VALIDATION ACROSS CPYTHON 3.11–3.14`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**SDK publication:** `NOT AUTHORIZED`

## 1. Purpose

This record captures direct GitHub Actions evidence that the declared `AX-PUB-API-001` machine-readable public API contract candidate matched the actual Python SDK release-candidate surface across every declared package runtime at the reviewed source state.

The validation is intentionally pre-support and pre-publication.

```text
API CONTRACT PASS
≠ STABLE 1.0 GUARANTEE
≠ SUPPORTED SDK
≠ PRODUCTION FITNESS CERTIFICATION
≠ SDK PUBLICATION AUTHORITY
```

## 2. Reviewed Candidate

Pull request:

```text
#47 — SDK productization: establish public API contract candidate
```

Reviewed source head:

```text
47a5a5407db950bd9cc8ccdce822e53dc18fc8eb
```

GitHub pull-request synthetic merge commit used by validation:

```text
2a09e749c0969d053f574a95775f90b5169146c2
```

The candidate was subsequently merged to `main` as:

```text
aba4f31bbd33ed8669a0adec63eaa0c41bf932cd
```

## 3. Primary Workflow Evidence

```text
Workflow:   Validate SDK Public API Contract
Run ID:     32192207745
Run number: 1
Conclusion: SUCCESS
```

All four declared runtime jobs completed successfully:

```text
CPython 3.11 — Job ID 95888767182 — SUCCESS
CPython 3.12 — Job ID 95888767192 — SUCCESS
CPython 3.13 — Job ID 95888767103 — SUCCESS
CPython 3.14 — Job ID 95888767227 — SUCCESS
```

The same reviewed head also passed:

```text
Validate Public Artifact Manifest
Run ID: 32192207723
Conclusion: SUCCESS
```

## 4. Contract Surface Validated

The CI validated the actual imported package against:

```text
artifacts/AX-PUB-API-001.json
```

Declared distribution identity:

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Import:       aetherxglobal.governed_intelligence
Requires-Python: >=3.11,<3.15
Runtime dependencies: none
```

Exact top-level candidate exports validated:

```text
SDK_VERSION
__version__
ErrorCategory
Finding
ValidationResult
supported_contracts
validate
validate_eav
validate_point_in_time
validate_agent_authority
```

## 5. Callable Compatibility Checks

For every declared public callable, the checker compared the actual Python signature structure to the machine-readable candidate contract.

Validated properties included:

- exact parameter names;
- positional-or-keyword versus keyword-only calling convention;
- required versus optional status;
- `version="1.0"` default semantics where declared;
- presence of every declared callable;
- absence of accidental replacement by a non-callable object.

The candidate validated callable surface includes:

```text
supported_contracts()
validate(contract_id, payload, *, version="1.0")
validate_eav(payload, *, version="1.0")
validate_point_in_time(payload, *, version="1.0")
validate_agent_authority(payload, *, version="1.0")
```

## 6. Public Type Compatibility Checks

The checker validated the exported result types directly from the package.

### `Finding`

```text
frozen dataclass: YES
field order:
category
source_code
path
message
public method: as_dict
```

### `ValidationResult`

```text
frozen dataclass: YES
field order:
contract_id
contract_version
reference_validator_id
valid
findings
sdk_version
public method: as_dict
```

Field order is compatibility-sensitive because the exported dataclasses remain directly constructible.

## 7. Error Taxonomy Validation

The exact `ErrorCategory` string-enum inventory was validated against `AX-PUB-API-001`, including all declared `AXDEV-*` values.

The checker also verified that every enum value remains a string.

This does not freeze the enum under a stable `1.0` commitment; it establishes the exact reviewed candidate state.

## 8. Contract Inventory Validation

The actual result of `supported_contracts()` matched the machine-readable contract exactly:

```text
AX-PUB-SPEC-002 v1.0 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001
AX-PUB-SPEC-003 v1.0 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002
AX-PUB-SPEC-004 v1.0 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003
```

No additional contract was silently exposed.

## 9. Fail-Closed Behavior Checks

The contract checker directly exercised unsupported behavior.

Unsupported contract:

```text
valid = false
category = AXDEV-UNSUPPORTED-OPERATION
source code = AX-SDK-RC-CONTRACT-UNSUPPORTED
```

Unsupported version:

```text
valid = false
category = AXDEV-VERSION-UNSUPPORTED
source code = AX-SDK-RC-VERSION-UNSUPPORTED
```

Identical unsupported input/version evaluation was also checked for deterministic result equality.

## 10. Public-Surface Execution Boundary

The checker verified that the declared top-level public export inventory did not introduce the candidate-forbidden execution/network capability names used by the bounded product contract.

The SDK remains an **offline validation candidate**.

This validation does not establish that every possible implementation defect or security property has been exhaustively proven.

## 11. Installed-Candidate Regression Evidence

After the API-contract checker passed, the workflow re-ran the existing installed-candidate unit-test suite on each runtime:

```text
CPython 3.11 — PASS
CPython 3.12 — PASS
CPython 3.13 — PASS
CPython 3.14 — PASS
```

This ensures that API-shape validation did not replace behavioral candidate regression testing.

## 12. What This Evidence Establishes

`AX-PUB-CI-012` establishes that, for reviewed head `47a5a540...`:

- the SDK candidate had an explicit machine-readable public API contract;
- the actual import surface matched that contract;
- callable parameter semantics matched the contract;
- exported dataclass shape/order matched the contract;
- the error-category inventory matched the contract;
- the supported-contract inventory matched the contract;
- unsupported contract/version behavior remained explicitly fail-closed;
- the same API contract validated across CPython 3.11–3.14;
- the candidate unit tests passed across the same runtime matrix.

## 13. What This Evidence Does Not Establish

This evidence does **not** establish:

- a stable `1.0` API guarantee;
- general semantic-versioning support commitment;
- PyPI/TestPyPI registry ownership;
- public SDK licence grant;
- production security certification;
- external human evaluation;
- external adoption;
- a supported SDK;
- production SDK status;
- `DEV-GATE-05C` closure;
- `DEV-GATE-05D` authority;
- SDK publication.

## 14. Current Disposition

```text
AX-PUB-API-001: VALIDATED CANDIDATE CONTRACT
VALIDATED RUNTIME MATRIX: CPYTHON 3.11–3.14
STABLE 1.0 GUARANTEE: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
PRODUCTION SDK: NOT ESTABLISHED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

---

`API CONTRACT VALIDATED ≠ API SUPPORT COMMITMENT`  
`API SUPPORT COMMITMENT ≠ PRODUCTION FITNESS CERTIFICATION`  
`SDK PUBLICATION NOT AUTHORIZED`
