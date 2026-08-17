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

The public conformance workflow includes a fail-closed boundary check intended to detect selected private-repository references and private-access markers before executing the public test kit.

`PUBLIC ENGINEERING ≠ PRIVATE PRODUCT IMPLEMENTATION`

`PUBLIC TEST VECTOR ≠ PRIVATE PROJECT DATA`

## Scope of This Repository

The code under `reference-implementations/` is explicitly **educational / non-production**. A defect in a reference validator should not be interpreted as evidence of a vulnerability in any private AETHER X product, and a passing validator or conformance result is not a security certification.

`REFERENCE IMPLEMENTATION ≠ PRODUCTION SECURITY CONTROL`

`CONFORMANCE PASS ≠ SECURITY CERTIFICATION`

---

**AETHER X GLOBAL**
