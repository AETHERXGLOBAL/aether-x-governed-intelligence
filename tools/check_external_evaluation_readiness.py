#!/usr/bin/env python3
"""Validate DEV-GATE-04 external-evaluation-readiness governance state."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/AX-PUB-DEV-006.json"
MANIFEST = ROOT / "artifacts/AX-PUB-MANIFEST-001.json"

REQUIRED_PATHS = [
    "docs/AX-PUB-DEV-006_EXTERNAL_EVALUATION_READINESS.md",
    "artifacts/AX-PUB-DEV-006.json",
    "docs/EXTERNAL_EVALUATOR_GUIDE.md",
    "docs/LIMITATIONS_AND_UNSUPPORTED_USES.md",
    "docs/MIGRATION_AND_DEPRECATION_DRAFT.md",
    "docs/FEEDBACK_AND_TRIAGE.md",
    ".github/ISSUE_TEMPLATE/external-evaluation.yml",
    "tools/run_external_evaluation.py",
    "tools/check_external_evaluation_report.py",
    "tools/check_external_evaluation_readiness.py",
    ".github/workflows/validate-external-evaluation-readiness.yml",
]


def fail(message: str) -> int:
    print(f"AX_DEV_GATE_04_STATE_FAIL {message}")
    return 1


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def parse_version(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)", value)
    if not match:
        raise ValueError(f"invalid version: {value}")
    return int(match.group(1)), int(match.group(2))


def require_text(path: str, *needles: str) -> str | None:
    content = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in content:
            return f"missing_text={path}:{needle}"
    return None


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        return fail("missing_paths=" + ",".join(missing))

    try:
        state = load_json(ARTIFACT)
        manifest = load_json(MANIFEST)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(f"invalid_json={exc}")

    if state.get("artifact_id") != "AX-PUB-DEV-006" or state.get("version") != "1.0":
        return fail("artifact_identity")
    if state.get("gate") != "DEV-GATE-04":
        return fail("gate_identity")
    if state.get("state") not in {"CANDIDATE", "CLOSED"}:
        return fail("unsupported_gate_state")
    if state.get("sdk_publication") != "NOT_AUTHORIZED":
        return fail("sdk_publication_boundary")
    if state.get("external_evaluation_occurred") is not False:
        return fail("external_evaluation_claim_boundary")
    if state.get("external_adoption_established") is not False:
        return fail("external_adoption_claim_boundary")
    if state.get("supported_sdk_established") is not False:
        return fail("supported_sdk_boundary")
    if state.get("package_identity_approved") is not False:
        return fail("package_identity_boundary")
    if state.get("package_registry_authorized") is not False:
        return fail("package_registry_boundary")
    if state.get("public_sdk_licence_decided") is not False:
        return fail("licence_boundary")

    if set(state.get("declared_candidate_runtime_matrix", [])) != {"3.10", "3.11", "3.12", "3.13"}:
        return fail("runtime_matrix")

    expected_contracts = {
        ("AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-SPEC-004", "1.0"),
    }
    contracts = {
        (item.get("contract_id"), item.get("version"))
        for item in state.get("declared_contract_surface", [])
        if isinstance(item, dict)
    }
    if contracts != expected_contracts:
        return fail("declared_contract_surface")

    checks = [
        require_text(
            "docs/AX-PUB-DEV-006_EXTERNAL_EVALUATION_READINESS.md",
            "EXTERNAL EVALUATION READINESS NOT YET ESTABLISHED" if state["state"] == "CANDIDATE" else "DEV-GATE-04: CLOSED",
            "SDK PUBLICATION NOT AUTHORIZED",
            "EXTERNAL EVALUATION READINESS",
            "EXTERNAL EVALUATION OCCURRED",
            "EXTERNAL ADOPTION",
        ),
        require_text(
            "docs/EXTERNAL_EVALUATOR_GUIDE.md",
            "python3 tools/run_external_evaluation.py --json-out external-evaluation-report.json",
            "AX_EXTERNAL_EVALUATION_RUN_PASS",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
        require_text(
            "docs/LIMITATIONS_AND_UNSUPPORTED_USES.md",
            "No External Adoption Claim",
            "No Support Promise",
            "SDK PUBLICATION: NOT AUTHORIZED",
        ),
        require_text(
            "docs/MIGRATION_AND_DEPRECATION_DRAFT.md",
            "NOT A SUPPORT COMMITMENT",
            "No Fixed Support Window Yet",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
        require_text(
            "docs/FEEDBACK_AND_TRIAGE.md",
            "NO SUPPORT SLA",
            "SECURITY.md",
            "FEATURE REQUEST ≠ ROADMAP COMMITMENT",
        ),
        require_text(
            ".github/ISSUE_TEMPLATE/external-evaluation.yml",
            "External evaluation feedback",
            "SECURITY.md",
            "does not create a support or response-time SLA",
        ),
    ]
    for error in checks:
        if error:
            return fail(error)

    evaluator_guide = (ROOT / "docs/EXTERNAL_EVALUATOR_GUIDE.md").read_text(encoding="utf-8")
    forbidden = [
        "pip install aetherx",
        "SUPPORTED SDK: ESTABLISHED",
        "SDK PUBLICATION: AUTHORIZED",
        "EXTERNAL ADOPTION: ESTABLISHED",
    ]
    for needle in forbidden:
        if needle in evaluator_guide:
            return fail(f"forbidden_claim={needle}")

    try:
        if parse_version(str(manifest.get("manifest_version"))) < (1, 17):
            return fail("manifest_version_lt_1.17")
    except ValueError as exc:
        return fail(str(exc))

    artifacts = {item.get("id"): item for item in manifest.get("artifacts", []) if isinstance(item, dict)}
    manifest_dev006 = artifacts.get("AX-PUB-DEV-006")
    if not manifest_dev006:
        return fail("manifest_missing_AX-PUB-DEV-006")
    if manifest_dev006.get("version") != "1.0":
        return fail("manifest_DEV006_version")
    if manifest_dev006.get("path") != "docs/AX-PUB-DEV-006_EXTERNAL_EVALUATION_READINESS.md":
        return fail("manifest_DEV006_path")
    if manifest_dev006.get("machine_readable_companion") != "artifacts/AX-PUB-DEV-006.json":
        return fail("manifest_DEV006_companion")

    maturity = str(manifest_dev006.get("public_maturity", ""))
    if state["state"] == "CANDIDATE":
        if "DEV-GATE-04 CANDIDATE" not in maturity or "NOT YET ESTABLISHED" not in maturity:
            return fail("manifest_candidate_maturity")
        marker = "AX_DEV_GATE_04_CANDIDATE_STATE_PASS"
    else:
        if state.get("external_evaluation_readiness") != "ESTABLISHED":
            return fail("closed_state_readiness")
        if "DEV-GATE-04 CLOSED" not in maturity or "EXTERNAL EVALUATION READINESS ESTABLISHED" not in maturity:
            return fail("manifest_closed_maturity")
        evidence = {item.get("id"): item for item in manifest.get("validation_evidence", []) if isinstance(item, dict)}
        if "AX-PUB-CI-007" not in evidence:
            return fail("closed_state_missing_CI007")
        marker = "AX_DEV_GATE_04_CLOSED_STATE_PASS"

    print(
        f"{marker} manifest={manifest['manifest_version']} "
        "sdk_publication=NOT_AUTHORIZED external_evaluation_occurred=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
