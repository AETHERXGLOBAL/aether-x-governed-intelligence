# AX-PUB-API-001 — Python SDK Public API Contract Candidate

**Artifact ID:** `AX-PUB-API-001`  
**Version:** `0.1`  
**State:** `DEV-GATE-05C API CONTRACT CANDIDATE`  
**Distribution candidate:** `aetherxglobal-governed-intelligence`  
**Version candidate:** `0.1.0rc1`  
**Import namespace:** `aetherxglobal.governed_intelligence`  
**Supported SDK established:** `NO`  
**Stable 1.0 compatibility guarantee established:** `NO`  
**SDK publication:** `NOT AUTHORIZED`

## 1. Purpose

This document converts the current Python release-candidate surface from an implicit collection of importable symbols into an explicit, testable **public API contract candidate**.

The objective is to prevent accidental SDK drift before AETHER X grants a production support commitment.

```text
IMPORTABLE SYMBOL
≠ SUPPORTED PUBLIC API

DECLARED API CONTRACT
+ COMPATIBILITY RULES
+ CROSS-RUNTIME CI
+ RELEASE AUTHORITY
= CANDIDATE PATH TOWARD A SUPPORTED SDK
```

This artifact defines the candidate contract. It does not itself create a stable `1.0` guarantee or production support obligation.

---

## 2. Public namespace

The only declared top-level public exports are:

```python
from aetherxglobal.governed_intelligence import (
    SDK_VERSION,
    __version__,
    ErrorCategory,
    Finding,
    ValidationResult,
    supported_contracts,
    validate,
    validate_eav,
    validate_point_in_time,
    validate_agent_authority,
)
```

Any other package module, symbol or implementation detail is internal unless a later governed API artifact explicitly promotes it.

Names beginning with `_` are internal implementation surfaces.

---

## 3. Candidate callable contract

### `supported_contracts()`

Purpose: return the bounded contract inventory supported by the candidate.

Parameters: none.

Current descriptor keys:

```text
contract_id
contract_version
schema_id
reference_validator_id
```

### `validate(contract_id, payload, *, version="1.0")`

Candidate parameter contract:

```text
contract_id  POSITIONAL_OR_KEYWORD  REQUIRED
payload      POSITIONAL_OR_KEYWORD  REQUIRED
version      KEYWORD_ONLY           DEFAULT "1.0"
```

Returns `ValidationResult`.

Unsupported contract IDs fail explicitly through a `ValidationResult`; they do not silently select another contract.

Unsupported contract versions fail explicitly through a `ValidationResult`; they do not silently coerce to the supported version.

### `validate_eav(payload, *, version="1.0")`

Bound contract:

```text
AX-PUB-SPEC-002 v1.0
```

Returns `ValidationResult`.

### `validate_point_in_time(payload, *, version="1.0")`

Bound contract:

```text
AX-PUB-SPEC-003 v1.0
```

Returns `ValidationResult`.

### `validate_agent_authority(payload, *, version="1.0")`

Bound contract:

```text
AX-PUB-SPEC-004 v1.0
```

Returns `ValidationResult`.

---

## 4. Candidate public result types

### `Finding`

Frozen dataclass fields, in constructor order:

```text
category
source_code
path
message
```

Public method:

```text
as_dict()
```

### `ValidationResult`

Frozen dataclass fields, in constructor order:

```text
contract_id
contract_version
reference_validator_id
valid
findings
sdk_version
```

Public method:

```text
as_dict()
```

The field order is treated as compatibility-sensitive because the exported dataclasses remain directly constructible in Python.

---

## 5. Error-category contract candidate

`ErrorCategory` is a string enum. Current values:

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

Removing an existing value or changing the string represented by an existing value is compatibility-sensitive.

Adding a value remains a reviewed API change because consumers may perform exhaustive handling.

---

## 6. Contract inventory

The candidate is limited to:

| Contract | Version | Schema | Reference validator |
|---|---:|---|---|
| `AX-PUB-SPEC-002` | `1.0` | `AX-PUB-SCHEMA-001` | `AX-PUB-REF-001` |
| `AX-PUB-SPEC-003` | `1.0` | `AX-PUB-SCHEMA-002` | `AX-PUB-REF-002` |
| `AX-PUB-SPEC-004` | `1.0` | `AX-PUB-SCHEMA-003` | `AX-PUB-REF-003` |

Adding support for a new contract is an explicit API/product decision; it is not inferred from the existence of another public specification.

---

## 7. Behavioral invariants

The first SDK product scope is deliberately bounded to offline validation.

The candidate contract requires:

```text
OFFLINE_ONLY
NO_NETWORK_CALLS
NO_CREDENTIAL_SURFACE
NO_TOOL_EXECUTION
NO_PRODUCTION_AUTHORIZATION
NO_BROKERAGE_OR_FINANCIAL_EXECUTION
UNSUPPORTED_CONTRACT_FAILS_EXPLICITLY
UNSUPPORTED_VERSION_FAILS_EXPLICITLY
IDENTICAL INPUT + VERSION → DETERMINISTIC VALIDATION RESULT
```

These invariants are part of the reason the first production SDK scope can be made supportable without implying a production execution platform.

---

## 8. Python compatibility target

Package metadata currently declares:

```text
Requires-Python: >=3.11,<3.15
```

Candidate package validation target:

```text
CPython 3.11
CPython 3.12
CPython 3.13
CPython 3.14
```

The API contract checker must execute across the full declared candidate runtime matrix before this contract is treated as validated.

`CI ON A RUNTIME ≠ PERMANENT SUPPORT COMMITMENT`

---

## 9. Compatibility rules

The following are candidate breaking changes and require explicit versioning/migration treatment before a supported release:

- removing or renaming a declared public export;
- removing or renaming a required callable parameter;
- changing a parameter from positional-or-keyword to an incompatible calling convention;
- changing the current keyword-only `version` behavior incompatibly;
- removing a public dataclass field;
- reordering public dataclass constructor fields;
- removing or changing an existing `ErrorCategory` string value;
- changing existing contract descriptor identifiers;
- changing fail-closed unsupported-contract or unsupported-version behavior;
- adding production side effects to an API currently declared offline-only.

Additive changes still require review because new enum members, new contracts or new public exports can affect downstream exhaustive logic and compatibility expectations.

---

## 10. Pre-1.0 boundary

The current SDK version is:

```text
0.1.0rc1
```

AETHER X has **not** yet established a stable `1.0` semantic-versioning commitment.

The purpose of this contract is to identify and mechanically protect the candidate surface before that commitment is granted.

A later release-authority artifact must explicitly state the compatibility policy that becomes binding for the supported release line.

---

## 11. Machine-readable contract and validation

Canonical machine-readable companion:

```text
artifacts/AX-PUB-API-001.json
```

Fail-closed checker:

```text
tools/check_sdk_public_api_contract.py
```

The checker validates the candidate against the actual package source and metadata, including:

- exact `__all__` inventory;
- package version identity;
- `Requires-Python` identity;
- function parameter names/kinds/defaults;
- dataclass field order and frozen state;
- `ErrorCategory` values;
- supported-contract descriptors;
- declared no-execution/no-network public-surface boundary.

---

## 12. Claim boundary

```text
AX-PUB-API-001 = PUBLIC API CONTRACT CANDIDATE
AX-PUB-API-001 ≠ STABLE 1.0 GUARANTEE
AX-PUB-API-001 ≠ SUPPORTED SDK
AX-PUB-API-001 ≠ PRODUCTION FITNESS CERTIFICATION
AX-PUB-API-001 ≠ SDK PUBLICATION AUTHORITY
SDK PUBLICATION NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
