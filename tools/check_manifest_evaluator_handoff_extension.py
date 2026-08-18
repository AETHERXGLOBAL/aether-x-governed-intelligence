#!/usr/bin/env python3
"""Validate AX-PUB-MANIFEST-001 evaluator-handoff promotion state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
PACK = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
CI014 = ROOT / "evidence" / "AX-PUB-CI-014_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF_VALIDATION.md"
CI015 = ROOT / "evidence" / "AX-PUB-CI-015_EVALUATOR_HANDOFF_PROMOTED_MATERIALIZATION.md"
PACK_DOC = ROOT / "docs" / "AX-PUB-EVAL-PACK-001_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF.md"

VALIDATION_SUBJECT_SHA = "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2"
PROMOTED_SHA = "2a7c85422421428af7e51c6b4ec86a1dc7ec10f8995585d9886b38e6f0e3f085"
ACTIONS_SHA_014 = "9aab68064bf93319056dfb3d75135ab75559a26bad78ff8b949e7297c9e68961"
ACTIONS_SHA_015 = "64cd6724dc90241d5df243b6c5e1a2c8bddcb298ef049bce3a2731f634a8e0e6"
RUNTIMES = ["3.11", "3.12", "3.13", "3.14"]


def fail(message: str) -> None:
    raise SystemExit(f"AX_MANIFEST_EVALUATOR_HANDOFF_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain object")
    return value


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    require(isinstance(raw, str), "manifest_version must be string")
    try:
        parts = raw.split("-", 1)[0].split(".")
        return (int(parts[0]), int(parts[1])) >= (major, minor)
    except (ValueError, IndexError):
        fail(f"invalid manifest_version: {raw!r}")


def main() -> int:
    manifest = load(MANIFEST)
    pack = load(PACK)
    require(CI014.is_file() and CI015.is_file() and PACK_DOC.is_file(), "evaluator handoff governed paths missing")
    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest identity mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 25), "manifest must be >= v1.25")

    artifacts = {(x.get("id"), x.get("version")): x for x in manifest.get("artifacts", []) if isinstance(x, dict)}
    item = artifacts.get(("AX-PUB-EVAL-PACK-001", "0.1"))
    require(isinstance(item, dict), "AX-PUB-EVAL-PACK-001 missing from artifacts")
    require(item.get("type") == "INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF_PACK", "evaluator artifact type mismatch")
    require(item.get("path") == "docs/AX-PUB-EVAL-PACK-001_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF.md", "evaluator artifact path mismatch")
    require(item.get("machine_readable_companion") == "artifacts/AX-PUB-EVAL-PACK-001.json", "evaluator companion mismatch")
    require(item.get("entrypoint") == "tools/build_installable_evaluator_handoff.py", "evaluator builder mismatch")
    maturity = str(item.get("public_maturity", ""))
    for marker in ("CI-VALIDATED", "DETERMINISTIC", "HUMAN EXTERNAL EVALUATION NOT ESTABLISHED", "EXTERNAL REGISTRY VALIDATION NOT ESTABLISHED", "SDK PUBLICATION NOT AUTHORIZED"):
        require(marker in maturity, f"evaluator maturity missing: {marker}")

    relations = {
        (str(x.get("from_id")), str(x.get("from_version")), str(x.get("relationship")), str(x.get("to_id")), str(x.get("to_version")))
        for x in manifest.get("relationships", []) if isinstance(x, dict) and x.get("state") == "COMPATIBLE"
    }
    require(("AX-PUB-EVAL-PACK-001", "0.1", "BUILDS_ON", "AX-PUB-DEV-009", "0.1") in relations, "evaluator DEV-009 relation missing")
    require(("AX-PUB-EVAL-PACK-001", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0") in relations, "evaluator gate relation missing")

    evidence = {x.get("id"): x for x in manifest.get("validation_evidence", []) if isinstance(x, dict)}
    ci014 = evidence.get("AX-PUB-CI-014")
    ci015 = evidence.get("AX-PUB-CI-015")
    require(isinstance(ci014, dict) and isinstance(ci015, dict), "CI-014/CI-015 missing from manifest evidence")
    require(ci014.get("verified_head_commit") == "8817b4540a8dee4ab0b1e1ad1fcb21c4826d710f", "CI-014 head mismatch")
    require(ci014.get("workflow_run_id") == 32196714529 and ci014.get("job_id") == 95902129022, "CI-014 workflow identity mismatch")
    require(ci014.get("validation_subject_zip_sha256") == VALIDATION_SUBJECT_SHA, "CI-014 subject SHA mismatch")
    require(ci014.get("actions_artifact_id") == 9346099991 and ci014.get("actions_artifact_sha256") == ACTIONS_SHA_014, "CI-014 Actions artifact mismatch")
    require(ci014.get("verified_runtime_matrix") == RUNTIMES and ci014.get("conclusion") == "SUCCESS", "CI-014 validation result mismatch")
    require(ci015.get("verified_head_commit") == "51524fed7d7aee44254ec318e7897b988deb8498", "CI-015 head mismatch")
    require(ci015.get("workflow_run_id") == 32197243557 and ci015.get("job_id") == 95903654036, "CI-015 workflow identity mismatch")
    require(ci015.get("promoted_zip_sha256") == PROMOTED_SHA, "CI-015 promoted SHA mismatch")
    require(ci015.get("actions_artifact_id") == 9346271842 and ci015.get("actions_artifact_sha256") == ACTIONS_SHA_015, "CI-015 Actions artifact mismatch")
    require(ci015.get("verified_runtime_matrix") == RUNTIMES and ci015.get("conclusion") == "SUCCESS", "CI-015 validation result mismatch")
    for record, label in ((ci014, "CI-014"), (ci015, "CI-015")):
        for key in ("human_external_evaluation", "external_registry_validation", "supported_sdk_established", "sdk_publication_authorized"):
            require(record.get(key) is False, f"{label} boundary changed: {key}")

    current = manifest.get("current_installable_external_evaluator_handoff")
    require(isinstance(current, dict), "current evaluator handoff state missing")
    require(current.get("id") == "AX-PUB-EVAL-PACK-001" and current.get("version") == "0.1", "current evaluator identity mismatch")
    require(current.get("state") == "CI_VALIDATED_HANDOFF_READY_FOR_AUTHORIZED_EXTERNAL_EVALUATOR", "current evaluator state mismatch")
    require(current.get("validation_evidence") == "AX-PUB-CI-014", "current evaluator validation evidence mismatch")
    require(current.get("promoted_materialization_evidence") == "AX-PUB-CI-015", "current evaluator materialization evidence mismatch")
    require(current.get("validation_subject_zip_sha256") == VALIDATION_SUBJECT_SHA, "current subject SHA mismatch")
    require(current.get("current_promoted_zip_sha256") == PROMOTED_SHA, "current promoted SHA mismatch")
    require(current.get("verified_runtime_matrix") == RUNTIMES, "current evaluator runtime matrix mismatch")
    require(current.get("final_external_index_required") is True, "final external-index requirement missing")
    for key in ("external_registry_validation_established", "human_external_evaluation_occurred", "independent_evaluator_result_established", "external_adoption_established", "release_control_readiness_established", "registry_ownership_established", "public_sdk_licence_granted", "supported_sdk_established"):
        require(current.get(key) is False, f"current evaluator boundary changed: {key}")
    require(current.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current evaluator publication boundary changed")

    require(pack.get("state") == "DEV_GATE_05C_EXTERNAL_EVALUATOR_HANDOFF_PACK_CI_VALIDATED", "pack source state mismatch")
    pack_state = pack.get("current_state")
    require(isinstance(pack_state, dict) and pack_state.get("handoff_pack_ci_validated") is True, "pack CI validation state missing")
    for key in ("external_registry_validation_established", "human_external_evaluation_occurred", "external_adoption_established", "release_control_readiness_established", "registry_ownership_established", "public_sdk_licence_granted", "supported_sdk_established", "sdk_publication_authorized"):
        require(pack_state.get(key) is False, f"pack boundary changed: {key}")

    boundaries = set(manifest.get("claim_boundary", []))
    for marker in (
        "EVALUATOR HANDOFF PACK PASS DOES NOT ESTABLISH HUMAN EXTERNAL EVALUATION",
        "LOCAL REHEARSAL PASS DOES NOT ESTABLISH EXTERNAL-INDEX VALIDATION",
        "CI HANDOFF ARTIFACT DOES NOT ESTABLISH TESTPYPI OR PYPI PUBLICATION",
        "PROMOTED EVALUATOR HANDOFF DOES NOT ESTABLISH A SUPPORTED SDK OR RELEASE AUTHORITY",
    ):
        require(marker in boundaries, f"manifest claim boundary missing: {marker}")

    print(
        "AX_MANIFEST_EVALUATOR_HANDOFF_PASS manifest>=1.25 handoff=CI_VALIDATED "
        f"promoted_sha={PROMOTED_SHA} runtimes=3.11-3.14 external_registry=false "
        "human_evaluation=false supported_sdk=false publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
