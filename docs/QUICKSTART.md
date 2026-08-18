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

The public reference validators, Gate-01 developer-experience runner and current repository-local Gate-02 SDK candidate use the Python standard library only.

The directly verified Gate-01 **public reference developer-experience** matrix is Python 3.10, 3.11, 3.12 and 3.13. This matrix is evidenced by `AX-PUB-CI-004` and does not create a general SDK support commitment.

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

Published reproducibility result for `AX-PUB-TEST-001`:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
```

Agent-authority suite:

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py
```

Expected conformance marker:

```text
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
```

Public-only conformance boundary checker:

```bash
python3 tools/check_public_conformance_boundary.py
```

Expected boundary marker:

```text
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

The two conformance suites and the public-boundary checker are separate controls and are evaluated separately by the Gate-01 developer-experience runner.

Current agent-authority test state: `10 synthetic cases · CI-TESTED`.

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
AX-PUB-MANIFEST-001 v1.14
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

## 11. Developer Adoption Program

The current developer-adoption program is:

- [`AX-PUB-DEV-001 — Developer Adoption & SDK Readiness Program`](./AX-PUB-DEV-001_DEVELOPER_ADOPTION_SDK_READINESS_PROGRAM.md)

Current program state:

```text
PROGRAM: ACTIVE / UNDER DEVELOPMENT
DEV-GATE-00: CLOSED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
CURRENT ENGINEERING OBJECTIVE: DEV-GATE-03 — SUPPLY-CHAIN & RELEASE CANDIDATE
SDK CANDIDATE: ESTABLISHED
PUBLIC SDK: NOT PUBLISHED
PACKAGE IDENTITY: NOT APPROVED
PACKAGE REGISTRY: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT DECIDED
SDK PUBLICATION: NOT AUTHORIZED
```

The program defines a gated path from inspectable public engineering toward a reproducible developer experience, bounded SDK candidate, supply-chain evidence, external evaluation readiness and an eventual separate release decision.

`DEVELOPER ADOPTION PROGRAM ≠ SDK RELEASE`

## 12. Developer Contract Baseline

The established developer-facing contract baseline is:

- [`AX-PUB-DEV-002 — Developer Contract Baseline`](./AX-PUB-DEV-002_DEVELOPER_CONTRACT_BASELINE.md)
- [Machine-readable `AX-PUB-DEV-002.json`](../artifacts/AX-PUB-DEV-002.json)
- [`AX-PUB-CI-003 — DEV-GATE-00 validation evidence`](../evidence/AX-PUB-CI-003_DEVELOPER_CONTRACT_BASELINE_VALIDATION.md)

Current program context:

```text
DEV-GATE-00: CLOSED
PUBLIC DEVELOPER CONTRACT BASELINE: ESTABLISHED
DEV-GATE-01: CLOSED
DEV-GATE-02: CLOSED
CURRENT PROGRAM GATE: DEV-GATE-03 — Supply-Chain & Release Candidate
SDK PUBLICATION: NOT AUTHORIZED
```

The baseline defines the bounded initial developer problem, canonical contract inventory, explicit non-goals, semantic error taxonomy, compatibility baseline, fail-closed rules and public/private dependency boundary.

`DEVELOPER CONTRACT BASELINE ≠ SUPPORTED SDK`  
`CONTRACTED PUBLIC SEMANTICS ≠ PRODUCT IMPLEMENTATION`

## 13. Reproducible Developer Experience

The established Gate-01 public reference experience is:

- [`AX-PUB-DEV-003 — Reproducible Developer Experience`](./AX-PUB-DEV-003_REPRODUCIBLE_DEVELOPER_EXPERIENCE.md)
- [Machine-readable `AX-PUB-DEV-003.json`](../artifacts/AX-PUB-DEV-003.json)
- [`AX-PUB-CI-004 — Gate-01 runtime-matrix validation evidence`](../evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)

Canonical runner:

```bash
python3 tools/check_developer_experience.py
```

Machine-readable report:

```bash
python3 tools/check_developer_experience.py --json
```

Closed-state governance checker:

```bash
python3 tools/check_developer_experience_state.py
```

The runner evaluates **nine declared checks** using the active Python interpreter and public repository files only: three valid public reference examples, three intentionally invalid fixtures, two conformance suites, and the separate public-only conformance-boundary check.

Current Gate-01 state:

```text
DEV-GATE-01: CLOSED
VERIFIED RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13
SUCCESS MARKER: AX_DEVELOPER_EXPERIENCE_PASS
CLOSED-STATE MARKER: AX_DEV_GATE_01_CLOSED_STATE_PASS
```

`AX-PUB-CI-004` records successful dedicated runtime jobs for Python 3.10, 3.11, 3.12 and 3.13, plus successful public-artifact governance validation for the candidate state used for closure.

The verified matrix applies to this bounded public reference experience. It does not establish a supported SDK runtime policy for a future package.

`REPRODUCIBLE DEVELOPER EXPERIENCE ≠ PRODUCTION READINESS`

## 14. SDK Candidate

The established Gate-02 SDK candidate is:

- [`AX-PUB-DEV-004 — SDK Candidate Engineering Baseline`](./AX-PUB-DEV-004_SDK_CANDIDATE_ENGINEERING_BASELINE.md)
- [Machine-readable `AX-PUB-DEV-004.json`](../artifacts/AX-PUB-DEV-004.json)
- [`AX-PUB-CI-005 — Gate-02 SDK candidate validation evidence`](../evidence/AX-PUB-CI-005_SDK_CANDIDATE_VALIDATION.md)
- repository-local candidate module: [`sdk-candidate/python/aetherx_sdk_candidate.py`](../sdk-candidate/python/aetherx_sdk_candidate.py)

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
NEXT GATE: DEV-GATE-03 — Supply-Chain & Release Candidate
```

The candidate surface is deliberately repository-local and non-distributable. It does not contain distribution metadata and does not create a package name, package-registry presence, installation support contract, reuse licence or public SDK release.

Run the candidate unit tests:

```bash
python3 -m unittest discover -s sdk-candidate/python/tests -v
```

Run the candidate example:

```bash
python3 sdk-candidate/python/example.py
```

Run candidate conformance:

```bash
python3 sdk-candidate/python/run_candidate_conformance.py
```

Expected:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

Run the candidate boundary checker:

```bash
python3 tools/check_sdk_candidate_boundary.py
```

Expected:

```text
AX_SDK_CANDIDATE_BOUNDARY_PASS
```

Run the closed-state governance checker:

```bash
python3 tools/check_sdk_candidate_state.py
```

Expected:

```text
AX_DEV_GATE_02_CLOSED_STATE_PASS
```

`AX-PUB-CI-005` directly records successful candidate validation across Python 3.10, 3.11, 3.12 and 3.13 plus successful manifest/governance validation. These are bounded repository CI results, not security certification, production validation or a general support commitment.

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SDK RELEASE`  
`VERIFIED CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`

## 15. SDK Publication Readiness

This repository does **not** currently publish or imply an officially supported SDK.

The controlling gate is:

- [`AX-PUB-GATE-001 — Developer SDK Publication Readiness Gate`](./AX-PUB-GATE-001_DEVELOPER_SDK_PUBLICATION_READINESS.md)

Current disposition:

```text
SDK PUBLICATION NOT AUTHORIZED
```

The gate requires explicit evidence and authority for licence/IP terms, interface compatibility, package identity/distribution, security and credential boundaries, failure semantics, SDK-specific conformance, supply-chain controls, documentation and maintenance/support commitments before any supported SDK publication is represented as approved.

`SDK CANDIDATE ≠ SUPPORTED SDK`  
`PUBLIC ENGINEERING RELEASE ≠ SDK RELEASE`  
`SDK READINESS GATE ≠ SDK COMMITMENT`

## 16. Private-Project Boundary

The public schemas, reference validators, examples, conformance kits, Gate-01 runners/checkers and Gate-02 repository-local candidate surface are self-contained in this public repository.

They do not checkout, import, execute, package, or depend on private AETHER X project repositories. Public examples are synthetic. Private source code, unpublished research, credentials, internal endpoints, proprietary algorithms and confidential implementation architecture remain outside the public disclosure boundary.

## 17. Public Claim Boundary

`PUBLIC ARTIFACT ≠ PRODUCT IMPLEMENTATION`  
`PUBLIC SPECIFICATION ≠ INTERNAL CONTROL IMPLEMENTATION`  
`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`  
`AGENT AUTHORITY REFERENCE ≠ PRODUCTION AUTHORIZATION`  
`PUBLIC SNAPSHOT ≠ PRODUCT RELEASE`  
`PUBLIC ENGINEERING RELEASE ≠ PRODUCT RELEASE`  
`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`SDK CANDIDATE ≠ SDK RELEASE`  
`VERIFIED CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`  
`REPRODUCIBLE DEVELOPER EXPERIENCE ≠ PRODUCTION READINESS`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
