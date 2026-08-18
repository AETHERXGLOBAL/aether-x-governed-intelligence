# AETHER X Governed Intelligence — Public Quickstart

`PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This quickstart is for engineers, reviewers, researchers and institutional evaluators who want to inspect or exercise the public AETHER X governed-intelligence artifacts without inferring product implementation.

## 1. Choose a Public Technical Path

### Evidence / Authority / Verification

```text
AX-PUB-SPEC-002
→ AX-PUB-SCHEMA-001
→ AX-PUB-REF-001
→ AX-PUB-TEST-001
```

### Point-in-Time Knowledge / Provenance

```text
AX-PUB-SPEC-003
→ AX-PUB-SCHEMA-002
→ AX-PUB-REF-002
→ AX-PUB-TEST-001
```

### Governed Agent Authority / Tool Use

```text
AX-PUB-SPEC-004
→ AX-PUB-SCHEMA-003
→ AX-PUB-REF-003
→ AX-PUB-TEST-002
```

- [`AX-PUB-SPEC-004`](../specifications/AX-PUB-SPEC-004_GOVERNED_AGENT_AUTHORITY_TOOL_USE_STANDARD.md)
- [`AX-PUB-SCHEMA-003`](../schemas/AX-PUB-SCHEMA-003_AGENT_TOOL_USE_AUTHORITY_ENVELOPE.schema.json)
- [`AX-PUB-REF-003`](../reference-implementations/agent-tool-authority-validator/README.md)
- [`AX-PUB-TEST-002`](../conformance/AX-PUB-TEST-002/README.md)

The agent-authority path is a public reference chain only. It does not establish a production agent runtime, authorization plane, credential broker, product SDK, or implementation inside any AETHER X initiative.

For system-level context, start with [`AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`](../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md).

## 2. Clone

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
```

The public reference validators and conformance runners use the Python standard library only. Python 3.10+ is recommended.

## 3. Run the EAV Reference Path

```bash
python3 reference-implementations/eav-contract-validator/validator.py \
  reference-implementations/eav-contract-validator/examples/valid_bundle.json
```

Expected: `AX_EAV_REFERENCE_VALIDATION_PASS`

## 4. Run the Point-in-Time Reference Path

```bash
python3 reference-implementations/point-in-time-knowledge-validator/validator.py \
  reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json
```

Expected: `AX_PTK_REFERENCE_VALIDATION_PASS`

## 5. Run the Agent Authority Reference Path

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Expected: `AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS`

Unit tests:

```bash
python3 -m unittest discover -s reference-implementations/agent-tool-authority-validator/tests -v
```

`AX-PUB-REF-003` is `CI-TESTED` for its declared public reference scope. Direct GitHub Actions evidence is recorded in [`AX-PUB-CI-001`](../evidence/AX-PUB-CI-001_AGENT_AUTHORITY_VNEXT_VALIDATION.md).

`REFERENCE VALIDATOR PASS ≠ PRODUCTION AUTHORIZATION`

## 6. Run Public Conformance

EAV + point-in-time suite:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
```

Published reproducibility evidence for `AX-PUB-TEST-001`:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

Agent-authority suite:

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py
```

Current state: `10 synthetic cases · CI-TESTED`.

The verified GitHub Actions conformance run is recorded in [`AX-PUB-CI-001`](../evidence/AX-PUB-CI-001_AGENT_AUTHORITY_VNEXT_VALIDATION.md).

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`  
`CONFORMANCE PASS ≠ PRODUCTION AUTHORIZATION`  
`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

## 7. Understand the Evidence Layers

```text
SPECIFICATION
        ↓
JSON SCHEMA
        ↓
REFERENCE VALIDATOR
        ↓
CONFORMANCE KIT
        ↓
PUBLIC CI EVIDENCE
        ↓
COMMIT-ANCHORED SNAPSHOT
        ↓
FORMAL PUBLIC ENGINEERING RELEASE
```

The layers have different responsibilities. Schema validity does not guarantee semantic validity. Validator, conformance or CI passes do not establish production fitness, security certification, product adoption, or authorization for consequential action.

## 8. Compatibility & Versions

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) as the machine-readable compatibility index.

Current moving state:

```text
AX-PUB-MANIFEST-001 v1.7
AX-PUB-POL-001 v1.6
```

See [`COMPATIBILITY_AND_VERSIONING.md`](./COMPATIBILITY_AND_VERSIONING.md).

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

## 9. Reproducible Snapshots

Historical public snapshot:

- [`AX-PUB-SNAP-001 — Governed Intelligence Public v1.0`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)
- [Machine-readable `AX-PUB-SNAP-001.json`](../snapshots/AX-PUB-SNAP-001.json)

Current fixed vNext public snapshot:

- [`AX-PUB-SNAP-002 — Governed Intelligence Public vNext`](../snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)
- [Machine-readable `AX-PUB-SNAP-002.json`](../snapshots/AX-PUB-SNAP-002.json)
- [Verified snapshot/manifest closure evidence — `AX-PUB-CI-002`](../evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)

`AX-PUB-SNAP-002` is anchored to a fixed public Git commit and has a successful published snapshot-integrity workflow. The moving `main` branch may advance independently.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 10. Formal Public Engineering Release

The formal public engineering publication is:

```text
Tag: public-engineering-vnext-1.0
Title: AETHER X Governed Intelligence — Public Engineering vNext 1.0
Tag target: 4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6
```

Release publication evidence:

- [`AX-PUB-REL-001 — Public Engineering vNext Release Record`](../evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)

The release tag target packages the published repository state. `AX-PUB-SNAP-002` separately preserves the fixed technical-review anchor and Git-blob inventory.

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

## 11. SDK Publication Readiness

This repository does **not** currently publish or imply an officially supported SDK.

The current gate is:

- [`AX-PUB-GATE-001 — Developer SDK Publication Readiness Gate`](./AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)

Current disposition:

```text
SDK PUBLICATION NOT AUTHORIZED
```

The gate requires explicit evidence and authority for licence/IP terms, interface compatibility, package identity/distribution, security and credential boundaries, failure semantics, SDK-specific conformance, supply-chain controls, documentation and maintenance/support commitments before any supported SDK publication is represented as approved.

`PUBLIC REFERENCE IMPLEMENTATION ≠ SUPPORTED SDK`  
`PUBLIC ENGINEERING RELEASE ≠ SDK RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## 12. Private-Project Boundary

The public schemas, reference validators, examples and conformance kits are self-contained in this public repository.

They do not checkout, import, execute, package, or depend on private AETHER X project repositories. Public examples are synthetic. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside the public disclosure boundary.

## 13. Public Claim Boundary

`PUBLIC ARTIFACT ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC SPECIFICATION ≠ INTERNAL CONTROL IMPLEMENTATION`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`  
`AGENT AUTHORITY REFERENCE ≠ PRODUCTION AUTHORIZATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`PUBLIC REFERENCE IMPLEMENTATION ≠ SUPPORTED SDK`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
