# AETHER X Governed Intelligence — Public Quickstart

`PUBLIC ENGINEERING GUIDE · NON-PRODUCTION`

This quickstart is for engineers, reviewers, researchers and institutional evaluators who want to inspect or exercise the public AETHER X governed-intelligence artifacts without inferring product implementation.

## 1. Choose a Public Technical Path

### Evidence / Authority / Verification

```text
AX-PUB-SPEC-002 → AX-PUB-SCHEMA-001 → AX-PUB-REF-001 → AX-PUB-TEST-001
```

### Point-in-Time Knowledge / Provenance

```text
AX-PUB-SPEC-003 → AX-PUB-SCHEMA-002 → AX-PUB-REF-002 → AX-PUB-TEST-001
```

### Governed Agent Authority / Tool Use

```text
AX-PUB-SPEC-004 → AX-PUB-SCHEMA-003 → AX-PUB-REF-003 → AX-PUB-TEST-002
```

For system-level context, start with [`AX-PUB-ARCH-001 — Governed Intelligence Reference Architecture`](../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md).

`PUBLIC REFERENCE PATH ≠ PRODUCT IMPLEMENTATION`

## 2. Clone

```bash
git clone https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence.git
cd aether-x-governed-intelligence
```

The public reference validators, Gate-01 developer-experience runner and current repository-local Gate-02 SDK candidate use the Python standard library only.

## 3. Run the EAV Reference Path

```bash
python3 reference-implementations/eav-contract-validator/validator.py \
  reference-implementations/eav-contract-validator/examples/valid_bundle.json
```

Expected:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

## 4. Run the Point-in-Time Reference Path

```bash
python3 reference-implementations/point-in-time-knowledge-validator/validator.py \
  reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json
```

Expected:

```text
AX_PTK_REFERENCE_VALIDATION_PASS
```

## 5. Run the Agent Authority Reference Path

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Expected:

```text
AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS
```

`REFERENCE VALIDATOR PASS ≠ PRODUCTION AUTHORIZATION`

## 6. Run Public Conformance

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
python3 conformance/AX-PUB-TEST-002/run_conformance.py
python3 tools/check_public_conformance_boundary.py
```

Published / expected markers for the bounded public paths include:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

`CONFORMANCE PASS ≠ PRODUCT IMPLEMENTATION`  
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

Schema, validator, conformance or CI passes do not establish production fitness, security certification, product adoption or authority for consequential action.

## 8. Compatibility & Versions

Use [`artifacts/AX-PUB-MANIFEST-001.json`](../artifacts/AX-PUB-MANIFEST-001.json) as the machine-readable compatibility index.

Current moving state:

```text
AX-PUB-MANIFEST-001 v1.15
AX-PUB-POL-001 v1.6
```

See [`COMPATIBILITY_AND_VERSIONING.md`](./COMPATIBILITY_AND_VERSIONING.md).

`PUBLIC COMPATIBILITY ≠ PRODUCT INTEGRATION`

## 9. Reproducible Snapshots

Historical snapshot:

- [`AX-PUB-SNAP-001`](../snapshots/AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md)

Current fixed vNext technical-review snapshot:

- [`AX-PUB-SNAP-002`](../snapshots/AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md)
- [`AX-PUB-CI-002`](../evidence/AX-PUB-CI-002_VNEXT_SNAPSHOT_VALIDATION.md)

The moving `main` branch may advance independently of the fixed snapshot.

`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`

## 10. Formal Public Engineering Release

```text
Tag: public-engineering-vnext-1.0
Title: AETHER X Governed Intelligence — Public Engineering vNext 1.0
Tag target: 4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6
```

Evidence:

- [`AX-PUB-REL-001`](../evidence/AX-PUB-REL-001_PUBLIC_ENGINEERING_VNEXT_RELEASE.md)

`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`

## 11. Developer Adoption Program

- [`AX-PUB-DEV-001`](./AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md)

Current program state:

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
DEV-GATE-03: CANDIDATE / UNDER VALIDATION
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-03 — SUPPLY-CHAIN & RELEASE CANDIDATE
SDK CANDIDATE: ESTABLISHED
RELEASE CANDIDATE: NOT YET ESTABLISHED
PUBLIC SDK: NOT PUBLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

`DEVELOPER ADOPTION PROGRAM ≠ SDK RELEASE`

## 12. Developer Contract Baseline

- [`AX-PUB-DEV-002`](./AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md)
- [`AX-PUB-CI-003`](../evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md)

```text
DEV-GATE-00: CLOSED
PUBLIC DEVELOPER CONTRACT BASELINE: ESTABLISHED
```

## 13. Reproducible Developer Experience

- [`AX-PUB-DEV-003`](./AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md)
- [`AX-PUB-CI-004`](../evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)

Canonical runner:

```bash
python3 tools/check_developer_experience.py
python3 tools/check_developer_experience_state.py
```

Current state:

```text
DEV-GATE-01: CLOSED
VERIFIED RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13
```

`VERIFIED REFERENCE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`

## 14. SDK Candidate

- [`AX-PUB-DEV-004`](./AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md)
- [`AX-PUB-CI-005`](../evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md)
- [`sdk-candidate/python/aetherx_sdk_candidate.py`](../sdk-candidate/python/aetherx_sdk_candidate.py)

Run:

```bash
python3 -m unittest discover -s sdk-candidate/python/tests -v
python3 sdk-candidate/python/example.py
python3 sdk-candidate/python/run_candidate_conformance.py
python3 tools/check_sdk_candidate_boundary.py
python3 tools/check_sdk_candidate_state.py
```

Current state:

```text
DEV-GATE-02: CLOSED
SDK CANDIDATE: ESTABLISHED
CANDIDATE VERSION: 0.1.0-candidate
VERIFIED CANDIDATE RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`

## 15. Supply-Chain & Release-Candidate Engineering

Current Gate-03 artifacts:

- [`AX-PUB-DEV-005 — Supply-Chain & Release Candidate`](./AX-PUB-DEV-005_SUPPLY_CHAIN_RELEASE_CANDIDATE.md)
- [`AX-PUB-DEV-005.json`](../artifacts/AX-PUB-DEV-005.json)
- [`AX-PUB-RC-001`](../release-candidate/AX-PUB-RC-001.json)
- [`release-candidate/README.md`](../release-candidate/README.md)

Current state:

```text
DEV-GATE-03: CANDIDATE / UNDER VALIDATION
RELEASE CANDIDATE: NOT YET ESTABLISHED
ENGINEERING BUNDLE: AX-PUB-RC-001.zip
ARTIFACT UPLOAD SCOPE: CI_ONLY
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
AX-PUB-CI-006: NOT YET RECORDED
```

Local deterministic candidate build:

```bash
SOURCE_DATE_EPOCH=315532800 \
python3 tools/build_release_candidate.py --output-dir dist
```

Validate candidate state and built artifact:

```bash
python3 tools/check_supply_chain_release_candidate.py
python3 tools/check_supply_chain_release_candidate.py --dist dist
```

The build creates:

```text
dist/AX-PUB-RC-001.zip
dist/AX-PUB-RC-001.sha256
dist/AX-PUB-RC-001_BUILD_MANIFEST.json
dist/AX-PUB-RC-001.spdx.json
```

The dedicated CI workflow additionally tests byte-identical rebuilds, extracted-bundle unit/conformance execution, GitHub build-provenance attestation, SPDX SBOM attestation and `gh attestation verify`.

`DEV-GATE-03 CANDIDATE ≠ RELEASE-CANDIDATE VALIDATED`  
`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SPDX SBOM ≠ SOFTWARE REUSE LICENCE`

## 16. SDK Publication Readiness

- [`AX-PUB-GATE-001`](./AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)

Current disposition:

```text
SDK PUBLICATION NOT AUTHORIZED
```

The gate still requires explicit licence/IP authority, package identity and distribution, supported compatibility commitments, supply-chain controls, documentation, maintenance/support ownership and release authority before publication can be represented as approved.

## 17. Private-Project Boundary

The public schemas, reference validators, examples, conformance kits, Gate-01 developer experience, Gate-02 SDK candidate and Gate-03 engineering candidate are designed to remain self-contained in this public repository.

They do not require private AETHER X project repositories, private package indexes, private endpoints or private credentials.

## 18. Public Claim Boundary

`PUBLIC ARTIFACT ≠ PRODUCT IMPLEMENTATION`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`DEV-GATE-03 CANDIDATE ≠ RELEASE-CANDIDATE VALIDATED`  
`CI ARTIFACT ≠ PACKAGE PUBLICATION`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SBOM ≠ SOFTWARE REUSE LICENCE`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
