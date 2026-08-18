#!/usr/bin/env python3
"""Fail-closed validation for AX-PUB-SUP-001 and AX-PUB-SEC-001 candidates."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC = ROOT / "artifacts" / "AX-PUB-SEC-001.json"
API = ROOT / "artifacts" / "AX-PUB-API-001.json"
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
AUDIT = ROOT / "evidence" / "AX-PUB-RELEASE-CONTROL-AUDIT-001.json"
SUP_DOC = ROOT / "docs" / "AX-PUB-SUP-001_SDK_SUPPORT_COMPATIBILITY_MAINTENANCE_CONTRACT.md"
SEC_DOC = ROOT / "docs" / "AX-PUB-SEC-001_SDK_SECURITY_OPERATIONS_READINESS_CONTRACT.md"
SECURITY = ROOT / "SECURITY.md"
MIGRATION = ROOT / "docs" / "MIGRATION_AND_DEPRECATION_DRAFT.md"

PROJECT = "aetherxglobal-governed-intelligence"
VERSION = "0.1.0rc1"
IMPORT = "aetherxglobal.governed_intelligence"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]
PROVISIONAL_SECURITY_EMAIL = "aether.x.eg@gmail.com"

SUP_ACTIVATION = {
    "AX_PUB_API_001_VALIDATED_AND_RELEASE_BOUND",
    "RELEASE_CONTROL_READINESS_ESTABLISHED",
    "REGISTRY_OWNERSHIP_ESTABLISHED",
    "PYPI_TRUSTED_PUBLISHER_ESTABLISHED",
    "IP_COPYRIGHT_CLEARANCE_ESTABLISHED",
    "PUBLIC_SDK_LICENCE_GRANTED",
    "DEDICATED_SECURITY_INTAKE_ESTABLISHED",
    "SECURITY_RESPONSE_OWNER_ASSIGNED",
    "INDEPENDENT_HUMAN_EXTERNAL_EVALUATION_COMPLETE",
    "FINAL_RELEASE_EVIDENCE_PACK_COMPLETE",
    "EXPLICIT_DEV_GATE_05D_RELEASE_AUTHORITY",
}
SEC_ACTIVATION = {
    "DEDICATED_OR_FORMALLY_DESIGNATED_PRIVATE_SECURITY_CHANNEL",
    "NAMED_SECURITY_RESPONSE_OWNER",
    "DOCUMENTED_ESCALATION_PATH",
    "RELEASE_REMEDIATION_AUTHORITY",
    "SUPPORTED_VERSION_INVENTORY",
    "VULNERABILITY_CASE_RECORD_PROCESS",
    "SECURITY_RELEASE_AND_WITHDRAWAL_PROCESS",
    "RELEASE_CONTROL_READINESS_ESTABLISHED",
    "PUBLIC_SECURITY_POLICY_SYNCHRONIZED",
    "EXPLICIT_DEV_GATE_05D_RELEASE_AUTHORITY",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_SUPPORT_SECURITY_CONTRACT_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def require_markers(path: Path, markers: tuple[str, ...]) -> None:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    value = path.read_text(encoding="utf-8")
    for marker in markers:
        require(marker in value, f"{path.relative_to(ROOT)} missing marker: {marker}")


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    require(isinstance(raw, str), "manifest_version must be string")
    try:
        parts = raw.split("-", 1)[0].split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        fail(f"invalid manifest_version: {raw!r}")


def main() -> int:
    sup = load(SUP)
    sec = load(SEC)
    api = load(API)
    manifest = load(MANIFEST)
    audit = load(AUDIT)

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 23), "support/security contracts require manifest >= 1.23 baseline")
    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current developer program missing")
    require(program.get("active_phase") == "DEV-GATE-05C — Distribution & External Validation", "Gate-05C must remain active")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication boundary changed")

    require(sup.get("artifact_id") == "AX-PUB-SUP-001", "support artifact identity mismatch")
    require(sup.get("version") == "0.1", "support artifact version mismatch")
    require(sup.get("state") == "DEV_GATE_05C_SUPPORT_CONTRACT_CANDIDATE", "support candidate state mismatch")
    require(sup.get("sdk_distribution_candidate") == PROJECT, "support distribution identity mismatch")
    require(sup.get("sdk_version_candidate") == VERSION, "support version mismatch")
    require(sup.get("import_namespace") == IMPORT, "support import namespace mismatch")
    require(sup.get("public_api_contract") == "AX-PUB-API-001", "support API contract link mismatch")
    require(sup.get("public_api_validation_evidence") == "AX-PUB-CI-012", "support API evidence link mismatch")
    require(sup.get("candidate_runtime_matrix") == RUNTIMES, "support runtime matrix mismatch")
    for key in (
        "support_commitment_established",
        "production_support_activated",
        "stable_1_0_semver_commitment",
        "commercial_sla_established",
        "sdk_publication_authorized",
    ):
        require(sup.get(key) is False, f"support boundary changed: {key}")

    versioning = sup.get("versioning_model_after_activation")
    require(isinstance(versioning, dict), "support versioning model missing")
    require(versioning.get("scheme") == "SEMANTIC_VERSIONING", "target support versioning scheme mismatch")
    for key in ("patch", "minor", "major", "pre_1_0"):
        require(isinstance(versioning.get(key), str) and bool(versioning.get(key)), f"support version rule missing: {key}")

    deprecation = sup.get("candidate_deprecation_policy")
    require(isinstance(deprecation, dict), "candidate deprecation policy missing")
    require(deprecation.get("normal_removal_requires_prior_deprecation") is True, "normal removal must require prior deprecation")
    require(deprecation.get("target_minimum_notice_days_after_activation") == 90, "target deprecation notice must remain 90 days")
    require(deprecation.get("target_minimum_intervening_minor_release") == 1, "target deprecation minor-release requirement mismatch")
    require(
        deprecation.get("effective_rule_after_activation") == "LATER_OF_90_DAYS_OR_ONE_INTERVENING_MINOR_RELEASE_UNDER_NORMAL_CONDITIONS",
        "target deprecation rule mismatch",
    )
    require(deprecation.get("emergency_exception_allowed") is True, "emergency exception path missing")

    maintenance = sup.get("candidate_maintenance_model")
    require(isinstance(maintenance, dict), "candidate maintenance model missing")
    require(maintenance.get("previous_minor_security_correctness_window_days") == 90, "previous-minor target window mismatch")
    require(maintenance.get("previous_minor_window_is_target_until_release_authority") is True, "previous-minor target must remain non-activated")
    require(maintenance.get("long_term_support_line_established") is False, "LTS line must not be pre-claimed")
    require(maintenance.get("end_of_support_notice_period_committed") is False, "EOS notice period must not be pre-committed")
    require(set(sup.get("activation_requirements", [])) == SUP_ACTIVATION, "support activation requirements changed unexpectedly")

    require(sec.get("artifact_id") == "AX-PUB-SEC-001", "security artifact identity mismatch")
    require(sec.get("version") == "0.1", "security artifact version mismatch")
    require(sec.get("state") == "DEV_GATE_05C_SECURITY_OPERATIONS_CANDIDATE", "security candidate state mismatch")
    for key in (
        "security_operations_ready",
        "dedicated_security_channel_established",
        "security_response_owner_assigned",
        "security_response_sla_established",
        "bug_bounty_established",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        require(sec.get(key) is False, f"security boundary changed: {key}")

    provisional = sec.get("current_provisional_intake")
    require(isinstance(provisional, dict), "provisional security intake missing")
    require(provisional.get("channel") == PROVISIONAL_SECURITY_EMAIL, "provisional security email mismatch")
    require(provisional.get("dedicated_security_service") is False, "provisional email must not become a dedicated service claim")
    require(provisional.get("sla") is False, "provisional security channel must not imply SLA")

    require(sec.get("case_lifecycle") == [
        "RECEIVED",
        "TRIAGED",
        "VALIDATED_OR_REJECTED",
        "REMEDIATION_PLANNED",
        "FIX_VALIDATED",
        "RELEASE_OR_MITIGATION_READY",
        "DISCLOSURE_OR_ADVISORY_DECIDED",
        "CLOSED",
    ], "security case lifecycle mismatch")
    require(sec.get("severity_classes") == ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"], "security severity inventory mismatch")
    require(set(sec.get("activation_requirements", [])) == SEC_ACTIVATION, "security activation requirements changed unexpectedly")

    require(api.get("artifact_id") == "AX-PUB-API-001", "API contract missing")
    require(api.get("sdk_distribution_candidate") == PROJECT, "API distribution identity mismatch")
    require(api.get("sdk_version_candidate") == VERSION, "support/security candidate must bind current API version")
    require(api.get("import_namespace") == IMPORT, "API namespace mismatch")
    require(api.get("verified_runtime_target") == RUNTIMES, "API runtime target mismatch")
    require(api.get("support_commitment_established") is False, "API artifact must not pre-establish support")
    require(api.get("stable_api_guarantee_established") is False, "API artifact must remain pre-stable")
    require(api.get("sdk_publication_authorized") is False, "API artifact publication boundary changed")

    require(audit.get("report_format") == "AX-PUB-RELEASE-CONTROL-AUDIT-001", "release-control audit missing")
    require(audit.get("github_controls_ready_for_release_promotion") is False, "release controls must remain not ready at this candidate state")
    external = audit.get("external_controls_not_audited_here")
    require(isinstance(external, dict), "external release-control state missing")
    require(external.get("final_release_authority") == "NOT_AUTHORIZED", "final release authority boundary changed")

    require_markers(SUP_DOC, (
        "AX-PUB-SUP-001",
        "Support commitment established:** `NO`",
        "90 days",
        "one intervening supported minor release",
        "SUPPORTED SDK: NOT ESTABLISHED",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ))
    require_markers(SEC_DOC, (
        "AX-PUB-SEC-001",
        PROVISIONAL_SECURITY_EMAIL,
        "SECURITY OPERATIONS READY: NO",
        "SECURITY RESPONSE SLA: NOT ESTABLISHED",
        "BUG BOUNTY: NOT ESTABLISHED",
        "SDK PUBLICATION: NOT AUTHORIZED",
    ))
    require_markers(SECURITY, (
        PROVISIONAL_SECURITY_EMAIL,
        "provisional public reporting path",
        "does not represent a dedicated security-response service, SLA, bug-bounty program or certification",
        "SDK CANDIDATE ≠ SUPPORTED SDK",
    ))
    require_markers(MIGRATION, (
        "Migration & Deprecation Draft",
        PROJECT,
        VERSION,
        "AX-PUB-API-001",
        "AX-PUB-SUP-001",
        "No Fixed Support Window Yet",
        "PRE-STABLE CANDIDATE ≠ STABLE PUBLIC API",
        "SDK PUBLICATION NOT AUTHORIZED",
    ))

    print(
        "AX_SDK_SUPPORT_SECURITY_CONTRACT_PASS "
        "manifest>=1.23 support=NOT_ACTIVATED security_ops=NOT_READY "
        "deprecation_target=90d/1minor release_controls=NOT_READY publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
