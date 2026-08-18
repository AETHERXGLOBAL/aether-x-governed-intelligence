# AETHER X Governed Intelligence — Python SDK Release Candidate

`DEV-GATE-05B ENGINEERING CANDIDATE · NON-PUBLISHED · NON-PRODUCTION · SDK PUBLICATION NOT AUTHORIZED`

This directory is the installable-package engineering candidate for the bounded AETHER X governed-intelligence validation surface.

It exists to prove that the validated repository-local candidate can become a self-contained Python distribution without private AETHER X dependencies, repository-relative runtime loading, network access, credentials, production authorization or execution capability.

## Candidate identity

```text
Distribution candidate: aetherxglobal-governed-intelligence
Import namespace:      aetherxglobal.governed_intelligence
Namespace model:       PEP 420 implicit company namespace
Version candidate:     0.1.0rc1
Target runtime:        CPython 3.11–3.14
Runtime dependencies:  0 third-party packages
Canonical registry:    PyPI — NOT RESERVED / NOT PUBLISHED
```

The distribution name remains a **candidate** until live registry availability and ownership are explicitly established.

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

The package performs **local validation only**.

It does **not** provide:

- network calls or a remote API client;
- credentials or authentication;
- production authorization;
- tool invocation;
- brokerage, financial or real-world execution;
- private product integration;
- background agents;
- a production service client.

## Namespace architecture

`aetherxglobal` is intentionally an implicit PEP 420 namespace package: there is no top-level `aetherxglobal/__init__.py` in this distribution.

This allows future AETHER X Python distributions to share the company namespace without forcing unrelated SDKs into one monolithic package.

The supported package for this candidate is:

```text
aetherxglobal.governed_intelligence
```

## Source traceability

The three internal validator modules preserve the exact Git blob identities of the current public reference validators:

```text
AX-PUB-REF-001 → 10b31f990cdeb0a2285081d4b4a8cc2457564c69
AX-PUB-REF-002 → f4344dfb70685b490e716e33f8f2fd2da1f0ca50
AX-PUB-REF-003 → 6c8f4d325ef3d3f2041909f8bba7d554ced4366e
```

This preserves semantic traceability while the package facade removes repository-relative runtime loading.

## Packaging model

The candidate uses:

- `pyproject.toml` / PEP 621 metadata;
- PEP 517 build semantics;
- `src/` layout;
- PEP 420 company namespace;
- Hatchling `1.31.0` as the fixed Gate-05B build-backend candidate;
- wheel + sdist output;
- zero runtime third-party dependencies.

Gate-05B CI is required to build the same source twice under a fixed canonical build epoch and prove byte-identical wheel and sdist outputs before package-candidate validation can be accepted.

The exact first-build wheel is then installed and tested on every declared runtime. Rebuilding separately for each Python version is intentionally avoided: the object under test is the same candidate distribution artifact.

## Licence boundary

No software reuse licence is granted by this candidate directory yet.

The closed Gate-05A decision baseline selects **Apache-2.0 as the target SDK licence direction**, but attachment of that licence remains blocked pending explicit IP / copyright clearance over the final distribution inventory.

`TARGET LICENCE ≠ LICENCE GRANTED`

## Publication boundary

This candidate must not be uploaded to TestPyPI or PyPI merely because it can be built or validated.

Before any public SDK publication, the governing Gate-05 process still requires, among other controls:

- Gate-05B direct package-level evidence;
- live package-name availability / ownership confirmation;
- IP/copyright clearance;
- protected repository and release controls;
- protected PyPI publication environment;
- Trusted Publishing configuration;
- independent human external evaluation;
- final release evidence pack;
- explicit Gate-05D release authority.

```text
INSTALLABLE PACKAGE CANDIDATE ≠ SUPPORTED SDK
DETERMINISTIC BUILD ≠ PUBLICATION AUTHORITY
CI ARTIFACT ≠ REGISTRY RELEASE
SDK PUBLICATION NOT AUTHORIZED
```
