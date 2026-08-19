#!/usr/bin/env python3
"""One-shot, fail-closed textual migration from AX-PUB-MANIFEST-001 v1.25 to v1.26.

This preserves the existing compact manifest formatting and historical records while
adding only the CI-validated release-readiness aggregation extension.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"

ARTIFACT_LINE = '    {"id":"AX-PUB-RELPACK-001","version":"0.1","type":"SDK_RELEASE_READINESS_EVIDENCE_AGGREGATION","path":"docs/AX-PUB-RELPACK-001_SDK_RELEASE_READINESS_EVIDENCE_PACK.md","machine_readable_companion":"artifacts/AX-PUB-RELPACK-001.json","entrypoint":"tools/build_sdk_release_readiness_pack.py","state":"CURRENT","public_maturity":"DEV-GATE-05D READINESS AGGREGATION / CI-VALIDATED / CURRENTLY BLOCKED / 4 OF 13 HARD DIMENSIONS ESTABLISHED / 9 BLOCKED / DEV-GATE-05D NOT AUTHORIZED / SDK PUBLICATION NOT AUTHORIZED"},\n'
REL_LINES = (
    '    {"from_id":"AX-PUB-RELPACK-001","from_version":"0.1","relationship":"IMPLEMENTS_PROGRAM_GATE_OF","to_id":"AX-PUB-DEV-001","to_version":"1.0","state":"COMPATIBLE"},\n'
    '    {"from_id":"AX-PUB-RELPACK-001","from_version":"0.1","relationship":"BUILDS_ON","to_id":"AX-PUB-EVAL-PACK-001","to_version":"0.1","state":"COMPATIBLE"},\n'
    '    {"from_id":"AX-PUB-RELPACK-001","from_version":"0.1","relationship":"GOVERNED_BY","to_id":"AX-PUB-GATE-001","to_version":"1.0","state":"COMPATIBLE"},\n'
)
CI016_LINE = '    {"id":"AX-PUB-CI-016","version":"1.0","path":"evidence/AX-PUB-CI-016_SDK_RELEASE_READINESS_EVIDENCE_PACK_VALIDATION.md","scope":"DEV_GATE_05D_RELEASE_READINESS_EVIDENCE_AGGREGATION_VALIDATION","verified_head_commit":"c9efbf2cb7a2d837c97ff378e9918500e8662e26","validation_merge_commit":"836217925bcf7e5cff2cf8a09d1d5e7cdb244800","workflow_run_id":32200229804,"workflow_run_number":3,"job_id":95912269419,"governance_workflow_run_id":32200229793,"governance_workflow_run_number":210,"actions_artifact_id":9347211356,"actions_artifact_sha256":"e9614ca5b70667e6d2218d1f19c764ce2cf09ada13764282c5758cf1865fa331","required_dimension_count":13,"established_dimension_count":4,"blocked_dimension_count":9,"ready_for_dev_gate_05d_authority_review":false,"dev_gate_05d_authorized":false,"sdk_publication_authorized":false,"conclusion":"SUCCESS"}'
CURRENT_LINE = '  "current_sdk_release_readiness_aggregation": {"id":"AX-PUB-RELPACK-001","version":"0.1","path":"docs/AX-PUB-RELPACK-001_SDK_RELEASE_READINESS_EVIDENCE_PACK.md","machine_readable_companion":"artifacts/AX-PUB-RELPACK-001.json","builder":"tools/build_sdk_release_readiness_pack.py","checker":"tools/check_sdk_release_readiness_pack.py","validation_evidence":"AX-PUB-CI-016","state":"CI_VALIDATED_BLOCKED_BEFORE_DEV_GATE_05D_AUTHORITY_REVIEW","required_dimension_count":13,"established_dimension_count":4,"blocked_dimension_count":9,"ready_for_dev_gate_05d_authority_review":false,"external_registry_validation_established":false,"independent_human_external_evaluation_established":false,"release_control_readiness_established":false,"registry_ownership_and_trusted_publisher_established":false,"licence_and_ip_clearance_established":false,"support_contract_activated":false,"security_operations_ready":false,"release_owner_and_accountability_established":false,"dev_gate_05d_authorized":false,"supported_sdk_established":false,"sdk_publication_disposition":"SDK PUBLICATION NOT AUTHORIZED"},\n'
CLAIM_LINES = (
    '    "RELEASE READINESS AGGREGATION PASS DOES NOT ESTABLISH RELEASE READINESS WHILE HARD DIMENSIONS ARE BLOCKED",\n'
    '    "READY FOR DEV-GATE-05D AUTHORITY REVIEW DOES NOT AUTHORIZE DEV-GATE-05D OR SDK PUBLICATION",\n'
)


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise SystemExit(f"AX_MANIFEST_V126_FAIL: expected one {label}, found {count}")


def main() -> int:
    raw = PATH.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    if parsed.get("manifest_id") != "AX-PUB-MANIFEST-001" or parsed.get("manifest_version") != "1.25":
        raise SystemExit("AX_MANIFEST_V126_FAIL: migration requires canonical v1.25 source")
    if "AX-PUB-RELPACK-001" in raw or "AX-PUB-CI-016" in raw:
        raise SystemExit("AX_MANIFEST_V126_FAIL: release-readiness extension already present")

    require_once(raw, '  "manifest_version": "1.25",', "v1.25 version marker")
    require_once(raw, '    {"id":"AX-PUB-RC-001","version":"0.1.0-rc1"', "RC artifact insertion marker")
    require_once(raw, '    {"from_id":"AX-PUB-RC-001","from_version":"0.1.0-rc1"', "RC relationship insertion marker")
    require_once(raw, '\n  ],\n  "current_snapshot":', "validation evidence terminator")
    require_once(raw, '  "claim_boundary": [\n', "claim-boundary marker")

    raw = raw.replace('  "manifest_version": "1.25",', '  "manifest_version": "1.26",', 1)
    raw = raw.replace('    {"id":"AX-PUB-RC-001","version":"0.1.0-rc1"', ARTIFACT_LINE + '    {"id":"AX-PUB-RC-001","version":"0.1.0-rc1"', 1)
    raw = raw.replace('    {"from_id":"AX-PUB-RC-001","from_version":"0.1.0-rc1"', REL_LINES + '    {"from_id":"AX-PUB-RC-001","from_version":"0.1.0-rc1"', 1)
    raw = raw.replace('\n  ],\n  "current_snapshot":', ',\n' + CI016_LINE + '\n  ],\n  "current_snapshot":', 1)
    raw = raw.replace('  "claim_boundary": [\n', CURRENT_LINE + '  "claim_boundary": [\n' + CLAIM_LINES, 1)

    updated = json.loads(raw)
    if updated.get("manifest_version") != "1.26":
        raise SystemExit("AX_MANIFEST_V126_FAIL: version promotion missing")
    artifact_ids = [x.get("id") for x in updated.get("artifacts", []) if isinstance(x, dict)]
    if artifact_ids.count("AX-PUB-RELPACK-001") != 1:
        raise SystemExit("AX_MANIFEST_V126_FAIL: RELPACK artifact cardinality mismatch")
    evidence_ids = [x.get("id") for x in updated.get("validation_evidence", []) if isinstance(x, dict)]
    if evidence_ids.count("AX-PUB-CI-016") != 1:
        raise SystemExit("AX_MANIFEST_V126_FAIL: CI-016 evidence cardinality mismatch")
    current = updated.get("current_sdk_release_readiness_aggregation")
    if not isinstance(current, dict) or current.get("ready_for_dev_gate_05d_authority_review") is not False:
        raise SystemExit("AX_MANIFEST_V126_FAIL: fail-closed current state missing")
    if current.get("dev_gate_05d_authorized") is not False:
        raise SystemExit("AX_MANIFEST_V126_FAIL: 05D authority boundary changed")

    PATH.write_text(raw, encoding="utf-8")
    print("AX_MANIFEST_V126_PROMOTION_PASS relpack=CI_VALIDATED_BLOCKED ci=AX-PUB-CI-016 ready_for_05d=false sdk_publication=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
