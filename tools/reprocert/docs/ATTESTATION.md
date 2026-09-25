# Signed Producer Attestation

ReproCert's local verifier checks certificate/evidence integrity. It deliberately does **not** pretend that a self-digest authenticates the producer.

The parent public repository includes a reference workflow, `ReproCert Attested Demo`, that checks out the exact Git revision, runs the reference claim, verifies the certificate against local evidence, uses GitHub Artifact Attestations to create signed provenance for the certificate, and publishes the certificate as a workflow artifact.

For public repositories, GitHub Artifact Attestations use Sigstore's public-good instance and transparency infrastructure.

## Boundary

A valid GitHub attestation answers **where/how this certificate artifact was produced**. It does not establish that the benchmark design is unbiased, that a scientific hypothesis is true, or that the underlying software is secure.
