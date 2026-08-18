# Security Policy

## Public Reporting Boundary

This repository contains public, non-production reference material and an installable SDK release candidate. It must not be used to disclose credentials, private customer information, confidential architecture, proprietary implementation details, private research records, or exploit information that could increase operational risk.

If you believe you have identified a security issue related to AETHER X GLOBAL public engineering, **do not publish sensitive details in a public GitHub issue, discussion, pull request, or commit**.

Until a dedicated or formally designated private vulnerability-disclosure channel is established, use the current public organization contact email:

```text
aether.x.eg@gmail.com
```

Use a subject such as:

```text
Security Report — AETHER X Public Engineering
```

Avoid sending secrets, credentials, customer data, or unrelated private information unless a secure follow-up channel is explicitly established.

This is a **provisional public reporting path**. It does not represent a dedicated security-response service, SLA, bug-bounty program or certification.

---

## SDK Security-Operations Candidate

AETHER X has defined a candidate security-operations readiness contract for a future supported SDK:

[`AX-PUB-SEC-001 — SDK Security Operations Readiness Contract Candidate`](./docs/AX-PUB-SEC-001_SDK_SECURITY_OPERATIONS_READINESS_CONTRACT.md)

Current state:

```text
SECURITY OPERATIONS READY: NO
DEDICATED SECURITY CHANNEL: NOT ESTABLISHED
SECURITY RESPONSE OWNER: NOT ASSIGNED / NOT PUBLICLY ESTABLISHED
SECURITY RESPONSE SLA: NOT ESTABLISHED
BUG BOUNTY: NOT ESTABLISHED
SUPPORTED SDK: NOT ESTABLISHED
SDK PUBLICATION: NOT AUTHORIZED
```

`AX-PUB-SEC-001` defines the minimum operating model that must exist before production-supported SDK status can be represented. Its existence does not establish those capabilities today.

---

## Candidate Security Case Lifecycle

The future operating model is intended to support a traceable lifecycle:

```text
RECEIVED
→ TRIAGED
→ VALIDATED OR REJECTED
→ REMEDIATION PLANNED
→ FIX VALIDATED
→ RELEASE OR MITIGATION READY
→ DISCLOSURE / ADVISORY DECIDED
→ CLOSED
```

A production security process must preserve enough evidence to identify the affected version/artifact, severity, remediation or risk decision, fixed/mitigated version where applicable, disclosure state, and closure evidence.

No response-time commitment is created by this candidate lifecycle.

---

## Release and Supply-Chain Incidents

If a report concerns a public release-candidate build, artifact attestation, SBOM, dependency boundary, registry artifact, or release-integrity issue, include the applicable public artifact ID, Git commit, workflow/run identifier, and digest when known.

A material release-path incident should be capable of triggering, subject to proper authority:

- release-promotion freeze;
- identification of exact affected artifact digests;
- source/build/registry provenance verification;
- blocking compromised credential or release-path reuse;
- fixed, withdrawn, or mitigated release action where supported and authorized;
- consumer-safe guidance when material;
- preservation of incident/remediation evidence.

Do not include private-repository material or credentials as public evidence.

---

## Private-Project Separation

Public engineering artifacts must remain separated from private AETHER X project repositories.

Public reference code, schemas, examples, tests, conformance vectors, CI workflows, SDK candidates, and release evidence must not require or expose:

- private repository source;
- private package indexes;
- private endpoints;
- credentials or secrets;
- customer information;
- unpublished research;
- proprietary product algorithms;
- confidential implementation architecture.

---

## Public Reference-Code Boundary

Reference implementations and candidate developer surfaces in this repository are non-production engineering artifacts. Validation, conformance, CI, build-provenance, API-contract, or supply-chain checks do not establish production fitness, product authorization, security certification, or a supported SDK.

`PUBLIC REFERENCE CODE ≠ PRODUCTION SECURITY CONTROL`  
`CI PASS ≠ SECURITY CERTIFICATION`  
`ATTESTED BUILD ≠ SECURITY CERTIFICATION`  
`SECURITY OPERATIONS CONTRACT CANDIDATE ≠ SECURITY OPERATIONS READY`  
`SDK CANDIDATE ≠ SUPPORTED SDK`

---

## Scope

This policy governs only the public `AETHERXGLOBAL/aether-x-governed-intelligence` repository and its intentionally published artifacts. It does not disclose or define the security policy, architecture, response organization, or operational controls of private AETHER X products or systems.

---

**AETHER X GLOBAL — Institutional Intelligence. Governed Autonomy.**
