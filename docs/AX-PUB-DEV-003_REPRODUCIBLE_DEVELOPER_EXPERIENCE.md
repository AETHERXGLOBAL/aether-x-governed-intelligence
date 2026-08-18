# AX-PUB-DEV-003 — Reproducible Developer Experience

**Artifact ID:** `AX-PUB-DEV-003`  
**Version:** `1.0`  
**Status:** `PUBLIC DEVELOPER EXPERIENCE · DEV-GATE-01 CLOSED · SDK PUBLICATION NOT AUTHORIZED`  
**Program:** `AX-PUB-DEV-001`  
**Contract baseline:** `AX-PUB-DEV-002`  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-003.json`  
**Closure evidence:** `AX-PUB-CI-004`

## 1. Purpose

DEV-GATE-01 establishes a reproducible public developer experience that can be exercised from a clean public checkout without private AETHER X knowledge, repositories, endpoints, credentials or package infrastructure.

The target is deterministic first-use behavior against the published public contract paths. It is not package installation and it is not an SDK release.

```text
CLEAN CHECKOUT
→ VERIFIED RUNTIME
→ RUN DECLARED EXAMPLES
→ OBSERVE DETERMINISTIC PASS / FAIL
→ RUN CONFORMANCE
→ VERIFY PUBLIC-ONLY BOUNDARY
→ RECORD CI EVIDENCE
```

`DEV-GATE-01 CLOSED ≠ SDK CANDIDATE`  
`REPRODUCIBLE DEVELOPER EXPERIENCE ≠ PRODUCTION READINESS`

## 2. Clean-Environment Definition

For this gate, a clean environment means:

- a fresh checkout of the public repository;
- a runtime from the directly verified Gate-01 matrix;
- no checkout of any private AETHER X repository;
- no private package index;
- no private endpoint;
- no credential or secret required to exercise the public reference path;
- no third-party runtime package required by the declared reference validators or conformance runners;
- execution from repository-controlled public files only.

GitHub-hosted Actions runners were used for reproducible CI validation. This does not make GitHub Actions a production dependency.

## 3. Verified Runtime Matrix

The Gate-01 reference-experience matrix directly validated by `AX-PUB-CI-004` is:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

All four runtime jobs completed successfully in the dedicated `Validate Developer Experience` workflow recorded by `AX-PUB-CI-004`.

This matrix describes the validated **public reference developer experience** for the evidenced repository state. It is not a general future SDK support window, package compatibility commitment, or production-runtime commitment.

No inference should be made about Python versions that were not directly tested by the Gate-01 workflow.

## 4. Canonical Developer Experience Runner

The canonical automated entry point is:

```bash
python3 tools/check_developer_experience.py
```

Machine-readable report:

```bash
python3 tools/check_developer_experience.py --json
```

The runner uses the active interpreter (`sys.executable`) so the same developer experience can be exercised across the runtime matrix.

A successful run emits:

```text
AX_DEVELOPER_EXPERIENCE_PASS
```

The independent closed-state governance checker is:

```bash
python3 tools/check_developer_experience_state.py
```

Its successful marker is:

```text
AX_DEV_GATE_01_CLOSED_STATE_PASS
```

## 5. Nine Declared Checks

Gate-01 evaluates nine independent checks:

1. `EAV_VALID` — valid EAV reference example;
2. `PTK_VALID` — valid point-in-time/provenance reference example;
3. `AGENT_VALID` — valid agent-authority reference example;
4. `EAV_INVALID` — intentionally invalid EAV fixture must fail visibly;
5. `PTK_INVALID` — intentionally invalid point-in-time fixture must fail visibly;
6. `AGENT_INVALID` — intentionally invalid agent-authority fixture must fail visibly;
7. `PUBLIC_CONFORMANCE` — `AX-PUB-TEST-001`;
8. `AGENT_CONFORMANCE` — `AX-PUB-TEST-002`;
9. `PUBLIC_BOUNDARY` — separate public-only conformance-boundary checker.

The conformance runners and public-boundary checker are deliberately separate controls.

## 6. Deterministic Valid-Path Expectations

### EAV reference path

```bash
python3 reference-implementations/eav-contract-validator/validator.py \
  reference-implementations/eav-contract-validator/examples/valid_bundle.json
```

Required marker: `AX_EAV_REFERENCE_VALIDATION_PASS`

### Point-in-Time / Provenance reference path

```bash
python3 reference-implementations/point-in-time-knowledge-validator/validator.py \
  reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json
```

Required marker: `AX_PTK_REFERENCE_VALIDATION_PASS`

### Agent Authority / Tool-Use reference path

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Required marker: `AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS`

## 7. Deterministic Failure-Path Expectations

Each public reference path contains an intentionally invalid fixture.

The Gate-01 runner requires each invalid fixture to:

- return a non-zero process exit code;
- emit machine-readable JSON when invoked with `--json`;
- report `status = FAIL`;
- contain at least one finding;
- never emit the valid-path PASS marker as the result.

This validates fail-visible public reference behavior without prematurely mapping current validator finding codes into future SDK exception classes.

The higher-level semantic developer taxonomy remains governed by `AX-PUB-DEV-002`. SDK-specific error/API mappings belong to DEV-GATE-02.

## 8. Conformance & Public-Boundary Expectations

EAV + point-in-time conformance:

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
```

Required marker:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
```

Agent-authority conformance:

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py
```

Required marker:

```text
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
```

Public-only boundary:

```bash
python3 tools/check_public_conformance_boundary.py
```

Required marker:

```text
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

These are synthetic public reference/conformance checks. Passing them does not establish product implementation, production authorization, production readiness or security certification.

## 9. Documentation / Execution Drift Control

The dedicated Gate-01 workflow validates the same developer paths and deterministic markers described by this artifact and the public Quickstart.

CI is designed to fail when a declared valid example stops passing, an invalid fixture stops failing visibly, a deterministic marker changes without governance updates, a conformance suite no longer reaches its declared outcome, the public-only boundary fails, the closed Gate-00 baseline stops validating, or the closed Gate-01 governance state becomes inconsistent.

Documentation is therefore treated as an executable developer contract surface rather than static marketing copy.

## 10. Dependency Boundary

The validated Gate-01 reference path remains intentionally dependency-minimal:

```text
PUBLIC REPOSITORY CHECKOUT
+
PYTHON STANDARD LIBRARY
=
DECLARED GATE-01 REFERENCE EXPERIENCE
```

No third-party runtime dependency was introduced by DEV-GATE-01.

A future SDK candidate may introduce dependencies only through explicit inventory, compatibility and supply-chain review.

## 11. Closure Evidence

Direct candidate-validation evidence is recorded in:

- [`AX-PUB-CI-004 — Reproducible Developer Experience Validation Evidence`](../evidence/AX-PUB-CI-004_REPRODUCIBLE_DEVELOPER_EXPERIENCE_VALIDATION.md)

`AX-PUB-CI-004` records:

```text
Validate Developer Experience
run ID: 32136562796
run number: 10
conclusion: SUCCESS

Validate Public Artifact Manifest
run ID: 32136562828
run number: 118
conclusion: SUCCESS
```

The directly observed runtime jobs for Python 3.10, 3.11, 3.12 and 3.13 all completed successfully.

An earlier verification attempt exposed a contract error that incorrectly coupled the public-boundary marker to `AX-PUB-TEST-001`. The candidate was not promoted after that failure. The control model was corrected to nine independent checks before the successful validation recorded by `AX-PUB-CI-004`.

## 12. DEV-GATE-01 Closure

The Gate-01 exit criteria are now:

- [x] canonical clean-environment definition;
- [x] candidate runtime matrix declared;
- [x] deterministic valid-path outputs declared;
- [x] deterministic invalid-path behavior declared;
- [x] conformance outcomes declared;
- [x] public-boundary outcome declared separately;
- [x] failure-path interpretation documented;
- [x] canonical developer-experience runner published;
- [x] dedicated clean-environment CI matrix published;
- [x] all declared candidate runtimes completed successfully;
- [x] directly observed CI evidence recorded as `AX-PUB-CI-004`;
- [x] machine-readable Gate-01 state promoted to closed;
- [x] closed-state governance checker published.

The published state is therefore:

```text
DEV-GATE-01 CLOSED
REPRODUCIBLE PUBLIC DEVELOPER EXPERIENCE ESTABLISHED
VERIFIED RUNTIME MATRIX: Python 3.10, 3.11, 3.12, 3.13
SDK PUBLICATION NOT AUTHORIZED
```

## 13. Promotion Boundary

Closing DEV-GATE-01 means only:

```text
REPRODUCIBLE PUBLIC DEVELOPER EXPERIENCE ESTABLISHED
```

It does **not** mean:

```text
SDK CANDIDATE ESTABLISHED
SDK PUBLISHED
PACKAGE PUBLISHED
PRODUCTION API AVAILABLE
EXTERNAL DEVELOPER ADOPTION PROVEN
SUPPORT COMMITMENT ACTIVE
LICENCE GRANTED
```

The next engineering gate is:

```text
DEV-GATE-02 — SDK Candidate
```

`DEV-GATE-01 CLOSED ≠ SDK CANDIDATE`  
`VERIFIED RUNTIME MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`SDK PUBLICATION NOT AUTHORIZED`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
