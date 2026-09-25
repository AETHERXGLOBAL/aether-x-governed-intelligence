# Threat Model

## Explicit non-goals

ReproCert does not prove that a claim is scientifically meaningful, an evidence source is physically truthful, a benchmark is unbiased, the producer is trustworthy without separate signed attestation, arbitrary repository code is safe, or a PASS result generalizes beyond the declared environment.

## Threats and controls

### Shell injection
**Control:** `spec.command` is an array and execution uses `subprocess.run(..., shell=False)`.

### Path escape
**Control:** absolute paths and `..` traversal are rejected; runtime resolution re-checks containment.

### Secret exfiltration
**Control:** workflows must use least privilege and must not expose secrets to untrusted PR code.

### Certificate editing
**Control:** canonical SHA-256 self-digest detects content modification when the expected digest is trusted. It is not a signature.

### Producer impersonation
**Control:** use a producer-identity system such as GitHub Artifact Attestations/Sigstore.

### Verdict laundering
**Control:** offline verification recomputes verdict consistency from execution/check states.

### Missing evidence mislabeled as failure
**Control:** evidence-resolution failure maps to `INCONCLUSIVE`; execution failures map to `ERROR`.

## Trust model

```text
ReproCert local certificate integrity
        !=
producer authentication
        !=
source-of-evidence truth
        !=
scientific validity
```
