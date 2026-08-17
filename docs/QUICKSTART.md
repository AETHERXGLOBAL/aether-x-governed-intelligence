# AETHER X Governed Intelligence — Public Quickstart

`PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This quickstart is for engineers, reviewers, researchers and institutional evaluators who want to understand or exercise the public AETHER X governed-intelligence artifacts without inferring product implementation.

## 1. Start With the Right Path

There are currently two public technical paths.

### Evidence / Authority / Verification

Use this path when you want to inspect how a governed workflow separates evidence, decisions, bounded authority, execution and verification.

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

Use this path when you want to inspect temporal integrity, provenance, revision history, lineage and no-future-leakage controls.

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

For the system-level context, begin with [`AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`](../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md).

## 2. Clone the Repository

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
```

The published reference validators use the Python standard library only. Python 3.10+ is recommended.

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

Run the unit tests:

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

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

## 5. Understand Schema vs. Semantic Validation

The JSON Schemas and executable validators serve different purposes.

```text
JSON SCHEMA
structure · types · required fields · selected enums · timestamp formats
        ↓
REFERENCE VALIDATOR
cross-record references · scope · time relationships · lineage · revision semantics
```

A conforming JSON structure can still violate a semantic rule. Conversely, these public validators do not represent complete production validation or security enforcement.

If you use an external JSON Schema implementation, use one that supports **Draft 2020-12**. No third-party schema-validation dependency is bundled with this repository.

## 6. What PASS Means

A public reference validator returning `PASS` means only that the supplied example satisfied the selected deterministic checks implemented by that specific validator version.

It does **not** mean:

- production readiness;
- security approval;
- regulatory compliance;
- product integration;
- authorization by AETHER X;
- scientific validity;
- data completeness or correctness beyond the implemented checks;
- predictive or investment performance;
- adoption inside AETHER X Quantum, AX-OS, AIC or AETHER X Research.

`REFERENCE PASS ≠ PRODUCTION APPROVAL`

## 7. Determine Compatible Artifact Versions

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) as the machine-readable public compatibility index.

The current compatibility and change rules are documented in [`COMPATIBILITY_AND_VERSIONING.md`](./COMPATIBILITY_AND_VERSIONING.md).

For reproducible external review, pin a repository commit SHA. The `main` branch represents the current public engineering state and may advance.

## 8. Public Claim Boundary

This repository publishes reference engineering material. It does not expose or establish proprietary product implementation.

Shared public doctrine does not imply shared runtime, shared data infrastructure, deployment dependency or technical integration across AETHER X initiatives.

`PUBLIC ARTIFACT ≠ PRODUCT IMPLEMENTATION`

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SYSTEM`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**