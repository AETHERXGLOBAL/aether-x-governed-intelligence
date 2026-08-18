#!/usr/bin/env python3
"""Fail-closed validation for AX-PUB-DEV-007 / DEV-GATE-05A.

DEV-GATE-05A remains permanently closed once AX-PUB-CI-008 is established.
Later phase progression is accepted only through evidence-backed states: either
05B is the active engineering objective, or 05B is closed by AX-PUB-CI-009 and
05C becomes active. Nothing here grants registry ownership, a software licence,
a supported SDK, release authority or SDK publication.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
EXPECTED_EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md"
PACKAGE_EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_RELEASE_DECISION_BASELINE_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load() -> dict[str, Any]:
    require(ARTIFACT.is_file(), "AX-PUB-DEV-007 machine-readable artifact is missing")
    try:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse AX-PUB-DEV-007: {exc}")
    require(isinstance(data, dict), "AX-PUB-DEV-007 must be a JSON object")
    return data


def require_dict(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    require(isinstance(value, dict), f"{key} must be an object")
    return value


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    require(isinstance(value, list), f"{key} must be an array")
    return value


def check_gate05a_closure(data: dict[str, Any]) -> None:
    closure = require_dict(data, "closure_evidence")
    require(closure.get("id") == "AX-PUB-CI-008", "closed Gate-05A must cite AX-PUB-CI-008")
    require(closure.get("version") == "1.0", "closure evidence version mismatch")
    require(closure.get("path") == "evidence/AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md", "closure evidence path mismatch")
    require(closure.get("validated_base_commit") == "fa1e2d132071ddff195fb998d0d27a6b5b9d4e40", "validated base commit mismatch")
    require(closure.get("verified_head_commit") == "7877abceda8fa6a372300fceb1ae0c124853d2b6", "verified head commit mismatch")
    require(closure.get("verification_pr") == 31, "verification PR mismatch")
    require(closure.get("workflow_run_id") == 32168696722, "Gate-05A workflow run mismatch")
    require(closure.get("governance_workflow_run_id") == 32168696655, "governance workflow run mismatch")
    require(closure.get("conclusion") == "SUCCESS", "closure evidence must be SUCCESS")
    require(closure.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "verified runtime matrix mismatch")
    require(EXPECTED_EVIDENCE.is_file(), "AX-PUB-CI-008 evidence file is missing")
    evidence_text = EXPECTED_EVIDENCE.read_text(encoding="utf-8")
    for token in (
        "AX-PUB-CI-008",
        "32168696722",
        "32168696655",
        "95814358240",
        "95814357868",
        "95814357940",
        "95814358020",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(token in evidence_text, f"closure evidence file missing token: {token}")


def check_gate05b_closure(data: dict[str, Any]) -> None:
    package = require_dict(data, "installable_package_closure_evidence")
    expected = {
        "id": "AX-PUB-CI-009",
        "version": "1.0",
        "path": "evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md",
        "published_baseline_commit": "774abcce340c3fbaf3481ab5244ee1d41b88243c",
        "verification_head_commit": "63477bb11124aebbad4034587a366d5ef882b3c2",
        "verification_merge_commit": "3267c66681e417bf5eb0f8a384e8c2d992d266c0",
        "verification_pr": 36,
        "workflow_run_id": 32171606094,
        "workflow_run_number": 19,
        "job_id": 95823835258,
        "governance_workflow_run_id": 32171606079,
        "governance_workflow_run_number": 168,
        "conclusion": "SUCCESS",
    }
    for key, value in expected.items():
        require(package.get(key) == value, f"Gate-05B closure evidence mismatch for {key}")
    require(package.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "Gate-05B verified runtime matrix mismatch")
    require(PACKAGE_EVIDENCE.is_file(), "AX-PUB-CI-009 evidence file is missing")


def main() -> None:
    data = load()

    require(data.get("artifact_id") == "AX-PUB-DEV-007", "artifact_id must be AX-PUB-DEV-007")
    require(data.get("version") == "0.1", "version must remain 0.1 for this baseline")
    require(data.get("gate") == "DEV-GATE-05", "gate must be DEV-GATE-05")
    require(data.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication disposition must remain fail-closed")
    require(data.get("release_authorized") is False, "release_authorized must remain false")

    scope = require_dict(data, "release_scope")
    require(scope.get("mode") == "OFFLINE_VALIDATION_ONLY", "first release scope must remain offline validation only")
    excluded = set(require_list(scope, "excluded"))
    required_exclusions = {
        "network_api", "remote_service", "credentials", "authentication",
        "production_authorization", "tool_invocation", "real_world_execution",
        "private_repository_dependency",
    }
    require(required_exclusions <= excluded, "offline release scope lost one or more mandatory exclusions")

    licensing = require_dict(data, "licensing")
    require(licensing.get("strategy") == "OPEN_SDK_CONTROLLED_CORE", "licensing strategy changed without a new decision")
    require(licensing.get("target_sdk_license") == "Apache-2.0", "target SDK licence must be Apache-2.0")
    require(licensing.get("license_granted_now") is False, "Gate-05A must not grant a licence")
    require(licensing.get("ip_clearance_required") is True, "IP clearance must remain mandatory")
    require(licensing.get("repository_wide_relicense") is False, "Gate-05 must not relicense the whole repository")
    require(licensing.get("trademark_rights_included") is False, "software licence must not imply trademark rights")

    package = require_dict(data, "package_identity")
    require(package.get("distribution_candidate") == "aetherxglobal-governed-intelligence", "unexpected distribution identity candidate")
    require(package.get("import_namespace") == "aetherxglobal.governed_intelligence", "unexpected import namespace")
    require(package.get("canonical_registry") == "PyPI", "canonical Python registry must be PyPI")
    require(package.get("staging_registry") == "TestPyPI", "staging registry must be TestPyPI")
    require(package.get("live_registry_availability_check_required") is True, "live package-name verification must remain required")
    require(package.get("aetherx_distribution_name_rejected_due_to_existing_unrelated_project") is True, "the ambiguous aetherx distribution name must remain rejected")

    runtime = require_dict(data, "runtime_support_target")
    require(runtime.get("implementation") == "CPython", "initial runtime contract must remain CPython")
    require(runtime.get("supported_candidate_versions") == ["3.11", "3.12", "3.13", "3.14"], "target runtime set must be exactly CPython 3.11-3.14")
    require(runtime.get("python_3_10") == "HISTORICAL_CANDIDATE_EVIDENCE_ONLY_NOT_SELECTED_FOR_NEW_SUPPORT_CONTRACT", "Python 3.10 must not silently become part of the new support contract")
    require(runtime.get("python_3_15") == "PRE_RELEASE_NOT_SUPPORTED", "Python 3.15 must remain unsupported while pre-release")

    versioning = require_dict(data, "versioning")
    require(versioning.get("standard") == "PEP 440", "package versions must follow PEP 440")
    require(versioning.get("first_distributable_candidate") == "0.1.0rc1", "first package RC must be 0.1.0rc1")
    require(versioning.get("first_public_release_if_authorized") == "0.1.0", "first authorized public release must be 0.1.0")
    require(versioning.get("stable_1_0_requires_separate_decision") is True, "1.0 stability must require a separate decision")

    architecture = require_dict(data, "package_architecture")
    require(architecture.get("layout") == "src", "release candidate must use src layout")
    require(architecture.get("runtime_third_party_dependency_target") == 0, "v0.1 runtime dependency target must remain zero")
    require(architecture.get("repository_relative_runtime_imports_allowed") is False, "installed package must be repository-independent")
    require(architecture.get("build_metadata") == "pyproject.toml / PEP 621", "package metadata must use pyproject.toml / PEP 621")

    security = require_dict(data, "release_security")
    for key in (
        "ci_build_required", "build_once_test_exact_artifacts",
        "full_commit_sha_pinning_required_for_release_actions",
        "github_provenance_attestation_required", "pypi_trusted_publishing_oidc_required",
        "pypi_digital_attestations_required", "protected_pypi_environment_required",
        "human_release_approval_required",
    ):
        require(security.get(key) is True, f"release security control {key} must remain required")
    require(security.get("long_lived_pypi_token_as_primary_release_credential_allowed") is False, "long-lived PyPI token must not become the primary release credential")
    require(security.get("pull_request_target_untrusted_release_path_allowed") is False, "untrusted pull_request_target release path must remain prohibited")

    controls = require_dict(data, "repository_release_controls")
    for key in (
        "branch_or_ruleset_protection_required", "pull_request_required",
        "independent_approval_required", "required_status_checks",
        "release_tag_control_required", "self_approval_disabled_where_supported",
    ):
        require(controls.get(key) is True, f"repository release control {key} must remain required")
    require(controls.get("current_main_protection_sufficient_for_release") is False, "current main-branch state must not be represented as release-ready")

    evaluation = require_dict(data, "external_evaluation")
    require(evaluation.get("required_before_0_1_0") is True, "human external evaluation must remain a 0.1.0 prerequisite")
    require(evaluation.get("minimum_independent_human_evaluators") >= 1, "at least one independent human evaluator is required")
    require(evaluation.get("machine_readable_result_required") is True, "machine-readable external evaluation result is required")
    require(evaluation.get("unresolved_critical_allowed") is False, "unresolved critical findings must block release")

    maintenance = require_dict(data, "maintenance")
    require(maintenance.get("commercial_sla_implied") is False, "initial public SDK must not imply a commercial SLA")
    require(maintenance.get("previous_minor_security_correctness_window_days") == 90, "previous-minor maintenance window changed")
    require(maintenance.get("private_product_integration_support_implied") is False, "SDK support must not imply private-product support")

    phases = require_dict(data, "gate_05_phases")
    phase_a = phases.get("DEV-GATE-05A")
    require(phase_a in {"DECISION_BASELINE_CANDIDATE", "CLOSED"}, "DEV-GATE-05A state mismatch")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "DEV-GATE-05D must remain unauthorized")

    if phase_a == "DECISION_BASELINE_CANDIDATE":
        require(data.get("verification_state") in {"PR_VALIDATION_PENDING", "CI_PENDING"}, "candidate verification state mismatch")
        require(phases.get("DEV-GATE-05B") == "NOT_ESTABLISHED", "DEV-GATE-05B must not be promoted before Gate-05A closure")
        require(phases.get("DEV-GATE-05C") == "NOT_ESTABLISHED", "DEV-GATE-05C must not be promoted before Gate-05A closure")
        marker = "AX_SDK_RELEASE_DECISION_BASELINE_PASS"
    else:
        require(data.get("verification_state") == "DIRECT_CI_VALIDATED", "closed Gate-05A requires direct CI validation")
        check_gate05a_closure(data)
        b_state = phases.get("DEV-GATE-05B")
        require(b_state in {"ACTIVE_ENGINEERING_OBJECTIVE", "CLOSED"}, "closed Gate-05A has invalid Gate-05B progression")
        if b_state == "ACTIVE_ENGINEERING_OBJECTIVE":
            require(phases.get("DEV-GATE-05C") == "NOT_ESTABLISHED", "active Gate-05B must not pre-promote Gate-05C")
            require(data.get("next_phase") == "DEV-GATE-05B — Installable Package Candidate", "next phase mismatch")
        else:
            require(phases.get("DEV-GATE-05C") == "ACTIVE_ENGINEERING_OBJECTIVE", "closed Gate-05B must advance Gate-05C")
            require(data.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "Gate-05C next phase mismatch")
            check_gate05b_closure(data)
        marker = "AX_SDK_RELEASE_DECISION_BASELINE_CLOSED_STATE_PASS"

    blockers = set(require_list(data, "hard_blockers_before_publication"))
    always_required = {
        "IP_AND_COPYRIGHT_CLEARANCE",
        "PACKAGE_NAME_LIVE_AVAILABILITY_AND_OWNERSHIP",
        "BRANCH_OR_REPOSITORY_RULESET_PROTECTION",
        "PROTECTED_PYPI_RELEASE_ENVIRONMENT",
        "HUMAN_EXTERNAL_EVALUATION",
        "FINAL_RELEASE_EVIDENCE_PACK",
        "EXPLICIT_RELEASE_AUTHORITY",
    }
    require(always_required <= blockers, "one or more unresolved hard release blockers were removed")

    if phase_a == "CLOSED" and phases.get("DEV-GATE-05B") == "CLOSED":
        require("INSTALLABLE_PACKAGE_CANDIDATE_EVIDENCE" not in blockers, "resolved package evidence must not remain a hard blocker")
        require("PYTHON_3_11_TO_3_14_PACKAGE_LEVEL_CI" not in blockers, "resolved runtime CI must not remain a hard blocker")
        resolved = set(require_list(data, "resolved_release_prerequisites"))
        require({"RELEASE_DECISION_BASELINE", "INSTALLABLE_PACKAGE_CANDIDATE_EVIDENCE", "PYTHON_3_11_TO_3_14_PACKAGE_LEVEL_CI"} <= resolved, "resolved prerequisite ledger incomplete")
    elif phase_a == "CLOSED":
        require({"INSTALLABLE_PACKAGE_CANDIDATE_EVIDENCE", "PYTHON_3_11_TO_3_14_PACKAGE_LEVEL_CI"} <= blockers, "pre-closure Gate-05B blockers missing")

    print(marker)


if __name__ == "__main__":
    main()
