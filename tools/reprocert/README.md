# AETHER X ReproCert

[![ReproCert CI](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/actions/workflows/reprocert-ci.yml/badge.svg)](https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/actions/workflows/reprocert-ci.yml)

**Claim → Experiment → Evidence → Verdict → Certificate**

ReproCert is an open developer tool from **AETHER X GLOBAL** for turning technical claims into machine-checkable, reproducible evidence records in local development and CI.

Instead of placing an unsupported statement such as “this benchmark is under 2 seconds” in a README, a project can define the claim, exact command, evidence files and acceptance checks in a small YAML file. ReproCert runs it without a shell, records the environment and evidence digests, evaluates the checks, and emits a certificate with one of four explicit outcomes:

`PASS` · `FAIL` · `INCONCLUSIVE` · `ERROR`

> **Alpha boundary:** ReproCert v0.1 is an engineering tool, not a scientific peer-review system, security certification system, or proof that an artifact is trustworthy. A self-digest detects accidental/tampered certificate content only when the expected digest is trusted. Producer authenticity is a separate concern and should be established with a signed CI attestation such as GitHub Artifact Attestations/Sigstore.

## Why this exists

Software projects routinely publish benchmark, compatibility, data-quality and reproducibility claims without shipping the exact evidence path behind those claims. Existing provenance standards are valuable, but build provenance and claim adjudication are different problems.

ReproCert focuses on the narrow boundary:

```text
CLAIM
  ↓ exact command
EXPERIMENT / CHECK
  ↓ observed result
EVIDENCE
  ↓ explicit comparator
VERDICT
  ↓ canonical certificate
REPRODUCIBILITY RECORD
```

It is designed to complement — not replace — SLSA, in-toto, Sigstore, GitHub Artifact Attestations, test frameworks, benchmark harnesses, or experiment trackers.

## Five-minute quickstart

Requires Python 3.11+.

```bash
python -m pip install -e .
cd examples/basic
reprocert run claim.yml --output certificate.json
reprocert verify certificate.json --claim claim.yml --evidence-root .
reprocert inspect certificate.json
```

Expected first line:

```text
ReproCert verdict: PASS
```

## Claim format

```yaml
apiVersion: reprocert.dev/v1alpha1
kind: ReproducibilityClaim
metadata:
  id: api-latency
  title: Median latency stays below the agreed threshold
spec:
  command: [python, benchmark.py]
  timeout_seconds: 60
  evidence: [results.json]
  checks:
    - id: latency
      source:
        type: json
        path: results.json
        pointer: /median_ms
      op: lt
      expected: 2000
```

### Sources

`json` · `text` · `stdout` · `stderr` · `exit_code` · `file_sha256` · `file_size`

### Comparators

`eq` · `ne` · `lt` · `le` · `gt` · `ge` · `approx` · `contains`

`approx` requires `abs_tolerance`.

## Verdict semantics

| Verdict | Meaning |
|---|---|
| `PASS` | The command completed as expected, required evidence was available, and every check passed. |
| `FAIL` | The experiment completed and at least one explicit claim check was false. |
| `INCONCLUSIVE` | The run completed, but required evidence could not be resolved or adjudicated. |
| `ERROR` | The experiment could not execute as specified, timed out, or returned an unexpected process exit code. |

The distinction is deliberate: a crashed benchmark is **not** automatically evidence that the benchmark claim is false.

## GitHub Action

While ReproCert is incubated in this repository, projects can invoke the scoped composite action directly:

```yaml
- uses: AETHERXGLOBAL/aether-x-governed-intelligence/tools/reprocert@main
  with:
    claim: path/to/claim.yml
    certificate: reprocert-certificate.json
```

For pull requests, run untrusted code only with least-privilege workflow permissions and never expose secrets to code from untrusted forks.

## Certificate integrity vs producer authenticity

ReproCert intentionally separates two questions:

1. **Is this certificate internally consistent with the evidence files I have?** `reprocert verify` checks canonical certificate integrity, verdict consistency, optional claim digest and optional local evidence hashes.
2. **Who produced this certificate and in which workflow/repository?** Use a signed external attestation. GitHub Artifact Attestations use Sigstore and can bind an artifact to repository/workflow/commit identity.

`INTERNAL CONSISTENCY != PRODUCER AUTHENTICITY != SCIENTIFIC TRUTH`

## Design principles

- explicit claims, not implied claims;
- explicit evidence, not screenshots;
- fail closed on path escape and malformed configuration;
- no shell execution for claim commands;
- no environment-variable value capture;
- distinguish false claim from failed experiment;
- human-readable and machine-readable outputs;
- offline verification of local certificate/evidence integrity;
- open schemas for interoperability;
- complementary to standard provenance/attestation ecosystems.

## Current alpha scope

Included: YAML/JSON claims, deterministic claim hashing, bounded subprocess execution, JSON Pointer observations, stdout/stderr/file observations, evidence SHA-256 records, environment snapshot, canonical certificate digest, offline verification, certificate diffing, composite GitHub Action, JSON Schemas, and adversarial path-boundary tests.

Not yet included: remote execution, cryptographic signing inside ReproCert, OCI publishing, policy engines, distributed benchmark orchestration, statistical suites beyond explicit scalar tolerance, or scientific correctness adjudication.

## Security

Read [SECURITY.md](SECURITY.md) and [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md). A claim file author controls a command that CI will execute. Treat claim changes exactly like code changes.

## License

The **`tools/reprocert/` subtree only** is licensed under Apache License 2.0. See [LICENSE](LICENSE) and [LICENSE_SCOPE.md](LICENSE_SCOPE.md). This scoped license does not change the licensing or IP terms of the rest of the parent repository.

## Status

`PUBLIC ALPHA · DEVELOPER TOOL · NO PRODUCTION OR SCIENTIFIC CERTIFICATION CLAIM`
