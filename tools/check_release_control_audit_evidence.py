#!/usr/bin/env python3
"""Fail-closed integrity check for AX-PUB-CI-011 and its preserved live audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "evidence" / "AX-PUB-RELEASE-CONTROL-AUDIT-001.json"
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-011_RELEASE_CONTROL_LIVE_AUDIT.md"
DOC = ROOT / "docs" / "RELEASE_CONTROL_AUDIT.md"

EXPECTED = {
    "observed_branch_commit": "6b4a067d38ec2f823cadcb7bad51564917cab3ba",
    "reviewed_head_commit": "6f1cd33a2a7f4c3715e51d0b6f8fd18b86b29f98",
    "pull_request_synthetic_merge_commit": "9c71cef3416c58f226995b1756f5464f504583af",
    "workflow_run_id": 32191506412,
    "workflow_run_number": 1,
    "job_id": 95886632381,
    "artifact_id": 9344354547,
    "artifact_sha256": "1d1ced97bd21f5dea68924700c2e1243fc06c037b951b88f69be80f8ef9ff768",
}

MANDATORY_GITHUB_CONTROLS = {
    "branch_protected",
    "pull_request_required",
    "required_status_checks",
    "force_push_blocked",
    "deletion_blocked",
    "pypi_environment_exists",
    "pypi_environment_required_reviewers",
    "pypi_environment_deployment_branch_policy",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_RELEASE_CONTROL_AUDIT_EVIDENCE_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), "audit report must contain a JSON object")
    return value


def require_markers(path: Path, markers: tuple[str, ...]) -> None:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    value = path.read_text(encoding="utf-8")
    for marker in markers:
        require(marker in value, f"{path.relative_to(ROOT)} missing marker: {marker}")


def main() -> int:
    report = load_json(REPORT)

    require(report.get("report_format") == "AX-PUB-RELEASE-CONTROL-AUDIT-001", "report format mismatch")
    require(report.get("report_version") == "1.0", "report version mismatch")
    require(report.get("audit_mode") == "READ_ONLY_GITHUB_API", "audit mode must remain read-only")
    require(report.get("api_version") == "2026-03-10", "GitHub API version mismatch")
    require(report.get("repository") == "AETHERXGLOBAL/aether-x-governed-intelligence", "repository identity mismatch")
    require(report.get("branch") == "main", "branch identity mismatch")
    require(report.get("production_environment") == "pypi", "production environment identity mismatch")
    require(report.get("observed_branch_commit") == EXPECTED["observed_branch_commit"], "observed main commit mismatch")
    require(report.get("github_controls_ready_for_release_promotion") is False, "baseline must remain release-control-not-ready")
    require(report.get("branch_rule_types") == [], "baseline must contain no active branch rule types")
    require(report.get("enabled_repository_rulesets") == [], "baseline must contain no enabled repository rulesets")

    endpoints = report.get("endpoint_status")
    require(isinstance(endpoints, dict), "endpoint_status missing")
    require(endpoints == {
        "branch": 200,
        "branch_rules": 200,
        "environment": 404,
        "legacy_branch_protection": 403,
        "rulesets": 200,
    }, "endpoint observation baseline mismatch")

    controls = report.get("github_controls")
    require(isinstance(controls, dict), "github_controls missing")
    require(set(controls) == MANDATORY_GITHUB_CONTROLS, "unexpected GitHub-control inventory")
    for key in sorted(MANDATORY_GITHUB_CONTROLS):
        require(controls.get(key) == "NOT_ESTABLISHED", f"baseline control {key} must remain NOT_ESTABLISHED")

    legacy = report.get("legacy_branch_protection_observation")
    require(isinstance(legacy, dict), "legacy protection observation missing")
    require(legacy.get("api_state") == "UNVERIFIED", "legacy protection 403 must remain UNVERIFIED")
    require(legacy.get("http_status") == 403, "legacy protection HTTP state mismatch")

    external = report.get("external_controls_not_audited_here")
    require(isinstance(external, dict), "external_controls_not_audited_here missing")
    require(external.get("final_release_authority") == "NOT_AUTHORIZED", "final release authority boundary changed")
    for key in (
        "human_external_evaluation",
        "ip_copyright_clearance",
        "pypi_registry_ownership",
        "pypi_trusted_publisher",
        "software_licence_grant",
    ):
        require(external.get(key) == "UNVERIFIED", f"external control {key} must remain UNVERIFIED in this audit")

    source = report.get("source_ci")
    require(isinstance(source, dict), "source_ci missing")
    for key in (
        "reviewed_head_commit",
        "pull_request_synthetic_merge_commit",
        "workflow_run_id",
        "workflow_run_number",
        "job_id",
        "artifact_id",
        "artifact_sha256",
    ):
        require(source.get(key) == EXPECTED[key], f"source_ci mismatch: {key}")
    require(source.get("workflow") == "Audit Release Control Plane", "workflow name mismatch")
    require(source.get("conclusion") == "SUCCESS", "source workflow must be SUCCESS")

    require_markers(
        EVIDENCE,
        (
            "AX-PUB-CI-011",
            str(EXPECTED["workflow_run_id"]),
            str(EXPECTED["job_id"]),
            EXPECTED["reviewed_head_commit"],
            EXPECTED["pull_request_synthetic_merge_commit"],
            EXPECTED["artifact_sha256"],
            "GITHUB CONTROLS READY FOR RELEASE:          FALSE",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
    )
    require_markers(
        DOC,
        (
            "AX-PUB-RELEASE-CONTROL-AUDIT-001.json",
            "AX-PUB-CI-011",
            "GITHUB CONTROLS READY FOR RELEASE:    FALSE",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
    )

    print(
        "AX_RELEASE_CONTROL_AUDIT_EVIDENCE_PASS "
        "github_ready=false controls=8/8_NOT_ESTABLISHED publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
