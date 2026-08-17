# AETHER X Governed Intelligence — Public Quickstart

`PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This quickstart is for engineers, reviewers, researchers and institutional evaluators who want to understand or exercise the public AETHER X governed-intelligence artifacts without inferring product implementation.

## 1. Start With the Right Path

There are currently two public technical paths.

### Evidence / Authority / Verification

```text
AX-PUB-SPEC-002
Evidence, Authority & Verification Contract
        ↓
AX-PUB-SCHEMA-001
Governed EAV Contract Schema
        ↓
AX-PUB-REF-001
EAV Contract Validator
```

Read:

- [`AX-PUB-SPEC-002`](../specifications/AX-PUB-SPEC-002_EVIDENCE_AUTHORITY_VERIFICATION_CONTRACT.md)
- [`AX-PUB-SCHEMA-001`](../schemas/AX-PUB-SCHEMA-001_EAV_CONTRACT.schema.json)
- [`AX-PUB-REF-001`](../reference-implementations/eav-contract-validator/README.md)

### Point-in-Time Knowledge / Provenance

```text
AX-PUB-SPEC-003
Point-in-Time Knowledge & Provenance Standard
        ↓
AX-PUB-SCHEMA-002
Point-in-Time Knowledge Envelope
        ↓
AX-PUB-REF-002
Point-in-Time Knowledge Validator
```

Read:

- [`AX-PUB-SPEC-003`](../specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)
- [`AX-PUB-SCHEMA-002`](../schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json)
- [`AX-PUB-REF-002`](../reference-implementations/point-in-time-knowledge-validator/README.md)

For system-level context, begin with [`AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`](../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md).

## 2. Clone the Repository

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
```

The published reference validators and conformance runner use the Python standard library only. Python 3.10+ is recommended.

## 3. Run the EAV Reference Validator

```bash
cd reference-implementations/eav-contract-validator
python3 validator.py examples/valid_bundle.json
```

Expected result:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

The intentionally invalid example should be rejected:

```bash
python3 validator.py examples/invalid_bundle.json
```

Run unit tests:

```bash
python3 -m unittest discover -s tests -v
```

## 4. Run the Point-in-Time Knowledge Validator

From the repository root:

```bash
cd reference-implementations/point-in-time-knowledge-validator
python3 validator.py examples/valid_envelope.json
```

Expected result:

```text
AX_PTK_REFERENCE_VALIDATION_PASS
```

The intentionally invalid envelope should be rejected:

```bash
python3 validator.py examples/invalid_envelope.json
```

Run unit tests:

```bash
python3 -m unittest discover -s tests -v
```

## 5. Run the Public Conformance Kit

From the repository root:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
```

Machine-readable report:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py --json
```

The current kit defines 15 synthetic cases across EAV and point-in-time/provenance behavior. The runner compares actual validator behavior with declared expected `PASS`/`FAIL` results and required finding codes.

See:

- [`AX-PUB-TEST-001`](../conformance/AX-PUB-TEST-001/README.md)
- [`vectors.json`](../conformance/AX-PUB-TEST-001/vectors.json)

Byte-identical copies of the published public Git blobs have been reproducibly executed with:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

The exact Git blob identities used for that reproducible execution are recorded in the `AX-PUB-TEST-001` documentation. The GitHub Actions workflow is published, but a successful Actions run remains **unclaimed until directly verified**.

`REPRODUCIBLY VERIFIED ≠ GITHUB CI VERIFIED`

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`

`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

## 6. Understand Schema, Semantic Validation and Conformance

```text
JSON SCHEMA
structure · types · required fields · selected enums · timestamp formats
        ↓
REFERENCE VALIDATOR
cross-record references · scope · time relationships · lineage · revision semantics
        ↓
CONFORMANCE KIT
synthetic cases · expected behavior · required finding codes
```

A conforming JSON structure can still violate a semantic rule. A public reference validator pass does not represent complete production validation. A conformance-kit pass demonstrates only that declared public test behavior matches the specific public validator versions under test.

If you use an external JSON Schema implementation, use one that supports **Draft 2020-12**. No third-party schema-validation dependency is bundled with this repository.

## 7. What PASS Means

A public reference validator returning `PASS` means only that the supplied example satisfied the selected deterministic checks implemented by that specific validator version.

It does **not** mean production readiness, security approval, regulatory compliance, product integration, scientific validity, production data quality, predictive or investment performance, or adoption inside AETHER X Quantum, AX-OS, AIC or AETHER X Research.

`REFERENCE PASS ≠ PRODUCTION APPROVAL`

## 8. Determine Compatible Artifact Versions

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) as the machine-readable public compatibility index. The current manifest is `AX-PUB-MANIFEST-001 v1.1`.

The current compatibility and change rules are documented in [`COMPATIBILITY_AND_VERSIONING.md`](./COMPATIBILITY_AND_VERSIONING.md).

## 9. Reproduce the Published v1.0 Snapshot

For a fixed external-review state, use [`AX-PUB-SNAP-001 — Governed Intelligence Public v1.0`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md).

Its immutable Git anchor is:

```text
f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

Check it out directly:

```bash
git checkout f839d4ac0a0b69dcbb682e900f02aad7e24524eb
```

The machine-readable snapshot record is [`snapshots/AX-PUB-SNAP-001.json`](../snapshots/AX-PUB-SNAP-001.json). It records Git blob identities for material files and selected public CI evidence.

The snapshot has its own public integrity workflow. It is **not** a GitHub Release, Git tag or product release.

For other reproducible review points, pin an explicit Git commit SHA. The `main` branch represents the current public engineering state and may advance.

## 10. Private-Project Boundary

The public validators and conformance kit are self-contained within this public repository. They do not checkout, import, execute, package, or depend on private AETHER X project repositories.

No private project source code, unpublished research, credentials, internal endpoints, proprietary algorithms or confidential implementation architecture should be placed into public test vectors.

## 11. Public Claim Boundary

This repository publishes reference engineering material. It does not expose or establish proprietary product implementation.

Shared public doctrine does not imply shared runtime, shared data infrastructure, deployment dependency or technical integration across AETHER X initiatives.

`PUBLIC ARTIFACT ≠ PRODUCT IMPLEMENTATION`

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
