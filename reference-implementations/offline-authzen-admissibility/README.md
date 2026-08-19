# AX Offline AuthZEN Decision Admissibility — Reference Proof

`BOUNDED REFERENCE IMPLEMENTATION · OFFLINE · READ-ONLY · SINGLE ACCESS EVALUATION ONLY · NON-PRODUCTION`

This directory is the executable proof for the independently reviewed
`AX-AUTHZEN-DECISION-ADMISSIBILITY-PROFILE-001` design at
`b8e3b145ceb5db1274d8c55e6910a97da20ebec0`.

## Scope

The proof accepts one already-supplied AuthZEN single Access Evaluation
request/response pair and executes only:

`RECEIVED -> REQUEST_BOUND -> RESPONSE_INTEGRITY_VERIFIED -> PDP_TRUSTED -> DECISION_ADMISSIBLE`

The raw request, response, boolean decision, and all PDP/policy/time/freshness/
replay claims are recorded first as external `SOURCE_DATA`.

The proof never creates:

- AETHER Decision;
- `authority_context`;
- `tool_use_grant`;
- capability;
- execution permission;
- AETHER Verification;
- Verified Outcome.

Therefore:

`DECISION_ADMISSIBLE != AETHER_DECISION != AETHER_AUTHORITY != EXECUTION_PERMISSION`

## Interface boundary

No cryptography, PDP, trust store, network client, policy engine, freshness
store, or replay store is implemented here.

The following determinations are injected through interfaces:

- request binding;
- response integrity/correlation;
- PDP identity verification;
- PDP trust evaluation;
- PDP policy/evaluation-time provenance verification;
- freshness verification;
- replay verification.

A callback returning `PASS` is insufficient by itself. PASS evidence used for
admissibility must be attributable and bound to the exact immutable request
identity, exact immutable response identity, exact AETHER proposal, intended
purpose, applicable policy identity/version-or-digest, and check/evaluation
time where required. Incomplete or unbound PASS claims are downgraded to
`UNKNOWN`.

Bare values such as `freshness_pass=true`, `replay_pass=true`, caller-supplied
timestamps, or PDP/policy identifiers cannot establish admissibility.

## Immutable identity boundary

When original request/response bytes are available, the proof preserves
separate SHA-256 identities of those exact bytes.

Parsed-object-only inputs remain importable as `SOURCE_DATA`, but they cannot
reach `DECISION_ADMISSIBLE` because original immutable request/response
identities are unavailable.

The proof never hashes reserialized parsed objects as a substitute for
received-byte identity and defines no canonical-object identity mechanism.

## API surface

v0.1 supports only one AuthZEN single Access Evaluation.

AuthZEN Access Evaluations/boxcarring and Search APIs are `UNSUPPORTED`.
They may be preserved as raw `SOURCE_DATA`, but receive no admissibility
semantics and always remain `NO_PROCEED`.

## Tests

```bash
python -m py_compile \
  reference-implementations/offline-authzen-admissibility/admissibility.py \
  reference-implementations/offline-authzen-admissibility/tests/test_admissibility.py

python -m unittest discover \
  -s reference-implementations/offline-authzen-admissibility/tests \
  -p 'test_*.py' \
  -v
```

The regression suite implements `NEG-AZ-001` through `NEG-AZ-032`.

`REFERENCE PROOF != PRODUCT IMPLEMENTATION`

`TEST PASS != SECURITY GO`

`IMPLEMENTED != VERIFIED != ACCEPTED`

`NO NETWORK / PDP / CEDAR / OPENFGA / OAUTH / WIMSE / RELEASE / GATE AUTHORITY`
