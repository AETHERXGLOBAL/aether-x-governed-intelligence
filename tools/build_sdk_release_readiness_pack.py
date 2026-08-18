#!/usr/bin/env python3
"""Build AX-PUB-RELPACK-REPORT-001 from canonical repository evidence.

The report is a deterministic, fail-closed aggregation of already-established
repository evidence. It cannot create human evaluation, registry ownership,
licence rights, operating readiness, or release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "artifacts" / "AX-PUB-RELPACK-001.json"
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV009 = ROOT / "artifacts" / "AX-PUB-DEV-009.json"
API001 = ROOT / "artifacts" / "AX-PUB-API-001.json"
SUP001 = ROOT / "artifacts" / "AX-PUB-SUP-001.json"
SEC001 = ROOT / "artifacts" / "AX-PUB-SEC-001.json"
EVAL_PACK = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
RELEASE_AUDIT = ROOT / "evidence" / "AX-PUB-RELEASE-CONTROL-AUDIT-001.json"

WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
GATE03_DIGEST = "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]


def fail(message: str) -> None:
    raise SystemExit(f"AX_RELEASE_PACK_BUILD_FAIL: {message}")


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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dim(dimension_id: str, state: str, established: bool, evidence: list[str], blockers: list[str] | None = None) -> dict[str, Any]:
    return {
        "id": dimension_id,
        "state": state,
        "established": established,
        "evidence": evidence,
        "blockers": blockers or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    require(len(args.source_commit) == 40 and all(c in "0123456789abcdef" for c in args.source_commit.lower()), "source commit must be a 40-character Git SHA")

    contract = load(CONTRACT)
    manifest = load(MANIFEST)
    dev009 = load(DEV009)
    api = load(API001)
    sup = load(SUP001)
    sec = load(SEC001)
    evaluator = load(EVAL_PACK)
    load(RELEASE_AUDIT)  # parseability and retained source evidence are mandatory

    require(contract.get("artifact_id") == "AX-PUB-RELPACK-001" and contract.get("version") == "0.1", "release-pack contract identity mismatch")
    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")

    candidate = contract.get("candidate")
    require(isinstance(candidate, dict), "release-pack candidate identity missing")
    require(candidate.get("distribution") == "aetherxglobal-governed-intelligence", "distribution identity mismatch")
    require(candidate.get("version") == "0.1.0rc1", "candidate version mismatch")
    require(candidate.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA and candidate.get("sdist_sha256") == SDIST_SHA, "candidate artifact digest mismatch")
    require(candidate.get("runtime_matrix") == RUNTIMES, "candidate runtime matrix mismatch")

    manifest_supply = manifest.get("current_supply_chain_release_candidate")
    manifest_api = manifest.get("current_sdk_public_api_contract")
    manifest_support = manifest.get("current_sdk_support_contract")
    manifest_security = manifest.get("current_sdk_security_operations_contract")
    manifest_eval = manifest.get("current_installable_external_evaluator_handoff")
    manifest_release_audit = manifest.get("current_release_control_audit")
    manifest_gate = manifest.get("current_readiness_gate")
    manifest_program = manifest.get("current_developer_program")
    manifest_dist = manifest.get("current_distribution_external_validation")

    for label, value in (
        ("current_supply_chain_release_candidate", manifest_supply),
        ("current_sdk_public_api_contract", manifest_api),
        ("current_sdk_support_contract", manifest_support),
        ("current_sdk_security_operations_contract", manifest_security),
        ("current_installable_external_evaluator_handoff", manifest_eval),
        ("current_release_control_audit", manifest_release_audit),
        ("current_readiness_gate", manifest_gate),
        ("current_developer_program", manifest_program),
        ("current_distribution_external_validation", manifest_dist),
    ):
        require(isinstance(value, dict), f"manifest {label} missing")

    validated_candidate = dev009.get("validated_candidate_identity")
    package_identity = dev009.get("package_identity")
    distribution = dev009.get("distribution_validation")
    controls = dev009.get("release_controls_observation")
    for label, value in (
        ("validated_candidate_identity", validated_candidate),
        ("package_identity", package_identity),
        ("distribution_validation", distribution),
        ("release_controls_observation", controls),
    ):
        require(isinstance(value, dict), f"DEV-009 {label} missing")

    dimensions: list[dict[str, Any]] = []

    engineering_identity = (
        validated_candidate.get("wheel_sha256") == WHEEL_SHA
        and validated_candidate.get("sdist_sha256") == SDIST_SHA
        and validated_candidate.get("verified_runtime_matrix") == RUNTIMES
        and package_identity.get("distribution_candidate") == "aetherxglobal-governed-intelligence"
        and package_identity.get("version_candidate") == "0.1.0rc1"
    )
    dimensions.append(dim(
        "ENGINEERING_CANDIDATE_IDENTITY",
        "ESTABLISHED" if engineering_identity else "NOT_ESTABLISHED",
        engineering_identity,
        ["AX-PUB-DEV-008", "AX-PUB-CI-009", "AX-PUB-DEV-009", "AX-PUB-CI-010"],
        [] if engineering_identity else ["Exact candidate identity or runtime evidence is incomplete."],
    ))

    api_established = (
        isinstance(manifest_api, dict)
        and manifest_api.get("state") == "VALIDATED_CANDIDATE_CONTRACT"
        and manifest_api.get("validation_evidence") == "AX-PUB-CI-012"
        and manifest_api.get("verified_runtime_matrix") == RUNTIMES
        and api.get("artifact_id") == "AX-PUB-API-001"
    )
    dimensions.append(dim(
        "PUBLIC_API_CONTRACT",
        "VALIDATED_CANDIDATE" if api_established else "NOT_ESTABLISHED",
        api_established,
        ["AX-PUB-API-001", "AX-PUB-CI-012"],
        [] if api_established else ["Public API candidate contract validation is incomplete."],
    ))

    runtime_established = validated_candidate.get("verified_runtime_matrix") == RUNTIMES
    dimensions.append(dim(
        "EXACT_ARTIFACT_RUNTIME_VALIDATION",
        "ESTABLISHED" if runtime_established else "NOT_ESTABLISHED",
        runtime_established,
        ["AX-PUB-CI-009", "AX-PUB-CI-010", "AX-PUB-CI-012", "AX-PUB-CI-014", "AX-PUB-CI-015"],
        [] if runtime_established else ["Exact artifact runtime matrix is incomplete."],
    ))

    supply_established = (
        isinstance(manifest_supply, dict)
        and manifest_supply.get("deterministic_build") == "VERIFIED"
        and manifest_supply.get("build_provenance_attestation") == "VERIFIED"
        and manifest_supply.get("sbom_attestation") == "VERIFIED"
        and manifest_supply.get("verified_build_digest") == GATE03_DIGEST
    )
    dimensions.append(dim(
        "SUPPLY_CHAIN_PROVENANCE_SBOM",
        "ESTABLISHED_ENGINEERING_EVIDENCE" if supply_established else "NOT_ESTABLISHED",
        supply_established,
        ["AX-PUB-DEV-005", "AX-PUB-CI-006", "AX-PUB-CI-013"],
        [] if supply_established else ["Supply-chain engineering evidence is incomplete."],
    ))

    external_registry = bool(
        isinstance(manifest_eval, dict)
        and manifest_eval.get("external_registry_validation_established") is True
    )
    dimensions.append(dim(
        "EXTERNAL_REGISTRY_VALIDATION",
        "ESTABLISHED" if external_registry else "NOT_ESTABLISHED",
        external_registry,
        ["AX-PUB-DEV-009", "AX-PUB-EVAL-PACK-001"],
        [] if external_registry else ["Exact candidate has not been validated through an authorized external package index."],
    ))

    human_eval = bool(
        isinstance(manifest_eval, dict)
        and manifest_eval.get("human_external_evaluation_occurred") is True
        and manifest_eval.get("independent_evaluator_result_established") is True
    )
    dimensions.append(dim(
        "INDEPENDENT_HUMAN_EXTERNAL_EVALUATION",
        "ESTABLISHED" if human_eval else "NOT_ESTABLISHED",
        human_eval,
        ["AX-PUB-EVAL-PACK-001", "AX-PUB-EVAL-REPORT-002"],
        [] if human_eval else ["No FINAL independent-human AX-PUB-EVAL-REPORT-002 is established."],
    ))

    release_controls = bool(
        isinstance(manifest_release_audit, dict)
        and manifest_release_audit.get("github_controls_ready_for_release_promotion") is True
        and manifest_release_audit.get("release_control_readiness") == "ESTABLISHED"
    )
    dimensions.append(dim(
        "RELEASE_CONTROL_READINESS",
        "ESTABLISHED" if release_controls else "NOT_ESTABLISHED",
        release_controls,
        ["AX-PUB-CI-011", "AX-PUB-RELEASE-CONTROL-AUDIT-001"],
        [] if release_controls else ["Required branch/ruleset/status-check/publishing-environment controls are not established."],
    ))

    registry_owned = bool(package_identity.get("registry_ownership_established") is True)
    trusted_publisher = bool(controls.get("pypi_trusted_publisher_established") is True)
    protected_environment = bool(controls.get("protected_pypi_environment_established") is True)
    registry_ready = registry_owned and trusted_publisher and protected_environment
    dimensions.append(dim(
        "REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER",
        "ESTABLISHED" if registry_ready else "NOT_ESTABLISHED",
        registry_ready,
        ["AX-PUB-DEV-009", "AX-PUB-CI-011"],
        [] if registry_ready else [
            "PyPI project ownership/control is not established." if not registry_owned else "",
            "PyPI Trusted Publisher is not established." if not trusted_publisher else "",
            "Protected PyPI publishing environment is not established." if not protected_environment else "",
        ],
    ))
    dimensions[-1]["blockers"] = [x for x in dimensions[-1]["blockers"] if x]

    eval_state = evaluator.get("current_state")
    require(isinstance(eval_state, dict), "evaluator current_state missing")
    licence_granted = bool(dev009.get("license_granted") is True and eval_state.get("public_sdk_licence_granted") is True)
    dimensions.append(dim(
        "LICENCE_AND_IP_CLEARANCE",
        "ESTABLISHED" if licence_granted else "NOT_ESTABLISHED",
        licence_granted,
        ["AX-PUB-DEV-007", "AX-PUB-DEV-009", "PRODUCTION_SDK_DEFINITION_OF_DONE"],
        [] if licence_granted else ["Public SDK licence grant and IP/copyright clearance are not established."],
    ))

    support_activated = bool(
        isinstance(manifest_support, dict)
        and manifest_support.get("support_commitment_established") is True
        and manifest_support.get("production_support_activated") is True
        and sup.get("support_commitment_established") is True
        and sup.get("production_support_activated") is True
    )
    dimensions.append(dim(
        "SUPPORT_CONTRACT_ACTIVATION",
        "ACTIVATED" if support_activated else "NOT_ACTIVATED",
        support_activated,
        ["AX-PUB-SUP-001", "AX-PUB-CI-013"],
        [] if support_activated else ["Validated support contract candidate has not been explicitly activated."],
    ))

    security_ready = bool(
        isinstance(manifest_security, dict)
        and manifest_security.get("security_operations_ready") is True
        and sec.get("security_operations_ready") is True
    )
    dimensions.append(dim(
        "SECURITY_OPERATIONS_READINESS",
        "READY" if security_ready else "NOT_READY",
        security_ready,
        ["AX-PUB-SEC-001", "AX-PUB-CI-013"],
        [] if security_ready else ["Security operations owner/intake/remediation/release process is not established as ready."],
    ))

    # No repository evidence currently establishes a named release owner with
    # explicit accountability for this package release. Absence is fail-closed.
    release_owner = manifest.get("current_sdk_release_owner")
    release_owner_established = isinstance(release_owner, dict) and bool(release_owner.get("established") is True and release_owner.get("owner_id"))
    dimensions.append(dim(
        "RELEASE_OWNER_AND_ACCOUNTABILITY",
        "ESTABLISHED" if release_owner_established else "NOT_ESTABLISHED",
        release_owner_established,
        ["AX-PUB-MANIFEST-001"],
        [] if release_owner_established else ["No canonical named SDK release owner/accountability record is established."],
    ))

    release_authorized = bool(
        isinstance(manifest_gate, dict)
        and manifest_gate.get("disposition") == "SDK PUBLICATION AUTHORIZED"
        and isinstance(manifest_program, dict)
        and manifest_program.get("active_phase") == "DEV-GATE-05D — Release Authority"
    )
    dimensions.append(dim(
        "EXPLICIT_RELEASE_AUTHORITY",
        "AUTHORIZED" if release_authorized else "NOT_AUTHORIZED",
        release_authorized,
        ["AX-PUB-GATE-001", "AX-PUB-MANIFEST-001"],
        [] if release_authorized else ["DEV-GATE-05D explicit release authority is not established."],
    ))

    required_ids = [x.get("id") for x in contract.get("required_dimensions", []) if isinstance(x, dict) and x.get("required_for_05d") is True]
    observed_ids = [x["id"] for x in dimensions]
    require(required_ids == observed_ids, "builder dimension order/identity differs from release-pack contract")

    blockers = [
        {"dimension": item["id"], "state": item["state"], "reasons": item["blockers"]}
        for item in dimensions
        if not item["established"]
    ]
    ready = not blockers

    report = {
        "report_format": "AX-PUB-RELPACK-REPORT-001",
        "report_version": "1.0",
        "source_commit": args.source_commit.lower(),
        "contract": {"id": "AX-PUB-RELPACK-001", "version": "0.1"},
        "manifest": {
            "id": manifest.get("manifest_id"),
            "version": manifest.get("manifest_version"),
            "sha256": sha256(MANIFEST),
        },
        "candidate": candidate,
        "dimensions": dimensions,
        "blockers": blockers,
        "required_dimension_count": len(dimensions),
        "established_dimension_count": sum(1 for item in dimensions if item["established"]),
        "blocked_dimension_count": len(blockers),
        "ready_for_dev_gate_05d_authority_review": ready,
        "report_state": "READY_FOR_DEV_GATE_05D_AUTHORITY_REVIEW" if ready else "BLOCKED_BEFORE_DEV_GATE_05D_AUTHORITY_REVIEW",
        "dev_gate_05d_authorized": False,
        "sdk_publication_authorized": False,
        "claim_boundaries": [
            "REPORT GENERATION DOES NOT CREATE MISSING EVIDENCE OR AUTHORITY",
            "READY FOR AUTHORITY REVIEW DOES NOT ITSELF AUTHORIZE PUBLICATION",
            "DEV-GATE-05D EXPLICIT AUTHORITY REMAINS A SEPARATE DECISION",
            "SDK PUBLICATION NOT AUTHORIZED",
        ],
    }

    # The current contract explicitly predicts a blocked baseline. If the
    # repository evolves enough to become ready, the governed contract must be
    # updated and independently reviewed rather than silently crossing 05D.
    expected = contract.get("current_expected_disposition")
    require(isinstance(expected, dict), "current expected disposition missing")
    require(expected.get("ready_for_dev_gate_05d_authority_review") is ready, "derived readiness differs from governed current expected disposition")
    require(expected.get("dev_gate_05d_authorized") is False, "contract must not pre-authorize 05D")
    require(expected.get("sdk_publication_authorized") is False, "contract must not pre-authorize publication")

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "AX_RELEASE_PACK_BUILD_PASS "
        f"report_state={report['report_state']} established={report['established_dimension_count']} "
        f"blocked={report['blocked_dimension_count']} ready_for_05d={str(ready).lower()} "
        "dev_gate_05d_authorized=false sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
