# AX-INTEROP-IMPORT-PROFILE-001

**Version:** 0.1  
**Status:** DESIGN CANDIDATE / NON-BINDING / OFFLINE / READ-ONLY / IMPORT-ONLY / NO RUNTIME IMPLEMENTATION  
**Base revision:** `e6501f9ea665d1c3e88bfe38f82ceae7199d7034`  
**Parent research:** `AX-INTEROP-GAP-MATRIX-001`  
**Oversight correction basis:** `fd7122c9ebd4bce3960cceb30ce362521a45d89e`

## Objective

Define the smallest semantic contract candidate for importing already-supplied in-toto / SLSA attestations into AETHER evidence records without converting external claims into AETHER decisions, authority, verification, acceptance, or verified outcomes.

This document is a design candidate only. It authorizes no runtime adapter, network access, registry access, signing, release integration, dependency, schema change, or cryptographic subsystem.

## Required semantic separation

The import model is explicitly staged:

`PARSED ≠ SUBJECT_BOUND ≠ SIGNATURE_VERIFIED ≠ TRUSTED_ISSUER ≠ PREDICATE/POLICY_VALIDATED ≠ AETHER_VERIFICATION ≠ VERIFIED_OUTCOME`

No earlier state implies a later state.

| Stage | Meaning | Does not imply |
|---|---|---|
| `PARSED` | Input bytes decoded and selected structural rules satisfied. | subject binding, signature validity, trust, policy validity |
| `SUBJECT_BOUND` | Expected artifact/resource identity matched while preserving the complete original subject set. | signature validity, trust, predicate validity |
| `SIGNATURE_VERIFIED` | Aggregate signature result derived from preserved per-signature results under an explicit applicable signature policy. | trusted issuer, truth, authorization, policy satisfaction |
| `TRUSTED_ISSUER` | Verified signer/issuer admitted by explicit point-in-time trust policy for this purpose. | predicate correctness, AETHER verification, authority |
| `PREDICATE_POLICY_VALIDATED` | Supported predicate/version passed explicit predicate-specific policy checks and any predicate-specific trust prerequisites. | AETHER Verification, Acceptance, Authority, Verified Outcome |
| `AETHER_VERIFICATION` | Separate AETHER process evaluated imported evidence. Importer cannot create this state. | Verified Outcome |
| `VERIFIED_OUTCOME` | Separate downstream AETHER process established the outcome. Importer cannot create this state. | — |

`UNKNOWN`, `UNSUPPORTED`, `NOT_EVALUATED`, and missing evidence are never PASS.

## Default AETHER mapping

Every imported external attestation enters as two explicitly distinct AETHER properties:

- `target = evidence_record`
- `classification = SOURCE_DATA`
- `semantic status = UNVERIFIED_EXTERNAL_CLAIM`
- `promotion = NONE`

`evidence_record` is the target record type; `SOURCE_DATA` is its classification. They are not one semantic type.

No external attestation field, signature, signer identity, SLSA level, verification result, or trusted-issuer state directly creates AETHER Decision, Authority, Verification, Acceptance, or Verified Outcome.

## Multiple-signature semantics

When an envelope or accepted input form contains multiple signatures:

1. Preserve each signature identity and its verification result independently.
2. Preserve the verification-material identity/reference and signer/issuer claim associated with each signature.
3. Preserve failure, unknown, or unsupported reasons per signature.
4. Evaluate aggregate `SIGNATURE_VERIFIED` only under an explicit applicable signature policy.
5. That policy must define the acceptable signer set, threshold or required signatures, and handling of unknown/unsupported signatures.

The existence of one valid signature is insufficient for aggregate `SIGNATURE_VERIFIED=PASS` unless the explicit policy says that result satisfies the policy.

If multiple signatures exist and no applicable aggregate signature policy is defined, preserve the per-signature results and set aggregate `SIGNATURE_VERIFIED=UNKNOWN`.

An aggregate signature PASS still does not imply trusted issuer, predicate truth, authorization, AETHER Verification, Acceptance, Authority, or Verified Outcome.

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

Mapped as:

- `target = evidence_record`
- `classification = SOURCE_DATA`
- `semantic_role = BUILD_PROVENANCE_EXTERNAL_CLAIM`

Preserve complete subjects, `buildDefinition`, `runDetails`, builder identity claims, relevant timestamps/dependencies, exact raw identities, and per-signature results.

Even authentic, trusted, policy-valid provenance does not establish AETHER correctness, security approval, Authority, Acceptance, AETHER Verification, or Verified Outcome.

### Verification Summary Attestation

`predicateType = https://slsa.dev/verification_summary/v1`

Mapped as:

- `target = evidence_record`
- `classification = SOURCE_DATA`
- `semantic_role = EXTERNAL_VERIFIER_ASSESSMENT`

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
- exact raw identities;
- per-signature results.

A VSA `verificationResult=PASSED` remains evidence of an external verifier assessment. It is not AETHER Verification, Acceptance, Authority, or Verified Outcome.

For SLSA VSA specifically, `PREDICATE_POLICY_VALIDATED=PASS` is permitted only if all applicable requirements are satisfied, including explicitly:

1. `PARSED=PASS`;
2. `SUBJECT_BOUND=PASS`;
3. `SIGNATURE_VERIFIED=PASS` under the applicable aggregate signature policy;
4. `TRUSTED_ISSUER=PASS`;
5. the exact VSA predicate type/version is supported;
6. the applicable **point-in-time** trust policy is identified by digest or another immutable version;
7. that policy explicitly accepts the `signer/issuer + verifier.id` pair for the intended purpose;
8. all VSA predicate-specific policy checks pass.

If either `SIGNATURE_VERIFIED` or `TRUSTED_ISSUER` is not PASS, VSA `PREDICATE_POLICY_VALIDATED` cannot be PASS.

## Unsupported or unknown semantics

- Unknown `predicateType`: may remain parseable and subject-bound, but `PREDICATE_POLICY_VALIDATED=UNSUPPORTED`; no semantic promotion.
- Unknown extension field allowed by applicable parsing rules: preserve raw identity; assign no AETHER meaning.
- Subject identifier the selected policy cannot verify: `SUBJECT_BOUND=UNKNOWN`.
- Missing VSA policy digest without another immutable policy-version mechanism: preserve absence and treat exact policy-instance validation as `UNKNOWN`.
- Multiple signatures without an applicable aggregate signature policy: preserve all per-signature results and set aggregate `SIGNATURE_VERIFIED=UNKNOWN`.

## Negative semantic cases

The original fourteen cases are preserved and corrected where needed:

1. malformed/structurally invalid Statement;
2. multi-subject scope loss by dropping co-subjects;
3. leakage of PEP 740 filename rules into generic in-toto/SLSA;
4. unsupported predicate remains `target=evidence_record`, `classification=SOURCE_DATA`, `UNSUPPORTED`;
5. unverifiable subject identifier;
6. invalid signature under the applicable signature policy;
7. signature policy PASS with no applicable point-in-time trust policy;
8. VSA signer/verifier pair mismatch under applicable point-in-time trust policy;
9. VSA PASS incorrectly promoted to AETHER Verification;
10. VSA FAIL treated as PASS;
11. missing exact policy digest;
12. invented timestamp;
13. unknown extension field promoted semantically;
14. byte-distinct attestations collapsed to one reserialized identity.

Three additional correction cases are added:

15. one valid signature in a multi-signature input with no aggregate signature policy must not produce aggregate PASS;
16. explicit threshold/required-signer policy not satisfied must produce aggregate signature FAIL, not PASS from a valid subset;
17. VSA content cannot receive `PREDICATE_POLICY_VALIDATED=PASS` unless both aggregate `SIGNATURE_VERIFIED=PASS` and `TRUSTED_ISSUER=PASS` are established.

The machine-readable companion defines the exact expected and forbidden outcomes for all 17 cases.

## Explicit non-goals

No runtime importer, crypto implementation, dependency, schema change, network retrieval, external registry, Release/Gate integration, AuthZEN/SCITT/Cedar/OpenFGA integration, custom crypto, custom predicate, export contract, signing, or trust-store management.

## Review boundary

**Implementation is not authorized by this corrected design candidate.**

Before any executable importer or runtime contract is created, Independent Technical Oversight must re-review this exact corrected design revision because the mapping defines Core evidence/verification semantic boundaries.

## Standards basis

The design remains aligned to:

- in-toto Attestation Framework v1.2 / Statement v1 / Envelope v1;
- SLSA v1.2 Approved;
- SLSA Build Provenance;
- SLSA Verification Summary Attestation v1.

The machine-readable profile contains the source references used.
