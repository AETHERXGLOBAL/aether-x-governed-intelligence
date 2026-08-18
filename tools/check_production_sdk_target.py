#!/usr/bin/env python3
"""Fail-closed consistency check for the AETHER X production-SDK productization target.

This checker validates repository-declared engineering state only. It does not
establish live GitHub branch protection, PyPI ownership, Trusted Publishing,
software licence authority, human external evaluation, or release authority.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV009 = ROOT / "artifacts" / "AX-PUB-DEV-009.json"
QUICKSTART = ROOT / "docs" / "QUICKSTART.md"
CURRENT = ROOT / "docs" / "PUBLIC_ENGINEERING_STATE.md"
DOD = ROOT / "docs" / "PRODUCTION_SDK_DEFINITION_OF_DONE.md"
CONTROL = ROOT / "docs" / "RELEASE_CONTROL_PLANE.md"
CI010 = ROOT / "evidence" / "AX-PUB-CI-010_DISTRIBUTION_EXTERNAL_VALIDATION_BASELINE_VALIDATION.md"

PROJECT = "aetherxglobal-governed-intelligence"
IMPORT = "aetherxglobal.governed_intelligence"
VERSION = "0.1.0rc1"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"


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


def main() -> int:
    manifest = load_json(MANIFEST)
    dev009 = load_json(DEV009)
    quickstart = text(QUICKSTART)
    current = text(CURRENT)
    dod = text(DOD)
    control = text(CONTROL)
    ci010 = text(CI010)

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 22), "manifest must be >= v1.22")

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
    require(candidate.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "package runtime matrix mismatch")

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

    for marker in (
        "AX-PUB-MANIFEST-001 v1.22",
        PROJECT,
        IMPORT,
        VERSION,
        "DEV-GATE-05C",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in quickstart, f"Quickstart missing current marker: {marker}")

    for marker in (
        "DEV-GATE-05C  ACTIVE",
        "LOCAL INDEX ENGINEERING VALIDATION: VERIFIED / LOCAL ONLY",
        "AX-PUB-MANIFEST-001 v1.22",
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

    print(
        "AX_PRODUCTION_SDK_TARGET_PASS "
        "manifest>=1.22 gate05c=ACTIVE local_index=VERIFIED_LOCAL_ONLY "
        "production_sdk=NOT_ESTABLISHED sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
