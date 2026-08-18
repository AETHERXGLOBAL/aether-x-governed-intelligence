#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 repository consistency."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
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


def safe_path(raw: Any, findings: list[str], label: str) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        findings.append(f"{label}: invalid path")
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        findings.append(f"{label}: path escapes repository: {raw}")
        return None
    return ROOT / path


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain an object")
        return None
    return data


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


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    if not isinstance(raw, str) or VERSION_RE.fullmatch(raw) is None:
        return False
    parts = raw.split("-", 1)[0].split(".")
    try:
        current = (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return False
    return current >= (major, minor)


def fail(findings: list[str]) -> int:
    for item in findings:
        print(f"AX_MANIFEST_FAIL: {item}")
    return 1


def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None:
        return fail(findings)

    if manifest.get("manifest_id") != "AX-PUB-MANIFEST-001":
        findings.append("manifest_id mismatch")
    if not version_at_least(manifest.get("manifest_version"), 1, 17):
        findings.append("manifest_version must be >= 1.17")
    if manifest.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence":
        findings.append("repository identity mismatch")

    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict) or policy.get("id") != "AX-PUB-POL-001" or policy.get("version") != "1.6":
        findings.append("versioning policy must be AX-PUB-POL-001 v1.6")
    else:
        path = safe_path(policy.get("path"), findings, "versioning_policy")
        if path is not None and not path.is_file():
            findings.append("versioning policy path missing")

    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
    if not artifacts:
        findings.append("artifacts must be a non-empty array")
    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    ids: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            findings.append(f"artifacts[{index}] must be object")
            continue
        artifact_id, version = artifact.get("id"), artifact.get("version")
        if not isinstance(artifact_id, str) or not artifact_id.startswith("AX-PUB-"):
            findings.append(f"artifacts[{index}].id invalid")
            continue
        if not isinstance(version, str) or VERSION_RE.fullmatch(version) is None:
            findings.append(f"artifacts[{index}].version invalid")
            continue
        if artifact_id in ids:
            findings.append(f"duplicate current artifact id: {artifact_id}")
        ids.add(artifact_id)
        by_pair[(artifact_id, version)] = artifact
        if artifact.get("state") not in STATES:
            findings.append(f"artifacts[{index}].state invalid")
        path = safe_path(artifact.get("path"), findings, f"artifacts[{index}]")
        if path is not None:
            check_artifact(path, artifact_id, version, findings)
        for field in ("entrypoint", "machine_readable_companion"):
            if artifact.get(field) is not None:
                target = safe_path(artifact.get(field), findings, f"artifacts[{index}].{field}")
                if target is not None and not target.is_file():
                    findings.append(f"{field} missing: {artifact.get(field)}")

    for pair in sorted(REQUIRED_PAIRS - set(by_pair)):
        findings.append(f"required current artifact missing: {pair}")

    relations: set[tuple[str, str, str, str, str]] = set()
    raw_relations = manifest.get("relationships") if isinstance(manifest.get("relationships"), list) else []
    for index, relation in enumerate(raw_relations):
        if not isinstance(relation, dict):
            findings.append(f"relationships[{index}] must be object")
            continue
        source = (relation.get("from_id"), relation.get("from_version"))
        target = (relation.get("to_id"), relation.get("to_version"))
        kind = relation.get("relationship")
        if source not in by_pair:
            findings.append(f"relationship source missing: {source}")
        if target not in by_pair:
            findings.append(f"relationship target missing: {target}")
        if relation.get("state") not in STATES - {"CURRENT"}:
            findings.append(f"relationships[{index}].state invalid")
        relations.add((str(source[0]), str(source[1]), str(kind), str(target[0]), str(target[1])))
    for relation in sorted(REQUIRED_RELATIONS - relations):
        findings.append(f"required compatibility relationship missing: {relation}")

    evidence = manifest.get("validation_evidence")
    if not isinstance(evidence, list):
        findings.append("validation_evidence must be an array")
        evidence = []
    evidence_by_id: dict[Any, dict[str, Any]] = {}
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            findings.append(f"validation_evidence[{index}] invalid")
            continue
        evidence_by_id[item.get("id")] = item
        path = safe_path(item.get("path"), findings, f"validation_evidence[{index}]")
        if path is not None and not path.is_file():
            findings.append(f"validation evidence path missing: {item.get('path')}")
        if not isinstance(item.get("verified_head_commit"), str) or len(item.get("verified_head_commit", "")) != 40:
            findings.append(f"validation_evidence[{index}].verified_head_commit invalid")
    for evidence_id in ("AX-PUB-CI-001", "AX-PUB-CI-002", "AX-PUB-CI-003", "AX-PUB-CI-004", "AX-PUB-CI-005", "AX-PUB-CI-006"):
        if evidence_id not in evidence_by_id:
            findings.append(f"required validation evidence missing: {evidence_id}")

    ci006 = evidence_by_id.get("AX-PUB-CI-006")
    if isinstance(ci006, dict):
        if ci006.get("version") != "1.1":
            findings.append("AX-PUB-CI-006 evidence version must be 1.1")
        if ci006.get("workflow_run_id") != 32150126557 or ci006.get("workflow_run_number") != 7:
            findings.append("AX-PUB-CI-006 supply-chain workflow identity mismatch")
        if ci006.get("governance_workflow_run_id") != 32150126711 or ci006.get("governance_workflow_run_number") != 135:
            findings.append("AX-PUB-CI-006 governance workflow identity mismatch")
        if ci006.get("verified_build_digest") != EXPECTED_GATE_03_DIGEST:
            findings.append("AX-PUB-CI-006 verified build digest mismatch")
        if ci006.get("source_date_epoch") != EXPECTED_GATE_03_EPOCH:
            findings.append("AX-PUB-CI-006 source epoch mismatch")
        if ci006.get("conclusion") != "SUCCESS":
            findings.append("AX-PUB-CI-006 conclusion must be SUCCESS")

    snapshot = manifest.get("current_snapshot")
    if not isinstance(snapshot, dict) or snapshot.get("id") != "AX-PUB-SNAP-002" or snapshot.get("version") != "1.0":
        findings.append("current_snapshot must identify AX-PUB-SNAP-002 v1.0")
    elif snapshot.get("anchor_commit") != "6dfdec04a4d8375bc2da0bb6a3830ff07eeb1711":
        findings.append("current snapshot anchor mismatch")

    release = manifest.get("current_release")
    if not isinstance(release, dict) or release.get("id") != "AX-PUB-REL-001" or release.get("version") != "1.0":
        findings.append("current_release must identify AX-PUB-REL-001 v1.0")
    else:
        if release.get("tag") != "public-engineering-vnext-1.0":
            findings.append("current release tag mismatch")
        if release.get("tag_target_commit") != "4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6":
            findings.append("current release tag target mismatch")

    gate = manifest.get("current_readiness_gate")
    if not isinstance(gate, dict) or gate.get("id") != "AX-PUB-GATE-001" or gate.get("version") != "1.0":
        findings.append("current_readiness_gate must identify AX-PUB-GATE-001 v1.0")
    else:
        path = safe_path(gate.get("path"), findings, "current_readiness_gate")
        if path is not None and not path.is_file():
            findings.append("current readiness gate path missing")
        if gate.get("disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("SDK readiness disposition mismatch")

    developer_program = manifest.get("current_developer_program")
    if not isinstance(developer_program, dict) or developer_program.get("id") != "AX-PUB-DEV-001" or developer_program.get("version") != "1.0":
        findings.append("current_developer_program must identify AX-PUB-DEV-001 v1.0")
    else:
        path = safe_path(developer_program.get("path"), findings, "current_developer_program")
        if path is not None and not path.is_file():
            findings.append("current developer program path missing")
        if developer_program.get("state") != "UNDER DEVELOPMENT":
            findings.append("developer program state mismatch")
        if developer_program.get("closed_gate") != "DEV-GATE-03 — Supply-Chain & Release Candidate":
            findings.append("developer program latest closed gate mismatch")
        if developer_program.get("active_gate") != "DEV-GATE-04 — External Evaluation Readiness":
            findings.append("developer program active gate mismatch")
        if developer_program.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("developer program SDK disposition mismatch")

    baseline = manifest.get("current_developer_contract_baseline")
    if not isinstance(baseline, dict) or baseline.get("id") != "AX-PUB-DEV-002" or baseline.get("version") != "1.0":
        findings.append("current_developer_contract_baseline must identify AX-PUB-DEV-002 v1.0")
    else:
        if baseline.get("gate") != "DEV-GATE-00" or baseline.get("state") != "CLOSED":
            findings.append("developer contract baseline state mismatch")
        if baseline.get("closure_evidence") != "AX-PUB-CI-003":
            findings.append("developer contract baseline closure evidence mismatch")
        for field in ("path", "machine_readable_companion"):
            target = safe_path(baseline.get(field), findings, f"current_developer_contract_baseline.{field}")
            if target is not None and not target.is_file():
                findings.append(f"current developer contract baseline {field} missing")

    developer_experience = manifest.get("current_developer_experience")
    if not isinstance(developer_experience, dict) or developer_experience.get("id") != "AX-PUB-DEV-003" or developer_experience.get("version") != "1.0":
        findings.append("current_developer_experience must identify AX-PUB-DEV-003 v1.0")
    else:
        for field in ("path", "machine_readable_companion", "runner", "state_checker"):
            target = safe_path(developer_experience.get(field), findings, f"current_developer_experience.{field}")
            if target is not None and not target.is_file():
                findings.append(f"current developer experience {field} missing")
        if developer_experience.get("gate") != "DEV-GATE-01" or developer_experience.get("state") != "CLOSED":
            findings.append("developer experience state mismatch")
        if developer_experience.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("developer experience verified runtime matrix mismatch")
        if developer_experience.get("closure_evidence") != "AX-PUB-CI-004":
            findings.append("developer experience closure evidence mismatch")

    sdk_candidate = manifest.get("current_sdk_candidate")
    if not isinstance(sdk_candidate, dict) or sdk_candidate.get("id") != "AX-PUB-DEV-004" or sdk_candidate.get("version") != "1.0":
        findings.append("current_sdk_candidate must identify AX-PUB-DEV-004 v1.0")
    else:
        for field in ("path", "machine_readable_companion", "candidate_module"):
            target = safe_path(sdk_candidate.get(field), findings, f"current_sdk_candidate.{field}")
            if target is not None and not target.is_file():
                findings.append(f"current SDK candidate {field} missing")
        if sdk_candidate.get("gate") != "DEV-GATE-02" or sdk_candidate.get("state") != "CLOSED":
            findings.append("SDK candidate closed state mismatch")
        if sdk_candidate.get("candidate_version") != "0.1.0-candidate":
            findings.append("SDK candidate version mismatch")
        if sdk_candidate.get("candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("SDK candidate runtime matrix mismatch")
        if sdk_candidate.get("verified_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("SDK candidate verified runtime matrix mismatch")
        if sdk_candidate.get("closure_evidence") != "AX-PUB-CI-005":
            findings.append("SDK candidate closure evidence mismatch")
        if sdk_candidate.get("package_identity_status") != "NOT APPROVED":
            findings.append("SDK package identity must remain NOT APPROVED")
        if sdk_candidate.get("registry_status") != "NOT AUTHORIZED":
            findings.append("SDK registry must remain NOT AUTHORIZED")
        if sdk_candidate.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("SDK candidate publication disposition mismatch")

    supply_chain = manifest.get("current_supply_chain_release_candidate")
    if not isinstance(supply_chain, dict) or supply_chain.get("id") != "AX-PUB-DEV-005" or supply_chain.get("version") != "1.0":
        findings.append("current_supply_chain_release_candidate must identify AX-PUB-DEV-005 v1.0")
    else:
        for field in ("path", "machine_readable_companion"):
            target = safe_path(supply_chain.get(field), findings, f"current_supply_chain_release_candidate.{field}")
            if target is not None and not target.is_file():
                findings.append(f"current supply-chain candidate {field} missing")
        if supply_chain.get("release_candidate_id") != "AX-PUB-RC-001" or supply_chain.get("release_candidate_version") != "0.1.0-rc1":
            findings.append("release-candidate descriptor identity mismatch")
        if supply_chain.get("gate") != "DEV-GATE-03" or supply_chain.get("state") != "CLOSED":
            findings.append("DEV-GATE-03 manifest state must be CLOSED")
        for field in ("deterministic_build", "build_provenance_attestation", "sbom_attestation", "extracted_bundle_validation"):
            if supply_chain.get(field) != "VERIFIED":
                findings.append(f"closed Gate-03 requires {field}=VERIFIED")
        if supply_chain.get("closure_evidence") != "AX-PUB-CI-006":
            findings.append("Gate-03 closure evidence mismatch")
        if supply_chain.get("verified_build_digest") != EXPECTED_GATE_03_DIGEST:
            findings.append("Gate-03 verified build digest mismatch")
        if supply_chain.get("verified_source_date_epoch") != EXPECTED_GATE_03_EPOCH:
            findings.append("Gate-03 verified source epoch mismatch")
        if supply_chain.get("artifact_upload_scope") != "CI_ONLY":
            findings.append("Gate-03 artifact upload scope must remain CI_ONLY")
        if supply_chain.get("package_identity_status") != "NOT APPROVED":
            findings.append("Gate-03 package identity must remain NOT APPROVED")
        if supply_chain.get("registry_status") != "NOT AUTHORIZED":
            findings.append("Gate-03 registry must remain NOT AUTHORIZED")
        if supply_chain.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("Gate-03 SDK publication disposition mismatch")

    external_readiness = manifest.get("current_external_evaluation_readiness")
    if not isinstance(external_readiness, dict) or external_readiness.get("id") != "AX-PUB-DEV-006" or external_readiness.get("version") != "1.0":
        findings.append("current_external_evaluation_readiness must identify AX-PUB-DEV-006 v1.0")
    else:
        for field in ("path", "machine_readable_companion", "runner", "report_checker", "state_checker"):
            target = safe_path(external_readiness.get(field), findings, f"current_external_evaluation_readiness.{field}")
            if target is not None and not target.is_file():
                findings.append(f"current external evaluation readiness {field} missing")
        if external_readiness.get("gate") != "DEV-GATE-04":
            findings.append("external evaluation readiness gate mismatch")
        if external_readiness.get("declared_candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("external evaluation readiness runtime matrix mismatch")
        if external_readiness.get("external_evaluation_occurred") is not False:
            findings.append("external evaluation occurred must remain false unless separately evidenced")
        if external_readiness.get("external_adoption_established") is not False:
            findings.append("external adoption must remain false unless separately evidenced")
        if external_readiness.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("Gate-04 SDK publication disposition mismatch")
        ext_state = external_readiness.get("state")
        if ext_state == "CANDIDATE":
            if external_readiness.get("external_evaluation_readiness") != "NOT_YET_ESTABLISHED":
                findings.append("Gate-04 candidate readiness must be NOT_YET_ESTABLISHED")
        elif ext_state == "CLOSED":
            if external_readiness.get("external_evaluation_readiness") != "ESTABLISHED":
                findings.append("Gate-04 closed readiness must be ESTABLISHED")
            if external_readiness.get("closure_evidence") != "AX-PUB-CI-007":
                findings.append("Gate-04 closed state requires AX-PUB-CI-007")
            if "AX-PUB-CI-007" not in evidence_by_id:
                findings.append("Gate-04 closed state requires AX-PUB-CI-007 validation evidence")
        else:
            findings.append("Gate-04 state must be CANDIDATE or CLOSED")

    dev005 = load_json(ROOT / "artifacts" / "AX-PUB-DEV-005.json", findings)
    if dev005 is not None:
        if dev005.get("state") != "DEV-GATE-03_CLOSED" or dev005.get("release_candidate_established") is not True:
            findings.append("AX-PUB-DEV-005 machine-readable state must be closed/established")
        if dev005.get("verified_build_digest") != EXPECTED_GATE_03_DIGEST:
            findings.append("AX-PUB-DEV-005 digest mismatch")
        if dev005.get("verified_source_date_epoch") != EXPECTED_GATE_03_EPOCH:
            findings.append("AX-PUB-DEV-005 source epoch mismatch")
        closure = dev005.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
            findings.append("AX-PUB-DEV-005 closure evidence must be AX-PUB-CI-006 v1.1")
        if dev005.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("AX-PUB-DEV-005 publication boundary mismatch")

    dev006 = load_json(ROOT / "artifacts" / "AX-PUB-DEV-006.json", findings)
    if dev006 is not None:
        if dev006.get("artifact_id") != "AX-PUB-DEV-006" or dev006.get("version") != "1.0":
            findings.append("AX-PUB-DEV-006 descriptor identity mismatch")
        if dev006.get("gate") != "DEV-GATE-04":
            findings.append("AX-PUB-DEV-006 gate mismatch")
        if dev006.get("sdk_publication") != "NOT_AUTHORIZED":
            findings.append("AX-PUB-DEV-006 SDK publication boundary mismatch")
        if dev006.get("external_evaluation_occurred") is not False:
            findings.append("AX-PUB-DEV-006 external evaluation claim boundary mismatch")
        if dev006.get("external_adoption_established") is not False:
            findings.append("AX-PUB-DEV-006 external adoption boundary mismatch")
        if dev006.get("supported_sdk_established") is not False:
            findings.append("AX-PUB-DEV-006 supported SDK boundary mismatch")
        if dev006.get("declared_candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("AX-PUB-DEV-006 runtime matrix mismatch")
        if dev006.get("state") == "CANDIDATE":
            if dev006.get("external_evaluation_readiness") != "NOT_YET_ESTABLISHED":
                findings.append("AX-PUB-DEV-006 candidate readiness mismatch")
        elif dev006.get("state") == "CLOSED":
            if dev006.get("external_evaluation_readiness") != "ESTABLISHED":
                findings.append("AX-PUB-DEV-006 closed readiness mismatch")
        else:
            findings.append("AX-PUB-DEV-006 state must be CANDIDATE or CLOSED")

    rc = load_json(ROOT / "release-candidate" / "AX-PUB-RC-001.json", findings)
    if rc is not None:
        if rc.get("artifact_id") != "AX-PUB-RC-001" or rc.get("version") != "0.1.0-rc1":
            findings.append("AX-PUB-RC-001 descriptor identity mismatch")
        if rc.get("state") != "DEV-GATE-03_VALIDATED" or rc.get("release_candidate_established") is not True:
            findings.append("AX-PUB-RC-001 must be validated/established after Gate-03 closure")
        if rc.get("verified_build_digest") != EXPECTED_GATE_03_DIGEST:
            findings.append("AX-PUB-RC-001 verified digest mismatch")
        if rc.get("verified_source_date_epoch") != EXPECTED_GATE_03_EPOCH:
            findings.append("AX-PUB-RC-001 verified source epoch mismatch")
        closure = rc.get("closure_evidence")
        if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
            findings.append("AX-PUB-RC-001 closure evidence must be AX-PUB-CI-006 v1.1")
        if rc.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("AX-PUB-RC-001 publication boundary mismatch")

    if not isinstance(manifest.get("claim_boundary"), list) or not manifest.get("claim_boundary"):
        findings.append("claim_boundary must be non-empty array")

    if findings:
        return fail(findings)
    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
