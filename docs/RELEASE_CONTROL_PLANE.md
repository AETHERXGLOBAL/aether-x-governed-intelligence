# AETHER X Governed Intelligence — Release Control Plane

**Document state:** `ACTIVE RELEASE-ENGINEERING CONTRACT · CONTROLS NOT YET ESTABLISHED`  
**Scope:** `AETHERXGLOBAL/aether-x-governed-intelligence`  
**Production publication authority:** `NOT AUTHORIZED`

## Purpose

This document defines the repository, workflow and registry controls required before an AETHER X SDK release may cross from engineering candidate to externally distributed or production-supported software.

The release plane is treated as part of the product. A correct package produced by an uncontrolled release path is not an acceptable AETHER X production release.

---

## 1. Current observed control state

Latest directly observed repository state before this document was prepared:

```text
MAIN BRANCH PROTECTED: NO
REQUIRED STATUS CHECKS ENFORCED ON MAIN: NO
PROTECTED PYPI ENVIRONMENT: NOT ESTABLISHED
PYPI TRUSTED PUBLISHER: NOT ESTABLISHED
EXTERNAL REGISTRY WRITE AUTHORITY: NO
SDK PUBLICATION AUTHORITY: NO
```

These values are blockers, not defects to hide. They must be replaced by direct evidence before release promotion.

---

## 2. Control objectives

The production release plane must provide five properties:

### Change integrity

Release-relevant source and configuration cannot be changed through an uncontrolled direct path.

### Build integrity

The artifact published is the same immutable artifact that passed the release checks.

### Identity integrity

The registry can authenticate the approved GitHub release workload without relying on a long-lived primary publication secret.

### Human authority

Production publication requires an explicit authorized approval boundary independent from ordinary code execution.

### Evidence continuity

Source, build, artifact, approval, registry publication and post-publication verification remain traceably linked.

---

## 3. Main / release-relevant change controls

Target minimum controls:

```text
PULL REQUEST REQUIRED                    YES
INDEPENDENT APPROVAL                     >= 1
REQUIRED STATUS CHECKS                   YES
STALE APPROVAL INVALIDATION              YES WHERE SUPPORTED
FORCE PUSH                               BLOCKED
BRANCH DELETION                          BLOCKED
RELEASE-RELEVANT WORKFLOW CHANGES        REVIEWED
BYPASS                                   RESTRICTED / AUDITABLE
```

Required status checks should include the Gate-05 checks that protect the exact release surface. The final set must be recorded from live GitHub configuration rather than assumed from workflow filenames.

---

## 4. Release tag / input controls

A production release must originate from a controlled release input.

Target requirements:

- release tags follow an approved version pattern;
- release tags cannot be silently moved after publication;
- only authorized actors/workflows can create production release inputs;
- the source commit is already inside the governed branch state;
- version metadata matches the release input;
- the release workflow fails closed if source/version identity diverges.

A Git tag by itself is not release authority.

---

## 5. Workflow security contract

Release-sensitive GitHub Actions must:

- declare minimum required `permissions`;
- use `contents: read` unless a stronger permission is specifically required;
- grant `id-token: write` only to the job that needs OIDC publication/attestation;
- pin third-party and GitHub-maintained actions used in release-sensitive paths to reviewed full commit SHAs;
- use `persist-credentials: false` for checkout where practical;
- avoid `pull_request_target` with untrusted code in any publication-capable path;
- never publish from a pull-request event;
- not accept untrusted artifact paths or package versions without validation;
- separate build/test from production publish authority;
- treat release artifacts as immutable between verification and publication.

The current Gate-05 workflows already use full-SHA-pinned checkout/setup/upload actions and least-privilege read permissions for validation. Production publication requires a separate controlled workflow and authority boundary.

---

## 6. Build-once / promote-exact-artifact rule

Production release semantics:

```text
SOURCE COMMIT
→ BUILD ONCE
→ WHEEL + SDIST
→ HASH
→ TEST EXACT ARTIFACTS
→ CONFORMANCE
→ PROVENANCE / SBOM
→ CONTROLLED STAGING VALIDATION
→ HUMAN / RELEASE AUTHORITY
→ PUBLISH THE SAME ARTIFACTS
→ VERIFY REGISTRY RESULT
```

The production workflow must not rebuild a logically equivalent package after approval and publish that different build.

If any release artifact changes, release verification and approval are invalidated and must be repeated.

---

## 7. GitHub Environment boundary

Target production environment name:

```text
pypi
```

Before PyPI publication, the environment or equivalent control must establish the approved protection model, including reviewer/approval rules where supported and appropriate branch/tag restrictions.

The current existence/configuration of this environment must be checked from live platform state immediately before release promotion.

`ENVIRONMENT NAME ≠ ENVIRONMENT PROTECTION`

---

## 8. PyPI Trusted Publishing

Target production identity mechanism:

```text
GITHUB ACTIONS OIDC
→ PYPI TRUSTED PUBLISHER
→ SHORT-LIVED PUBLICATION CREDENTIAL
```

Production release must not rely on a long-lived PyPI API token as the primary publication credential when Trusted Publishing is available for the approved release design.

The trusted-publisher identity must be restricted to the exact AETHER X repository/workflow/environment combination selected for production publication.

Configuration of a pending or normal Trusted Publisher is an external registry identity action and requires separate explicit authority.

---

## 9. Staging / TestPyPI boundary

Gate-05C may perform controlled external distribution validation only after explicit authority.

Required staging behavior:

- fresh distribution-name check immediately before the action;
- release-control audit performed first;
- exact candidate artifacts identified by hash;
- upload through the approved staging identity mechanism;
- clean installation from TestPyPI or approved equivalent;
- package metadata and import identity verified;
- exact version and digest recorded;
- no production PyPI publication from the Gate-05C staging action;
- evidence recorded in a dedicated immutable release-validation record.

`TESTPYPI PASS ≠ PYPI RELEASE AUTHORITY`

---

## 10. Production PyPI publication boundary

Production publication is permitted only after `DEV-GATE-05D` explicitly authorizes the exact release evidence pack.

The publish job must fail closed unless it can establish, at minimum:

- expected repository identity;
- expected protected source/ref identity;
- expected release version;
- exact approved wheel and sdist digests;
- release evidence pack identity;
- licence/IP clearance state;
- release-control readiness state;
- external evaluation completion/disposition;
- OIDC Trusted Publisher eligibility;
- protected production environment context.

No generic “publish latest dist/” behavior is acceptable for the production release path.

---

## 11. Post-publication verification

A successful upload is not the end of release validation.

The release evidence must verify:

- PyPI exposes the expected normalized project/version;
- published filenames match approved filenames;
- published artifact hashes match approved hashes;
- installation from canonical PyPI succeeds on the declared support matrix or selected verification subset under the release contract;
- package metadata is correct;
- imported SDK version matches the registry release;
- public provenance/attestation can be resolved where applicable;
- release documentation links to the exact supported version;
- any mismatch triggers incident handling rather than a silent documentation correction.

---

## 12. Release-control audit states

The audit must use explicit states:

```text
ESTABLISHED
NOT_ESTABLISHED
NOT_APPLICABLE
UNVERIFIED
```

Unknown or inaccessible platform state is `UNVERIFIED`, never `ESTABLISHED`.

Production readiness requires all mandatory controls to be `ESTABLISHED`.

---

## 13. Current blocker matrix

| Control | Current state | Release effect |
|---|---|---|
| Main branch protection / ruleset | `NOT ESTABLISHED` | Blocks external registry promotion |
| Required release checks enforcement | `NOT ESTABLISHED` | Blocks external registry promotion |
| Protected `pypi` environment | `NOT ESTABLISHED` | Blocks production publication |
| PyPI Trusted Publisher | `NOT ESTABLISHED` | Blocks production publication |
| Registry ownership | `NOT ESTABLISHED` | Blocks production publication |
| IP / copyright clearance | `NOT ESTABLISHED` | Blocks licence grant/publication |
| Independent human evaluation | `NOT ESTABLISHED` | Blocks Gate-05C closure |
| Final release evidence pack | `NOT ESTABLISHED` | Blocks Gate-05D |
| Explicit release authority | `NOT AUTHORIZED` | Blocks publication |

---

## 14. Platform configuration authority

Repository documentation and CI can prepare, audit and fail closed around these controls. Some controls require explicit platform administration or external registry actions, including:

- GitHub ruleset/branch-protection configuration;
- protected Environment configuration;
- PyPI/TestPyPI project or Trusted Publisher configuration;
- final software licence grant;
- final production publication.

Those actions must be separately authorized and then re-verified from live platform state.

---

## Current disposition

```text
RELEASE CONTROL CONTRACT: DEFINED
LIVE RELEASE CONTROL PLANE: NOT ESTABLISHED
EXTERNAL REGISTRY WRITE: NOT AUTHORIZED
DEV-GATE-05C: ACTIVE
DEV-GATE-05D: NOT AUTHORIZED
SDK PUBLICATION: NOT AUTHORIZED
```

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
