# Security Policy

## Public Reporting Boundary

This repository contains public, non-production reference material. It must not be used to disclose credentials, private customer information, confidential architecture, proprietary implementation details, private research records, or exploit information that could increase operational risk.

If you believe you have identified a security issue related to AETHER X GLOBAL, **do not publish sensitive details in a public GitHub issue, discussion, pull request, or commit**.

Until a dedicated vulnerability-disclosure channel is formally published, use the current public organization contact email:

```text
aether.x.eg@gmail.com
```

Use a clear subject such as `Security Report — AETHER X Public Engineering` and avoid sending secrets, credentials or unrelated private data unless a secure follow-up channel is explicitly established.

This is a provisional public reporting path. It does not represent a dedicated security-response service, SLA, bug-bounty program or certification.

## Private-Project Separation

Public engineering artifacts must remain separated from private AETHER X project repositories.

Public reference code, schemas, examples, tests, conformance vectors and CI workflows must not require or expose:

- private repository source;
- private package indexes;
- private endpoints;
- credentials or secrets;
- customer information;
- unpublished research;
- proprietary product algorithms;
- confidential implementation architecture.

## Public Reference-Code Boundary

Reference implementations and candidate developer surfaces in this repository are non-production engineering artifacts. Validation, conformance, CI, build-provenance or supply-chain checks do not establish production fitness, product authorization, security certification or a supported SDK.

`PUBLIC REFERENCE CODE ≠ PRODUCTION SECURITY CONTROL`  
`CI PASS ≠ SECURITY CERTIFICATION`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SDK CANDIDATE ≠ SUPPORTED SDK`

## Supply-Chain Reporting

If a report concerns a public release-candidate build, artifact attestation, SBOM, dependency boundary or release-integrity issue, include the applicable public artifact ID, Git commit, workflow/run identifier and digest when known.

Do not include credentials or private-repository material as evidence.

## Scope

This policy governs only the public `AETHERXGLOBAL/aether-x-governed-intelligence` repository and its intentionally published artifacts. It does not disclose or define the security policy, architecture or operational controls of private AETHER X products or systems.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**