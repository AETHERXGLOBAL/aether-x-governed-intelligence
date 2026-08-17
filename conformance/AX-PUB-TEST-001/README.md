# AX-PUB-TEST-001 — Governed Intelligence Conformance Test Kit

**Version:** `1.0`  
**Status:** `PUBLIC CONFORMANCE TEST KIT · CI-TESTED · NON-PRODUCTION`  
**Scope:** Public reference artifacts in `AETHERXGLOBAL/aether-x-governed-intelligence`

## Purpose

This test kit provides deterministic, machine-readable conformance vectors for the public AETHER X reference validators.

It is designed to let an external reviewer answer a narrow question:

> Does a specific public reference validator version produce the expected PASS/FAIL behavior for a defined set of public test vectors?

It does **not** inspect, execute, import, or depend on private AETHER X product repositories.

## Current Suites

### EAV — Evidence / Authority / Verification

Covers selected public behaviors including:

- valid bounded authority;
- revoked authority;
- execution after authority expiry;
- principal mismatch;
- action outside the grant;
- resource outside scope;
- verifier-independence failure;
- `VERIFIED` outcome without `PASS` verification.

### PTK — Point-in-Time Knowledge / Provenance

Covers selected public behaviors including:

- valid historical knowledge envelope;
- future source-retrieval leakage;
- future assertion-observation leakage;
- invalid transformation lineage;
- correction without a superseded assertion;
- silent missing value;
- assertion referencing an unknown source.

## Machine-Readable Vectors

The canonical vector set is:

[`vectors.json`](./vectors.json)

Each case declares:

- a public baseline example;
- deterministic mutations;
- expected `PASS` or `FAIL`;
- required finding codes for negative cases.

The vectors contain only synthetic public example data. They do not contain private project data, customer information, credentials, proprietary algorithms, unpublished research, internal endpoints, or internal architecture.

## Run

From the repository root:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
```

Machine-readable report:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py --json
```

A successful run ends with:

```text
AX_PUBLIC_CONFORMANCE_PASS
```

## Interpretation

A conformance case passes when the public validator behavior matches the vector's declared expectation and, for negative cases, the declared required finding codes are present.

`TEST CASE PASS ≠ INPUT APPROVAL`

`CONFORMANCE PASS ≠ PRODUCTION READINESS`

`CONFORMANCE PASS ≠ SECURITY CERTIFICATION`

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`

`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

## Dependency Boundary

This kit depends only on public files in this repository:

```text
AX-PUB-TEST-001
├── AX-PUB-REF-001
│   └── public EAV baseline example
└── AX-PUB-REF-002
    └── public PTK baseline example
```

No private AETHER X repository is required or referenced by path, token, checkout, submodule, package, or runtime dependency.

## Public Claim Boundary

This artifact demonstrates public reference-validator conformance behavior only. It does not establish behavior, implementation, adoption, maturity, or integration inside AETHER X Quantum, AX-OS, AIC, AETHER X Research, or any other private initiative.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
