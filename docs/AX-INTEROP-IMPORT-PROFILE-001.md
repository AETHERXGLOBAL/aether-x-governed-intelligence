# AX-INTEROP-IMPORT-PROFILE-001

**Version:** 0.1  
**Status:** DESIGN CANDIDATE / NON-BINDING / OFFLINE / READ-ONLY / IMPORT-ONLY / NO RUNTIME IMPLEMENTATION  
**Base revision:** `e6501f9ea665d1c3e88bfe38f82ceae7199d7034`  
**Parent research:** `AX-INTEROP-GAP-MATRIX-001`

## Objective

Define the smallest semantic contract candidate for importing already-supplied in-toto / SLSA attestations as AETHER evidence without converting external claims into AETHER decisions, authority, verification, acceptance, or verified outcomes.

This document is a design candidate only. It authorizes no runtime adapter, network access, registry access, signing, release integration, or cryptographic subsystem.

## Required semantic separation

The import model is explicitly staged:

`PARSED ≠ SUBJECT_BOUND ≠ SIGNATURE_VERIFIED ≠ TRUSTED_ISSUER ≠ PREDICATE/POLICY_VALIDATED ≠ AETHER_VERIFICATION ≠ VERIFIED_OUTCOME`

No earlier state implies a later state.

| Stage | Meaning | Does not imply |
|---|---|---|
| `PARSED` | Input bytes decoded and selected structural rules satisfied. | subject binding, signature validity, trust, policy validity |
| `SUBJECT_BOUND` | Expected artifact/resource identity matched while preserving the complete original subject set. | signature validity, trust, predicate validity |
| `SIGNATURE_VERIFIED` | Cryptographic verification succeeded with explicitly supplied verification material. | trusted issuer, truth, authorization, policy satisfaction |
| `TRUSTED_ISSUER` | Verified signer/issuer admitted by explicit point-in-time trust policy for this purpose. | predicate correctness, AETHER verification, authority |
| `PREDICATE_POLICY_VALIDATED` | Supported predicate/version passed explicit predicate-specific policy checks. | AETHER Verification, Acceptance, Authority, Verified Outcome |
| `AETHER_VERIFICATION` | Separate AETHER process evaluated imported evidence. Importer cannot create this state. | Verified Outcome |
| `VERIFIED_OUTCOME` | Separate downstream AETHER process established the outcome. Importer cannot create this state. | — |

`UNKNOWN`, `UNSUPPORTED`, `NOT_EVALUATED`, and missing evidence are never PASS.

## Default AETHER classification

Every imported attestation enters as:

- `AETHER type = Evidence / Source Data`
- `semantic status = UNVERIFIED_EXTERNAL_CLAIM`
- `promotion = NONE`

A valid signature authenticates signed bytes under the verification material used. It does **not** by itself establish a trusted issuer, truth of the predicate, AETHER authority, or an AETHER verification result.

## Exact raw identity

The design preserves two identities when applicable:

1. SHA-256 over the exact received envelope/attestation bytes.
2. SHA-256 over the exact signed payload bytes extracted from the envelope.

A digest over reserialized or canonicalized JSON must not replace either identity. Acquisition time is separate from any timestamp asserted inside the attestation; missing attestation timestamps remain missing.

## Subject semantics

### Generic in-toto / SLSA

The entire original `subject` array is preserved. Multi-subject Statements are supported.

A consumer may record which expected artifacts matched, but it must not silently discard co-subjects or split one attestation into equivalent per-subject evidence unless the predicate specification explicitly establishes distributive semantics.

Generic subject binding follows explicit digest/immutable-identifier policy. `name` is preserved, but its matching semantics come from the selected predicate/profile or explicit consumer policy.

**PEP 740 single-subject filename/SHA-256 rules are not generalized into this profile.**

## SLSA mappings

### Build Provenance

`predicateType = https://slsa.dev/provenance/v1`

Mapped as **Evidence / Source Data** describing where, when, and how artifacts were produced. Preserve complete subjects, `buildDefinition`, `runDetails`, builder identity claims, relevant timestamps/dependencies, and exact raw identities.

Even authentic, trusted, policy-valid provenance does not establish AETHER correctness, security approval, Authority, Acceptance, AETHER Verification, or Verified Outcome.

### Verification Summary Attestation

`predicateType = https://slsa.dev/verification_summary/v1`

Mapped as **Evidence of external verifier assessment**.

Preserve at minimum:

- complete subject set and digests;
- `verifier.id` and version when present;
- `timeVerified` when present;
- `resourceUri`;
- `policy.uri` and exact `policy.digest` when present;
- input attestation identities;
- `verificationResult`;
- `verifiedLevels`;
- `dependencyLevels`;
- `slsaVersion`;
- exact raw identities.

A VSA `verificationResult=PASSED` remains an external verifier claim. It is not AETHER Verification, Acceptance, Authority, or Verified Outcome.

If VSA predicate policy is evaluated, the explicit trust policy must accept the signer/issuer + `verifier.id` pair for the intended purpose.

## Unsupported or unknown semantics

- Unknown `predicateType`: may remain parseable and subject-bound, but `PREDICATE_POLICY_VALIDATED=UNSUPPORTED`; no semantic promotion.
- Unknown extension field allowed by applicable parsing rules: preserve raw identity; assign no AETHER meaning.
- Subject identifier the selected policy cannot verify: `SUBJECT_BOUND=UNKNOWN`.
- Missing VSA policy digest without another immutable policy-version mechanism: preserve absence and treat exact policy-instance validation as `UNKNOWN`.

## Negative semantic cases

The machine-readable companion contains explicit negative cases for:

1. malformed/structurally invalid Statement;
2. multi-subject scope loss by dropping co-subjects;
3. leakage of PEP 740 filename rules into generic in-toto/SLSA;
4. unsupported predicate;
5. unverifiable subject identifier;
6. invalid signature;
7. valid signature with no applicable trust policy;
8. VSA signer/verifier pair mismatch;
9. VSA PASS incorrectly promoted to AETHER Verification;
10. VSA FAIL treated as PASS;
11. missing exact policy digest;
12. invented timestamp;
13. unknown extension field promoted semantically;
14. byte-distinct attestations collapsed to one reserialized identity.

## Explicit non-goals

No runtime adapter, network retrieval, external registry, Release/Gate integration, AuthZEN/SCITT/Cedar/OpenFGA integration, custom crypto, custom predicate, export contract, signing, or trust-store management.

## Review boundary

**Implementation is not authorized by this design candidate.**

Before any executable importer or runtime contract is created, Independent Technical Oversight must re-review this exact design revision because the mapping defines Core evidence/verification semantic boundaries.

## Standards basis

The design is aligned to:

- in-toto Attestation Framework v1.2 / Statement v1 / Envelope v1;
- SLSA v1.2 Approved;
- SLSA Build Provenance;
- SLSA Verification Summary Attestation v1.

The machine-readable profile contains the source references used.
