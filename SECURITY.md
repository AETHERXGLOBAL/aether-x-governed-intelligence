# Security Policy

## Public Reporting Boundary

This repository contains public, non-production reference material. It must not be used to disclose credentials, private customer information, confidential architecture, proprietary implementation details, private research records, or exploit information that could increase operational risk.

If you believe you have identified a security issue related to AETHER X GLOBAL, **do not publish sensitive details in a public GitHub issue, discussion, pull request, or commit**.

Use the official institutional contact channels available through:

**https://www.aetherxglobal.com**

Until a dedicated vulnerability-disclosure channel is formally published, the company website is the authoritative public contact entry point.

## Private-Project Separation

Public engineering artifacts must remain separated from private AETHER X project repositories.

Public reference code, schemas, examples, tests, conformance vectors and CI workflows must not require or expose:

- checkout or runtime access to private project repositories;
- private-repository tokens or credentials;
- private customer or partner data;
- unpublished research records;
- proprietary product source code or algorithms;
- confidential internal endpoints, deployment topology or implementation architecture;
- private data-source credentials or restricted datasets.

The public conformance suites include fail-closed boundary checks intended to detect selected private-repository references and private-access markers before executing their public test vectors. The agent-authority conformance path is additionally constrained to its public validator and synthetic public baseline.

`PUBLIC ENGINEERING ≠ PRIVATE PRODUCT IMPLEMENTATION`

`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

`AGENT AUTHORITY REFERENCE ≠ PRODUCTION AUTHORIZATION`

## Scope of This Repository

The code under `reference-implementations/` is explicitly **educational / non-production**. A defect in a reference validator should not be interpreted as evidence of a vulnerability in any private AETHER X product, and a passing validator or conformance result is not a security certification or authority grant.

Machine-readable authority objects published here are structural/reference artifacts only. They are not credentials, real permissions, production authorization records, or evidence of an internal AETHER X authorization plane.

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SECURITY CONTROL`

`CONFORMANCE PASS ≠ SECURITY CERTIFICATION`

`MACHINE-READABLE AUTHORITY ≠ LIVE AUTHORITY`

---

**AETHER X GLOBAL**
