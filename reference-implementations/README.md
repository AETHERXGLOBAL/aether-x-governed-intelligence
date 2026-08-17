# AETHER X Public Reference Implementations

`PUBLIC ENGINEERING MATERIAL · EDUCATIONAL / NON-PRODUCTION`

This directory contains bounded executable companions to selected AETHER X public technical specifications and machine-readable schemas.

## Current Reference Implementations

| ID | Reference implementation | Related public artifacts | Public state |
|---|---|---|---|
| `AX-PUB-REF-001` | [EAV Contract Validator](./eav-contract-validator/README.md) | `AX-PUB-SPEC-002` · `AX-PUB-SCHEMA-001` | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |
| `AX-PUB-REF-002` | [Point-in-Time Knowledge Validator](./point-in-time-knowledge-validator/README.md) | `AX-PUB-SPEC-003` · `AX-PUB-SCHEMA-002` | `CI-TESTED · EDUCATIONAL / NON-PRODUCTION` |

## Reference Responsibilities

### AX-PUB-REF-001

Demonstrates selected evidence / decision / authority / execution / verification invariants, including bounded authority and the requirement that a `VERIFIED` outcome be backed by `PASS` verification.

### AX-PUB-REF-002

Demonstrates selected point-in-time knowledge / provenance invariants, including:

- no-future-leakage relative to a declared knowledge cutoff;
- source and transformation lineage references;
- revision/supersession references;
- explicit missing states for absent values;
- reproducibility-cutoff consistency.

## Claim Boundary

These implementations are intentionally small and dependency-light. They are designed to make public engineering semantics inspectable, not to imitate or expose proprietary platform code.

They do **not** establish:

- production readiness;
- product integration;
- implementation inside AETHER X Quantum, AX-OS, AIC or AETHER X Research;
- secure authorization enforcement;
- production data-quality guarantees;
- ownership or availability of financial-data sources;
- regulatory compliance or certification;
- customer deployment;
- predictive or investment performance.

`REFERENCE IMPLEMENTATION ≠ PRODUCT IMPLEMENTATION`

`CI PASS ≠ PRODUCTION APPROVAL`

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
