#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 repository consistency."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
STATES = {"CURRENT", "COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}
EXPECTED_RUNTIMES = ["3.10", "3.11", "3.12", "3.13"]

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
    if manifest.get("manifest_version") != "1.13":
        findings.append("manifest_version must be 1.13")
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
    evidence_ids: set[Any] = set()
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            findings.append(f"validation_evidence[{index}] invalid")
            continue
        evidence_ids.add(item.get("id"))
        path = safe_path(item.get("path"), findings, f"validation_evidence[{index}]")
        if path is not None and not path.is_file():
            findings.append(f"validation evidence path missing: {item.get('path')}")
        if not isinstance(item.get("verified_head_commit"), str) or len(item.get("verified_head_commit", "")) != 40:
            findings.append(f"validation_evidence[{index}].verified_head_commit invalid")
    for evidence_id in ("AX-PUB-CI-001", "AX-PUB-CI-002", "AX-PUB-CI-003", "AX-PUB-CI-004"):
        if evidence_id not in evidence_ids:
            findings.append(f"required validation evidence missing: {evidence_id}")

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
        if developer_program.get("closed_gate") != "DEV-GATE-01 — Reproducible Developer Experience":
            findings.append("developer program latest closed gate mismatch")
        if developer_program.get("active_gate") != "DEV-GATE-02 — SDK Candidate":
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
        if sdk_candidate.get("gate") != "DEV-GATE-02":
            findings.append("SDK candidate gate mismatch")
        if sdk_candidate.get("state") != "CANDIDATE_NOT_ESTABLISHED":
            findings.append("SDK candidate must remain CANDIDATE_NOT_ESTABLISHED before direct CI evidence")
        if sdk_candidate.get("candidate_version") != "0.1.0-candidate":
            findings.append("SDK candidate version mismatch")
        if sdk_candidate.get("candidate_runtime_matrix") != EXPECTED_RUNTIMES:
            findings.append("SDK candidate runtime matrix mismatch")
        if sdk_candidate.get("verified_runtime_matrix") != []:
            findings.append("SDK candidate runtime matrix must remain unverified")
        if sdk_candidate.get("package_identity_status") != "NOT APPROVED":
            findings.append("SDK package identity must remain NOT APPROVED")
        if sdk_candidate.get("registry_status") != "NOT AUTHORIZED":
            findings.append("SDK registry must remain NOT AUTHORIZED")
        if sdk_candidate.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("SDK candidate publication disposition mismatch")

    if not isinstance(manifest.get("claim_boundary"), list) or not manifest.get("claim_boundary"):
        findings.append("claim_boundary must be non-empty array")

    if findings:
        return fail(findings)
    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
