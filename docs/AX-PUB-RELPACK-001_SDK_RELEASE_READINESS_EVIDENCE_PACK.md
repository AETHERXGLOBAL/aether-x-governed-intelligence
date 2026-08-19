# AX-PUB-RELPACK-001 — SDK Release Readiness Evidence Pack

**Artifact ID:** `AX-PUB-RELPACK-001`  
**Version:** `0.1`  
**State:** `DEV-GATE-05D READINESS CANDIDATE · CURRENTLY BLOCKED`  
**Publication boundary:** `SDK PUBLICATION NOT AUTHORIZED`

## Purpose

This artifact turns the final SDK release-readiness question into a deterministic evidence aggregation rather than an informal checklist.

The builder reads the current governed repository state and emits:

```text
AX-PUB-RELPACK-REPORT-001
```

Every hard release dimension receives:

```text
DIMENSION ID
CURRENT STATE
ESTABLISHED = true / false
EVIDENCE REFERENCES
BLOCKER REASONS WHEN FALSE
```

The report then derives:

```text
READY_FOR_DEV_GATE_05D_AUTHORITY_REVIEW
```

only when every required dimension is established.

The report cannot itself authorize `DEV-GATE-05D` or publish an SDK.

---

## Current governed dimensions

```text
01 ENGINEERING_CANDIDATE_IDENTITY
02 PUBLIC_API_CONTRACT
03 EXACT_ARTIFACT_RUNTIME_VALIDATION
04 SUPPLY_CHAIN_PROVENANCE_SBOM
05 EXTERNAL_REGISTRY_VALIDATION
06 INDEPENDENT_HUMAN_EXTERNAL_EVALUATION
07 RELEASE_CONTROL_READINESS
08 REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER
09 LICENCE_AND_IP_CLEARANCE
10 SUPPORT_CONTRACT_ACTIVATION
11 SECURITY_OPERATIONS_READINESS
12 RELEASE_OWNER_AND_ACCOUNTABILITY
13 EXPLICIT_RELEASE_AUTHORITY
```

All thirteen are hard requirements for this candidate contract. No average score or partial percentage can override a failed dimension.

---

## Current expected baseline

The current repository evidence is expected to establish the first four engineering dimensions and to block on the remaining nine authority/operating/external dimensions:

```text
ESTABLISHED
- ENGINEERING_CANDIDATE_IDENTITY
- PUBLIC_API_CONTRACT
- EXACT_ARTIFACT_RUNTIME_VALIDATION
- SUPPLY_CHAIN_PROVENANCE_SBOM

BLOCKED / NOT ESTABLISHED
- EXTERNAL_REGISTRY_VALIDATION
- INDEPENDENT_HUMAN_EXTERNAL_EVALUATION
- RELEASE_CONTROL_READINESS
- REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER
- LICENCE_AND_IP_CLEARANCE
- SUPPORT_CONTRACT_ACTIVATION
- SECURITY_OPERATIONS_READINESS
- RELEASE_OWNER_AND_ACCOUNTABILITY
- EXPLICIT_RELEASE_AUTHORITY
```

Therefore the correct current result is:

```text
REQUIRED DIMENSIONS: 13
ESTABLISHED: 4
BLOCKED: 9
READY FOR DEV-GATE-05D AUTHORITY REVIEW: NO
DEV-GATE-05D AUTHORIZED: NO
SDK PUBLICATION AUTHORIZED: NO
```

This is a **successful fail-closed result**. CI should fail only if the report contradicts the governed evidence contract, not merely because the release is correctly blocked.

---

## Validation acceptance

This candidate becomes CI-validated only through a direct run of `Validate SDK Release Readiness Evidence Pack` against the reviewed source. Local execution, a merge to `main`, or a correctly blocked readiness result does not by itself establish CI validation.

A later promotion must preserve the exact workflow run, job and uploaded report-artifact identities as governed evidence. Until that evidence exists, the artifact remains a candidate even when its local checks pass.

---

## Machine-readable contract

[`artifacts/AX-PUB-RELPACK-001.json`](../artifacts/AX-PUB-RELPACK-001.json)

Builder:

[`tools/build_sdk_release_readiness_pack.py`](../tools/build_sdk_release_readiness_pack.py)

Checker:

[`tools/check_sdk_release_readiness_pack.py`](../tools/check_sdk_release_readiness_pack.py)

---

## Evidence model

The pack currently consumes the governed public state around:

- exact installable candidate identity;
- Gate-03 supply-chain/provenance/SBOM engineering evidence;
- Gate-05C local distribution validation;
- public API contract validation;
- support contract candidate state;
- security-operations contract candidate state;
- evaluator handoff / human-evaluation boundary;
- live release-control audit;
- registry/Trusted Publisher state;
- licence/IP state;
- explicit release authority.

A missing canonical state is interpreted as **not established**, not inferred from intent or documentation prose.

---

## Authority firewall

The release pack is intentionally unable to create any of the following:

- PyPI ownership;
- Trusted Publisher configuration;
- protected GitHub rules or environment;
- IP/copyright clearance;
- software licence grant;
- independent human evaluation;
- external adoption;
- security-response ownership;
- support activation;
- release-owner assignment;
- `DEV-GATE-05D` authority.

Those require their own authoritative evidence and, where applicable, human or administrative action.

```text
AGGREGATION ≠ EVIDENCE CREATION
READY FOR AUTHORITY REVIEW ≠ RELEASE AUTHORITY
CI PASS ≠ HUMAN EVALUATION
CI PASS ≠ LICENCE GRANT
CI PASS ≠ REGISTRY OWNERSHIP
DEV-GATE-05D NOT AUTHORIZED
SDK PUBLICATION NOT AUTHORIZED
```
