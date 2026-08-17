#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 public artifact integrity.

Repository-consistency only. This does not establish product adoption,
production compatibility, security approval, or release stability.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
ARTIFACT_STATES = {"CURRENT", "COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}
RELATION_STATES = {"COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}


def safe_path(raw: Any, findings: list[str], label: str) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        findings.append(f"{label}: path must be a non-empty string")
        return None
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        findings.append(f"{label}: path escapes repository: {raw}")
        return None
    return ROOT / candidate


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return data


def check_artifact_file(path: Path, artifact_id: str, version: str, findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"artifact path does not exist: {path.relative_to(ROOT)}")
        return
    if path.name.endswith(".schema.json"):
        data = load_json(path, findings)
        if data is None:
            return
        if f":{artifact_id}:{version}" not in str(data.get("$id", "")):
            findings.append(f"{path.relative_to(ROOT)} $id does not encode {artifact_id}:{version}")
        props = data.get("properties")
        if not isinstance(props, dict):
            findings.append(f"{path.relative_to(ROOT)} must define properties")
            return
        if not isinstance(props.get("schema_id"), dict) or props["schema_id"].get("const") != artifact_id:
            findings.append(f"{path.relative_to(ROOT)} schema_id const mismatch")
        if not isinstance(props.get("schema_version"), dict) or props["schema_version"].get("const") != version:
            findings.append(f"{path.relative_to(ROOT)} schema_version const mismatch")
    elif path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if artifact_id not in text:
            findings.append(f"{path.relative_to(ROOT)} does not declare {artifact_id}")
        if f"`{version}`" not in text:
            findings.append(f"{path.relative_to(ROOT)} does not declare version {version}")


def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None:
        for item in findings:
            print(f"AX_MANIFEST_FAIL: {item}")
        return 1

    if manifest.get("manifest_id") != "AX-PUB-MANIFEST-001":
        findings.append("manifest_id must be AX-PUB-MANIFEST-001")
    if manifest.get("manifest_version") != "1.1":
        findings.append("manifest_version must be 1.1 for the current manifest contract")
    if manifest.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence":
        findings.append("repository identity mismatch")

    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict) or policy.get("id") != "AX-PUB-POL-001" or policy.get("version") != "1.1":
        findings.append("versioning_policy must identify AX-PUB-POL-001 v1.1")
    else:
        policy_path = safe_path(policy.get("path"), findings, "versioning_policy")
        if policy_path is not None and not policy_path.is_file():
            findings.append("versioning policy path does not exist")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        findings.append("artifacts must be a non-empty array")
        artifacts = []

    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    ids_seen: set[str] = set()
    for index, artifact in enumerate(artifacts):
        label = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            findings.append(f"{label} must be an object")
            continue
        artifact_id = artifact.get("id")
        version = artifact.get("version")
        if not isinstance(artifact_id, str) or not artifact_id.startswith("AX-PUB-"):
            findings.append(f"{label}.id is invalid")
            continue
        if not isinstance(version, str) or VERSION_RE.fullmatch(version) is None:
            findings.append(f"{label}.version must use MAJOR.MINOR")
            continue
        pair = (artifact_id, version)
        if pair in by_pair or artifact_id in ids_seen:
            findings.append(f"duplicate current artifact identity: {artifact_id} {version}")
        by_pair[pair] = artifact
        ids_seen.add(artifact_id)
        if artifact.get("state") not in ARTIFACT_STATES:
            findings.append(f"{label}.state is unsupported")
        path = safe_path(artifact.get("path"), findings, label)
        if path is not None:
            check_artifact_file(path, artifact_id, version, findings)
        if artifact.get("entrypoint") is not None:
            entrypoint = safe_path(artifact.get("entrypoint"), findings, f"{label}.entrypoint")
            if entrypoint is not None and not entrypoint.is_file():
                findings.append(f"entrypoint does not exist: {artifact.get('entrypoint')}")

    required_pairs = {
        ("AX-PUB-ARCH-001", "1.0"),
        ("AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-SCHEMA-001", "1.0"),
        ("AX-PUB-SCHEMA-002", "1.0"),
        ("AX-PUB-REF-001", "1.0"),
        ("AX-PUB-REF-002", "1.0"),
        ("AX-PUB-TEST-001", "1.0"),
        ("AX-PUB-POL-001", "1.1"),
    }
    for pair in sorted(required_pairs - set(by_pair)):
        findings.append(f"required current artifact is missing: {pair}")

    relationships = manifest.get("relationships")
    if not isinstance(relationships, list):
        findings.append("relationships must be an array")
        relationships = []
    relation_keys: set[tuple[str, str, str, str, str]] = set()
    for index, relation in enumerate(relationships):
        if not isinstance(relation, dict):
            findings.append(f"relationships[{index}] must be an object")
            continue
        from_pair = (relation.get("from_id"), relation.get("from_version"))
        to_pair = (relation.get("to_id"), relation.get("to_version"))
        kind = relation.get("relationship")
        if from_pair not in by_pair:
            findings.append(f"relationship source missing: {from_pair}")
        if to_pair not in by_pair:
            findings.append(f"relationship target missing: {to_pair}")
        if not isinstance(kind, str) or not kind:
            findings.append(f"relationships[{index}] has invalid relationship type")
            continue
        if relation.get("state") not in RELATION_STATES:
            findings.append(f"relationships[{index}] has unsupported state")
        relation_keys.add((str(from_pair[0]), str(from_pair[1]), kind, str(to_pair[0]), str(to_pair[1])))

    required_relations = {
        ("AX-PUB-SCHEMA-001", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-REF-001", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-001", "1.0"),
        ("AX-PUB-SCHEMA-002", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-REF-002", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-002", "1.0"),
        ("AX-PUB-TEST-001", "1.0", "EXERCISES_PUBLIC_BEHAVIOR_OF", "AX-PUB-REF-001", "1.0"),
        ("AX-PUB-TEST-001", "1.0", "EXERCISES_PUBLIC_BEHAVIOR_OF", "AX-PUB-REF-002", "1.0"),
    }
    for relation in sorted(required_relations - relation_keys):
        findings.append(f"required compatibility relationship is missing: {relation}")

    quickstart = ROOT / "docs" / "QUICKSTART.md"
    if not quickstart.is_file():
        findings.append("docs/QUICKSTART.md is missing")
    else:
        text = quickstart.read_text(encoding="utf-8")
        for required in ("AX-PUB-MANIFEST-001.json", "COMPATIBILITY_AND_VERSIONING.md", "AX-PUB-SNAP-001.json"):
            if required not in text:
                findings.append(f"quickstart does not reference {required}")

    if not isinstance(manifest.get("claim_boundary"), list) or not manifest.get("claim_boundary"):
        findings.append("claim_boundary must be a non-empty array")

    if findings:
        for item in findings:
            print(f"AX_MANIFEST_FAIL: {item}")
        return 1
    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
