# ReproCert Consumer Integration

This directory contains the **consumer-side** ReproCert configuration for the public AETHER X Governed Intelligence repository.

It does not contain Governed Intelligence implementation code and does not alter the existing disclosure checker.

## Purpose

The existing public-disclosure checker remains the authoritative executable control:

`tools/check_public_surface.py`

ReproCert wraps that existing control with an additional evidence layer:

```text
existing disclosure checker
        ↓
ReproCert claim
        ↓
evidence hashes + explicit checks
        ↓
certificate
        ↓
acceptance policy
        ↓
signed producer attestation on main
```

## Isolation boundary

This integration intentionally does **not**:

- modify Governed Intelligence product logic;
- expose proprietary source code;
- replace the existing public-disclosure workflow;
- change the repository's licensing boundary;
- treat a ReproCert PASS result as a security, scientific, or production certification.

The ReproCert dependency is pinned by commit SHA in the workflow.

## Source of truth

ReproCert itself is maintained independently at:

https://github.com/AETHERXGLOBAL/reprocert
