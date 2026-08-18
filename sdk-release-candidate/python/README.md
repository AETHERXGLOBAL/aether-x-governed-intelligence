# AETHER X Governed Intelligence — Python SDK Release Candidate

`DEV-GATE-05B ENGINEERING CANDIDATE · NON-PUBLISHED · NON-PRODUCTION · SDK PUBLICATION NOT AUTHORIZED`

This directory is the installable-package engineering candidate for the bounded AETHER X governed-intelligence validation surface.

It is designed to prove that the existing repository-local candidate can become a self-contained Python distribution without importing private AETHER X code, depending on repository-relative runtime paths, or introducing network / credential / execution capability.

## Candidate identity

```text
Distribution candidate: aetherxglobal-governed-intelligence
Import namespace:      aetherxglobal.governed_intelligence
Version candidate:     0.1.0rc1
Target runtime:        CPython 3.11–3.14
Runtime dependencies:  0 third-party packages
Canonical registry:    PyPI — NOT RESERVED / NOT PUBLISHED
```

The distribution name remains a **candidate** until live registry availability is checked and package identity is explicitly approved.

## Public surface

```python
from aetherxglobal.governed_intelligence import (
    validate,
    validate_eav,
    validate_point_in_time,
    validate_agent_authority,
    supported_contracts,
)
```

The package performs local validation only.

It does **not** provide:

- network calls;
- credentials or authentication;
- production authorization;
- tool invocation;
- brokerage, financial or real-world execution;
- private product integration;
- background agents;
- a production service client.

## Source traceability

The three internal validator modules in this candidate are staged from the exact Git blob identities of the current public reference validators:

```text
AX-PUB-REF-001 → 10b31f990cdeb0a2285081d4b4a8cc2457564c69
AX-PUB-REF-002 → f4344dfb70685b490e716e33f8f2fd2da1f0ca50
AX-PUB-REF-003 → 6c8f4d325ef3d3f2041909f8bba7d554ced4366e
```

This preserves semantic traceability while the package facade removes repository-relative runtime loading.

## Packaging model

The candidate uses:

- `pyproject.toml` / PEP 621 metadata;
- PEP 517 build isolation;
- `src/` layout;
- Hatchling build backend candidate;
- wheel + sdist output;
- no runtime third-party dependencies.

Build tooling is not a runtime dependency.

## Licence boundary

No software reuse licence is granted by this candidate directory yet.

The Gate-05 decision baseline selects **Apache-2.0 as the target SDK licence direction**, but attachment of that licence remains blocked pending explicit IP / copyright clearance over the final distribution inventory.

`TARGET LICENCE ≠ LICENCE GRANTED`

## Publication boundary

This directory must not be published to PyPI or TestPyPI merely because it can be built.

Before publication, the governing Gate-05 process still requires, among other controls:

- package-level CI evidence on CPython 3.11–3.14;
- exact wheel/sdist inventory and digest evidence;
- IP/copyright clearance;
- live package-name availability / ownership confirmation;
- protected repository and release controls;
- trusted publishing configuration;
- independent human external evaluation;
- explicit release authority.

```text
INSTALLABLE PACKAGE CANDIDATE ≠ SUPPORTED SDK
BUILD PASS ≠ PUBLICATION AUTHORITY
SDK PUBLICATION NOT AUTHORIZED
```
