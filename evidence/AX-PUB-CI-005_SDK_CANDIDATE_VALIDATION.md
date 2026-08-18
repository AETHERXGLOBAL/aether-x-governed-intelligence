# AX-PUB-CI-005 — SDK Candidate Validation Evidence

**Artifact ID:** `AX-PUB-CI-005`  
**Version:** `1.0`  
**Type:** `PUBLIC CI VALIDATION EVIDENCE`  
**Scope:** `DEV-GATE-02 — SDK Candidate`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Status:** `VERIFIED CANDIDATE VALIDATION · NON-PRODUCTION`  
**Governing program:** `AX-PUB-DEV-001`  
**Candidate artifact:** `AX-PUB-DEV-004`  
**Publication gate:** `AX-PUB-GATE-001 — SDK PUBLICATION NOT AUTHORIZED`

## 1. Purpose

This record captures the directly observed GitHub Actions evidence used to determine whether the bounded repository-local DEV-GATE-02 Python surface satisfies the program's SDK-candidate exit requirements.

It does not establish a supported SDK, package publication, production API, security certification, product integration, customer adoption or reuse licence.

## 2. Verified Candidate State

Candidate validation was performed from a verification-only pull request against the public repository.

```text
Validated base commit:
4d4bb5e3bc7c4a104361e2950618badb15d9ff1f

Verified head commit:
74285009eb7ba151291e56490f60e483cc8dba85

Verification pull request:
#14 — ci: reverify DEV-GATE-02 candidate after governance fix

PR disposition:
CLOSED WITHOUT MERGE
```

The pull-request diff contained only a disposable verification trigger in `artifacts/AX-PUB-DEV-004.json`; the executable candidate, tests, governance checkers, manifest and Quickstart were inherited from the validated base state.

## 3. SDK Candidate Workflow

```text
Workflow: Validate SDK Candidate
Run ID: 32144445255
Run number: 3
Conclusion: SUCCESS
```

All declared runtime jobs completed successfully:

| Runtime | Job ID | Result |
|---|---:|---|
| Python 3.10 | `95734690316` | `SUCCESS` |
| Python 3.11 | `95734690342` | `SUCCESS` |
| Python 3.12 | `95734690181` | `SUCCESS` |
| Python 3.13 | `95734690480` | `SUCCESS` |

Each runtime job successfully executed the following controls:

```text
Parse SDK candidate machine-readable state
Compile SDK candidate surfaces
Run SDK candidate unit tests
Run SDK candidate example
Run SDK candidate conformance
Validate SDK candidate public boundary
Validate DEV-GATE-02 candidate state
Re-validate closed DEV-GATE-01 state
Re-validate public artifact governance
```

The candidate conformance contract for the run is:

```text
AX_SDK_CANDIDATE_CONFORMANCE_PASS cases=9 conforming=9
```

The candidate boundary contract is:

```text
AX_SDK_CANDIDATE_BOUNDARY_PASS
```

## 4. Public Artifact Governance Workflow

```text
Workflow: Validate Public Artifact Manifest
Run ID: 32144445221
Run number: 125
Conclusion: SUCCESS
```

The governance job successfully validated:

```text
artifact paths, versions and compatibility
DEV-GATE-00 developer contract baseline
closed DEV-GATE-01 governance state
DEV-GATE-02 candidate state
SDK candidate public/private boundary
public-only conformance boundary
```

## 5. Prior Failed Verification and Correction

An earlier verification attempt (`Validate SDK Candidate` run `32141250617` / #2 and `Validate Public Artifact Manifest` run `32141250528` / #122) failed because the durable DEV-GATE-01 closed-state checker incorrectly required the moving public manifest to remain exactly at version `1.12`.

The SDK candidate unit tests, example, candidate conformance, public-boundary checker and Gate-02 candidate-state checker had already succeeded in that run. The failure was isolated to the stale Gate-01 manifest-version assertion.

The governance defect was corrected by commit:

```text
cefcd026e63a1bd399a2c37a9ecb00993ee0f5d6
```

The Gate-01 checker now validates that the manifest is at least the closure-bearing version while preserving the fixed Gate-01 closure evidence. The subsequent verification recorded in this artifact completed successfully across all declared candidate runtimes and governance controls.

## 6. Exit-Criteria Assessment

The directly observed evidence supports the following DEV-GATE-02 exit conditions:

- bounded repository-local candidate implementation exists;
- no package-registry publication metadata is introduced;
- candidate operations map only to the three declared public contract paths;
- explicit typed candidate result interfaces exist;
- deterministic candidate `AXDEV-*` error mapping exists;
- unsupported contract and version behavior fails explicitly;
- unit tests exist and pass;
- SDK-candidate conformance exists and passes;
- the public/private candidate boundary checker exists and passes;
- the declared candidate runtime matrix is directly validated across Python 3.10–3.13;
- public artifact governance passes with the candidate state present.

This evidence is sufficient to support a governed promotion of `AX-PUB-DEV-004` to:

```text
DEV-GATE-02 CLOSED
SDK CANDIDATE ESTABLISHED
```

The promotion itself is a separate repository-governance state change and must preserve all publication boundaries below.

## 7. Claim Boundary

`SDK CANDIDATE ESTABLISHED ≠ SUPPORTED SDK`  
`SDK CANDIDATE ESTABLISHED ≠ PUBLISHED PACKAGE`  
`VERIFIED PYTHON 3.10–3.13 CANDIDATE MATRIX ≠ GENERAL SDK SUPPORT COMMITMENT`  
`REPOSITORY-LOCAL MODULE ≠ APPROVED PACKAGE IDENTITY`  
`CI PASS ≠ SECURITY CERTIFICATION`  
`CI PASS ≠ PRODUCT IMPLEMENTATION`  
`CI PASS ≠ PRODUCTION READINESS`  
`SDK PUBLICATION NOT AUTHORIZED`

The next developer-program gate after governed DEV-GATE-02 closure is:

```text
DEV-GATE-03 — Supply-Chain & Release Candidate
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
