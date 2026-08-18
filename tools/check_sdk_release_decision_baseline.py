#!/usr/bin/env python3
"""Fail-closed validation for AX-PUB-DEV-007 / DEV-GATE-05A.

This checker validates the release-decision baseline only. It does not establish
an installable package, registry ownership, a software licence grant, human
external evaluation, release authority, or SDK publication.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "AX-PUB-DEV-007.json"


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


def main() -> None:
    data = load()

    require(data.get("artifact_id") == "AX-PUB-DEV-007", "artifact_id must be AX-PUB-DEV-007")
    require(data.get("version") == "0.1", "version must remain 0.1 for this baseline candidate")
    require(data.get("gate") == "DEV-GATE-05", "gate must be DEV-GATE-05")
    require(
        data.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED",
        "publication disposition must remain fail-closed",
    )
    require(data.get("release_authorized") is False, "release_authorized must remain false")

    scope = require_dict(data, "release_scope")
    require(scope.get("mode") == "OFFLINE_VALIDATION_ONLY", "first release scope must remain offline validation only")
    excluded = set(require_list(scope, "excluded"))
    required_exclusions = {
        "network_api",
        "remote_service",
        "credentials",
        "authentication",
        "production_authorization",
        "tool_invocation",
        "real_world_execution",
        "private_repository_dependency",
    }
    require(required_exclusions <= excluded, "offline release scope lost one or more mandatory exclusions")

    licensing = require_dict(data, "licensing")
    require(licensing.get("strategy") == "OPEN_SDK_CONTROLLED_CORE", "licensing strategy changed without a new decision")
    require(licensing.get("target_sdk_license") == "Apache-2.0", "target SDK licence must be Apache-2.0")
    require(licensing.get("license_granted_now") is False, "candidate baseline must not grant a licence")
    require(licensing.get("ip_clearance_required") is True, "IP clearance must remain mandatory")
    require(licensing.get("repository_wide_relicense") is False, "Gate-05 must not relicense the whole repository")
    require(licensing.get("trademark_rights_included") is False, "software licence must not imply trademark rights")

    package = require_dict(data, "package_identity")
    require(
        package.get("distribution_candidate") == "aetherxglobal-governed-intelligence",
        "unexpected distribution identity candidate",
    )
    require(
        package.get("import_namespace") == "aetherxglobal.governed_intelligence",
        "unexpected import namespace",
    )
    require(package.get("canonical_registry") == "PyPI", "canonical Python registry must be PyPI")
    require(package.get("staging_registry") == "TestPyPI", "staging registry must be TestPyPI")
    require(package.get("live_registry_availability_check_required") is True, "live package-name verification must remain required")
    require(
        package.get("aetherx_distribution_name_rejected_due_to_existing_unrelated_project") is True,
        "the ambiguous aetherx distribution name must remain rejected",
    )

    runtime = require_dict(data, "runtime_support_target")
    require(runtime.get("implementation") == "CPython", "initial runtime contract must remain CPython")
    require(
        runtime.get("supported_candidate_versions") == ["3.11", "3.12", "3.13", "3.14"],
        "target runtime set must be exactly CPython 3.11-3.14",
    )
    require(
        runtime.get("python_3_10") == "HISTORICAL_CANDIDATE_EVIDENCE_ONLY_NOT_SELECTED_FOR_NEW_SUPPORT_CONTRACT",
        "Python 3.10 must not silently become part of the new support contract",
    )
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
    security_true = (
        "ci_build_required",
        "build_once_test_exact_artifacts",
        "full_commit_sha_pinning_required_for_release_actions",
        "github_provenance_attestation_required",
        "pypi_trusted_publishing_oidc_required",
        "pypi_digital_attestations_required",
        "protected_pypi_environment_required",
        "human_release_approval_required",
    )
    for key in security_true:
        require(security.get(key) is True, f"release security control {key} must remain required")
    require(
        security.get("long_lived_pypi_token_as_primary_release_credential_allowed") is False,
        "long-lived PyPI token must not become the primary release credential",
    )
    require(
        security.get("pull_request_target_untrusted_release_path_allowed") is False,
        "untrusted pull_request_target release path must remain prohibited",
    )

    controls = require_dict(data, "repository_release_controls")
    for key in (
        "branch_or_ruleset_protection_required",
        "pull_request_required",
        "independent_approval_required",
        "required_status_checks",
        "release_tag_control_required",
        "self_approval_disabled_where_supported",
    ):
        require(controls.get(key) is True, f"repository release control {key} must remain required")
    require(
        controls.get("current_main_protection_sufficient_for_release") is False,
        "current main-branch state must not be represented as release-ready",
    )

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
    require(phases.get("DEV-GATE-05A") == "DECISION_BASELINE_CANDIDATE", "DEV-GATE-05A state mismatch")
    require(phases.get("DEV-GATE-05B") == "NOT_ESTABLISHED", "DEV-GATE-05B must not be promoted yet")
    require(phases.get("DEV-GATE-05C") == "NOT_ESTABLISHED", "DEV-GATE-05C must not be promoted yet")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "DEV-GATE-05D must remain unauthorized")

    blockers = set(require_list(data, "hard_blockers_before_publication"))
    required_blockers = {
        "IP_AND_COPYRIGHT_CLEARANCE",
        "PACKAGE_NAME_LIVE_AVAILABILITY_AND_OWNERSHIP",
        "INSTALLABLE_PACKAGE_CANDIDATE_EVIDENCE",
        "PYTHON_3_11_TO_3_14_PACKAGE_LEVEL_CI",
        "BRANCH_OR_REPOSITORY_RULESET_PROTECTION",
        "PROTECTED_PYPI_RELEASE_ENVIRONMENT",
        "HUMAN_EXTERNAL_EVALUATION",
        "FINAL_RELEASE_EVIDENCE_PACK",
        "EXPLICIT_RELEASE_AUTHORITY",
    }
    require(required_blockers <= blockers, "one or more hard release blockers were removed")

    print("AX_SDK_RELEASE_DECISION_BASELINE_PASS")


if __name__ == "__main__":
    main()
