# AX-PUB-TEST-001 — Governed Intelligence Conformance Test Kit

**Version:** `1.0`  
**Status:** `PUBLIC CONFORMANCE TEST KIT · REPRODUCIBLY VERIFIED · CI WORKFLOW PUBLISHED · CI RUN UNVERIFIED · NON-PRODUCTION`  
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

Each case declares a public baseline example, deterministic mutations, expected `PASS` or `FAIL`, and required finding codes for negative cases.

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

When all declared cases conform, the runner ends with:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
```

## Reproducible Verification Evidence

A fresh isolated execution was performed against byte-identical copies of the current public Git blobs anchored to commit:

```text
e0052b53ceded7a27fa9f77e2d81cdb4c840a9ad
```

The reconstructed files were independently checked with Git blob hashing before execution. The verified public inputs were:

| Public file | Git blob SHA |
|---|---|
| `conformance/AX-PUB-TEST-001/run_conformance.py` | `bcab4e34f020a0c5feb37acb13bfe59ec27681ca` |
| `conformance/AX-PUB-TEST-001/vectors.json` | `579dd9f1fb79080aecbd60e04eb1f70211225b49` |
| `reference-implementations/eav-contract-validator/validator.py` | `10b31f990cdeb0a2285081d4b4a8cc2457564c69` |
| `reference-implementations/point-in-time-knowledge-validator/validator.py` | `f4344dfb70685b490e716e33f8f2fd2da1f0ca50` |
| `reference-implementations/eav-contract-validator/examples/valid_bundle.json` | `1872981d1c0610ff69ffa3942f529cb3e78be002` |
| `reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json` | `e4f721327ed3646b010819a35e41f9a50cd297ab` |
| `tools/check_public_conformance_boundary.py` | `481e10d04adf6c91ca90151950657fcb3808a70b` |
| `.github/workflows/validate-public-conformance.yml` | `9c3338652bd2e735d3144c283ba22889b1c8ed6b` |

Observed execution results:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

This establishes reproducible execution of the published public test kit and its public/private boundary guard for the listed Git blobs. It is deliberately **not** represented as a verified GitHub Actions CI run. The workflow is published, but GitHub CI status remains `UNVERIFIED` until a successful Actions run can be directly inspected.

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

This artifact demonstrates a public conformance-test design and reproducibly verified public runner for the published reference validators. It does not establish behavior, implementation, adoption, maturity, or integration inside AETHER X Quantum, AX-OS, AIC, AETHER X Research, or any other private initiative.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
