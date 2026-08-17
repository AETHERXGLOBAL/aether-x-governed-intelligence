#!/usr/bin/env python3
"""Validate AX-PUB-SNAP-001 against its immutable Git anchor.

This repository-consistency check verifies the recorded commit and Git blob
identities. It does not establish product adoption, production readiness,
security approval, or commercial release status.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_JSON = ROOT / "snapshots" / "AX-PUB-SNAP-001.json"
SNAPSHOT_DOC = ROOT / "snapshots" / "AX-PUB-SNAP-001_GOVERNED_INTELLIGENCE_PUBLIC_V1.0.md"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def main() -> int:
    findings: list[str] = []

    try:
        snapshot = load_json(SNAPSHOT_JSON)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"AX_SNAPSHOT_FAIL: cannot parse snapshot record: {exc}")
        return 1

    if snapshot.get("snapshot_id") != "AX-PUB-SNAP-001":
        findings.append("snapshot_id must be AX-PUB-SNAP-001")
    if snapshot.get("snapshot_version") != "1.0":
        findings.append("snapshot_version must be 1.0")
    if snapshot.get("repository") != "AETHERXGLOBAL/aether-x-governed-intelligence":
        findings.append("repository identity mismatch")

    anchor = snapshot.get("anchor_commit")
    if not isinstance(anchor, str) or len(anchor) != 40:
        findings.append("anchor_commit must be a full 40-character Git commit SHA")
        anchor = ""

    if anchor:
        try:
            resolved = git("rev-parse", f"{anchor}^{{commit}}")
            if resolved != anchor:
                findings.append(f"anchor does not resolve to itself: {resolved}")
        except RuntimeError as exc:
            findings.append(f"anchor commit is unavailable: {exc}")

        try:
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            findings.append("snapshot anchor is not an ancestor of current HEAD")

    def check_record(record: dict[str, Any], label: str) -> None:
        path = record.get("path")
        expected = record.get("git_blob_sha")
        if not isinstance(path, str) or not path:
            findings.append(f"{label}: missing path")
            return
        if not isinstance(expected, str) or len(expected) != 40:
            findings.append(f"{label}: invalid git_blob_sha")
            return
        if not anchor:
            return
        try:
            actual = git("rev-parse", f"{anchor}:{path}")
        except RuntimeError as exc:
            findings.append(f"{label}: cannot resolve {path} at anchor: {exc}")
            return
        if actual != expected:
            findings.append(f"{label}: blob mismatch for {path}: expected {expected}, got {actual}")

        entrypoint = record.get("entrypoint")
        entrypoint_expected = record.get("entrypoint_git_blob_sha")
        if entrypoint is not None or entrypoint_expected is not None:
            if not isinstance(entrypoint, str) or not entrypoint:
                findings.append(f"{label}: invalid entrypoint")
                return
            if not isinstance(entrypoint_expected, str) or len(entrypoint_expected) != 40:
                findings.append(f"{label}: invalid entrypoint_git_blob_sha")
                return
            try:
                actual_entrypoint = git("rev-parse", f"{anchor}:{entrypoint}")
            except RuntimeError as exc:
                findings.append(f"{label}: cannot resolve entrypoint {entrypoint}: {exc}")
                return
            if actual_entrypoint != entrypoint_expected:
                findings.append(
                    f"{label}: entrypoint blob mismatch for {entrypoint}: "
                    f"expected {entrypoint_expected}, got {actual_entrypoint}"
                )

    artifact_manifest = snapshot.get("artifact_manifest")
    if not isinstance(artifact_manifest, dict):
        findings.append("artifact_manifest must be an object")
    else:
        if artifact_manifest.get("id") != "AX-PUB-MANIFEST-001" or artifact_manifest.get("version") != "1.0":
            findings.append("artifact_manifest must identify AX-PUB-MANIFEST-001 v1.0")
        check_record(artifact_manifest, "artifact_manifest")

    inventory = snapshot.get("inventory")
    if not isinstance(inventory, list) or not inventory:
        findings.append("inventory must be a non-empty array")
        inventory = []

    ids: set[str] = set()
    required_ids = {
        "AX-PUB-ARCH-001",
        "AX-PUB-SPEC-002",
        "AX-PUB-SPEC-003",
        "AX-PUB-SCHEMA-001",
        "AX-PUB-SCHEMA-002",
        "AX-PUB-REF-001",
        "AX-PUB-REF-002",
        "AX-PUB-POL-001",
    }

    for index, record in enumerate(inventory):
        label = f"inventory[{index}]"
        if not isinstance(record, dict):
            findings.append(f"{label} must be an object")
            continue
        artifact_id = record.get("id")
        if not isinstance(artifact_id, str):
            findings.append(f"{label}: missing artifact id")
        else:
            if artifact_id in ids:
                findings.append(f"duplicate snapshot artifact id: {artifact_id}")
            ids.add(artifact_id)
        if record.get("version") != "1.0":
            findings.append(f"{label}: current public snapshot expects version 1.0")
        check_record(record, label)

    for missing in sorted(required_ids - ids):
        findings.append(f"required snapshot artifact missing: {missing}")

    supporting = snapshot.get("supporting_material")
    if not isinstance(supporting, list):
        findings.append("supporting_material must be an array")
        supporting = []
    for index, record in enumerate(supporting):
        if isinstance(record, dict):
            check_record(record, f"supporting_material[{index}]")
        else:
            findings.append(f"supporting_material[{index}] must be an object")

    if not SNAPSHOT_DOC.is_file():
        findings.append("snapshot documentation is missing")
    elif anchor:
        text = SNAPSHOT_DOC.read_text(encoding="utf-8")
        if anchor not in text:
            findings.append("snapshot documentation does not contain the anchor commit")
        normalized_text = text.replace("**", "").replace("__", "")
        if "not a GitHub Release" not in normalized_text or "not a Git tag" not in normalized_text:
            findings.append("snapshot documentation must preserve release/tag claim boundary")

    evidence = snapshot.get("validation_evidence")
    if not isinstance(evidence, list) or not evidence:
        findings.append("validation_evidence must be a non-empty array")
    else:
        exact_anchor_manifest_evidence = any(
            isinstance(item, dict)
            and item.get("workflow") == "Validate Public Artifact Manifest"
            and item.get("head_commit") == anchor
            and item.get("conclusion") == "success"
            for item in evidence
        )
        if not exact_anchor_manifest_evidence:
            findings.append("snapshot must record successful manifest validation on the exact anchor commit")

    claim_boundary = snapshot.get("claim_boundary")
    if not isinstance(claim_boundary, list) or not claim_boundary:
        findings.append("claim_boundary must be a non-empty array")

    if findings:
        for finding in findings:
            print(f"AX_SNAPSHOT_FAIL: {finding}")
        return 1

    print("AX_PUBLIC_SNAPSHOT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
