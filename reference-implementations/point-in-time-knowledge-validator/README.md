# Point-in-Time Knowledge Validator — Public Reference Implementation

**Artifact ID:** `AX-PUB-REF-002`  
**Version:** `1.0`  
**Status:** `PUBLIC REFERENCE IMPLEMENTATION · CI-TESTED · EDUCATIONAL / NON-PRODUCTION`  
**Related Specification:** [`AX-PUB-SPEC-003 — Point-in-Time Knowledge & Provenance Standard`](../../specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)  
**Related Machine-Readable Contract:** [`AX-PUB-SCHEMA-002 — Point-in-Time Knowledge Envelope`](../../schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json)  
**Organization:** AETHER X GLOBAL

## Purpose

This bounded reference implementation demonstrates selected temporal-integrity and provenance rules from `AX-PUB-SPEC-003` as deterministic checks over a public point-in-time knowledge envelope.

The core question is:

> **Could this information legitimately have been available under the declared knowledge cutoff, and can its source, version and lineage be reconstructed?**

## What It Checks

The validator currently checks selected reference conditions including:

- required point-in-time query context;
- unique identifiers across source, transformation and assertion records;
- explicit source identity and retrieval time;
- source publication/retrieval after the knowledge cutoff;
- assertion publication/observation after the knowledge cutoff;
- source-to-assertion references;
- observation occurring after source retrieval;
- effective and validity interval ordering;
- explicit revision kinds;
- correction/restatement/reclassification/supersession/withdrawal referencing a prior assertion;
- supersession reference validity and basic subject/predicate continuity;
- explicit freshness and missing-data states;
- absent/null values preserving an explicit missing state;
- transformation input/output references;
- assertion-to-transformation lineage references;
- reproducibility cutoff matching the query knowledge cutoff.

## No-Future-Leakage Boundary

For the reference profile, records observed or retrieved after `knowledge_cutoff_time` are rejected from a point-in-time envelope.

This reflects the distinction in `AX-PUB-SPEC-003` between **event history** and **knowledge history**. An event may have occurred before cutoff while the system learned about it only later; that later observation must not be silently injected into the earlier knowledge state.

## Public Claim Boundary

This artifact is **not** a production market-data system, production data-quality engine, AIC implementation, data entitlement system, source-reliability scorer, backtesting engine or product SDK.

It does **not** establish or imply:

- implementation inside AETHER Intelligence Core (AIC) or any other AETHER X initiative;
- ownership or availability of any financial-data source;
- production-scale global financial-information infrastructure;
- guaranteed completeness, correctness, timeliness or latency;
- production readiness;
- customer deployment;
- regulatory or security certification;
- technical integration between AETHER X initiatives.

`POINT-IN-TIME REFERENCE VALIDATION ≠ PRODUCTION DATA QUALITY`

`NO-FUTURE-LEAKAGE CHECK ≠ PREDICTIVE VALIDITY`

`REFERENCE IMPLEMENTATION ≠ AIC IMPLEMENTATION`

## Requirements

Python 3.10+ is recommended. The implementation uses only the Python standard library.

## Run

Validate the conforming reference envelope:

```bash
python3 validator.py examples/valid_envelope.json
```

Expected output:

```text
AX_PTK_REFERENCE_VALIDATION_PASS
```

Validate the intentionally invalid envelope:

```bash
python3 validator.py examples/invalid_envelope.json
```

The command exits with status `1` and prints the detected temporal/provenance violations.

For structured findings:

```bash
python3 validator.py examples/invalid_envelope.json --json
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The public workflow compiles the validator, runs unit tests, validates the conforming envelope and confirms that the intentionally invalid envelope is rejected.

## Related Public Material

- [Repository overview](../../README.md)
- [Public quickstart](../../docs/QUICKSTART.md)
- [Compatibility & versioning policy](../../docs/COMPATIBILITY_AND_VERSIONING.md)
- [AX-PUB-ARCH-001](../../specifications/AX-PUB-ARCH-001_GOVERNED_INTELLIGENCE_REFERENCE_ARCHITECTURE.md)
- [AX-PUB-SPEC-003](../../specifications/AX-PUB-SPEC-003_POINT_IN_TIME_KNOWLEDGE_PROVENANCE_STANDARD.md)
- [AX-PUB-SCHEMA-002](../../schemas/AX-PUB-SCHEMA-002_POINT_IN_TIME_KNOWLEDGE_ENVELOPE.schema.json)
- [Schema index](../../schemas/README.md)

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**