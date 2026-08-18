#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 repository consistency.

The checker preserves the closed Gate-00→04 governance chain while avoiding
hard-coding a previously active gate as a permanent invariant.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts/AX-PUB-MANIFEST-001.json"
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+(?:\.[0-9]+(?:-[0-9A-Za-z.-]+)?)?$")
STATES = {"CURRENT", "COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}
EXPECTED_RUNTIMES = ["3.10", "3.11", "3.12", "3.13"]
EXPECTED_GATE_03_DIGEST = "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21"
EXPECTED_GATE_03_EPOCH = 1787064230

REQUIRED_PAIRS = {
    ("AX-PUB-ARCH-001", "1.0"),
    ("AX-PUB-SPEC-002", "1.0"),
    ("AX-PUB-SPEC-003", "1.0"),
    ("AX-PUB-SPEC-004", "1.0"),
    ("AX-PUB-SCHEMA-001", "1.0"),
    ("AX-PUB-SCHEMA-002", "1.0"),
    ("AX-PUB-SCHEMA-003", "1.0"),
    ("AX-PUB-REF-001", "1.0"),
    ("AX-PUB-REF-002", "1.0"),
    ("AX-PUB-REF-003", "1.0"),
    ("AX-PUB-TEST-001", "1.0"),
    ("AX-PUB-TEST-002", "1.0"),
    ("AX-PUB-POL-001", "1.6"),
    ("AX-PUB-SNAP-002", "1.0"),
    ("AX-PUB-REL-001", "1.0"),
    ("AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-002", "1.0"),
    ("AX-PUB-DEV-003", "1.0"),
    ("AX-PUB-DEV-004", "1.0"),
    ("AX-PUB-DEV-005", "1.0"),
    ("AX-PUB-DEV-006", "1.0"),
    ("AX-PUB-RC-001", "0.1.0-rc1"),
}

REQUIRED_RELATIONS = {
    ("AX-PUB-SCHEMA-001", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-002", "1.0"),
    ("AX-PUB-REF-001", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-001", "1.0"),
    ("AX-PUB-SCHEMA-002", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-003", "1.0"),
    ("AX-PUB-REF-002", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-002", "1.0"),
    ("AX-PUB-SPEC-004", "1.0", "ALIGNS_WITH_ARCHITECTURE", "AX-PUB-ARCH-001", "1.0"),
    ("AX-PUB-SPEC-004", "1.0", "SPECIALIZES_AUTHORITY_BOUNDARY_OF", "AX-PUB-SPEC-002", "1.0"),
    ("AX-PUB-SCHEMA-003", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-004", "1.0"),
    ("AX-PUB-REF-003", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-003", "1.0"),
    ("AX-PUB-TEST-001", "1.0", "EXERCISES_PUBLIC_BEHAVIOR_OF", "AX-PUB-REF-001", "1.0"),
    ("AX-PUB-TEST-001", "1.0", "EXERCISES_PUBLIC_BEHAVIOR_OF", "AX-PUB-REF-002", "1.0"),
    ("AX-PUB-TEST-002", "1.0", "EXERCISES_PUBLIC_BEHAVIOR_OF", "AX-PUB-REF-003", "1.0"),
    ("AX-PUB-REL-001", "1.0", "PACKAGES_PUBLIC_STATE_WITH", "AX-PUB-SNAP-002", "1.0"),
    ("AX-PUB-DEV-001", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-002", "1.0", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-002", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-003", "1.0", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-003", "1.0", "BUILDS_ON", "AX-PUB-DEV-002", "1.0"),
    ("AX-PUB-DEV-003", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-004", "1.0", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-004", "1.0", "BUILDS_ON", "AX-PUB-DEV-003", "1.0"),
    ("AX-PUB-DEV-004", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-005", "1.0", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-005", "1.0", "BUILDS_ON", "AX-PUB-DEV-004", "1.0"),
    ("AX-PUB-DEV-005", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-DEV-006", "1.0", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0"),
    ("AX-PUB-DEV-006", "1.0", "BUILDS_ON", "AX-PUB-DEV-005", "1.0"),
    ("AX-PUB-DEV-006", "1.0", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0"),
    ("AX-PUB-RC-001", "0.1.0-rc1", "CANDIDATE_ARTIFACT_OF", "AX-PUB-DEV-005", "1.0"),
}

REQUIRED_CLAIM_BOUNDARIES = {
    "PUBLIC COMPATIBILITY DOES NOT ESTABLISH PRODUCT INTEGRATION",
    "SDK CANDIDATE ESTABLISHED DOES NOT ESTABLISH A SUPPORTED SDK OR PACKAGE RELEASE",
    "RELEASE-CANDIDATE VALIDATED DOES NOT ESTABLISH A SUPPORTED SDK OR PACKAGE RELEASE",
    "EXTERNAL EVALUATION READINESS ESTABLISHED DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION OR ADOPTION",
    "PACKAGE IDENTITY AND REGISTRY REMAIN UNAPPROVED OR UNAUTHORIZED",
    "SDK PUBLICATION REMAINS NOT AUTHORIZED",
}


def fail(findings: list[str]) -> int:
    for item in findings:
        print(f"AX_MANIFEST_FAIL: {item}")
    return 1


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(value, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain an object")
        return None
    return value


def safe_path(raw: Any, findings: list[str], label: str) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        findings.append(f"{label}: invalid path")
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        findings.append(f"{label}: path escapes repository: {raw}")
        return None
    return ROOT / path


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    if not isinstance(raw, str) or VERSION_RE.fullmatch(raw) is None:
        return False
    base = raw.split("-", 1)[0].split(".")
    try:
        return (int(base[0]), int(base[1])) >= (major, minor)
    except (ValueError, IndexError):
        return False


def check_artifact(path: Path, artifact_id: str, version: str, findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"artifact path missing: {path.relative_to(ROOT)}")
        return
    if path.name.endswith(".schema.json"):
        data = load_json(path, findings)
        if data is None:
            return
        if f":{artifact_id}:{version}" not in str(data.get("$id", "")):
            findings.append(f"{path.relative_to(ROOT)} $id mismatch")
        properties = data.get("properties", {})
        if properties.get("schema_id", {}).get("const") != artifact_id:
            findings.append(f"{path.relative_to(ROOT)} schema_id mismatch")
        if properties.get("schema_version", {}).get("const") != version:
            findings.append(f"{path.relative_to(ROOT)} schema_version mismatch")
    elif path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if artifact_id not in text:
            findings.append(f"{path.relative_to(ROOT)} does not declare {artifact_id}")
        if f"`{version}`" not in text:
            findings.append(f"{path.relative_to(ROOT)} does not declare version {version}")


def require_path(obj: dict[str, Any], field: str, findings: list[str], label: str) -> None:
    target = safe_path(obj.get(field), findings, f"{label}.{field}")
    if target is not None and not target.is_file():
        findings.append(f"{label}.{field} missing: {obj.get(field)}")


def expect(obj: dict[str, Any], field: str, expected: Any, findings: list[str], label: str) -> None:
    if obj.get(field) != expected:
        findings.append(f"{label}.{field} mismatch: expected={expected!r} actual={obj.get(field)!r}")


def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None:
        return fail(findings)

    expect(manifest, "manifest_id", "AX-PUB-MANIFEST-001", findings, "manifest")
    if not version_at_least(manifest.get("manifest_version"), 1, 18):
        findings.append("manifest_version must be >= 1.18")
    expect(manifest, "repository", "AETHERXGLOBAL/aether-x-governed-intelligence", findings, "manifest")

    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict):
        findings.append("versioning_policy must be object")
    else:
        expect(policy, "id", "AX-PUB-POL-001", findings, "versioning_policy")
        expect(policy, "version", "1.6", findings, "versioning_policy")
        require_path(policy, "path", findings, "versioning_policy")

    artifacts_raw = manifest.get("artifacts")
    artifacts = artifacts_raw if isinstance(artifacts_raw, list) else []
    if not artifacts:
        findings.append("artifacts must be a non-empty array")
    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    seen_ids: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            findings.append(f"artifacts[{index}] must be object")
            continue
        artifact_id = artifact.get("id")
        version = artifact.get("version")
        if not isinstance(artifact_id, str) or not artifact_id.startswith("AX-PUB-"):
            findings.append(f"artifacts[{index}].id invalid")
            continue
        if not isinstance(version, str) or VERSION_RE.fullmatch(version) is None:
            findings.append(f"artifacts[{index}].version invalid")
            continue
        if artifact_id in seen_ids:
            findings.append(f"duplicate current artifact id: {artifact_id}")
        seen_ids.add(artifact_id)
        by_pair[(artifact_id, version)] = artifact
        if artifact.get("state") not in STATES:
            findings.append(f"artifacts[{index}].state invalid")
        path = safe_path(artifact.get("path"), findings, f"artifacts[{index}]")
        if path is not None:
            check_artifact(path, artifact_id, version, findings)
        for field in ("entrypoint", "machine_readable_companion"):
            if field in artifact:
                require_path(artifact, field, findings, f"artifacts[{index}]")

    for pair in sorted(REQUIRED_PAIRS - set(by_pair)):
        findings.append(f"required current artifact missing: {pair}")

    dev001_artifact = by_pair.get(("AX-PUB-DEV-001", "1.0"), {})
    dev001_maturity = str(dev001_artifact.get("public_maturity", ""))
    for marker in ("DEV-GATE-04 CLOSED", "DEV-GATE-05 ACTIVE", "SDK PUBLICATION NOT AUTHORIZED"):
        if marker not in dev001_maturity:
            findings.append(f"AX-PUB-DEV-001 public_maturity missing: {marker}")

    dev006_artifact = by_pair.get(("AX-PUB-DEV-006", "1.0"), {})
    dev006_maturity = str(dev006_artifact.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-04 CLOSED",
        "EXTERNAL EVALUATION READINESS ESTABLISHED",
        "HUMAN EXTERNAL EVALUATION NOT ESTABLISHED",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        if marker not in dev006_maturity:
            findings.append(f"AX-PUB-DEV-006 public_maturity missing: {marker}")

    relations: set[tuple[str, str, str, str, str]] = set()
    for index, relation in enumerate(manifest.get("relationships", [])):
        if not isinstance(relation, dict):
            findings.append(f"relationships[{index}] must be object")
            continue
        source = (relation.get("from_id"), relation.get("from_version"))
        target = (relation.get("to_id"), relation.get("to_version"))
        if source not in by_pair:
            findings.append(f"relationship source missing: {source}")
        if target not in by_pair:
            findings.append(f"relationship target missing: {target}")
        if relation.get("state") not in STATES - {"CURRENT"}:
            findings.append(f"relationships[{index}].state invalid")
        relations.add((str(source[0]), str(source[1]), str(relation.get("relationship")), str(target[0]), str(target[1])))
    for relation in sorted(REQUIRED_RELATIONS - relations):
        findings.append(f"required compatibility relationship missing: {relation}")

    evidence_raw = manifest.get("validation_evidence")
    evidence = evidence_raw if isinstance(evidence_raw, list) else []
    if not isinstance(evidence_raw, list):
        findings.append("validation_evidence must be an array")
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            findings.append(f"validation_evidence[{index}] invalid")
            continue
        evidence_id = item.get("id")
        if isinstance(evidence_id, str):
            evidence_by_id[evidence_id] = item
        path = safe_path(item.get("path"), findings, f"validation_evidence[{index}]")
        if path is not None and not path.is_file():
            findings.append(f"validation evidence path missing: {item.get('path')}")
        head = item.get("verified_head_commit")
        if not isinstance(head, str) or len(head) != 40:
            findings.append(f"validation_evidence[{index}].verified_head_commit invalid")

    for evidence_id in (
        "AX-PUB-CI-001", "AX-PUB-CI-002", "AX-PUB-CI-003", "AX-PUB-CI-004",
        "AX-PUB-CI-005", "AX-PUB-CI-006", "AX-PUB-CI-007",
    ):
        if evidence_id not in evidence_by_id:
            findings.append(f"required validation evidence missing: {evidence_id}")

    ci006 = evidence_by_id.get("AX-PUB-CI-006", {})
    expect(ci006, "version", "1.1", findings, "CI006")
    expect(ci006, "workflow_run_id", 32150126557, findings, "CI006")
    expect(ci006, "workflow_run_number", 7, findings, "CI006")
    expect(ci006, "governance_workflow_run_id", 32150126711, findings, "CI006")
    expect(ci006, "governance_workflow_run_number", 135, findings, "CI006")
    expect(ci006, "verified_build_digest", EXPECTED_GATE_03_DIGEST, findings, "CI006")
    expect(ci006, "source_date_epoch", EXPECTED_GATE_03_EPOCH, findings, "CI006")
    expect(ci006, "conclusion", "SUCCESS", findings, "CI006")

    ci007 = evidence_by_id.get("AX-PUB-CI-007", {})
    expect(ci007, "version", "1.0", findings, "CI007")
    expect(ci007, "workflow_run_id", 32162256262, findings, "CI007")
    expect(ci007, "workflow_run_number", 6, findings, "CI007")
    expect(ci007, "governance_workflow_run_id", 32162256504, findings, "CI007")
    expect(ci007, "governance_workflow_run_number", 145, findings, "CI007")
    expect(ci007, "verified_runtime_matrix", EXPECTED_RUNTIMES, findings, "CI007")
    expect(ci007, "human_external_evaluation", False, findings, "CI007")
    expect(ci007, "external_adoption_established", False, findings, "CI007")
    expect(ci007, "conclusion", "SUCCESS", findings, "CI007")

    snapshot = manifest.get("current_snapshot")
    if not isinstance(snapshot, dict):
        findings.append("current_snapshot must be object")
    else:
        expect(snapshot, "id", "AX-PUB-SNAP-002", findings, "current_snapshot")
        expect(snapshot, "version", "1.0", findings, "current_snapshot")
        expect(snapshot, "anchor_commit", "6dfdec04a4d8375bc2da0bb6a3830ff07eeb1711", findings, "current_snapshot")
        require_path(snapshot, "path", findings, "current_snapshot")

    release = manifest.get("current_release")
    if not isinstance(release, dict):
        findings.append("current_release must be object")
    else:
        expect(release, "id", "AX-PUB-REL-001", findings, "current_release")
        expect(release, "version", "1.0", findings, "current_release")
        expect(release, "tag", "public-engineering-vnext-1.0", findings, "current_release")
        expect(release, "tag_target_commit", "4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6", findings, "current_release")
        require_path(release, "path", findings, "current_release")

    gate = manifest.get("current_readiness_gate")
    if not isinstance(gate, dict):
        findings.append("current_readiness_gate must be object")
    else:
        expect(gate, "id", "AX-PUB-GATE-001", findings, "current_readiness_gate")
        expect(gate, "version", "1.0", findings, "current_readiness_gate")
        expect(gate, "disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "current_readiness_gate")
        require_path(gate, "path", findings, "current_readiness_gate")

    program = manifest.get("current_developer_program")
    if not isinstance(program, dict):
        findings.append("current_developer_program must be object")
    else:
        expect(program, "id", "AX-PUB-DEV-001", findings, "current_developer_program")
        expect(program, "version", "1.0", findings, "current_developer_program")
        expect(program, "state", "UNDER DEVELOPMENT", findings, "current_developer_program")
        expect(program, "closed_gate", "DEV-GATE-04 — External Evaluation Readiness", findings, "current_developer_program")
        expect(program, "active_gate", "DEV-GATE-05 — SDK Release Decision", findings, "current_developer_program")
        expect(program, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "current_developer_program")
        require_path(program, "path", findings, "current_developer_program")

    baseline = manifest.get("current_developer_contract_baseline")
    if not isinstance(baseline, dict):
        findings.append("current_developer_contract_baseline must be object")
    else:
        expect(baseline, "id", "AX-PUB-DEV-002", findings, "DEV002")
        expect(baseline, "version", "1.0", findings, "DEV002")
        expect(baseline, "gate", "DEV-GATE-00", findings, "DEV002")
        expect(baseline, "state", "CLOSED", findings, "DEV002")
        expect(baseline, "closure_evidence", "AX-PUB-CI-003", findings, "DEV002")
        for field in ("path", "machine_readable_companion"):
            require_path(baseline, field, findings, "DEV002")

    experience = manifest.get("current_developer_experience")
    if not isinstance(experience, dict):
        findings.append("current_developer_experience must be object")
    else:
        expect(experience, "id", "AX-PUB-DEV-003", findings, "DEV003")
        expect(experience, "version", "1.0", findings, "DEV003")
        expect(experience, "gate", "DEV-GATE-01", findings, "DEV003")
        expect(experience, "state", "CLOSED", findings, "DEV003")
        expect(experience, "verified_runtime_matrix", EXPECTED_RUNTIMES, findings, "DEV003")
        expect(experience, "closure_evidence", "AX-PUB-CI-004", findings, "DEV003")
        for field in ("path", "machine_readable_companion", "runner", "state_checker"):
            require_path(experience, field, findings, "DEV003")

    sdk = manifest.get("current_sdk_candidate")
    if not isinstance(sdk, dict):
        findings.append("current_sdk_candidate must be object")
    else:
        expect(sdk, "id", "AX-PUB-DEV-004", findings, "DEV004")
        expect(sdk, "version", "1.0", findings, "DEV004")
        expect(sdk, "gate", "DEV-GATE-02", findings, "DEV004")
        expect(sdk, "state", "CLOSED", findings, "DEV004")
        expect(sdk, "candidate_version", "0.1.0-candidate", findings, "DEV004")
        expect(sdk, "candidate_runtime_matrix", EXPECTED_RUNTIMES, findings, "DEV004")
        expect(sdk, "verified_runtime_matrix", EXPECTED_RUNTIMES, findings, "DEV004")
        expect(sdk, "closure_evidence", "AX-PUB-CI-005", findings, "DEV004")
        expect(sdk, "package_identity_status", "NOT APPROVED", findings, "DEV004")
        expect(sdk, "registry_status", "NOT AUTHORIZED", findings, "DEV004")
        expect(sdk, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "DEV004")
        for field in ("path", "machine_readable_companion", "candidate_module"):
            require_path(sdk, field, findings, "DEV004")

    supply = manifest.get("current_supply_chain_release_candidate")
    if not isinstance(supply, dict):
        findings.append("current_supply_chain_release_candidate must be object")
    else:
        expect(supply, "id", "AX-PUB-DEV-005", findings, "DEV005")
        expect(supply, "version", "1.0", findings, "DEV005")
        expect(supply, "gate", "DEV-GATE-03", findings, "DEV005")
        expect(supply, "state", "CLOSED", findings, "DEV005")
        expect(supply, "release_candidate_id", "AX-PUB-RC-001", findings, "DEV005")
        expect(supply, "release_candidate_version", "0.1.0-rc1", findings, "DEV005")
        for field in ("deterministic_build", "build_provenance_attestation", "sbom_attestation", "extracted_bundle_validation"):
            expect(supply, field, "VERIFIED", findings, "DEV005")
        expect(supply, "closure_evidence", "AX-PUB-CI-006", findings, "DEV005")
        expect(supply, "verified_build_digest", EXPECTED_GATE_03_DIGEST, findings, "DEV005")
        expect(supply, "verified_source_date_epoch", EXPECTED_GATE_03_EPOCH, findings, "DEV005")
        expect(supply, "artifact_upload_scope", "CI_ONLY", findings, "DEV005")
        expect(supply, "package_identity_status", "NOT APPROVED", findings, "DEV005")
        expect(supply, "registry_status", "NOT AUTHORIZED", findings, "DEV005")
        expect(supply, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "DEV005")
        for field in ("path", "machine_readable_companion"):
            require_path(supply, field, findings, "DEV005")

    external = manifest.get("current_external_evaluation_readiness")
    if not isinstance(external, dict):
        findings.append("current_external_evaluation_readiness must be object")
    else:
        expect(external, "id", "AX-PUB-DEV-006", findings, "DEV006")
        expect(external, "version", "1.0", findings, "DEV006")
        expect(external, "gate", "DEV-GATE-04", findings, "DEV006")
        expect(external, "state", "CLOSED", findings, "DEV006")
        expect(external, "external_evaluation_readiness", "ESTABLISHED", findings, "DEV006")
        expect(external, "external_evaluation_occurred", False, findings, "DEV006")
        expect(external, "external_adoption_established", False, findings, "DEV006")
        expect(external, "declared_candidate_runtime_matrix", EXPECTED_RUNTIMES, findings, "DEV006")
        expect(external, "verified_readiness_runtime_matrix", EXPECTED_RUNTIMES, findings, "DEV006")
        expect(external, "closure_evidence", "AX-PUB-CI-007", findings, "DEV006")
        expect(external, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "DEV006")
        for field in ("path", "machine_readable_companion", "runner", "report_checker", "state_checker"):
            require_path(external, field, findings, "DEV006")

    dev005 = load_json(ROOT / "artifacts/AX-PUB-DEV-005.json", findings)
    if dev005 is not None:
        expect(dev005, "state", "DEV-GATE-03_CLOSED", findings, "AX-PUB-DEV-005.json")
        expect(dev005, "release_candidate_established", True, findings, "AX-PUB-DEV-005.json")
        expect(dev005, "verified_build_digest", EXPECTED_GATE_03_DIGEST, findings, "AX-PUB-DEV-005.json")
        expect(dev005, "verified_source_date_epoch", EXPECTED_GATE_03_EPOCH, findings, "AX-PUB-DEV-005.json")
        closure = dev005.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
            findings.append("AX-PUB-DEV-005.json closure evidence must be AX-PUB-CI-006 v1.1")
        expect(dev005, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "AX-PUB-DEV-005.json")

    dev006 = load_json(ROOT / "artifacts/AX-PUB-DEV-006.json", findings)
    if dev006 is not None:
        expect(dev006, "artifact_id", "AX-PUB-DEV-006", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "version", "1.0", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "gate", "DEV-GATE-04", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "state", "CLOSED", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "external_evaluation_readiness", "ESTABLISHED", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "external_evaluation_occurred", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "external_adoption_established", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "supported_sdk_established", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "package_identity_approved", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "package_registry_authorized", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "public_sdk_licence_decided", False, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "declared_candidate_runtime_matrix", EXPECTED_RUNTIMES, findings, "AX-PUB-DEV-006.json")
        expect(dev006, "verified_readiness_runtime_matrix", EXPECTED_RUNTIMES, findings, "AX-PUB-DEV-006.json")
        closure = dev006.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-007" or closure.get("version") != "1.0":
            findings.append("AX-PUB-DEV-006.json closure evidence must be AX-PUB-CI-007 v1.0")
        expect(dev006, "next_gate", "DEV-GATE-05 — SDK Release Decision", findings, "AX-PUB-DEV-006.json")
        expect(dev006, "sdk_publication", "NOT_AUTHORIZED", findings, "AX-PUB-DEV-006.json")

    rc = load_json(ROOT / "release-candidate/AX-PUB-RC-001.json", findings)
    if rc is not None:
        expect(rc, "artifact_id", "AX-PUB-RC-001", findings, "AX-PUB-RC-001")
        expect(rc, "version", "0.1.0-rc1", findings, "AX-PUB-RC-001")
        expect(rc, "state", "DEV-GATE-03_VALIDATED", findings, "AX-PUB-RC-001")
        expect(rc, "release_candidate_established", True, findings, "AX-PUB-RC-001")
        expect(rc, "verified_build_digest", EXPECTED_GATE_03_DIGEST, findings, "AX-PUB-RC-001")
        expect(rc, "verified_source_date_epoch", EXPECTED_GATE_03_EPOCH, findings, "AX-PUB-RC-001")
        closure = rc.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
            findings.append("AX-PUB-RC-001 closure evidence must be AX-PUB-CI-006 v1.1")
        expect(rc, "sdk_publication_disposition", "SDK PUBLICATION NOT AUTHORIZED", findings, "AX-PUB-RC-001")

    boundaries = manifest.get("claim_boundary")
    if not isinstance(boundaries, list) or not boundaries:
        findings.append("claim_boundary must be non-empty array")
    else:
        missing_boundaries = REQUIRED_CLAIM_BOUNDARIES - set(boundaries)
        for item in sorted(missing_boundaries):
            findings.append(f"required claim boundary missing: {item}")

    if findings:
        return fail(findings)

    print(
        "AX_PUBLIC_ARTIFACT_MANIFEST_PASS "
        f"manifest={manifest['manifest_version']} closed_gate=DEV-GATE-04 "
        "active_gate=DEV-GATE-05 sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
