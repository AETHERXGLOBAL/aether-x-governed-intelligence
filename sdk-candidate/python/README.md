# AETHER X Python SDK Candidate Surface

`DEV-GATE-02 CLOSED · SDK CANDIDATE ESTABLISHED · REPOSITORY-LOCAL · NON-DISTRIBUTABLE · NON-PRODUCTION`

This directory contains the bounded Python developer-surface candidate established under `DEV-GATE-02 — SDK Candidate`.

It remains intentionally **not** a package release:

- no `pyproject.toml`;
- no `setup.py` / `setup.cfg`;
- no approved package-registry identity;
- no installation support contract;
- no reuse licence granted by this directory;
- no remote service or credential dependency;
- no production execution or authorization API.

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`  
`DEV-GATE-02 CLOSED ≠ SDK RELEASE`

## Candidate Surface

The candidate exposes only validation-oriented interfaces over the three declared public contract paths:

```python
validate_eav(payload, version="1.0")
validate_point_in_time(payload, version="1.0")
validate_agent_authority(payload, version="1.0")
validate(contract_id, payload, version="1.0")
supported_contracts()
```

The candidate returns `ValidationResult` and `CandidateFinding` records. It does not execute real-world actions.

The public contract inventory remains:

```text
AX-PUB-SPEC-002 v1.0 → AX-PUB-REF-001
AX-PUB-SPEC-003 v1.0 → AX-PUB-REF-002
AX-PUB-SPEC-004 v1.0 → AX-PUB-REF-003
```

The candidate facade preserves the original reference-validator finding code and maps it to a developer-facing `AXDEV-*` semantic category. Unmapped reference findings fail to the conservative `AXDEV-CONTRACT-INVALID` category rather than inventing a more specific semantic interpretation.

## Verified Candidate Runtime Matrix

`AX-PUB-CI-005` directly records successful candidate validation across:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

This matrix applies to the bounded repository-local candidate. It is not a general support policy for a future published package.

## Run the Candidate Example

From the repository root:

```bash
python3 sdk-candidate/python/example.py
```

## Run Unit Tests

```bash
python3 -m unittest discover -s sdk-candidate/python/tests -v
```

## Run Candidate Conformance

```bash
python3 sdk-candidate/python/run_candidate_conformance.py
```

Expected candidate marker after successful execution:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

## Run Candidate Boundary Check

```bash
python3 tools/check_sdk_candidate_boundary.py
```

Expected:

```text
AX_SDK_CANDIDATE_BOUNDARY_PASS
```

## Current Authority Boundary

The governing publication gate remains `AX-PUB-GATE-001`:

```text
SDK PUBLICATION NOT AUTHORIZED
```

No package name, registry publication, reuse licence, support commitment or production deployment should be inferred or performed from this candidate directory.

The next developer-program gate is:

```text
DEV-GATE-03 — Supply-Chain & Release Candidate
```
