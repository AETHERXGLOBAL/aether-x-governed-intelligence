#!/usr/bin/env python3
"""Fail closed if AX-PUB-TEST-002 crosses the private-project boundary."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTORS = ROOT / "conformance" / "AX-PUB-TEST-002" / "vectors.json"
RUNNER = ROOT / "conformance" / "AX-PUB-TEST-002" / "run_conformance.py"
VALIDATOR = ROOT / "reference-implementations" / "agent-tool-authority-validator" / "validator.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-agent-authority-conformance.yml"
PRIVATE_REPOSITORY_SLUGS = ("aether-x-quantum","AX-OS","aether-intelligence-core-AIC-","aether-x-research","aether-x-governance","aether-x-global-website","amii-research-lab")

def main() -> int:
    findings: list[str] = []
    for path in (VECTORS, RUNNER, VALIDATOR, WORKFLOW):
        if not path.is_file(): findings.append(f"missing public runtime file: {path.relative_to(ROOT)}")
    if findings:
        for f in findings: print(f"AX_AGENT_PUBLIC_BOUNDARY_FAIL: {f}")
        return 1
    runtime_text = "\n".join(p.read_text(encoding="utf-8") for p in (VECTORS,RUNNER,VALIDATOR,WORKFLOW)); lower = runtime_text.lower()
    for slug in PRIVATE_REPOSITORY_SLUGS:
        if slug.lower() in lower: findings.append(f"private repository slug referenced by public runtime: {slug}")
    for marker in ("${{ secrets.","private_key","access_token","personal_access_token","repository:","submodules: true"):
        if marker.lower() in lower: findings.append(f"forbidden private-access marker in public runtime: {marker}")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    if "permissions:\n  contents: read" not in workflow_text: findings.append("workflow must preserve contents: read permission")
    try: vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: findings.append(f"cannot parse vectors: {exc}"); vectors = {}
    if vectors.get("validator") != "AX-PUB-REF-003": findings.append("test kit must depend only on AX-PUB-REF-003")
    baseline = vectors.get("baseline"); allowed = "reference-implementations/agent-tool-authority-validator/examples/"
    if not isinstance(baseline, str) or not baseline.startswith(allowed): findings.append("baseline is outside approved public example path")
    elif ".." in Path(baseline).parts or Path(baseline).is_absolute(): findings.append("unsafe baseline path")
    if findings:
        for f in findings: print(f"AX_AGENT_PUBLIC_BOUNDARY_FAIL: {f}")
        return 1
    print("AX_AGENT_AUTHORITY_PUBLIC_BOUNDARY_PASS")
    return 0

if __name__ == "__main__": raise SystemExit(main())
