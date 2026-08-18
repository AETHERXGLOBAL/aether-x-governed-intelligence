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
    ("AX-PUB-TEST-001","1.0"),("AX-PUB-TEST-002","1.0"),("AX-PUB-POL-001","1.6"),
    ("AX-PUB-SNAP-002","1.0"),("AX-PUB-REL-001","1.0"),("AX-PUB-GATE-001","1.0"),
    ("AX-PUB-DEV-001","1.0"),("AX-PUB-DEV-002","1.0"),("AX-PUB-DEV-003","1.0"),
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
    ("AX-PUB-REL-001","1.0","PACKAGES_PUBLIC_STATE_WITH","AX-PUB-SNAP-002","1.0"),
    ("AX-PUB-DEV-001","1.0","GOVERNED_BY","AX-PUB-GATE-001","1.0"),
    ("AX-PUB-DEV-002","1.0","IMPLEMENTS_PROGRAM_GATE_OF","AX-PUB-DEV-001","1.0"),
    ("AX-PUB-DEV-002","1.0","GOVERNED_BY","AX-PUB-GATE-001","1.0"),
    ("AX-PUB-DEV-003","1.0","IMPLEMENTS_PROGRAM_GATE_OF","AX-PUB-DEV-001","1.0"),
    ("AX-PUB-DEV-003","1.0","BUILDS_ON","AX-PUB-DEV-002","1.0"),
    ("AX-PUB-DEV-003","1.0","GOVERNED_BY","AX-PUB-GATE-001","1.0"),
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

def check_artifact(path: Path, aid: str, ver: str, findings: list[str]) -> None:
    if not path.is_file(): findings.append(f"artifact path missing: {path.relative_to(ROOT)}"); return
    if path.name.endswith(".schema.json"):
        data = load_json(path, findings)
        if data is None: return
        if f":{aid}:{ver}" not in str(data.get("$id", "")): findings.append(f"{path.relative_to(ROOT)} $id mismatch")
        props = data.get("properties", {})
        if props.get("schema_id", {}).get("const") != aid: findings.append(f"{path.relative_to(ROOT)} schema_id mismatch")
        if props.get("schema_version", {}).get("const") != ver: findings.append(f"{path.relative_to(ROOT)} schema_version mismatch")
    elif path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        if aid not in text: findings.append(f"{path.relative_to(ROOT)} does not declare {aid}")
        if f"`{ver}`" not in text: findings.append(f"{path.relative_to(ROOT)} does not declare version {ver}")

def fail(findings: list[str]) -> int:
    for item in findings: print(f"AX_MANIFEST_FAIL: {item}")
    return 1

def main() -> int:
    findings: list[str] = []
    manifest = load_json(MANIFEST_PATH, findings)
    if manifest is None: return fail(findings)
    if manifest.get("manifest_id") != "AX-PUB-MANIFEST-001": findings.append("manifest_id mismatch")
    if manifest.get("manifest_version") != "1.11": findings.append("manifest_version must be 1.11")
    if manifest.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence": findings.append("repository identity mismatch")

    policy = manifest.get("versioning_policy")
    if not isinstance(policy, dict) or policy.get("id") != "AX-PUB-POL-001" or policy.get("version") != "1.6": findings.append("versioning policy must be AX-PUB-POL-001 v1.6")
    else:
        p = safe_path(policy.get("path"), findings, "versioning_policy")
        if p is not None and not p.is_file(): findings.append("versioning policy path missing")

    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
    if not artifacts: findings.append("artifacts must be a non-empty array")
    by_pair: dict[tuple[str,str],dict[str,Any]] = {}; ids: set[str] = set()
    for i, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict): findings.append(f"artifacts[{i}] must be object"); continue
        aid, ver = artifact.get("id"), artifact.get("version")
        if not isinstance(aid, str) or not aid.startswith("AX-PUB-"): findings.append(f"artifacts[{i}].id invalid"); continue
        if not isinstance(ver, str) or VERSION_RE.fullmatch(ver) is None: findings.append(f"artifacts[{i}].version invalid"); continue
        if aid in ids: findings.append(f"duplicate current artifact id: {aid}")
        ids.add(aid); by_pair[(aid,ver)] = artifact
        if artifact.get("state") not in STATES: findings.append(f"artifacts[{i}].state invalid")
        p = safe_path(artifact.get("path"), findings, f"artifacts[{i}]")
        if p is not None: check_artifact(p, aid, ver, findings)
        if artifact.get("entrypoint") is not None:
            ep = safe_path(artifact.get("entrypoint"), findings, f"artifacts[{i}].entrypoint")
            if ep is not None and not ep.is_file(): findings.append(f"entrypoint missing: {artifact.get('entrypoint')}")
        if artifact.get("machine_readable_companion") is not None:
            cp = safe_path(artifact.get("machine_readable_companion"), findings, f"artifacts[{i}].machine_readable_companion")
            if cp is not None and not cp.is_file(): findings.append(f"machine-readable companion missing: {artifact.get('machine_readable_companion')}")
    for pair in sorted(REQUIRED_PAIRS - set(by_pair)): findings.append(f"required current artifact missing: {pair}")

    rels: set[tuple[str,str,str,str,str]] = set()
    for i, rel in enumerate(manifest.get("relationships") if isinstance(manifest.get("relationships"), list) else []):
        if not isinstance(rel, dict): findings.append(f"relationships[{i}] must be object"); continue
        fp, tp = (rel.get("from_id"),rel.get("from_version")), (rel.get("to_id"),rel.get("to_version")); kind = rel.get("relationship")
        if fp not in by_pair: findings.append(f"relationship source missing: {fp}")
        if tp not in by_pair: findings.append(f"relationship target missing: {tp}")
        if rel.get("state") not in STATES - {"CURRENT"}: findings.append(f"relationships[{i}].state invalid")
        rels.add((str(fp[0]),str(fp[1]),str(kind),str(tp[0]),str(tp[1])))
    for rel in sorted(REQUIRED_RELATIONS - rels): findings.append(f"required compatibility relationship missing: {rel}")

    evidence = manifest.get("validation_evidence")
    if not isinstance(evidence, list): findings.append("validation_evidence must be an array"); evidence=[]
    evidence_ids=set()
    for i,item in enumerate(evidence):
        if not isinstance(item,dict): findings.append(f"validation_evidence[{i}] invalid"); continue
        evidence_ids.add(item.get("id"))
        ep=safe_path(item.get("path"),findings,f"validation_evidence[{i}]")
        if ep is not None and not ep.is_file(): findings.append(f"validation evidence path missing: {item.get('path')}")
        if not isinstance(item.get("verified_head_commit"),str) or len(item.get("verified_head_commit",""))!=40: findings.append(f"validation_evidence[{i}].verified_head_commit invalid")
    for eid in ("AX-PUB-CI-001","AX-PUB-CI-002","AX-PUB-CI-003"):
        if eid not in evidence_ids: findings.append(f"required validation evidence missing: {eid}")

    snapshot=manifest.get("current_snapshot")
    if not isinstance(snapshot,dict) or snapshot.get("id")!="AX-PUB-SNAP-002" or snapshot.get("version")!="1.0": findings.append("current_snapshot must identify AX-PUB-SNAP-002 v1.0")
    elif snapshot.get("anchor_commit")!="6dfdec04a4d8375bc2da0bb6a3830ff07eeb1711": findings.append("current snapshot anchor mismatch")

    release=manifest.get("current_release")
    if not isinstance(release,dict) or release.get("id")!="AX-PUB-REL-001" or release.get("version")!="1.0": findings.append("current_release must identify AX-PUB-REL-001 v1.0")
    else:
        if release.get("tag")!="public-engineering-vnext-1.0": findings.append("current release tag mismatch")
        if release.get("tag_target_commit")!="4f067c9fd3d3ac065ac50b10faf1abd1bdb91bb6": findings.append("current release tag target mismatch")

    gate=manifest.get("current_readiness_gate")
    if not isinstance(gate,dict) or gate.get("id")!="AX-PUB-GATE-001" or gate.get("version")!="1.0": findings.append("current_readiness_gate must identify AX-PUB-GATE-001 v1.0")
    else:
        gp=safe_path(gate.get("path"),findings,"current_readiness_gate")
        if gp is not None and not gp.is_file(): findings.append("current readiness gate path missing")
        if gate.get("disposition")!="SDK PUBLICATION NOT AUTHORIZED": findings.append("SDK readiness disposition mismatch")

    dev=manifest.get("current_developer_program")
    if not isinstance(dev,dict) or dev.get("id")!="AX-PUB-DEV-001" or dev.get("version")!="1.0": findings.append("current_developer_program must identify AX-PUB-DEV-001 v1.0")
    else:
        dp=safe_path(dev.get("path"),findings,"current_developer_program")
        if dp is not None and not dp.is_file(): findings.append("current developer program path missing")
        if dev.get("state")!="UNDER DEVELOPMENT": findings.append("developer program state mismatch")
        if dev.get("closed_gate")!="DEV-GATE-00 — Contract Baseline": findings.append("developer program closed gate mismatch")
        if dev.get("active_gate")!="DEV-GATE-01 — Reproducible Developer Experience": findings.append("developer program active gate mismatch")
        if dev.get("sdk_publication_disposition")!="SDK PUBLICATION NOT AUTHORIZED": findings.append("developer program SDK disposition mismatch")

    baseline=manifest.get("current_developer_contract_baseline")
    if not isinstance(baseline,dict) or baseline.get("id")!="AX-PUB-DEV-002" or baseline.get("version")!="1.0": findings.append("current_developer_contract_baseline must identify AX-PUB-DEV-002 v1.0")
    else:
        bp=safe_path(baseline.get("path"),findings,"current_developer_contract_baseline")
        if bp is not None and not bp.is_file(): findings.append("current developer contract baseline path missing")
        cp=safe_path(baseline.get("machine_readable_companion"),findings,"current_developer_contract_baseline companion")
        if cp is not None and not cp.is_file(): findings.append("current developer contract baseline companion missing")
        if baseline.get("gate")!="DEV-GATE-00": findings.append("developer contract baseline gate mismatch")
        if baseline.get("state")!="CLOSED": findings.append("developer contract baseline must be CLOSED")
        if baseline.get("closure_evidence")!="AX-PUB-CI-003": findings.append("developer contract baseline closure evidence mismatch")
        if baseline.get("sdk_publication_disposition")!="SDK PUBLICATION NOT AUTHORIZED": findings.append("developer contract baseline SDK disposition mismatch")

    devex=manifest.get("current_developer_experience")
    if not isinstance(devex,dict) or devex.get("id")!="AX-PUB-DEV-003" or devex.get("version")!="1.0": findings.append("current_developer_experience must identify AX-PUB-DEV-003 v1.0")
    else:
        xp=safe_path(devex.get("path"),findings,"current_developer_experience")
        if xp is not None and not xp.is_file(): findings.append("current developer experience path missing")
        cp=safe_path(devex.get("machine_readable_companion"),findings,"current_developer_experience companion")
        if cp is not None and not cp.is_file(): findings.append("current developer experience companion missing")
        rp=safe_path(devex.get("runner"),findings,"current_developer_experience runner")
        if rp is not None and not rp.is_file(): findings.append("current developer experience runner missing")
        if devex.get("gate")!="DEV-GATE-01": findings.append("developer experience gate mismatch")
        if devex.get("state")!="CANDIDATE_NOT_CLOSED": findings.append("developer experience candidate state mismatch")
        if devex.get("candidate_runtime_matrix") != ["3.10","3.11","3.12","3.13"]: findings.append("developer experience candidate runtime matrix mismatch")
        if devex.get("verified_runtime_matrix") != []: findings.append("developer experience verified runtime matrix must remain empty before CI evidence")
        if devex.get("sdk_publication_disposition")!="SDK PUBLICATION NOT AUTHORIZED": findings.append("developer experience SDK disposition mismatch")

    quickstart = ROOT / "docs" / "QUICKSTART.md"
    if not quickstart.is_file(): findings.append("docs/QUICKSTART.md missing")
    else:
        text = quickstart.read_text(encoding="utf-8")
        for marker in (
            "AX-PUB-MANIFEST-001 v1.11","COMPATIBILITY_AND_VERSIONING.md","AX-PUB-SNAP-001.json","AX-PUB-SNAP-002.json",
            "AX-PUB-SCHEMA-003","AX-PUB-REF-003","AX-PUB-TEST-002","AX-PUB-REL-001","public-engineering-vnext-1.0",
            "AX-PUB-GATE-001","AX-PUB-DEV-001","AX-PUB-DEV-002","AX-PUB-CI-003","DEV-GATE-00: CLOSED",
            "AX-PUB-DEV-003","check_developer_experience.py","DEV-GATE-01: CANDIDATE / NOT CLOSED",
            "AX_DEVELOPER_EXPERIENCE_PASS"
        ):
            if marker not in text: findings.append(f"quickstart missing reference: {marker}")
    if not isinstance(manifest.get("claim_boundary"), list) or not manifest.get("claim_boundary"): findings.append("claim_boundary must be non-empty array")
    if findings: return fail(findings)
    print("AX_PUBLIC_ARTIFACT_MANIFEST_PASS"); return 0

if __name__ == "__main__": raise SystemExit(main())
