#!/usr/bin/env python3
"""Fail-closed consistency check for the AETHER X production-SDK productization target.

This checker validates repository-declared engineering state only. It does not
establish live GitHub branch protection, PyPI ownership, Trusted Publishing,
software licence authority, human external evaluation, support activation,
security-operations readiness, release-owner accountability or release authority.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV009 = ROOT / "artifacts" / "AX-PUB-DEV-009.json"
API001 = ROOT / "artifacts" / "AX-PUB-API-001.json"
SUP001 = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC001 = ROOT / "artifacts" / "AX-PUB-SEC-001.json"
RELPACK = ROOT / "artifacts" / "AX-PUB-RELPACK-001.json"
QUICKSTART = ROOT / "docs" / "QUICKSTART.md"
CURRENT = ROOT / "docs" / "PUBLIC_ENGINEERING_STATE.md"
DOD = ROOT / "docs" / "PRODUCTION_SDK_DEFINITION_OF_DONE.md"
CONTROL = ROOT / "docs" / "RELEASE_CONTROL_PLANE.md"
CI010 = ROOT / "evidence" / "AX-PUB-CI-010_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE_VALIDATION.md"
CI011 = ROOT / "evidence" / "AX-PUB-CI-011_RELEASE_CONTROL_LIVE_AUDIT.md"
CI012 = ROOT / "evidence" / "AX-PUB-CI-012_SDK_PUBLIC_API_CONTRACT_VALIDATION.md"
CI013 = ROOT / "evidence" / "AX-PUB-CI-013_SDK_SUPPORT_SECURITY_CONTRACT_VALIDATION.md"
CI016 = ROOT / "evidence" / "AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md"

PROJECT = "aetherxglobal-governed-intelligence"
IMPORT = "aetherxglobal.governed_intelligence"
VERSION = "0.1.0rc1"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]
GATE03_DIGEST = "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21"
RELPACK_ACTIONS_SHA = "e9614ca5b70667e6d2218d1f19c764ce2cf09ada13764282c5758cf1865fa331"


def fail(message: str) -> None:
    raise SystemExit(f"AX_PRODUCTION_SDK_TARGET_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value


def text(path: Path) -> str:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    require(isinstance(raw, str), "manifest_version must be a string")
    try:
        parts = raw.split("-", 1)[0].split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        fail(f"invalid manifest_version: {raw!r}")


def evidence_by_id(manifest: dict[str, Any], evidence_id: str) -> dict[str, Any]:
    raw = manifest.get("validation_evidence")
    require(isinstance(raw, list), "manifest validation_evidence missing")
    matches = [item for item in raw if isinstance(item, dict) and item.get("id") == evidence_id]
    require(len(matches) == 1, f"manifest must contain exactly one {evidence_id} evidence record")
    return matches[0]


def main() -> int:
    manifest = load_json(MANIFEST)
    dev009 = load_json(DEV009)
    api001 = load_json(API001)
    sup001 = load_json(SUP001)
    sec001 = load_json(SEC001)
    relpack = load_json(RELPACK)
    quickstart = text(QUICKSTART)
    current = text(CURRENT)
    dod = text(DOD)
    control = text(CONTROL)
    ci010 = text(CI010)
    ci011 = text(CI011)
    ci012 = text(CI012)
    ci013 = text(CI013)
    ci016 = text(CI016)

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 26), "manifest must be >= v1.26")

    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current_developer_program missing")
    require(program.get("active_gate") == "DEV-GATE-05 — SDK Release Decision", "Gate-05 must remain active")
    require(program.get("closed_phase") == "DEV-GATE-05B — Installable Package Candidate", "Gate-05B closure missing")
    require(program.get("active_phase") == "DEV-GATE-05C — Distribution & External Validation", "Gate-05C must remain active")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication boundary changed")

    current_dist = manifest.get("current_distribution_external_validation")
    require(isinstance(current_dist, dict), "current_distribution_external_validation missing")
    require(current_dist.get("local_index_validation") == "VERIFIED_LOCAL_ONLY", "local-index validation must be verified local-only")
    require(current_dist.get("local_index_validation_evidence") == "AX-PUB-CI-010", "CI-010 linkage missing")
    require(current_dist.get("external_registry_validation") == "NOT_AUTHORIZED", "external registry boundary changed")
    require(current_dist.get("human_external_evaluation_occurred") is False, "human evaluation must not be pre-claimed")
    require(current_dist.get("registry_ownership_established") is False, "registry ownership must not be pre-claimed")
    require(current_dist.get("main_release_protection_established") is False, "release protection must not be pre-claimed")

    release_audit = manifest.get("current_release_control_audit")
    require(isinstance(release_audit, dict), "current_release_control_audit missing")
    require(release_audit.get("id") == "AX-PUB-CI-011", "release-control audit identity mismatch")
    require(release_audit.get("state") == "BASELINE_RECORDED_CONTROLS_NOT_READY", "release-control baseline state mismatch")
    require(release_audit.get("github_controls_ready_for_release_promotion") is False, "release controls must remain not ready")
    require(release_audit.get("release_control_readiness") == "NOT_ESTABLISHED", "release-control readiness must remain not established")
    require(release_audit.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "release audit publication boundary changed")

    api_state = manifest.get("current_sdk_public_api_contract")
    require(isinstance(api_state, dict), "current_sdk_public_api_contract missing")
    require(api_state.get("id") == "AX-PUB-API-001", "public API contract identity mismatch")
    require(api_state.get("state") == "VALIDATED_CANDIDATE_CONTRACT", "public API contract candidate must be validated")
    require(api_state.get("validation_evidence") == "AX-PUB-CI-012", "public API contract evidence linkage mismatch")
    require(api_state.get("sdk_candidate_version") == VERSION, "public API candidate version mismatch")
    require(api_state.get("verified_runtime_matrix") == RUNTIMES, "public API runtime matrix mismatch")
    require(api_state.get("stable_api_guarantee_established") is False, "stable 1.0 guarantee must not be pre-claimed")
    require(api_state.get("support_commitment_established") is False, "API support commitment must not be pre-claimed")
    require(api_state.get("supported_sdk_established") is False, "supported SDK must remain unestablished")
    require(api_state.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "API contract publication boundary changed")

    support_state = manifest.get("current_sdk_support_contract")
    require(isinstance(support_state, dict), "current_sdk_support_contract missing")
    require(support_state.get("id") == "AX-PUB-SUP-001", "support contract identity mismatch")
    require(support_state.get("state") == "VALIDATED_CANDIDATE_CONTRACT_NOT_ACTIVATED", "support contract must remain not activated")
    require(support_state.get("validation_evidence") == "AX-PUB-CI-013", "support evidence linkage mismatch")
    require(support_state.get("sdk_candidate_version") == VERSION, "support candidate version mismatch")
    require(support_state.get("target_deprecation_notice_days") == 90, "target deprecation notice mismatch")
    require(support_state.get("target_intervening_minor_releases") == 1, "target intervening minor mismatch")
    for key in ("support_commitment_established", "production_support_activated", "commercial_sla_established", "supported_sdk_established"):
        require(support_state.get(key) is False, f"support state boundary changed: {key}")
    require(support_state.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "support publication boundary changed")

    security_state = manifest.get("current_sdk_security_operations_contract")
    require(isinstance(security_state, dict), "current_sdk_security_operations_contract missing")
    require(security_state.get("id") == "AX-PUB-SEC-001", "security contract identity mismatch")
    require(security_state.get("state") == "VALIDATED_CANDIDATE_CONTRACT_NOT_READY", "security contract must remain not ready")
    require(security_state.get("validation_evidence") == "AX-PUB-CI-013", "security evidence linkage mismatch")
    for key in (
        "security_operations_ready",
        "dedicated_security_channel_established",
        "security_response_owner_assigned",
        "security_response_sla_established",
        "bug_bounty_established",
        "supported_sdk_established",
    ):
        require(security_state.get(key) is False, f"security state boundary changed: {key}")
    require(security_state.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "security publication boundary changed")

    readiness = manifest.get("current_sdk_release_readiness_aggregation")
    require(isinstance(readiness, dict), "current_sdk_release_readiness_aggregation missing")
    require(readiness.get("id") == "AX-PUB-RELPACK-001", "release-readiness identity mismatch")
    require(readiness.get("state") == "CI_VALIDATED_BLOCKED_BEFORE_DEV_GATE_05D_AUTHORITY_REVIEW", "release-readiness state mismatch")
    require(readiness.get("validation_evidence") == "AX-PUB-CI-016", "release-readiness evidence linkage mismatch")
    require((readiness.get("required_dimension_count"), readiness.get("established_dimension_count"), readiness.get("blocked_dimension_count")) == (13, 4, 9), "release-readiness counts mismatch")
    require(readiness.get("ready_for_dev_gate_05d_authority_review") is False, "release readiness must remain false")
    for key in (
        "external_registry_validation_established",
        "independent_human_external_evaluation_established",
        "release_control_readiness_established",
        "registry_ownership_and_trusted_publisher_established",
        "licence_and_ip_clearance_established",
        "support_contract_activated",
        "security_operations_ready",
        "release_owner_and_accountability_established",
        "dev_gate_05d_authorized",
        "supported_sdk_established",
    ):
        require(readiness.get(key) is False, f"release-readiness boundary changed: {key}")
    require(readiness.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "release-readiness publication boundary changed")

    ci011_manifest = evidence_by_id(manifest, "AX-PUB-CI-011")
    require(ci011_manifest.get("github_controls_ready_for_release_promotion") is False, "CI-011 manifest state must remain controls-not-ready")
    require(ci011_manifest.get("conclusion") == "SUCCESS", "CI-011 audit run must remain successful")

    ci012_manifest = evidence_by_id(manifest, "AX-PUB-CI-012")
    require(ci012_manifest.get("verified_runtime_matrix") == RUNTIMES, "CI-012 runtime matrix mismatch")
    require(ci012_manifest.get("stable_api_guarantee_established") is False, "CI-012 must not create stable API guarantee")
    require(ci012_manifest.get("supported_sdk_established") is False, "CI-012 must not create supported SDK state")
    require(ci012_manifest.get("conclusion") == "SUCCESS", "CI-012 validation must remain successful")

    ci013_manifest = evidence_by_id(manifest, "AX-PUB-CI-013")
    require(ci013_manifest.get("verified_runtime_matrix") == RUNTIMES, "CI-013 runtime matrix mismatch")
    require(ci013_manifest.get("gate03_identity_preserved") is True, "CI-013 must preserve Gate-03 identity")
    require(ci013_manifest.get("gate03_verified_build_digest") == GATE03_DIGEST, "CI-013 Gate-03 digest mismatch")
    for key in ("support_commitment_established", "security_operations_ready", "supported_sdk_established", "sdk_publication_authorized"):
        require(ci013_manifest.get(key) is False, f"CI-013 boundary changed: {key}")
    require(ci013_manifest.get("conclusion") == "SUCCESS", "CI-013 validation must remain successful")

    ci016_manifest = evidence_by_id(manifest, "AX-PUB-CI-016")
    require(ci016_manifest.get("workflow_run_id") == 32200229804 and ci016_manifest.get("job_id") == 95912269419, "CI-016 workflow identity mismatch")
    require(ci016_manifest.get("actions_artifact_id") == 9347211356 and ci016_manifest.get("actions_artifact_sha256") == RELPACK_ACTIONS_SHA, "CI-016 artifact identity mismatch")
    require((ci016_manifest.get("required_dimension_count"), ci016_manifest.get("established_dimension_count"), ci016_manifest.get("blocked_dimension_count")) == (13, 4, 9), "CI-016 counts mismatch")
    require(ci016_manifest.get("ready_for_dev_gate_05d_authority_review") is False, "CI-016 readiness boundary changed")
    require(ci016_manifest.get("dev_gate_05d_authorized") is False, "CI-016 05D boundary changed")
    require(ci016_manifest.get("sdk_publication_authorized") is False, "CI-016 publication boundary changed")
    require(ci016_manifest.get("conclusion") == "SUCCESS", "CI-016 validation must remain successful")

    require(dev009.get("phase") == "DEV-GATE-05C", "DEV-009 phase mismatch")
    require(dev009.get("phase_state") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05C must remain active")
    require(dev009.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "DEV-009 publication boundary changed")
    for key in (
        "external_registry_write_authorized",
        "testpypi_publication_authorized",
        "pypi_publication_authorized",
        "license_granted",
        "supported_sdk_established",
    ):
        require(dev009.get(key) is False, f"{key} must remain false")

    identity = dev009.get("package_identity")
    require(isinstance(identity, dict), "package identity missing")
    require(identity.get("distribution_candidate") == PROJECT, "distribution candidate mismatch")
    require(identity.get("version_candidate") == VERSION, "version candidate mismatch")
    require(identity.get("import_namespace") == IMPORT, "import namespace mismatch")
    require(identity.get("registry_ownership_established") is False, "registry ownership must remain unestablished")

    candidate = dev009.get("validated_candidate_identity")
    require(isinstance(candidate, dict), "validated candidate identity missing")
    require(candidate.get("wheel_sha256") == WHEEL_SHA, "wheel digest mismatch")
    require(candidate.get("sdist_sha256") == SDIST_SHA, "sdist digest mismatch")
    require(candidate.get("verified_runtime_matrix") == RUNTIMES, "package runtime matrix mismatch")

    distribution = dev009.get("distribution_validation")
    require(isinstance(distribution, dict), "distribution validation missing")
    require(distribution.get("local_simple_index_simulation") == "DIRECT_CI_VALIDATED_LOCAL_ONLY", "DEV-009 local-index state mismatch")
    require(distribution.get("local_simple_index_validation_evidence") == "AX-PUB-CI-010", "DEV-009 CI-010 evidence link missing")
    require(distribution.get("local_simple_index_is_external_registry_validation") is False, "local validation must not become external validation")
    require(distribution.get("production_pypi_allowed_in_phase_05c") is False, "Gate-05C must not permit production PyPI")

    controls = dev009.get("release_controls_observation")
    require(isinstance(controls, dict), "release_controls_observation missing")
    require(controls.get("main_branch_protected") is False, "main protection must not be asserted without fresh evidence")
    require(controls.get("required_status_checks_enforced_on_main") is False, "required checks must not be asserted without fresh evidence")
    require(controls.get("current_release_controls_sufficient_for_external_registry_write") is False, "release controls must remain insufficient")
    require(controls.get("protected_pypi_environment_established") is False, "pypi environment must not be pre-claimed")
    require(controls.get("pypi_trusted_publisher_established") is False, "Trusted Publisher must not be pre-claimed")

    require(api001.get("artifact_id") == "AX-PUB-API-001", "API artifact ID mismatch")
    require(api001.get("sdk_distribution_candidate") == PROJECT, "API distribution identity mismatch")
    require(api001.get("sdk_version_candidate") == VERSION, "API version identity mismatch")
    require(api001.get("import_namespace") == IMPORT, "API import namespace mismatch")
    require(api001.get("verified_runtime_target") == RUNTIMES, "API target runtime matrix mismatch")
    require(api001.get("support_commitment_established") is False, "API artifact must not establish support")
    require(api001.get("stable_api_guarantee_established") is False, "API artifact must not establish stable guarantee")
    require(api001.get("sdk_publication_authorized") is False, "API artifact must not authorize publication")

    require(sup001.get("artifact_id") == "AX-PUB-SUP-001", "support artifact ID mismatch")
    require(sup001.get("sdk_distribution_candidate") == PROJECT, "support distribution identity mismatch")
    require(sup001.get("sdk_version_candidate") == VERSION, "support version identity mismatch")
    require(sup001.get("public_api_contract") == "AX-PUB-API-001", "support API binding mismatch")
    for key in ("support_commitment_established", "production_support_activated", "stable_1_0_semver_commitment", "commercial_sla_established", "sdk_publication_authorized"):
        require(sup001.get(key) is False, f"support artifact boundary changed: {key}")

    require(sec001.get("artifact_id") == "AX-PUB-SEC-001", "security artifact ID mismatch")
    for key in (
        "security_operations_ready",
        "dedicated_security_channel_established",
        "security_response_owner_assigned",
        "security_response_sla_established",
        "bug_bounty_established",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        require(sec001.get(key) is False, f"security artifact boundary changed: {key}")

    require(relpack.get("artifact_id") == "AX-PUB-RELPACK-001", "RELPACK artifact ID mismatch")
    require(relpack.get("state") == "CI_VALIDATED_DEV_GATE_05D_RELEASE_READINESS_PACK_BLOCKED", "RELPACK source state mismatch")
    require(relpack.get("validation_evidence") == "AX-PUB-CI-016", "RELPACK source evidence mismatch")
    relpack_disposition = relpack.get("current_expected_disposition")
    require(isinstance(relpack_disposition, dict), "RELPACK disposition missing")
    require(relpack_disposition.get("ready_for_dev_gate_05d_authority_review") is False, "RELPACK readiness must remain false")
    require(relpack_disposition.get("dev_gate_05d_authorized") is False, "RELPACK must not authorize 05D")
    require(relpack_disposition.get("sdk_publication_authorized") is False, "RELPACK must not authorize publication")

    for marker in (
        "AX-PUB-MANIFEST-001 v1.26",
        PROJECT,
        IMPORT,
        VERSION,
        "AX-PUB-API-001",
        "AX-PUB-CI-012",
        "AX-PUB-SUP-001",
        "AX-PUB-SEC-001",
        "AX-PUB-CI-013",
        "AX-PUB-RELPACK-001",
        "AX-PUB-CI-016",
        "DEV-GATE-05C",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in quickstart, f"Quickstart missing current marker: {marker}")

    for marker in (
        "DEV-GATE-05C  ACTIVE",
        "LOCAL INDEX ENGINEERING VALIDATION: VERIFIED / LOCAL ONLY",
        "AX-PUB-MANIFEST-001 v1.26",
        "AX-PUB-CI-011",
        "AX-PUB-API-001",
        "AX-PUB-CI-012",
        "AX-PUB-SUP-001",
        "AX-PUB-SEC-001",
        "AX-PUB-CI-013",
        "AX-PUB-RELPACK-001",
        "AX-PUB-CI-016",
        "RELEASE READINESS HARD DIMENSIONS: 13",
        "RELEASE READINESS ESTABLISHED: 4",
        "RELEASE READINESS BLOCKED: 9",
        "READY FOR DEV-GATE-05D AUTHORITY REVIEW: NO",
        "SUPPORT COMMITMENT: NOT ESTABLISHED",
        "SECURITY OPERATIONS READY: NO",
        "STABLE 1.0 GUARANTEE: NOT ESTABLISHED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in current, f"current-state page missing marker: {marker}")

    for marker in (
        "Production SDK Definition of Done",
        "PRODUCTION SDK: NOT ESTABLISHED",
        "PYPI DISTRIBUTION: NOT ESTABLISHED",
        "PUBLIC SDK LICENCE: NOT GRANTED",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ):
        require(marker in dod, f"Definition of Done missing marker: {marker}")

    for marker in (
        "Release Control Plane",
        "MAIN BRANCH PROTECTED: NO",
        "PYPI TRUSTED PUBLISHER: NOT ESTABLISHED",
        "LIVE RELEASE CONTROL PLANE: NOT ESTABLISHED",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ):
        require(marker in control, f"release-control document missing marker: {marker}")

    for marker in (
        "AX-PUB-CI-010",
        WHEEL_SHA,
        SDIST_SHA,
        "LOCAL INDEX DISTRIBUTION VALIDATION: VERIFIED / LOCAL ONLY",
        "EXTERNAL REGISTRY VALIDATION: NOT ESTABLISHED / NOT AUTHORIZED",
    ):
        require(marker in ci010, f"CI-010 evidence missing marker: {marker}")

    for marker in (
        "AX-PUB-CI-011",
        "GITHUB CONTROLS READY FOR RELEASE:          FALSE",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in ci011, f"CI-011 evidence missing marker: {marker}")

    for marker in (
        "AX-PUB-CI-012",
        "CPython 3.11",
        "CPython 3.14",
        "STABLE 1.0 GUARANTEE: NOT ESTABLISHED",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ):
        require(marker in ci012, f"CI-012 evidence missing marker: {marker}")

    for marker in (
        "AX-PUB-CI-013",
        "CPython 3.11",
        "CPython 3.14",
        GATE03_DIGEST,
        "SUPPORT COMMITMENT: NOT ESTABLISHED",
        "SECURITY OPERATIONS READY: NO",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ):
        require(marker in ci013, f"CI-013 evidence missing marker: {marker}")

    for marker in (
        "AX-PUB-CI-016",
        "required = 13",
        "established = 4",
        "blocked = 9",
        "ready_for_05d = false",
        "DEV-GATE-05D NOT AUTHORIZED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in ci016, f"CI-016 evidence missing marker: {marker}")

    print(
        "AX_PRODUCTION_SDK_TARGET_PASS "
        "manifest>=1.26 gate05c=ACTIVE local_index=VERIFIED_LOCAL_ONLY "
        "release_controls=NOT_READY api_contract=VALIDATED_CANDIDATE "
        "support=NOT_ACTIVATED security_ops=NOT_READY gate03_identity=PRESERVED "
        "release_pack=CI_VALIDATED_BLOCKED required=13 established=4 blocked=9 "
        "ready_for_05d=false production_sdk=NOT_ESTABLISHED sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
