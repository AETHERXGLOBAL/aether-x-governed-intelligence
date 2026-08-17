#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 public artifact integrity.

This is a repository-consistency check. It does not establish product adoption,
production compatibility, security approval, or release stability.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
ALLOWED_ARTIFACT_STATES = {"CURRENT", "COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}
ALLOWED_RELATIONSHIP_STATES = {"COMPATIBLE", "SUPERSEDED", "DEPRECATED", "WITHDRAWN"}


def fail(findings: list[str], message: str) -> None:
    findings.append(message)


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(findings, f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        fail(findings, f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return data


def safe_repo_path(raw_path: Any, findings: list[str], label: str) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        fail(findings, f"{label}: path must be a non-empty string")
        return None
    candidate = Path(raw_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(findings, f"{label}: path must remain inside the repository: {raw_path}")
        return None
    return ROOT / candidate


def check_markdown_metadata(path: Path, artifact_id: str, version: str, findings: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(findings, f"cannot read {path.relative_to(ROOT)}: {exc}")
        return
    if f"`{artifact_id}`" not in text:
        fail(findings, f"{path.relative_to(ROOT)} does not declare artifact id {artifact_id}")
    if f"`{version}`" not in text:
        fail(findings, f"{path.relative_to(ROOT)} does not declare version {version}")


def check_schema_metadata(path: Path, artifact_id: str, version: str, findings: list[str]) -> None:
    data = load_json(path, findings)
    if data is None:
        return
    schema_id = data.get("$id")
    if not isinstance(schema_id, str) or f":{artifact_id}:{version}" not in schema_id:
        fail(findings, f"{path.relative_to(ROOT)} $id does not encode {artifact_id}:{version}")
    properties = data.get("properties")
    if not isinstance(properties, dict):
        fail(findings, f"{path.relative_to(ROOT)} must define properties")
        return
    declared_id = properties.get("schema_id")
    declared_version = properties.get("schema_version")
    if not isinstance(declared_id, dict) or declared_id.get("const") != artifact_id:
        fail(findings, f"{path.relative_to(ROOT)} schema_id const does not match {artifact_id}")
    if not isinstance(declared_version, dict) or declared_version.get("const") != version:
        fail(findings, f"{path.relative_to(ROOT)} schema_version const does not match {version}")


def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None:
        for item in findings:
            print(f"AX_MANIFEST_FAIL: {item}")
        return 1

    if manifest.get("manifest_id") != "AX-PUB-MANIFEST-001":
        fail(findings, "manifest_id must be AX-PUB-MANIFEST-001")
    if manifest.get("manifest_version") != "1.0":
        fail(findings, "manifest_version must be 1.0 for the current manifest contract")
    if manifest.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence":
        fail(findings, "repository identity does not match the canonical public engineering repository")

    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict):
        fail(findings, "versioning_policy must be an object")
    else:
        if policy.get("id") != "AX-PUB-POL-001" or policy.get("version") != "1.0":
            fail(findings, "versioning_policy must identify AX-PUB-POL-001 v1.0")
        policy_path = safe_repo_path(policy.get("path"), findings, "versioning_policy")
        if policy_path is not None and not policy_path.is_file():
            fail(findings, f"versioning policy path does not exist: {policy.get('path')}")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail(findings, "artifacts must be a non-empty array")
        artifacts = []

    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    ids_seen: set[str] = set()

    for index, artifact in enumerate(artifacts):
        label = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            fail(findings, f"{label} must be an object")
            continue
        artifact_id = artifact.get("id")
        version = artifact.get("version")
        state = artifact.get("state")
        if not isinstance(artifact_id, str) or not artifact_id.startswith("AX-PUB-"):
            fail(findings, f"{label}.id must be an AX-PUB artifact identifier")
            continue
        if not isinstance(version, str) or VERSION_RE.fullmatch(version) is None:
            fail(findings, f"{label}.version must use MAJOR.MINOR format")
            continue
        pair = (artifact_id, version)
        if pair in by_pair:
            fail(findings, f"duplicate artifact/version pair: {artifact_id} {version}")
        by_pair[pair] = artifact
        if artifact_id in ids_seen:
            fail(findings, f"current manifest contains multiple versions for {artifact_id}; explicit multi-version handling is required")
        ids_seen.add(artifact_id)
        if state not in ALLOWED_ARTIFACT_STATES:
            fail(findings, f"{label}.state is unsupported: {state}")

        path = safe_repo_path(artifact.get("path"), findings, label)
        if path is None:
            continue
        if not path.is_file():
            fail(findings, f"artifact path does not exist: {artifact.get('path')}")
            continue

        if path.suffix == ".json" and path.name.endswith(".schema.json"):
            check_schema_metadata(path, artifact_id, version, findings)
        elif path.suffix == ".md":
            check_markdown_metadata(path, artifact_id, version, findings)

        entrypoint_raw = artifact.get("entrypoint")
        if entrypoint_raw is not None:
            entrypoint = safe_repo_path(entrypoint_raw, findings, f"{label}.entrypoint")
            if entrypoint is not None and not entrypoint.is_file():
                fail(findings, f"entrypoint does not exist: {entrypoint_raw}")

    required_pairs = {
        ("AX-PUB-ARCH-001", "1.0"),
        ("AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-SCHEMA-001", "1.0"),
        ("AX-PUB-SCHEMA-002", "1.0"),
        ("AX-PUB-REF-001", "1.0"),
        ("AX-PUB-REF-002", "1.0"),
        ("AX-PUB-POL-001", "1.0"),
    }
    missing_pairs = sorted(required_pairs - set(by_pair))
    for artifact_id, version in missing_pairs:
        fail(findings, f"required current artifact is missing: {artifact_id} {version}")

    relationships = manifest.get("relationships")
    if not isinstance(relationships, list):
        fail(findings, "relationships must be an array")
        relationships = []

    relationship_keys: set[tuple[str, str, str, str, str]] = set()
    for index, relationship in enumerate(relationships):
        label = f"relationships[{index}]"
        if not isinstance(relationship, dict):
            fail(findings, f"{label} must be an object")
            continue
        from_pair = (relationship.get("from_id"), relationship.get("from_version"))
        to_pair = (relationship.get("to_id"), relationship.get("to_version"))
        relation_type = relationship.get("relationship")
        relation_state = relationship.get("state")
        if from_pair not in by_pair:
            fail(findings, f"{label} references missing source artifact/version: {from_pair}")
        if to_pair not in by_pair:
            fail(findings, f"{label} references missing target artifact/version: {to_pair}")
        if not isinstance(relation_type, str) or not relation_type:
            fail(findings, f"{label}.relationship must be a non-empty string")
            continue
        if relation_state not in ALLOWED_RELATIONSHIP_STATES:
            fail(findings, f"{label}.state is unsupported: {relation_state}")
        key = (str(from_pair[0]), str(from_pair[1]), relation_type, str(to_pair[0]), str(to_pair[1]))
        if key in relationship_keys:
            fail(findings, f"duplicate compatibility relationship: {key}")
        relationship_keys.add(key)

    required_relationships = {
        ("AX-PUB-SCHEMA-001", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-REF-001", "1.0", "DEMONSTRATES_SELECTED_SEMANTICS_OF", "AX-PUB-SPEC-002", "1.0"),
        ("AX-PUB-REF-001", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-001", "1.0"),
        ("AX-PUB-SCHEMA-002", "1.0", "STRUCTURAL_PROFILE_OF", "AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-REF-002", "1.0", "DEMONSTRATES_SELECTED_SEMANTICS_OF", "AX-PUB-SPEC-003", "1.0"),
        ("AX-PUB-REF-002", "1.0", "USES_STRUCTURAL_CONTRACT", "AX-PUB-SCHEMA-002", "1.0"),
    }
    missing_relations = sorted(required_relationships - relationship_keys)
    for relationship in missing_relations:
        fail(findings, f"required compatibility relationship is missing: {relationship}")

    quickstart = ROOT / "docs" / "QUICKSTART.md"
    if not quickstart.is_file():
        fail(findings, "docs/QUICKSTART.md is missing")
    else:
        quickstart_text = quickstart.read_text(encoding="utf-8")
        for required_reference in ("AX-PUB-MANIFEST-001.json", "COMPATIBILITY_AND_VERSIONING.md"):
            if required_reference not in quickstart_text:
                fail(findings, f"quickstart does not reference {required_reference}")

    claim_boundary = manifest.get("claim_boundary")
    if not isinstance(claim_boundary, list) or not claim_boundary:
        fail(findings, "claim_boundary must be a non-empty array")

    if findings:
        for item in findings:
            print(f"AX_MANIFEST_FAIL: {item}")
        return 1

    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
