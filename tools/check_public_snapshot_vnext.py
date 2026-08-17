#!/usr/bin/env python3
"""Validate AX-PUB-SNAP-002 against its immutable public Git anchor."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "snapshots" / "AX-PUB-SNAP-002.json"
DOC = ROOT / "snapshots" / "AX-PUB-SNAP-002_GOVERNED_INTELLIGENCE_PUBLIC_VNEXT.md"
REQUIRED = {
    "AX-PUB-ARCH-001","AX-PUB-SPEC-002","AX-PUB-SPEC-003","AX-PUB-SPEC-004",
    "AX-PUB-SCHEMA-001","AX-PUB-SCHEMA-002","AX-PUB-SCHEMA-003",
    "AX-PUB-REF-001","AX-PUB-REF-002","AX-PUB-REF-003",
    "AX-PUB-TEST-001","AX-PUB-TEST-002","AX-PUB-POL-001",
}
REQUIRED_CI = {
    "Validate Agent Authority Conformance Kit",
    "Validate Agent Tool-Use Authority Contract",
    "Validate Agent Tool-Use Authority Reference",
    "Validate Public Artifact Manifest",
}

def git(*args: str) -> str:
    p = subprocess.run(["git",*args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0: raise RuntimeError(p.stderr.strip() or "git command failed")
    return p.stdout.strip()

def check_record(record: dict[str,Any], anchor: str, label: str, findings: list[str]) -> None:
    path, expected = record.get("path"), record.get("git_blob_sha")
    if not isinstance(path,str) or not path: findings.append(f"{label}: missing path"); return
    if not isinstance(expected,str) or len(expected)!=40: findings.append(f"{label}: invalid git_blob_sha"); return
    try: actual = git("rev-parse", f"{anchor}:{path}")
    except RuntimeError as exc: findings.append(f"{label}: cannot resolve {path}: {exc}"); return
    if actual != expected: findings.append(f"{label}: blob mismatch for {path}: expected {expected}, got {actual}")
    ep, ep_sha = record.get("entrypoint"), record.get("entrypoint_git_blob_sha")
    if ep is not None or ep_sha is not None:
        if not isinstance(ep,str) or not ep or not isinstance(ep_sha,str) or len(ep_sha)!=40:
            findings.append(f"{label}: invalid entrypoint identity"); return
        try: actual_ep = git("rev-parse", f"{anchor}:{ep}")
        except RuntimeError as exc: findings.append(f"{label}: cannot resolve entrypoint {ep}: {exc}"); return
        if actual_ep != ep_sha: findings.append(f"{label}: entrypoint blob mismatch for {ep}")

def main() -> int:
    findings: list[str] = []
    try: data = json.loads(SNAP.read_text(encoding="utf-8"))
    except Exception as exc: print(f"AX_VNEXT_SNAPSHOT_FAIL: {exc}"); return 1
    if data.get("snapshot_id") != "AX-PUB-SNAP-002": findings.append("snapshot_id mismatch")
    if data.get("snapshot_version") != "1.0": findings.append("snapshot_version mismatch")
    if data.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence": findings.append("repository mismatch")
    anchor = data.get("anchor_commit")
    if not isinstance(anchor,str) or len(anchor)!=40: findings.append("invalid anchor_commit"); anchor=""
    if anchor:
        try:
            if git("rev-parse",f"{anchor}^{{commit}}") != anchor: findings.append("anchor does not resolve to itself")
            subprocess.run(["git","merge-base","--is-ancestor",anchor,"HEAD"], cwd=ROOT, check=True)
        except Exception as exc: findings.append(f"anchor unavailable or not ancestor: {exc}")
    manifest = data.get("artifact_manifest")
    if not isinstance(manifest,dict): findings.append("artifact_manifest missing")
    else:
        if manifest.get("id")!="AX-PUB-MANIFEST-001" or manifest.get("version")!="1.4": findings.append("artifact_manifest must be AX-PUB-MANIFEST-001 v1.4")
        if anchor: check_record(manifest,anchor,"artifact_manifest",findings)
    inv = data.get("inventory")
    ids=set()
    if not isinstance(inv,list) or not inv: findings.append("inventory missing"); inv=[]
    for i,record in enumerate(inv):
        if not isinstance(record,dict): findings.append(f"inventory[{i}] invalid"); continue
        aid=record.get("id")
        if isinstance(aid,str): ids.add(aid)
        else: findings.append(f"inventory[{i}] missing id")
        if anchor: check_record(record,anchor,f"inventory[{i}]",findings)
    for missing in sorted(REQUIRED-ids): findings.append(f"required artifact missing: {missing}")
    support=data.get("supporting_material")
    if not isinstance(support,list): findings.append("supporting_material missing"); support=[]
    for i,record in enumerate(support):
        if isinstance(record,dict) and anchor: check_record(record,anchor,f"supporting_material[{i}]",findings)
    ci=data.get("ci_evidence")
    if not isinstance(ci,dict): findings.append("ci_evidence missing")
    else:
        runs=ci.get("runs") if isinstance(ci.get("runs"),list) else []
        successful={r.get("workflow") for r in runs if isinstance(r,dict) and r.get("conclusion")=="success"}
        for name in sorted(REQUIRED_CI-successful): findings.append(f"required successful CI evidence missing: {name}")
    if not DOC.is_file(): findings.append("snapshot documentation missing")
    elif anchor:
        text=DOC.read_text(encoding="utf-8")
        if anchor not in text: findings.append("snapshot documentation missing anchor")
        normalized=text.replace("**","")
        for marker in ("not a GitHub Release","not a Git tag","not a product release"):
            if marker not in normalized: findings.append(f"snapshot documentation missing boundary: {marker}")
    if not isinstance(data.get("claim_boundary"),list) or not data.get("claim_boundary"): findings.append("claim_boundary missing")
    if findings:
        for f in findings: print(f"AX_VNEXT_SNAPSHOT_FAIL: {f}")
        return 1
    print("AX_PUBLIC_VNEXT_SNAPSHOT_PASS")
    return 0

if __name__ == "__main__": raise SystemExit(main())
