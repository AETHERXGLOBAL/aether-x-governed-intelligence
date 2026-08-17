# AX-PUB-TEST-002 — Agent Authority Conformance Test Kit

**Version:** `1.0`  
**Status:** `PUBLIC CONFORMANCE TEST KIT · CI WORKFLOW PUBLISHED · VALIDATION PENDING · NON-PRODUCTION`  
**Scope:** `AX-PUB-REF-003` public agent/tool-use authority behavior

## Purpose

This kit provides deterministic synthetic conformance vectors for the public `AX-PUB-REF-003` reference validator.

It answers a narrow public question:

> Does the published reference validator produce the declared PASS/FAIL behavior for selected agent/tool-use authority cases?

It does not inspect, import, execute, or depend on private AETHER X repositories.

## Current Cases

The current public suite contains `10` synthetic cases covering valid bounded authority, revocation, principal/tool/action/resource mismatch, grant expiry, parameter scope, environment scope, and grant-to-context parameter narrowing.

The canonical vector set is [`vectors.json`](./vectors.json).

## Run

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py
```

Machine-readable report:

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py --json
```

The suite is designed to end with:

```text
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
```

The public dependency-boundary checker is designed to end with:

```text
AX_AGENT_AUTHORITY_PUBLIC_BOUNDARY_PASS
```

A GitHub Actions workflow is published at `.github/workflows/validate-agent-authority-conformance.yml`. Until a successful workflow run against the published repository state is directly verified, this artifact remains `VALIDATION PENDING`.

## Dependency Boundary

```text
AX-PUB-TEST-002
        ↓
AX-PUB-REF-003
        ↓
AX-PUB-SCHEMA-003
        ↓
AX-PUB-SPEC-004
```

All runtime inputs are synthetic public files in this repository.

`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

## Interpretation

`CONFORMANCE PASS ≠ PRODUCTION AUTHORIZATION`

`CONFORMANCE PASS ≠ SECURITY CERTIFICATION`

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
