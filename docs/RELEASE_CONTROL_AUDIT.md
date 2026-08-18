# AETHER X Governed Intelligence — Live Release-Control Audit

**State:** `READ-ONLY AUDIT MECHANISM · RELEASE CONTROLS MAY REMAIN NOT ESTABLISHED`  
**Tool:** `tools/audit_release_control_plane.py`  
**Workflow:** `.github/workflows/audit-release-control-plane.yml`

## Purpose

The release-control contract must be checked against live platform state rather than inferred from repository documentation.

The auditor performs read-only GitHub API observations and produces:

```text
AX-PUB-RELEASE-CONTROL-AUDIT-001
```

The report covers:

- `main` branch protected state;
- active rules applying to `main`;
- pull-request requirement where observable;
- required status checks where observable;
- force-push/deletion controls where observable;
- repository ruleset inventory;
- existence and protection signals for the `pypi` GitHub Environment;
- exact API endpoint status used for each observation.

The workflow preserves the JSON report as a short-lived GitHub Actions artifact for engineering review.

---

## Fail-closed observation semantics

Every control uses one of:

```text
ESTABLISHED
NOT_ESTABLISHED
UNVERIFIED
NOT_APPLICABLE
```

If the token or public API cannot prove a control, the state is `UNVERIFIED`; it is never promoted to `ESTABLISHED` by assumption.

The command succeeds when the **audit itself completed**. That success does not mean the release control plane is ready.

A later gate may intentionally invoke:

```bash
python3 tools/audit_release_control_plane.py \
  --require-github-controls-ready
```

which fails unless all mandatory GitHub-side controls observed by the tool are established.

---

## External controls outside this audit

The GitHub audit deliberately does not claim to establish:

- PyPI/TestPyPI project ownership;
- PyPI Trusted Publisher configuration;
- software licence grant;
- IP/copyright clearance;
- independent human external evaluation;
- final release authority.

Those states require their own authoritative evidence.

---

## Mutation boundary

The auditor performs HTTP `GET` operations only. The workflow does not:

- create/update/delete branches or rulesets;
- configure branch protection;
- configure a GitHub Environment;
- create a PyPI/TestPyPI project;
- configure a Trusted Publisher;
- upload a package;
- grant a software licence;
- authorize SDK publication.

```text
AUDIT PASS ≠ RELEASE-CONTROL READY
RELEASE-CONTROL READY ≠ PYPI AUTHORIZED
SDK PUBLICATION NOT AUTHORIZED
```
