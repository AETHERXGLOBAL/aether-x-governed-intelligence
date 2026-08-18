# AETHER X Governed Intelligence — Installable Package External Evaluator Guide

`DEV-GATE-05C CANDIDATE · INDEPENDENT HUMAN EVALUATION CONTRACT · SDK PUBLICATION NOT AUTHORIZED`

## Purpose

This guide is for an independent technical evaluator reviewing the exact Gate-05B installable package candidate.

You are **not** being asked to endorse AETHER X, adopt the SDK, test a production service or evaluate any private AETHER X product.

## Exact Candidate

```text
Distribution: aetherxglobal-governed-intelligence
Version:      0.1.0rc1
Wheel SHA-256:
bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac

Source distribution SHA-256:
2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99

Declared evaluation runtimes:
CPython 3.11 / 3.12 / 3.13 / 3.14
```

Do not evaluate a package with a different digest and report it as this candidate.

## Installation Source

Gate-05C closure requires an explicitly authorized controlled external distribution path. Until AETHER X separately provides that authorized index location, **do not infer that TestPyPI or PyPI publication exists**.

If an authorized evaluation index is later supplied, record its exact URL/domain and the artifact digests actually installed.

## Evaluation Objectives

Evaluate, at minimum:

1. installation from the supplied controlled index;
2. package/version identity;
3. import of `aetherxglobal.governed_intelligence`;
4. declared contract inventory;
5. valid-input behavior;
6. fail-closed invalid-input behavior;
7. unsupported contract/version behavior;
8. clarity of errors/findings;
9. absence of unexpected network/credential requirements for the declared offline scope;
10. documentation clarity and material limitations.

You may perform additional non-destructive technical review within the public package/repository scope.

## Required Evaluation Record

Use the `AX-PUB-EVAL-REPORT-002` template and record:

- evaluator identity or bounded evaluator identifier;
- whether the evaluator is independent of the implementation work;
- date/time;
- operating system/platform;
- Python runtime;
- installation source;
- exact wheel/sdist digest where applicable;
- each check and result;
- findings with severity and reproduction detail;
- overall result;
- issue/finding disposition state.

A report with placeholder evaluator identity, missing artifact digest or `record_state=TEMPLATE` is **not** human external evaluation evidence.

## Severity

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

An unresolved `CRITICAL` finding blocks Gate-05C closure. A `HIGH` finding requires a fix or explicit authorized risk acceptance before closure.

## Sensitive Findings

Do not publish secrets, credentials, personal data or exploitable security details in a public issue. Use the repository security reporting process for sensitive findings.

## Claim Boundary

A successful evaluation may establish only that the named evaluator reproduced or reviewed the declared bounded package path in the recorded environment.

It does not establish:

- security certification;
- standards certification;
- production readiness;
- product integration;
- customer adoption;
- endorsement;
- support SLA;
- software reuse permission;
- SDK publication authority.

`EVALUATION ≠ ENDORSEMENT`  
`EVALUATION ≠ ADOPTION`  
`EVALUATION PASS ≠ RELEASE AUTHORITY`  
`SDK PUBLICATION NOT AUTHORIZED`
