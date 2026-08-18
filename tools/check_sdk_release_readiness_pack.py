#!/usr/bin/env python3
"""Validate AX-PUB-RELPACK-001 and a generated readiness report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "artifacts" / "AX-PUB-RELPACK-001.json"
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"

EXPECTED_ORDER = [
    "ENGINEERING_CANDIDATE_IDENTITY",
    "PUBLIC_API_CONTRACT",
    "EXACT_ARTIFACT_RUNTIME_VALIDATION",
    "SUPPLY_CHAIN_PROVENANCE_SBOM",
    "EXTERNAL_REGISTRY_VALIDATION",
    "INDEPENDENT_HUMAN_EXTERNAL_EVALUATION",
    "RELEASE_CONTROL_READINESS",
    "REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER",
    "LICENCE_AND_IP_CLEARANCE",
    "SUPPORT_CONTRACT_ACTIVATION",
    "SECURITY_OPERATIONS_READINESS",
    "RELEASE_OWNER_AND_ACCOUNTABILITY",
    "EXPLICIT_RELEASE_AUTHORITY",
]

EXPECTED_CURRENT_STATES = {
    "ENGINEERING_CANDIDATE_IDENTITY": ("ESTABLISHED", True),
    "PUBLIC_API_CONTRACT": ("VALIDATED_CANDIDATE", True),
    "EXACT_ARTIFACT_RUNTIME_VALIDATION": ("ESTABLISHED", True),
    "SUPPLY_CHAIN_PROVENANCE_SBOM": ("ESTABLISHED_ENGINEERING_EVIDENCE", True),
    "EXTERNAL_REGISTRY_VALIDATION": ("NOT_ESTABLISHED", False),
    "INDEPENDENT_HUMAN_EXTERNAL_EVALUATION": ("NOT_ESTABLISHED", False),
    "RELEASE_CONTROL_READINESS": ("NOT_ESTABLISHED", False),
    "REGISTRY_OWNERSHIP_AND_TRUSTED_PUBLISHER": ("NOT_ESTABLISHED", False),
    "LICENCE_AND_IP_CLEARANCE": ("NOT_ESTABLISHED", False),
    "SUPPORT_CONTRACT_ACTIVATION": ("NOT_ACTIVATED", False),
    "SECURITY_OPERATIONS_READINESS": ("NOT_READY", False),
    "RELEASE_OWNER_AND_ACCOUNTABILITY": ("NOT_ESTABLISHED", False),
    "EXPLICIT_RELEASE_AUTHORITY": ("NOT_AUTHORIZED", False),
}

WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]


def fail(message: str) -> None:
    raise SystemExit(f"AX_RELEASE_PACK_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path}: {exc}")
    require(isinstance(value, dict), f"{path} must contain an object")
    return value


def check_contract() -> None:
    contract = load(CONTRACT)
    require(contract.get("artifact_id") == "AX-PUB-RELPACK-001", "contract artifact ID mismatch")
    require(contract.get("version") == "0.1", "contract version mismatch")
    require(contract.get("state") == "DEV_GATE_05D_RELEASE_READINESS_PACK_CANDIDATE_BLOCKED", "contract state mismatch")
    candidate = contract.get("candidate")
    require(isinstance(candidate, dict), "contract candidate missing")
    require(candidate.get("distribution") == "aetherxglobal-governed-intelligence", "contract distribution mismatch")
    require(candidate.get("version") == "0.1.0rc1", "contract candidate version mismatch")
    require(candidate.get("import_namespace") == "aetherxglobal.governed_intelligence", "contract import mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA and candidate.get("sdist_sha256") == SDIST_SHA, "contract package digest mismatch")
    require(candidate.get("runtime_matrix") == RUNTIMES, "contract runtime matrix mismatch")

    dims = contract.get("required_dimensions")
    require(isinstance(dims, list), "required dimensions missing")
    ids = [item.get("id") for item in dims if isinstance(item, dict)]
    require(ids == EXPECTED_ORDER, "required dimension order/identity mismatch")
    require(all(item.get("required_for_05d") is True for item in dims if isinstance(item, dict)), "all declared dimensions must be hard 05D requirements")

    expected = contract.get("current_expected_disposition")
    require(isinstance(expected, dict), "current expected disposition missing")
    require(expected.get("ready_for_dev_gate_05d_authority_review") is False, "contract must remain blocked before 05D authority review")
    require(expected.get("dev_gate_05d_authorized") is False, "contract must not authorize 05D")
    require(expected.get("sdk_publication_authorized") is False, "contract must not authorize publication")

    boundaries = set(contract.get("claim_boundaries", []))
    for marker in (
        "RELEASE READINESS PACK PASS DOES NOT ESTABLISH RELEASE READINESS WHEN REQUIRED DIMENSIONS ARE BLOCKED",
        "AGGREGATED EVIDENCE DOES NOT CREATE REGISTRY OWNERSHIP, LICENCE RIGHTS, HUMAN EVALUATION OR RELEASE AUTHORITY",
        "CI CANNOT SUBSTITUTE FOR INDEPENDENT HUMAN EVALUATION OR EXPLICIT AUTHORIZED DECISION",
        "READY FOR AUTHORITY REVIEW DOES NOT ITSELF AUTHORIZE PUBLICATION",
        "DEV-GATE-05D NOT AUTHORIZED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in boundaries, f"contract claim boundary missing: {marker}")

    manifest = load(MANIFEST)
    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    try:
        major, minor = [int(x) for x in str(manifest.get("manifest_version", "0.0")).split(".")[:2]]
    except ValueError:
        fail("invalid manifest version")
    require((major, minor) >= (1, 25), "release-readiness pack requires manifest >= v1.25")


def check_report(report_path: Path) -> None:
    report = load(report_path)
    require(report.get("report_format") == "AX-PUB-RELPACK-REPORT-001", "report format mismatch")
    require(report.get("report_version") == "1.0", "report version mismatch")
    source_commit = report.get("source_commit")
    require(isinstance(source_commit, str) and len(source_commit) == 40 and all(c in "0123456789abcdef" for c in source_commit.lower()), "report source commit invalid")

    contract = report.get("contract")
    require(contract == {"id": "AX-PUB-RELPACK-001", "version": "0.1"}, "report contract identity mismatch")
    manifest = report.get("manifest")
    require(isinstance(manifest, dict), "report manifest identity missing")
    require(manifest.get("id") == "AX-PUB-MANIFEST-001", "report manifest ID mismatch")
    require(isinstance(manifest.get("sha256"), str) and len(manifest["sha256"]) == 64, "report manifest digest invalid")

    candidate = report.get("candidate")
    require(isinstance(candidate, dict), "report candidate missing")
    require(candidate.get("distribution") == "aetherxglobal-governed-intelligence", "report distribution mismatch")
    require(candidate.get("version") == "0.1.0rc1", "report candidate version mismatch")
    require(candidate.get("wheel_sha256") == WHEEL_SHA and candidate.get("sdist_sha256") == SDIST_SHA, "report package digest mismatch")
    require(candidate.get("runtime_matrix") == RUNTIMES, "report runtime matrix mismatch")

    dimensions = report.get("dimensions")
    require(isinstance(dimensions, list), "report dimensions missing")
    require([item.get("id") for item in dimensions if isinstance(item, dict)] == EXPECTED_ORDER, "report dimension order/identity mismatch")
    for item in dimensions:
        require(isinstance(item, dict), "report dimension must be object")
        dimension_id = item.get("id")
        require(dimension_id in EXPECTED_CURRENT_STATES, f"unknown dimension: {dimension_id}")
        expected_state, expected_established = EXPECTED_CURRENT_STATES[dimension_id]
        require(item.get("state") == expected_state, f"{dimension_id} state mismatch")
        require(item.get("established") is expected_established, f"{dimension_id} established flag mismatch")
        evidence = item.get("evidence")
        blockers = item.get("blockers")
        require(isinstance(evidence, list) and evidence, f"{dimension_id} evidence refs missing")
        require(isinstance(blockers, list), f"{dimension_id} blockers must be list")
        if expected_established:
            require(blockers == [], f"{dimension_id} established dimension must not carry blockers")
        else:
            require(bool(blockers), f"{dimension_id} blocked dimension must explain why")

    require(report.get("required_dimension_count") == 13, "required dimension count mismatch")
    require(report.get("established_dimension_count") == 4, "established dimension count mismatch")
    require(report.get("blocked_dimension_count") == 9, "blocked dimension count mismatch")

    blockers = report.get("blockers")
    require(isinstance(blockers, list) and len(blockers) == 9, "blocker summary mismatch")
    blocker_ids = [item.get("dimension") for item in blockers if isinstance(item, dict)]
    require(blocker_ids == EXPECTED_ORDER[4:], "blocker dimension sequence mismatch")

    require(report.get("ready_for_dev_gate_05d_authority_review") is False, "current report must remain blocked before 05D authority review")
    require(report.get("report_state") == "BLOCKED_BEFORE_DEV_GATE_05D_AUTHORITY_REVIEW", "current report state mismatch")
    require(report.get("dev_gate_05d_authorized") is False, "report must not authorize 05D")
    require(report.get("sdk_publication_authorized") is False, "report must not authorize publication")

    boundaries = set(report.get("claim_boundaries", []))
    for marker in (
        "REPORT GENERATION DOES NOT CREATE MISSING EVIDENCE OR AUTHORITY",
        "READY FOR AUTHORITY REVIEW DOES NOT ITSELF AUTHORIZE PUBLICATION",
        "DEV-GATE-05D EXPLICIT AUTHORITY REMAINS A SEPARATE DECISION",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in boundaries, f"report claim boundary missing: {marker}")

    print(
        "AX_RELEASE_PACK_REPORT_PASS "
        "required=13 established=4 blocked=9 ready_for_05d=false "
        "dev_gate_05d_authorized=false sdk_publication=NOT_AUTHORIZED"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    check_contract()
    if args.report is not None:
        check_report(args.report)
    print("AX_RELEASE_PACK_CONTRACT_PASS state=BLOCKED dev_gate_05d=NOT_AUTHORIZED sdk_publication=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
