# AX-PUB-CI-011 — Release-Control Live Audit Evidence

**Artifact ID:** `AX-PUB-CI-011`  
**Version:** `1.0`  
**Scope:** `DEV-GATE-05C — Release-Control Readiness / Live GitHub Observation`  
**Evidence state:** `DIRECT READ-ONLY LIVE PLATFORM AUDIT · RELEASE CONTROLS NOT ESTABLISHED`  
**Repository:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Publication disposition:** `SDK PUBLICATION NOT AUTHORIZED`

## 1. Purpose

This record preserves the first reproducible live GitHub release-control audit for the public AETHER X Governed Intelligence SDK productization path.

The audit exists to replace manual or inferred release-control statements with a machine-readable observation of live GitHub state.

It records the release-control blockers that must be resolved before controlled external registry promotion can be considered.

```text
AUDIT SUCCESS
≠ RELEASE-CONTROL READY
≠ TESTPYPI AUTHORITY
≠ PYPI AUTHORITY
≠ SOFTWARE LICENCE GRANT
≠ SUPPORTED SDK
≠ SDK PUBLICATION AUTHORITY
```

## 2. Reviewed Audit Implementation

Pull request:

```text
#45 — Add read-only live release-control audit
```

Reviewed source head:

```text
6f1cd33a2a7f4c3715e51d0b6f8fd18b86b29f98
```

GitHub pull-request synthetic merge commit used by the audit run:

```text
9c71cef3416c58f226995b1756f5464f504583af
```

The audit implementation was subsequently merged to `main` as:

```text
f03749aab06a20788ae2231522311e60a10fbb74
```

## 3. Live State Observed

The audit observed the release-control state of:

```text
Repository: AETHERXGLOBAL/aether-x-governed-intelligence
Branch:     main
Observed main commit:
6b4a067d38ec2f823cadcb7bad51564917cab3ba

Target production environment:
pypi
```

The observed branch commit was the canonical post-productization-contract state established by PR #44.

## 4. Workflow Evidence

```text
Workflow:   Audit Release Control Plane
Run ID:     32191506412
Run number: 1
Job ID:     95886632381
Conclusion: SUCCESS
```

The successful job was:

```text
Read-only GitHub release-control audit
```

The workflow declared only:

```text
contents: read
actions: read
```

and the audit implementation used GitHub REST `GET` operations only.

No branch, ruleset, environment, registry, licence or release mutation was performed.

## 5. Machine-Readable Audit Record

Canonical preserved report:

```text
evidence/AX-PUB-RELEASE-CONTROL-AUDIT-001.json
```

Report identity:

```text
report_format:  AX-PUB-RELEASE-CONTROL-AUDIT-001
report_version: 1.0
audit_mode:     READ_ONLY_GITHUB_API
GitHub API:     2026-03-10
```

The report uses only these explicit observation states:

```text
ESTABLISHED
NOT_ESTABLISHED
UNVERIFIED
NOT_APPLICABLE
```

Unknown or permission-constrained state is never promoted to `ESTABLISHED` by assumption.

## 6. GitHub Actions Artifact Evidence

The audit workflow preserved its original JSON report as a short-lived GitHub Actions artifact:

```text
Artifact ID:      9344354547
Artifact name:    ax-release-control-audit-9c71cef3416c58f226995b1756f5464f504583af
Artifact size:    1097 bytes
Retention:        7 days
Expires:          2026-08-25
Artifact digest:  sha256:1d1ced97bd21f5dea68924700c2e1243fc06c037b951b88f69be80f8ef9ff768
```

The preserved repository JSON is the durable evidence copy; the Actions artifact remains short-lived CI evidence.

## 7. Endpoint Observation Results

The live audit recorded:

```text
Branch endpoint:                    HTTP 200
Branch rules endpoint:              HTTP 200
Repository rulesets endpoint:       HTTP 200
Target pypi environment endpoint:   HTTP 404
Legacy branch-protection endpoint:  HTTP 403
```

Interpretation:

- the branch, branch-rule and ruleset observations completed successfully;
- no `pypi` environment was established at the observed time;
- the legacy branch-protection endpoint could not be authoritatively read by the audit token and was therefore classified `UNVERIFIED` rather than guessed.

## 8. Release-Control Findings

The machine-readable audit established the following GitHub-side state:

```text
MAIN BRANCH PROTECTED:                    NOT_ESTABLISHED
PULL REQUEST REQUIRED:                    NOT_ESTABLISHED
REQUIRED STATUS CHECKS:                   NOT_ESTABLISHED
FORCE-PUSH BLOCKING:                      NOT_ESTABLISHED
DELETION BLOCKING:                        NOT_ESTABLISHED
PYPI ENVIRONMENT EXISTS:                  NOT_ESTABLISHED
PYPI ENVIRONMENT REQUIRED REVIEWERS:      NOT_ESTABLISHED
PYPI ENVIRONMENT BRANCH POLICY:            NOT_ESTABLISHED

ACTIVE BRANCH RULE TYPES:                  NONE
ENABLED REPOSITORY RULESETS:               NONE

GITHUB CONTROLS READY FOR RELEASE:          FALSE
```

The result is intentionally adverse: it proves that the current GitHub release plane is **not yet sufficient for release promotion**.

## 9. External Controls Not Established by This Audit

The read-only GitHub audit does not establish or infer:

```text
PYPI / TESTPYPI REGISTRY OWNERSHIP:  UNVERIFIED
PYPI TRUSTED PUBLISHER:              UNVERIFIED
IP / COPYRIGHT CLEARANCE:            UNVERIFIED
SOFTWARE LICENCE GRANT:              UNVERIFIED
HUMAN EXTERNAL EVALUATION:           UNVERIFIED
FINAL RELEASE AUTHORITY:             NOT_AUTHORIZED
```

These require separate authoritative evidence and, where applicable, separate explicit authority.

## 10. What This Evidence Establishes

`AX-PUB-CI-011` establishes only that:

- a read-only live release-control auditor exists and executed successfully;
- the audit generated a machine-readable report from live GitHub state;
- the observed GitHub release controls were not sufficient for release promotion;
- the absence of branch/ruleset/environment controls is now a reproducible engineering blocker rather than an informal observation;
- the audit can be repeated after platform-control changes to produce before/after evidence.

## 11. What This Evidence Does Not Establish

This evidence does **not** establish:

- branch protection or rulesets have been configured;
- required status checks are enforced;
- a protected `pypi` environment exists;
- TestPyPI or PyPI ownership;
- Trusted Publishing configuration;
- TestPyPI or PyPI validation;
- a software reuse licence;
- IP/copyright clearance;
- human external evaluation;
- external adoption;
- a supported SDK;
- `DEV-GATE-05C` closure;
- `DEV-GATE-05D` authority;
- SDK publication.

## 12. Required Next Evidence

The next release-control evidence should be a second live audit after authorized GitHub platform controls are configured.

A successful promotion-ready GitHub audit must show all mandatory GitHub controls as `ESTABLISHED`, including at minimum:

```text
main protection / applicable ruleset
pull-request requirement
required release status checks
force-push blocking
branch deletion blocking
protected pypi environment
required environment review / approval boundary
production environment branch/tag restriction
```

The second audit must preserve the exact live platform state and be compared against this baseline.

## 13. Current Gate State

```text
DEV-GATE-05:  ACTIVE
DEV-GATE-05A: CLOSED
DEV-GATE-05B: CLOSED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED

LIVE GITHUB RELEASE-CONTROL AUDIT: ESTABLISHED
GITHUB RELEASE-CONTROL READINESS: NOT ESTABLISHED
EXTERNAL REGISTRY WRITE: NOT AUTHORIZED
PUBLIC SDK LICENCE: NOT GRANTED
SUPPORTED SDK: NOT ESTABLISHED
PRODUCTION SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

---

`AX-PUB-CI-011 ≠ RELEASE AUTHORITY`  
`AUDIT PASS ≠ CONTROL READINESS`  
`CONTROL READINESS ≠ PYPI PUBLICATION`  
`SDK PUBLICATION NOT AUTHORIZED`
