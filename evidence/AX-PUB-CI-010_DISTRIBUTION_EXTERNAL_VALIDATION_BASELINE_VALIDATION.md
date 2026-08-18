# AX-PUB-CI-010 — Distribution & External Validation Baseline Validation Evidence

**Artifact ID:** `AX-PUB-CI-010`  
**Version:** `1.0`  
**Scope:** `DEV-GATE-05C — Distribution & External Validation`  
**Evidence state:** `DIRECT CI VALIDATION OF LOCAL-INDEX ENGINEERING BASELINE · DEV-GATE-05C REMAINS ACTIVE`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`

## 1. Purpose

This record captures direct GitHub Actions evidence for the bounded `DEV-GATE-05C` engineering baseline established by `AX-PUB-DEV-009`.

The validated capability is intentionally limited to a **loopback-only Python Simple Repository API-compatible test surface** using the exact Gate-05B package candidate.

```text
LOCAL INDEX VALIDATION
≠ TESTPYPI VALIDATION
≠ PYPI VALIDATION
≠ REGISTRY OWNERSHIP
≠ SOFTWARE LICENCE GRANT
≠ HUMAN EXTERNAL EVALUATION
≠ SUPPORTED SDK
≠ SDK PUBLICATION AUTHORITY
```

## 2. Reviewed Baseline

Pull request:

```text
#41 — DEV-GATE-05C: establish distribution and external-validation baseline
```

Reviewed source head:

```text
779bfe5813c7794ba04ca1f2efe35ec69155d88c
```

GitHub pull-request synthetic merge commit used by the validation run:

```text
d1d920b5f4463f3410a5bef68f30065c5c561661
```

The baseline was subsequently merged to `main` as:

```text
9398e8921124f1ffb2b289bcf7df5655123d1837
```

The merge does not itself close `DEV-GATE-05C`.

## 3. Primary Gate-05C Workflow Evidence

```text
Workflow: Validate SDK Distribution & External Validation Baseline
Run ID: 32177559732
Run number: 3
Job ID: 95842861606
Conclusion: SUCCESS
```

The successful job was:

```text
Local index distribution / CPython 3.11-3.14
```

The job directly exercised CPython:

```text
3.11
3.12
3.13
3.14
```

and completed the full Gate-05C engineering validation path successfully.

## 4. Validated Distribution Mechanism

The workflow validated an install path with the following bounded contract:

```text
INDEX SURFACE: Python Simple Repository API-compatible test surface
NETWORK BOUNDARY: 127.0.0.1 / loopback only
INSTALL METHOD: pip index discovery
DEPENDENCY MODE: --no-deps
EXTERNAL REGISTRY USED: NO
EXTERNAL REGISTRY WRITE PERFORMED: NO
SDK PUBLICATION AUTHORIZED: NO
```

For each declared runtime, the exact candidate was discovered through the local index, installed into a clean environment and verified outside the repository source path.

The installed package identified:

```text
Distribution: aetherxglobal-governed-intelligence
Version: 0.1.0rc1
Import namespace: aetherxglobal.governed_intelligence
```

and exposed the declared public contract identifiers:

```text
AX-PUB-SPEC-002
AX-PUB-SPEC-003
AX-PUB-SPEC-004
```

## 5. Exact Candidate Identity

### Wheel

```text
Filename:
aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl

SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac
```

### Source distribution

```text
Filename:
aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz

SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99
```

These are the same Gate-05B candidate identities recorded by `AX-PUB-CI-009`.

## 6. Runtime Reports

The retained CI artifact contains four `AX-PUB-DIST-REPORT-001` reports:

```text
python-3.11.json — PASS
python-3.12.json — PASS
python-3.13.json — PASS
python-3.14.json — PASS
```

Each report records:

- `validation_type = LOCAL_SIMPLE_INDEX_SIMULATION`;
- `external_registry_validation = false`;
- `external_registry_write_performed = false`;
- `sdk_publication_authorized = false`;
- the exact wheel and sdist SHA-256 identities above;
- the expected installed SDK version `0.1.0rc1`.

## 7. GitHub Actions Artifact Evidence

The successful workflow retained the local-index validation reports as a short-lived GitHub Actions artifact:

```text
Artifact ID:      9339582392
Artifact name:    ax-pub-dev-009-local-index-d1d920b5f4463f3410a5bef68f30065c5c561661
Artifact size:    4032 bytes
Retention:        7 days
Expires:          2026-08-25
Artifact digest:  sha256:cc5a56aff2c0052169bc8dd4b4816039cad66838c5a4d009e79378df52000f35
```

The artifact contains:

```text
python-3.11.json
python-3.12.json
python-3.13.json
python-3.14.json
```

`CI ARTIFACT ≠ PUBLIC PACKAGE RELEASE`

## 8. Inherited Governance Validation

The same reviewed PR head also completed successfully under all inherited public engineering workflows:

```text
Validate SDK Candidate                              SUCCESS
Validate External Evaluation Readiness              SUCCESS
Validate Public Artifact Manifest                   SUCCESS
Validate SDK Release Decision Baseline              SUCCESS
Validate SDK Installable Package Closure            SUCCESS
Validate Developer Experience                       SUCCESS
Validate Supply-Chain Release Candidate              SUCCESS
Validate SDK Distribution & External Validation     SUCCESS
```

This establishes that the Gate-05C baseline did not bypass or invalidate the closed Gate-00 through Gate-05B engineering chain.

## 9. What This Evidence Establishes

This evidence supports only the bounded statement that:

- the exact Gate-05B package candidate can be served through a local Simple Repository API-compatible index;
- pip can discover and install that exact candidate through index semantics rather than a direct wheel path;
- the installed candidate passes the declared verification on CPython 3.11, 3.12, 3.13 and 3.14;
- local-index distribution validation is reproducibly established for the reviewed engineering baseline;
- the external human-evaluation record contract remains machine-enforceable without allowing CI or a template to impersonate a human evaluator.

## 10. What Was Not Established

This evidence does **not** establish:

- TestPyPI validation;
- PyPI validation;
- TestPyPI or PyPI project ownership;
- package-name reservation;
- package-name availability at a later action time;
- a public software reuse licence;
- IP/copyright clearance;
- a protected publishing environment;
- PyPI Trusted Publishing configuration;
- sufficient branch/ruleset release protection;
- human external technical evaluation;
- external developer adoption;
- a supported SDK;
- a support SLA;
- `DEV-GATE-05C` closure;
- `DEV-GATE-05D` authority;
- SDK publication.

## 11. Current Gate State After Evidence Capture

```text
DEV-GATE-05: ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: CLOSED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED

LOCAL INDEX DISTRIBUTION VALIDATION: VERIFIED / LOCAL ONLY
EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED
HUMAN EXTERNAL EVALUATION: NOT ESTABLISHED
EXTERNAL ADOPTION: NOT ESTABLISHED
REGISTRY OWNERSHIP: NOT ESTABLISHED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

`AX-PUB-CI-010` records local engineering evidence only. It does not close `DEV-GATE-05C` and does not authorize an external registry write.

---

`LOCAL INDEX PASS ≠ TESTPYPI PASS`  
`HUMAN EVALUATION ≠ CI`  
`DEV-GATE-05C ENGINEERING ≠ DEV-GATE-05D RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
