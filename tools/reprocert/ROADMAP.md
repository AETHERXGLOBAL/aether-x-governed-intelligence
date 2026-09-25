# Roadmap

## v0.1 — claim-to-evidence core

- [x] bounded YAML/JSON claim format
- [x] explicit PASS / FAIL / INCONCLUSIVE / ERROR semantics
- [x] JSON, text, stdout/stderr, file hash and file size observations
- [x] evidence hashing
- [x] environment capture without environment-variable values
- [x] certificate self-digest and offline verification
- [x] certificate diff
- [x] composite GitHub Action
- [x] schemas and threat model

## v0.2 candidates

- custom attestation predicate profile for ReproCert certificates;
- reusable GitHub workflow with signed certificate attestation;
- statistical check profiles with explicit assumptions;
- JUnit/pytest/benchmark adapters;
- organization-wide claim policy;
- deterministic container runner profile;
- longitudinal regression view.

## v0.3 research questions

- portable CI identity across providers without collapsing trust semantics;
- claim dependency graphs;
- evidence freshness and temporal validity;
- reproducibility quorum across independent runners;
- scorecards that do not convert nuanced evidence into misleading scalar ratings.
