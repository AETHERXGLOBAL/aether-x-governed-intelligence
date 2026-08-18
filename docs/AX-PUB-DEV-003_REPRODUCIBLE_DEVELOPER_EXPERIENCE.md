# AX-PUB-DEV-003 — Reproducible Developer Experience

**Artifact ID:** `AX-PUB-DEV-003`  
**Version:** `1.0`  
**Status:** `PUBLIC DEVELOPER EXPERIENCE · DEV-GATE-01 CANDIDATE · SDK PUBLICATION NOT AUTHORIZED`  
**Program:** `AX-PUB-DEV-001`  
**Contract baseline:** `AX-PUB-DEV-002`  
**Governing publication gate:** `AX-PUB-GATE-001`  
**Machine-readable companion:** `artifacts/AX-PUB-DEV-003.json`

## 1. Purpose

DEV-GATE-01 converts the established public developer contract baseline into a reproducible developer experience that can be exercised from a clean public checkout without private AETHER X knowledge or dependencies.

The target is not package installation. The target is deterministic first-use behavior against the published contract paths.

```text
CLEAN CHECKOUT
→ KNOWN RUNTIME
→ RUN DECLARED EXAMPLES
→ OBSERVE DETERMINISTIC PASS / FAIL
→ RUN CONFORMANCE
→ VERIFY PUBLIC-ONLY BOUNDARY
→ RECORD CI EVIDENCE
```

`REPRODUCIBLE DEVELOPER EXPERIENCE ≠ SDK CANDIDATE`  
`CLEAN-ENVIRONMENT PASS ≠ PRODUCTION READINESS`

## 2. Clean-Environment Definition

For this gate, a clean environment means:

- a fresh checkout of the public repository;
- a declared Python runtime from the candidate matrix;
- no checkout of any private AETHER X repository;
- no private package index;
- no private endpoint;
- no credential or secret required to exercise the public reference path;
- no package installation required by the declared reference validators or conformance runners;
- execution from repository-controlled public files only.

GitHub-hosted Actions runners are used as the reproducible public CI environment for candidate validation. This does not make GitHub Actions a production dependency.

## 3. Candidate Runtime Matrix

The initial candidate matrix is:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
```

At initial publication these versions are **candidate test runtimes**, not an AETHER X SDK support commitment.

A runtime enters the verified Gate-01 matrix only after the same declared developer-experience workflow completes successfully on that runtime.

No inference should be made about versions not directly tested by the Gate-01 workflow.

## 4. Canonical Developer Experience Runner

The canonical automated entry point is:

```bash
python3 tools/check_developer_experience.py
```

The runner uses the active interpreter (`sys.executable`) so the same developer experience can be exercised across the CI runtime matrix.

The runner validates four categories:

1. valid reference examples;
2. invalid/fail-closed reference examples;
3. public conformance suites;
4. the public/private conformance-boundary check.

## 5. Deterministic Valid-Path Expectations

### EAV reference path

```bash
python3 reference-implementations/eav-contract-validator/validator.py \
  reference-implementations/eav-contract-validator/examples/valid_bundle.json
```

Required exit code: `0`

Required marker:

```text
AX_EAV_REFERENCE_VALIDATION_PASS
```

### Point-in-Time / Provenance reference path

```bash
python3 reference-implementations/point-in-time-knowledge-validator/validator.py \
  reference-implementations/point-in-time-knowledge-validator/examples/valid_envelope.json
```

Required exit code: `0`

Required marker:

```text
AX_PTK_REFERENCE_VALIDATION_PASS
```

### Agent Authority / Tool-Use reference path

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Required exit code: `0`

Required marker:

```text
AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS
```

## 6. Deterministic Failure-Path Expectations

Each public reference path also contains an intentionally invalid fixture.

The Gate-01 runner requires each invalid fixture to:

- return a non-zero process exit code;
- emit machine-readable JSON when invoked with `--json`;
- report `status = FAIL`;
- contain at least one finding;
- never emit the valid-path PASS marker as the result.

This validates fail-visible developer behavior without prematurely mapping existing reference-validator finding codes into future SDK exception classes.

The semantic developer taxonomy remains governed by `AX-PUB-DEV-002`. SDK-specific exception/API mappings belong to DEV-GATE-02.

## 7. Deterministic Conformance & Boundary Expectations

### EAV + Point-in-Time conformance

```bash
python3 conformance/AX-PUB-TEST-001/run_conformance.py
```

Required marker:

```text
AX_PUBLIC_CONFORMANCE_PASS cases=15 conforming=15
```

### Agent-authority conformance

```bash
python3 conformance/AX-PUB-TEST-002/run_conformance.py
```

Required marker:

```text
AX_AGENT_AUTHORITY_CONFORMANCE_PASS cases=10 conforming=10
```

### Public-only conformance boundary

```bash
python3 tools/check_public_conformance_boundary.py
```

Required marker:

```text
AX_PUBLIC_CONFORMANCE_BOUNDARY_PASS
```

The conformance runners and public-boundary checker are deliberately separate controls and are evaluated as separate Gate-01 checks.

These are synthetic public conformance/reference checks. Passing them does not establish production authorization, product implementation or security certification.

## 8. Failure-Path Interpretation

The public reference validators expose implementation-specific finding codes such as `AX-EAV-*`, `AX-PTK-*` and `AX-AGT-*`.

The higher-level developer-contract taxonomy in `AX-PUB-DEV-002` defines stable semantic categories for future developer surfaces, including:

```text
AXDEV-CONTRACT-INVALID
AXDEV-VERSION-UNSUPPORTED
AXDEV-EVIDENCE-INSUFFICIENT
AXDEV-AUTHORITY-UNESTABLISHED
AXDEV-AUTHORITY-INACTIVE
AXDEV-AUTHORITY-SCOPE-VIOLATION
AXDEV-TEMPORAL-CUTOFF-VIOLATION
AXDEV-PROVENANCE-INCOMPLETE
AXDEV-CONFLICT-UNRESOLVED
AXDEV-VERIFICATION-FAILED
AXDEV-VERIFICATION-INCONCLUSIVE
AXDEV-EXECUTION-NOT-VERIFIED
AXDEV-UNSUPPORTED-OPERATION
```

DEV-GATE-01 does not create a normative one-to-one mapping between every reference finding and every future SDK error. That mapping is a DEV-GATE-02 responsibility.

## 9. Documentation / Execution Drift Control

The Gate-01 CI workflow runs the same developer paths and expected markers documented here and in the public Quickstart.

At minimum, CI must fail when:

- a documented valid example stops passing;
- an invalid fixture stops failing visibly;
- a declared deterministic marker changes without governance updates;
- a conformance suite no longer reaches its declared outcome;
- the public-boundary checker no longer passes;
- the Gate-01 machine-readable artifact and documentation diverge;
- the closed Gate-00 baseline no longer validates.

Documentation is therefore treated as an executable developer contract surface, not static marketing copy.

## 10. No-Dependency Baseline

The current public reference developer path is intentionally dependency-minimal:

```text
PUBLIC REPOSITORY CHECKOUT
+
PYTHON STANDARD LIBRARY
=
DECLARED GATE-01 REFERENCE EXPERIENCE
```

No third-party runtime dependency is introduced by DEV-GATE-01.

This is a property of the current public reference experience only. A future SDK candidate may introduce dependencies, but that would require explicit inventory, compatibility and supply-chain review.

## 11. Developer Experience Output

A fully successful Gate-01 runner emits:

```text
AX_DEVELOPER_EXPERIENCE_PASS
```

and a machine-readable summary when `--json` is requested.

The Gate-01 runner currently evaluates **nine declared checks**: three valid examples, three invalid examples, two conformance suites and one public-boundary check.

The summary identifies the Python runtime and the result of each declared check without collecting credentials, private repository data or private environment information.

## 12. DEV-GATE-01 Exit Criteria

DEV-GATE-01 may close only when all of the following are evidenced:

- [x] canonical clean-environment definition;
- [x] candidate runtime matrix declared;
- [x] deterministic valid-path outputs declared;
- [x] deterministic invalid-path behavior declared;
- [x] conformance outcomes declared;
- [x] public-boundary outcome declared separately;
- [x] failure-path interpretation documented;
- [x] canonical developer-experience runner published;
- [x] dedicated clean-environment CI matrix published;
- [ ] all declared candidate runtimes complete successfully;
- [ ] directly observed CI evidence is recorded;
- [ ] machine-readable Gate-01 state is promoted from candidate to closed;
- [ ] final closed-state repository validation succeeds.

Until those remaining items are evidenced, this artifact remains `DEV-GATE-01 CANDIDATE`.

## 13. Promotion Boundary

Closing DEV-GATE-01 will mean only:

```text
REPRODUCIBLE PUBLIC DEVELOPER EXPERIENCE ESTABLISHED
```

It will not mean:

```text
SDK CANDIDATE ESTABLISHED
SDK PUBLISHED
PACKAGE PUBLISHED
PRODUCTION API AVAILABLE
EXTERNAL DEVELOPER ADOPTION PROVEN
SUPPORT COMMITMENT ACTIVE
LICENCE GRANTED
```

The next gate after verified closure is:

```text
DEV-GATE-02 — SDK CANDIDATE
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
