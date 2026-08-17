#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 repository consistency only."""
from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
STATES = {"CURRENT","COMPATIBLE","SUPERSEDED","DEPRECATED","WITHDRAWN"}

REQUIRED_PAIRS = {
    ("AX-PUB-ARCH-001","1.0"),("AX-PUB-SPEC-002","1.0"),("AX-PUB-SPEC-003","1.0"),("AX-PUB-SPEC-004","1.0"),
    ("AX-PUB-SCHEMA-001","1.0"),("AX-PUB-SCHEMA-002","1.0"),("AX-PUB-SCHEMA-003","1.0"),
    ("AX-PUB-REF-001","1.0"),("AX-PUB-REF-002","1.0"),("AX-PUB-REF-003","1.0"),
    ("AX-PUB-TEST-001","1.0"),("AX-PUB-TEST-002","1.0"),("AX-PUB-POL-001","1.3"),
}
REQUIRED_RELATIONS = {
    ("AX-PUB-SCHEMA-001","1.0","STRUCTURAL_PROFILE_OF","AX-PUB-SPEC-002","1.0"),
    ("AX-PUB-REF-001","1.0","USES_STRUCTURAL_CONTRACT","AX-PUB-SCHEMA-001","1.0"),
    ("AX-PUB-SCHEMA-002","1.0","STRUCTURAL_PROFILE_OF","AX-PUB-SPEC-003","1.0"),
    ("AX-PUB-REF-002","1.0","USES_STRUCTURAL_CONTRACT","AX-PUB-SCHEMA-002","1.0"),
    ("AX-PUB-SPEC-004","1.0","ALIGNS_WITH_ARCHITECTURE","AX-PUB-ARCH-001","1.0"),
    ("AX-PUB-SPEC-004","1.0","SPECIALIZES_AUTHORITY_BOUNDARY_OF","AX-PUB-SPEC-002","1.0"),
    ("AX-PUB-SCHEMA-003","1.0","STRUCTURAL_PROFILE_OF","AX-PUB-SPEC-004","1.0"),
    ("AX-PUB-REF-003","1.0","USES_STRUCTURAL_CONTRACT","AX-PUB-SCHEMA-003","1.0"),
    ("AX-PUB-TEST-001","1.0","EXERCISES_PUBLIC_BEHAVIOR_OF","AX-PUB-REF-001","1.0"),
    ("AX-PUB-TEST-001","1.0","EXERCISES_PUBLIC_BEHAVIOR_OF","AX-PUB-REF-002","1.0"),
    ("AX-PUB-TEST-002","1.0","EXERCISES_PUBLIC_BEHAVIOR_OF","AX-PUB-REF-003","1.0"),
}

def safe_path(raw: Any, findings: list[str], label: str) -> Path | None:
    if not isinstance(raw, str) or not raw.strip(): findings.append(f"{label}: invalid path"); return None
    p = Path(raw)
    if p.is_absolute() or ".." in p.parts: findings.append(f"{label}: path escapes repository: {raw}"); return None
    return ROOT / p

def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}"); return None
    if not isinstance(data, dict): findings.append(f"{path.relative_to(ROOT)} must contain an object"); return None
    return data

def check_artifact(path: Path, artifact_id: str, version: str, findings: list[str]) -> None:
    if not path.is_file(): findings.append(f"artifact path missing: {path.relative_to(ROOT)}"); return
    if path.name.endswith(".schema.json"):
        data = load_json(path, findings)
        if data is None: return
        if f":{artifact_id}:{version}" not in str(data.get("$id", "")): findings.append(f"{path.relative_to(ROOT)} $id mismatch")
        props = data.get("properties", {})
        if props.get("schema_id", {}).get("const") != artifact_id: findings.append(f"{path.relative_to(ROOT)} schema_id mismatch")
        if props.get("schema_version", {}).get("const") != version: findings.append(f"{path.relative_to(ROOT)} schema_version mismatch")
    elif path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if artifact_id not in text: findings.append(f"{path.relative_to(ROOT)} does not declare {artifact_id}")
        if f"`{version}`" not in text: findings.append(f"{path.relative_to(ROOT)} does not declare version {version}")

def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None: return fail(findings)
    if manifest.get("manifest_id") != "AX-PUB-MANIFEST-001": findings.append("manifest_id mismatch")
    if manifest.get("manifest_version") != "1.3": findings.append("manifest_version must be 1.3")
    if manifest.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence": findings.append("repository identity mismatch")
    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict) or policy.get("id") != "AX-PUB-POL-001" or policy.get("version") != "1.3": findings.append("versioning policy must be AX-PUB-POL-001 v1.3")
    else:
        p = safe_path(policy.get("path"), findings, "versioning_policy")
        if p is not None and not p.is_file(): findings.append("versioning policy path missing")

    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
    if not artifacts: findings.append("artifacts must be a non-empty array")
    by_pair: dict[tuple[str,str],dict[str,Any]] = {}
    ids: set[str] = set()
    for i, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict): findings.append(f"artifacts[{i}] must be object"); continue
        aid, ver = artifact.get("id"), artifact.get("version")
        if not isinstance(aid, str) or not aid.startswith("AX-PUB-"): findings.append(f"artifacts[{i}].id invalid"); continue
        if not isinstance(ver, str) or VERSION_RE.fullmatch(ver) is None: findings.append(f"artifacts[{i}].version invalid"); continue
        if aid in ids: findings.append(f"duplicate current artifact id: {aid}")
        ids.add(aid); by_pair[(aid,ver)] = artifact
        if artifact.get("state") not in STATES: findings.append(f"artifacts[{i}].state invalid")
        path = safe_path(artifact.get("path"), findings, f"artifacts[{i}]")
        if path is not None: check_artifact(path, aid, ver, findings)
        if artifact.get("entrypoint") is not None:
            ep = safe_path(artifact.get("entrypoint"), findings, f"artifacts[{i}].entrypoint")
            if ep is not None and not ep.is_file(): findings.append(f"entrypoint missing: {artifact.get('entrypoint')}")
    for pair in sorted(REQUIRED_PAIRS - set(by_pair)): findings.append(f"required current artifact missing: {pair}")

    relationships = manifest.get("relationships") if isinstance(manifest.get("relationships"), list) else []
    rels: set[tuple[str,str,str,str,str]] = set()
    for i, rel in enumerate(relationships):
        if not isinstance(rel, dict): findings.append(f"relationships[{i}] must be object"); continue
        fp, tp = (rel.get("from_id"), rel.get("from_version")), (rel.get("to_id"), rel.get("to_version")); kind = rel.get("relationship")
        if fp not in by_pair: findings.append(f"relationship source missing: {fp}")
        if tp not in by_pair: findings.append(f"relationship target missing: {tp}")
        if rel.get("state") not in STATES - {"CURRENT"}: findings.append(f"relationships[{i}].state invalid")
        key = (str(fp[0]),str(fp[1]),str(kind),str(tp[0]),str(tp[1]))
        if key in rels: findings.append(f"duplicate relationship: {key}")
        rels.add(key)
    for rel in sorted(REQUIRED_RELATIONS - rels): findings.append(f"required compatibility relationship missing: {rel}")

    quickstart = ROOT / "docs" / "QUICKSTART.md"
    if not quickstart.is_file(): findings.append("docs/QUICKSTART.md missing")
    else:
        text = quickstart.read_text(encoding="utf-8")
        for marker in ("AX-PUB-MANIFEST-001.json","COMPATIBILITY_AND_VERSIONING.md","AX-PUB-SNAP-001.json","AX-PUB-SCHEMA-003","AX-PUB-REF-003","AX-PUB-TEST-002"):
            if marker not in text: findings.append(f"quickstart missing reference: {marker}")
    if not isinstance(manifest.get("claim_boundary"), list) or not manifest.get("claim_boundary"): findings.append("claim_boundary must be non-empty array")
    if findings: return fail(findings)
    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS"); return 0

def fail(findings: list[str]) -> int:
    for item in findings: print(f"AX_MANIFEST_FAIL: {item}")
    return 1

if __name__ == "__main__": raise SystemExit(main())
