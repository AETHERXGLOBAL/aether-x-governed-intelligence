# AX-PUB-REF-003 — Agent Tool-Use Authority Validator

**Version:** `1.0`  
**Status:** `PUBLIC REFERENCE IMPLEMENTATION · CI WORKFLOW PUBLISHED · VALIDATION PENDING · EDUCATIONAL / NON-PRODUCTION`  
**Scope:** Selected deterministic semantics from `AX-PUB-SPEC-004`

## Purpose

This standard-library Python reference validator demonstrates selected public agent/tool-use authority invariants from:

- `AX-PUB-SPEC-004 — Governed Agent Authority & Tool-Use Boundary Standard`
- `AX-PUB-SCHEMA-003 — Agent Tool-Use Authority Envelope`

It is intentionally technology-neutral and synthetic. It is **not** a production authorization service, agent runtime, policy engine, credential broker, security control, or evidence of implementation inside any AETHER X product.

## Selected Checks

The validator checks selected relationships including:

- proposal principal and tool references;
- tool-declared action compatibility;
- authority-context validity and revocation state;
- grant-to-proposal and grant-to-context identity;
- grant tool/action/resource scope;
- grant parameter constraints not exceeding the authority context;
- invocation principal/tool/action/resource matching the grant;
- invocation time inside the grant validity window;
- invocation environment inside the authority context;
- effective parameters inside the public reference constraints;
- single-use and maximum-invocation limits;
- tool-result linkage to a known invocation;
- explicit `verification_required` state.

`CAPABILITY ≠ AUTHORITY`

`TOOL AVAILABILITY ≠ TOOL PERMISSION`

`INVOCATION SUCCESS ≠ VERIFIED OUTCOME`

## Run

```bash
python3 reference-implementations/agent-tool-authority-validator/validator.py \
  reference-implementations/agent-tool-authority-validator/examples/valid_envelope.json
```

Expected result when the published validator and example conform:

```text
AX_AGENT_AUTHORITY_REFERENCE_VALIDATION_PASS
```

The intentionally invalid example is designed to be rejected.

Run unit tests:

```bash
python3 -m unittest discover \
  -s reference-implementations/agent-tool-authority-validator/tests -v
```

A public GitHub Actions workflow is published at `.github/workflows/validate-agent-authority-reference.yml`. Until a successful run against the published repository state is directly verified, this artifact remains `VALIDATION PENDING` rather than being represented as CI-tested.

## Public Reference Profile

`parameter_constraints` supports a deliberately small public reference profile:

- `allowed_values`
- `minimum`
- `maximum`
- `required`

This profile demonstrates bounded parameter authority. It is not a universal policy language.

## Claim Boundary

A validator pass means only that the supplied envelope satisfied the selected deterministic checks implemented by that public reference version.

It does **not** establish product implementation, production authorization, security certification, regulatory approval, autonomous authority, private-repository behavior, agent-framework adoption, shared company runtime, or production API/SDK compatibility.

`REFERENCE VALIDATOR PASS ≠ PRODUCTION APPROVAL`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
