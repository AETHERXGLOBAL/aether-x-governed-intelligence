#!/usr/bin/env python3
"""Fail-closed validator for AX-PUB-DEV-009 / DEV-GATE-05C baseline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEV007 = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
DEV008 = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
DEV009 = ROOT / "artifacts" / "AX-PUB-DEV-009.json"
DOC = ROOT / "docs" / "AX-PUB-DEV-009_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE.md"
LOCAL_RUNNER = ROOT / "tools" / "run_sdk_local_index_validation.py"
CI009 = ROOT / "evidence" / "AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md"

WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
REQUIRED_BLOCKERS = {
    "IP_AND_COPYRIGHT_CLEARANCE",
    "PACKAGE_NAME_LIVE_AVAILABILITY_AND_OWNERSHIP",
    "BRANCH_OR_REPOSITORY_RULESET_PROTECTION",
    "PROTECTED_PYPI_RELEASE_ENVIRONMENT",
    "AUTHORIZED_CONTROLLED_EXTERNAL_REGISTRY_VALIDATION",
    "HUMAN_EXTERNAL_EVALUATION",
    "FINAL_RELEASE_EVIDENCE_PACK",
    "EXPLICIT_RELEASE_AUTHORITY",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_DEV_GATE_05C_BASELINE_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain an object")
    return data


def main() -> None:
    dev007 = load(DEV007)
    dev008 = load(DEV008)
    dev009 = load(DEV009)

    phases = dev007.get("gate_05_phases")
    require(isinstance(phases, dict), "DEV-007 phase state missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "Gate-05A must remain closed")
    require(phases.get("DEV-GATE-05B") == "CLOSED", "Gate-05B must be closed before Gate-05C")
    require(phases.get("DEV-GATE-05C") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C must be the active engineering objective")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "Gate-05D must remain unauthorized")
    require(dev007.get("release_authorized") is False, "DEV-007 release authority must remain false")
    require(dev007.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "DEV-007 publication boundary changed")

    require(dev008.get("phase_state") == "CLOSED", "DEV-008 must remain closed")
    require(dev008.get("distribution_authorized") is False, "DEV-008 distribution authority changed")
    require(dev008.get("license_granted") is False, "DEV-008 licence boundary changed")
    require(dev008.get("supported_sdk_established") is False, "DEV-008 support boundary changed")

    require(dev009.get("artifact_id") == "AX-PUB-DEV-009", "artifact ID mismatch")
    require(dev009.get("version") == "0.1", "unexpected baseline version")
    require(dev009.get("gate") == "DEV-GATE-05" and dev009.get("phase") == "DEV-GATE-05C", "Gate/phase identity mismatch")
    require(dev009.get("phase_state") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C baseline must remain active, not closed")
    require(dev009.get("parent_artifact") == "AX-PUB-DEV-008", "parent artifact mismatch")
    require(dev009.get("parent_phase_state") == "DEV-GATE-05B CLOSED", "parent phase state mismatch")
    require(dev009.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication must remain unauthorized")
    for key in (
        "external_registry_write_authorized",
        "testpypi_publication_authorized",
        "pypi_publication_authorized",
        "license_granted",
        "supported_sdk_established",
    ):
        require(dev009.get(key) is False, f"{key} must remain false")

    identity = dev009.get("package_identity")
    require(isinstance(identity, dict), "package_identity missing")
    require(identity.get("distribution_candidate") == "aetherxglobal-governed-intelligence", "distribution candidate mismatch")
    require(identity.get("normalized_name") == "aetherxglobal-governed-intelligence", "normalized name mismatch")
    require(identity.get("version_candidate") == "0.1.0rc1", "version candidate mismatch")
    require(identity.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(identity.get("canonical_registry") == "PyPI", "canonical registry mismatch")
    require(identity.get("controlled_external_registry") == "TestPyPI", "controlled registry mismatch")
    require(identity.get("registry_ownership_established") is False, "registry ownership must remain unestablished")
    require(identity.get("registry_name_reserved") is False, "registry name must not be represented as reserved")
    observation = identity.get("availability_observation")
    require(isinstance(observation, dict), "availability observation missing")
    require(observation.get("observation_date") == "2026-08-18", "availability observation date mismatch")
    require(observation.get("exact_project_discovered") is False, "unexpected exact-project discovery state")
    require(observation.get("fresh_recheck_required_immediately_before_any_AUTHORIZED_registry_action") is True, "fresh registry recheck must remain required")
    known = identity.get("known_collision_rejected")
    require(isinstance(known, dict) and known.get("distribution") == "AetherX", "known AetherX collision record missing")

    candidate = dev009.get("validated_candidate_identity")
    require(isinstance(candidate, dict), "validated candidate identity missing")
    require(candidate.get("baseline_commit") == "774abcce340c3fbaf3481ab5244ee1d41b88243c", "Gate-05B published baseline mismatch")
    require(candidate.get("closure_commit") == "b588425a8937293f900f3610d83d40880133fb79", "Gate-05B closure commit mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA, "wheel identity mismatch")
    require(candidate.get("sdist_sha256") == SDIST_SHA, "sdist identity mismatch")
    require(candidate.get("closure_evidence") == "AX-PUB-CI-009", "Gate-05B evidence linkage mismatch")
    require(candidate.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "runtime matrix mismatch")

    distribution = dev009.get("distribution_validation")
    require(isinstance(distribution, dict), "distribution validation state missing")
    require(distribution.get("local_simple_index_simulation") == "REQUIRED_ENGINEERING_EVIDENCE", "local-index engineering evidence must remain required")
    require(distribution.get("local_simple_index_is_external_registry_validation") is False, "local index must not be represented as external validation")
    require(distribution.get("install_from_index_required") is True, "install-from-index validation must remain required")
    require(distribution.get("exact_artifact_hash_verification_required") is True, "exact artifact hashing must remain required")
    require(distribution.get("external_registry_validation_required_for_phase_closure") is True, "external registry validation must remain a closure requirement")
    require(distribution.get("external_registry_validation_state") == "BLOCKED_PENDING_EXPLICIT_AUTHORITY_AND_RELEASE_CONTROLS", "external registry boundary changed")
    require(distribution.get("testpypi_or_equivalent_after_authorization") is True, "authorized TestPyPI/equivalent validation must remain required")
    require(distribution.get("production_pypi_allowed_in_phase_05c") is False, "production PyPI must remain forbidden in Gate-05C")

    evaluation = dev009.get("external_evaluation")
    require(isinstance(evaluation, dict), "external evaluation contract missing")
    require(evaluation.get("minimum_independent_human_evaluators") == 1, "minimum human evaluator count mismatch")
    require(evaluation.get("human_external_evaluation_occurred") is False, "human evaluation must not be pre-claimed")
    require(evaluation.get("external_adoption_established") is False, "external adoption must not be inferred")
    require(evaluation.get("machine_readable_result_required") is True, "machine-readable human evaluation result required")
    require(evaluation.get("issue_disposition_required") is True, "issue disposition must remain required")
    require(evaluation.get("unresolved_critical_allowed") is False, "unresolved critical findings must block closure")
    require(evaluation.get("endorsement_inferred_from_evaluation") is False, "evaluation must not imply endorsement")

    controls = dev009.get("release_controls_observation")
    require(isinstance(controls, dict), "release controls observation missing")
    require(controls.get("observation_date") == "2026-08-18", "release-control observation date mismatch")
    require(controls.get("main_branch_protected") is False, "main must not be falsely represented as protected")
    require(controls.get("required_status_checks_enforced_on_main") is False, "main checks must not be falsely represented as enforced")
    require(controls.get("current_release_controls_sufficient_for_external_registry_write") is False, "external registry controls must remain blocked")
    require(controls.get("protected_pypi_environment_established") is False, "protected PyPI environment must not be pre-claimed")
    require(controls.get("pypi_trusted_publisher_established") is False, "Trusted Publisher must not be pre-claimed")

    prohibited = set(dev009.get("prohibited_without_separate_authority", []))
    for marker in (
        "TESTPYPI_UPLOAD", "PYPI_UPLOAD", "PYPI_PROJECT_RESERVATION_OR_CREATION",
        "SOFTWARE_LICENCE_GRANT", "PUBLIC_SUPPORTED_SDK_CLAIM", "EXTERNAL_ADOPTION_CLAIM",
    ):
        require(marker in prohibited, f"missing prohibited action: {marker}")

    blockers = set(dev009.get("hard_blockers_current", []))
    require(REQUIRED_BLOCKERS <= blockers, "one or more current Gate-05C/release blockers missing")
    require(dev009.get("next_phase_after_closure") == "DEV-GATE-05D — Final Release Authority", "next phase mismatch")

    require(DOC.is_file(), "DEV-009 document missing")
    text = DOC.read_text(encoding="utf-8")
    for token in (
        "DEV-GATE-05C ENGINEERING CANDIDATE",
        "LOCAL INDEX PASS ≠ TESTPYPI PASS",
        "main protected: false",
        WHEEL_SHA,
        SDIST_SHA,
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(token in text, f"DEV-009 document missing marker: {token}")
    require(LOCAL_RUNNER.is_file(), "local-index validation runner missing")
    require(CI009.is_file(), "AX-PUB-CI-009 evidence missing")

    print("AX_DEV_GATE_05C_BASELINE_PASS external_write=false human_evaluation=false sdk_publication=NOT_AUTHORIZED")


if __name__ == "__main__":
    main()
