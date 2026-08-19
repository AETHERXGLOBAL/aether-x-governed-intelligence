# AX Offline Attestation Semantic Importer — Reference Proof

`BOUNDED REFERENCE IMPLEMENTATION · OFFLINE · READ-ONLY · IMPORT-ONLY · NON-PRODUCTION`

This directory is the executable proof for the independently reviewed `AX-INTEROP-IMPORT-PROFILE-001` design at `9bc8aab0988949fea614c449678ef5998cd7d07f`.

## Scope

The importer accepts only attestation bytes already supplied by the caller. It performs bounded semantic processing for:

- in-toto Statement v1 parsing;
- subject binding against explicit expected-subject input;
- SLSA Build Provenance / Verification Summary Attestation predicate classification;
- per-signature result preservation through a caller-supplied verification interface;
- aggregate signature status through a caller-supplied signature-policy interface;
- issuer/trust evaluation through a caller-supplied point-in-time trust-policy interface;
- predicate-policy evaluation through a caller-supplied policy interface;
- mapping to one AETHER `evidence_record` with `classification = SOURCE_DATA`.

The importer cannot create AETHER Decision, Authority, Execution, Verification, Acceptance, or Verified Outcome records.

## Semantic separation

`PARSED != SUBJECT_BOUND != SIGNATURE_VERIFIED != TRUSTED_ISSUER != PREDICATE_POLICY_VALIDATED != AETHER_VERIFICATION != VERIFIED_OUTCOME`

`UNKNOWN / UNSUPPORTED / NOT_EVALUATED != PASS`

A valid signature does not create a trusted issuer. A trusted issuer does not make the predicate true. A SLSA VSA PASS remains external verifier source data and never becomes AETHER Verification or Verified Outcome.

## Provenance and Point-in-Time handling

`source_identity` is derived from SHA-256 of the exact received attestation bytes. It is not populated from an untrusted signer claim.

`observed_at` is caller supplied, timezone-qualified observation time. Attestation-asserted timestamps are preserved separately and never substituted for observation time.

The exact raw-attestation digest and exact signed-payload digest are preserved separately. Reserialized JSON identity does not replace exact-byte identity.

## Cryptographic boundary

No cryptography is implemented here. Signature verification is an injected interface. Tests use deterministic fixtures only; they are not cryptographic verification.

No trust store, certificate validation, key discovery, network access, registry access, or signing infrastructure is included.

## Tests

Run:

```bash
python -m unittest discover -s reference-implementations/offline-attestation-importer/tests -p "test_*.py" -v
python -m py_compile reference-implementations/offline-attestation-importer/importer.py reference-implementations/offline-attestation-importer/tests/test_importer.py
```

The regression suite implements `NEG-001` through `NEG-017` from the reviewed design.

## Explicit non-goals

No network, registry, production runtime, Release/Gate integration, signing, trust-store management, AuthZEN, SCITT, Cedar, OpenFGA, export contract, custom crypto, or custom predicate.

`REFERENCE PROOF != PRODUCT IMPLEMENTATION`

`TEST PASS != SECURITY GO`

`IMPLEMENTED != VERIFIED != ACCEPTED`
