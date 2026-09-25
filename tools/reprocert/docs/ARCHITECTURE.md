# Architecture

```text
claim.yml
  │
  ├─ validate bounded schema
  ├─ execute argv with shell=False
  ├─ resolve declared observations
  ├─ adjudicate explicit comparators
  ├─ hash declared evidence
  ├─ capture non-secret environment metadata
  └─ emit canonical certificate + self-digest
         ├─ offline structural/evidence verification
         └─ optional external signed attestation
```

## Why no embedded signing key

ReproCert intentionally does not invent a private-key management system. In CI, workload identity systems such as GitHub OIDC + Sigstore can bind certificates to a workflow identity without long-lived signing secrets.

## Why self-digest still exists

The certificate digest is useful as a stable content identifier and as a subject digest for external attestation. It must not be interpreted as authentication by itself.
