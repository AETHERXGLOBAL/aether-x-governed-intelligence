#!/usr/bin/env python3
"""Read-only live audit of GitHub release controls for the public SDK repository.

The auditor performs GET requests only. It does not create or modify branch
protection, rulesets, environments, releases, registry projects, trusted
publishers, licences, or package artifacts.

A successful audit means the observation completed. It does NOT mean the
release control plane is ready. Use --require-github-controls-ready only when a
later gate intentionally requires the observed GitHub controls to be ready.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_VERSION = "2026-03-10"
REPORT_FORMAT = "AX-PUB-RELEASE-CONTROL-AUDIT-001"
REPORT_VERSION = "1.0"
DEFAULT_REPOSITORY = "AETHERXGLOBAL/aether-x-governed-intelligence"
DEFAULT_BRANCH = "main"
DEFAULT_ENVIRONMENT = "pypi"

ESTABLISHED = "ESTABLISHED"
NOT_ESTABLISHED = "NOT_ESTABLISHED"
UNVERIFIED = "UNVERIFIED"
NOT_APPLICABLE = "NOT_APPLICABLE"


def state(value: bool | None) -> str:
    if value is True:
        return ESTABLISHED
    if value is False:
        return NOT_ESTABLISHED
    return UNVERIFIED


def as_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def api_get(api_url: str, path: str, token: str | None) -> dict[str, Any]:
    url = f"{api_url.rstrip('/')}/{path.lstrip('/')}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "aether-x-release-control-auditor/1.0",
        "X-GitHub-Api-Version": API_VERSION,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
            payload: Any = json.loads(raw) if raw else None
            return {"http_status": int(response.status), "ok": True, "payload": payload}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            payload = {"message": raw[-1000:]}
        return {"http_status": int(exc.code), "ok": False, "payload": payload}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"http_status": None, "ok": False, "payload": {"message": str(exc)}}


def rule_types(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    values = {
        item.get("type")
        for item in payload
        if isinstance(item, dict) and isinstance(item.get("type"), str)
    }
    return sorted(values)


def enabled_rulesets(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    result: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        enforcement = str(item.get("enforcement", "")).lower()
        if enforcement not in {"active", "enabled"}:
            continue
        result.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "source_type": item.get("source_type"),
                "source": item.get("source"),
                "enforcement": item.get("enforcement"),
            }
        )
    return result


def protection_summary(response: dict[str, Any]) -> dict[str, Any]:
    if not response.get("ok"):
        return {
            "api_state": UNVERIFIED if response.get("http_status") == 403 else NOT_ESTABLISHED if response.get("http_status") == 404 else UNVERIFIED,
            "http_status": response.get("http_status"),
            "required_status_checks": UNVERIFIED,
            "pull_request_reviews": UNVERIFIED,
            "dismiss_stale_reviews": UNVERIFIED,
            "force_push_blocked": UNVERIFIED,
            "deletion_blocked": UNVERIFIED,
            "conversation_resolution": UNVERIFIED,
        }

    payload = response.get("payload")
    if not isinstance(payload, dict):
        return {
            "api_state": UNVERIFIED,
            "http_status": response.get("http_status"),
            "required_status_checks": UNVERIFIED,
            "pull_request_reviews": UNVERIFIED,
            "dismiss_stale_reviews": UNVERIFIED,
            "force_push_blocked": UNVERIFIED,
            "deletion_blocked": UNVERIFIED,
            "conversation_resolution": UNVERIFIED,
        }

    reviews = payload.get("required_pull_request_reviews")
    status_checks = payload.get("required_status_checks")
    allow_force = payload.get("allow_force_pushes")
    allow_delete = payload.get("allow_deletions")
    conversation = payload.get("required_conversation_resolution")

    return {
        "api_state": ESTABLISHED,
        "http_status": response.get("http_status"),
        "required_status_checks": state(isinstance(status_checks, dict)),
        "pull_request_reviews": state(isinstance(reviews, dict)),
        "dismiss_stale_reviews": state(reviews.get("dismiss_stale_reviews") if isinstance(reviews, dict) else None),
        "force_push_blocked": state(not allow_force.get("enabled") if isinstance(allow_force, dict) and isinstance(allow_force.get("enabled"), bool) else None),
        "deletion_blocked": state(not allow_delete.get("enabled") if isinstance(allow_delete, dict) and isinstance(allow_delete.get("enabled"), bool) else None),
        "conversation_resolution": state(conversation.get("enabled") if isinstance(conversation, dict) else None),
    }


def environment_summary(response: dict[str, Any]) -> dict[str, Any]:
    if not response.get("ok"):
        status = response.get("http_status")
        return {
            "existence": NOT_ESTABLISHED if status == 404 else UNVERIFIED,
            "http_status": status,
            "required_reviewers": UNVERIFIED if status != 404 else NOT_ESTABLISHED,
            "deployment_branch_policy": UNVERIFIED if status != 404 else NOT_ESTABLISHED,
        }

    payload = response.get("payload")
    if not isinstance(payload, dict):
        return {
            "existence": UNVERIFIED,
            "http_status": response.get("http_status"),
            "required_reviewers": UNVERIFIED,
            "deployment_branch_policy": UNVERIFIED,
        }

    rules = payload.get("protection_rules")
    rule_types_found = {
        item.get("type")
        for item in rules
        if isinstance(rules, list) and isinstance(item, dict) and isinstance(item.get("type"), str)
    }
    branch_policy = payload.get("deployment_branch_policy")
    return {
        "existence": ESTABLISHED,
        "http_status": response.get("http_status"),
        "required_reviewers": state("required_reviewers" in rule_types_found),
        "deployment_branch_policy": state(isinstance(branch_policy, dict)),
        "protection_rule_types": sorted(rule_types_found),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY", DEFAULT_REPOSITORY))
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--environment", default=DEFAULT_ENVIRONMENT)
    parser.add_argument("--api-url", default=os.getenv("GITHUB_API_URL", "https://api.github.com"))
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--require-github-controls-ready", action="store_true")
    args = parser.parse_args()

    if "/" not in args.repository:
        print("AX_RELEASE_CONTROL_AUDIT_FAIL: repository must be OWNER/REPO", file=sys.stderr)
        return 2
    owner, repo = args.repository.split("/", 1)
    owner_q = urllib.parse.quote(owner, safe="")
    repo_q = urllib.parse.quote(repo, safe="")
    branch_q = urllib.parse.quote(args.branch, safe="")
    env_q = urllib.parse.quote(args.environment, safe="")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

    branch = api_get(args.api_url, f"repos/{owner_q}/{repo_q}/branches/{branch_q}", token)
    branch_rules = api_get(args.api_url, f"repos/{owner_q}/{repo_q}/rules/branches/{branch_q}", token)
    rulesets = api_get(args.api_url, f"repos/{owner_q}/{repo_q}/rulesets?includes_parents=true&targets=branch,tag&per_page=100", token)
    protection = api_get(args.api_url, f"repos/{owner_q}/{repo_q}/branches/{branch_q}/protection", token)
    environment = api_get(args.api_url, f"repos/{owner_q}/{repo_q}/environments/{env_q}", token)

    branch_payload = branch.get("payload")
    branch_protected = None
    commit_sha = None
    if branch.get("ok") and isinstance(branch_payload, dict):
        branch_protected = as_bool(branch_payload.get("protected"))
        commit = branch_payload.get("commit")
        if isinstance(commit, dict) and isinstance(commit.get("sha"), str):
            commit_sha = commit["sha"]

    active_rules = rule_types(branch_rules.get("payload")) if branch_rules.get("ok") else []
    legacy = protection_summary(protection)
    env = environment_summary(environment)

    pr_rule = "pull_request" in active_rules
    checks_rule = "required_status_checks" in active_rules
    non_fast_forward_rule = "non_fast_forward" in active_rules
    deletion_rule = "deletion" in active_rules

    pull_request_required = ESTABLISHED if pr_rule else legacy["pull_request_reviews"] if branch_protected else NOT_ESTABLISHED if branch_protected is False else UNVERIFIED
    status_checks_required = ESTABLISHED if checks_rule else legacy["required_status_checks"] if branch_protected else NOT_ESTABLISHED if branch_protected is False else UNVERIFIED
    force_push_blocked = ESTABLISHED if non_fast_forward_rule else legacy["force_push_blocked"] if branch_protected else NOT_ESTABLISHED if branch_protected is False else UNVERIFIED
    deletion_blocked = ESTABLISHED if deletion_rule else legacy["deletion_blocked"] if branch_protected else NOT_ESTABLISHED if branch_protected is False else UNVERIFIED

    github_controls = {
        "branch_protected": state(branch_protected),
        "pull_request_required": pull_request_required,
        "required_status_checks": status_checks_required,
        "force_push_blocked": force_push_blocked,
        "deletion_blocked": deletion_blocked,
        "pypi_environment_exists": env["existence"],
        "pypi_environment_required_reviewers": env["required_reviewers"],
        "pypi_environment_deployment_branch_policy": env["deployment_branch_policy"],
    }
    mandatory = (
        "branch_protected",
        "pull_request_required",
        "required_status_checks",
        "force_push_blocked",
        "deletion_blocked",
        "pypi_environment_exists",
        "pypi_environment_required_reviewers",
        "pypi_environment_deployment_branch_policy",
    )
    github_ready = all(github_controls[key] == ESTABLISHED for key in mandatory)

    report = {
        "report_format": REPORT_FORMAT,
        "report_version": REPORT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_mode": "READ_ONLY_GITHUB_API",
        "api_version": API_VERSION,
        "repository": args.repository,
        "branch": args.branch,
        "observed_branch_commit": commit_sha,
        "production_environment": args.environment,
        "github_controls_ready_for_release_promotion": github_ready,
        "github_controls": github_controls,
        "branch_rule_types": active_rules,
        "enabled_repository_rulesets": enabled_rulesets(rulesets.get("payload")) if rulesets.get("ok") else [],
        "legacy_branch_protection_observation": legacy,
        "environment_observation": env,
        "endpoint_status": {
            "branch": branch.get("http_status"),
            "branch_rules": branch_rules.get("http_status"),
            "rulesets": rulesets.get("http_status"),
            "legacy_branch_protection": protection.get("http_status"),
            "environment": environment.get("http_status"),
        },
        "external_controls_not_audited_here": {
            "pypi_registry_ownership": UNVERIFIED,
            "pypi_trusted_publisher": UNVERIFIED,
            "software_licence_grant": UNVERIFIED,
            "ip_copyright_clearance": UNVERIFIED,
            "human_external_evaluation": UNVERIFIED,
            "final_release_authority": "NOT_AUTHORIZED",
        },
        "claim_boundaries": [
            "AUDIT PASS MEANS OBSERVATION COMPLETED; IT DOES NOT MEAN RELEASE CONTROLS ARE READY",
            "GITHUB CONTROL READINESS DOES NOT ESTABLISH PYPI TRUSTED PUBLISHER OR REGISTRY OWNERSHIP",
            "GITHUB CONTROL READINESS DOES NOT GRANT A SOFTWARE LICENCE",
            "GITHUB CONTROL READINESS DOES NOT ESTABLISH A SUPPORTED SDK",
            "SDK PUBLICATION NOT AUTHORIZED",
        ],
    }

    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    print(
        "AX_RELEASE_CONTROL_AUDIT_PASS "
        f"branch_protected={github_controls['branch_protected']} "
        f"required_checks={github_controls['required_status_checks']} "
        f"pypi_environment={github_controls['pypi_environment_exists']} "
        f"github_ready={str(github_ready).lower()} publication=NOT_AUTHORIZED"
    )

    if args.require_github_controls_ready and not github_ready:
        print("AX_RELEASE_CONTROL_READY_FAIL: mandatory GitHub release controls are not all established", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
