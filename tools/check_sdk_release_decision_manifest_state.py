#!/usr/bin/env python3
"""Cross-check the permanently closed DEV-GATE-05A state against the public manifest.

The checker accepts the original post-05A state (05B active) and the later
AX-PUB-CI-009-backed state (05B closed / 05C active). Advancing past 05B does
not weaken any Gate-05A invariant or publication boundary.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "AX-PUB-MANIFEST-001.json"
DEV007 = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
DEV008 = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
EVIDENCE_008 = ROOT / "evidence" / "AX-PUB-CI-008_SDK_RELEASE_DECISION_BASELINE_VALIDATION.md"
EVIDENCE_009 = ROOT / "evidence" / "AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_RELEASE_DECISION_MANIFEST_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain an object")
    return data


def version_at_least(raw: Any, major: int, minor: int) -> bool:
    if not isinstance(raw, str):
        return False
    try:
        head = raw.split("-", 1)[0].split(".")
        return (int(head[0]), int(head[1])) >= (major, minor)
    except (ValueError, IndexError):
        return False


def one(items: list[dict[str, Any]], artifact_id: str, version: str) -> dict[str, Any]:
    matches = [x for x in items if x.get("id") == artifact_id and x.get("version") == version]
    require(len(matches) == 1, f"manifest must contain exactly one {artifact_id} v{version}")
    return matches[0]


def main() -> None:
    manifest = load(MANIFEST)
    dev007 = load(DEV007)

    require(dev007.get("artifact_id") == "AX-PUB-DEV-007", "DEV-007 artifact ID mismatch")
    phases = dev007.get("gate_05_phases")
    require(isinstance(phases, dict), "DEV-007 gate_05_phases missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "DEV-GATE-05A is not closed")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "DEV-GATE-05D must remain unauthorized")
    b_state = phases.get("DEV-GATE-05B")
    require(b_state in {"ACTIVE_ENGINEERING_OBJECTIVE", "CLOSED"}, "unsupported DEV-GATE-05B progression state")
    advanced = b_state == "CLOSED"
    if advanced:
        require(phases.get("DEV-GATE-05C") == "ACTIVE_ENGINEERING_OBJECTIVE", "closed 05B must advance 05C")
        require(dev007.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "DEV-007 next phase mismatch after 05B closure")
        closure = dev007.get("installable_package_closure_evidence")
        require(isinstance(closure, dict), "DEV-007 installable-package closure evidence missing")
        require(closure.get("id") == "AX-PUB-CI-009" and closure.get("conclusion") == "SUCCESS", "DEV-007 must cite successful AX-PUB-CI-009")
    else:
        require(phases.get("DEV-GATE-05C") == "NOT_ESTABLISHED", "active 05B must not pre-promote 05C")
        require(dev007.get("next_phase") == "DEV-GATE-05B — Installable Package Candidate", "DEV-007 candidate next phase mismatch")

    require(dev007.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "SDK publication boundary changed")
    require(dev007.get("release_authorized") is False, "release authority must remain false")

    require(manifest.get("manifest_id") == "AX-PUB-MANIFEST-001", "manifest ID mismatch")
    require(version_at_least(manifest.get("manifest_version"), 1, 20 if advanced else 19), "manifest version is too old for Gate-05 progression state")

    artifacts_raw = manifest.get("artifacts")
    require(isinstance(artifacts_raw, list), "manifest artifacts must be an array")
    artifacts = [x for x in artifacts_raw if isinstance(x, dict)]
    dev_entry = one(artifacts, "AX-PUB-DEV-007", "0.1")
    require(dev_entry.get("state") == "CURRENT", "AX-PUB-DEV-007 manifest state must be CURRENT")
    maturity = str(dev_entry.get("public_maturity", ""))
    for marker in (
        "DEV-GATE-05A CLOSED",
        "DIRECT CI VALIDATED PYTHON 3.11-3.14",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in maturity, f"AX-PUB-DEV-007 public maturity missing {marker}")
    require(("DEV-GATE-05B CLOSED" if advanced else "DEV-GATE-05B ACTIVE") in maturity, "DEV-007 maturity does not match 05B state")
    if advanced:
        require("DEV-GATE-05C ACTIVE" in maturity, "DEV-007 maturity missing active 05C")

    relations = manifest.get("relationships")
    require(isinstance(relations, list), "manifest relationships must be an array")
    relation_set = {
        (x.get("from_id"), x.get("from_version"), x.get("relationship"), x.get("to_id"), x.get("to_version"), x.get("state"))
        for x in relations if isinstance(x, dict)
    }
    for required in (
        ("AX-PUB-DEV-007", "0.1", "IMPLEMENTS_PROGRAM_GATE_OF", "AX-PUB-DEV-001", "1.0", "COMPATIBLE"),
        ("AX-PUB-DEV-007", "0.1", "BUILDS_ON", "AX-PUB-DEV-006", "1.0", "COMPATIBLE"),
        ("AX-PUB-DEV-007", "0.1", "GOVERNED_BY", "AX-PUB-GATE-001", "1.0", "COMPATIBLE"),
    ):
        require(required in relation_set, f"missing DEV-007 manifest relation: {required[2]}")

    evidence_raw = manifest.get("validation_evidence")
    require(isinstance(evidence_raw, list), "manifest validation_evidence must be an array")
    evidence = [x for x in evidence_raw if isinstance(x, dict)]
    ci008 = one(evidence, "AX-PUB-CI-008", "1.0")
    require(ci008.get("validated_base_commit") == "fa1e2d132071ddff195fb998d0d27a6b5b9d4e40", "CI-008 validated base mismatch")
    require(ci008.get("verified_head_commit") == "7877abceda8fa6a372300fceb1ae0c124853d2b6", "CI-008 verified head mismatch")
    require(ci008.get("workflow_run_id") == 32168696722, "CI-008 workflow run mismatch")
    require(ci008.get("governance_workflow_run_id") == 32168696655, "CI-008 governance run mismatch")
    require(ci008.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "CI-008 runtime matrix mismatch")
    require(ci008.get("sdk_publication_authorized") is False, "CI-008 must not authorize SDK publication")
    require(ci008.get("conclusion") == "SUCCESS", "CI-008 conclusion must be SUCCESS")

    program = manifest.get("current_developer_program")
    require(isinstance(program, dict), "current_developer_program missing")
    require(program.get("active_gate") == "DEV-GATE-05 — SDK Release Decision", "active top-level gate changed")
    require(program.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "program publication boundary changed")

    current = manifest.get("current_sdk_release_decision_baseline")
    require(isinstance(current, dict), "current_sdk_release_decision_baseline missing")
    require(current.get("id") == "AX-PUB-DEV-007", "current release-decision baseline ID mismatch")
    require(current.get("state") == "CLOSED", "current release-decision baseline must be CLOSED")
    require(current.get("closure_evidence") == "AX-PUB-CI-008", "current Gate-05A closure evidence mismatch")
    require(current.get("registry_ownership_established") is False, "registry ownership must remain unestablished")
    require(current.get("sdk_publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "current publication boundary changed")

    if advanced:
        require(program.get("closed_phase") == "DEV-GATE-05B — Installable Package Candidate", "advanced closed phase mismatch")
        require(program.get("active_phase") == "DEV-GATE-05C — Distribution & External Validation", "advanced active phase mismatch")
        require(current.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "current baseline next phase mismatch")
        dev008 = load(DEV008)
        require(dev008.get("phase_state") == "CLOSED", "DEV-008 must be closed when DEV-007 advances")
        require(dev008.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "DEV-008 publication boundary changed")
        require(dev008.get("distribution_authorized") is False, "DEV-008 distribution must remain unauthorized")
        require(dev008.get("license_granted") is False, "DEV-008 must not grant a licence")
        require(dev008.get("supported_sdk_established") is False, "DEV-008 must not establish a supported SDK")
        ci009 = one(evidence, "AX-PUB-CI-009", "1.0")
        require(ci009.get("workflow_run_id") == 32171606094, "CI-009 workflow run mismatch")
        require(ci009.get("job_id") == 95823835258, "CI-009 job mismatch")
        require(ci009.get("conclusion") == "SUCCESS", "CI-009 conclusion must be SUCCESS")
        require(ci009.get("sdk_publication_authorized") is False, "CI-009 must not authorize publication")
        require(EVIDENCE_009.is_file(), "AX-PUB-CI-009 evidence file is missing")
    else:
        require(program.get("closed_phase") == "DEV-GATE-05A — Release Decision Baseline", "candidate closed phase mismatch")
        require(program.get("active_phase") == "DEV-GATE-05B — Installable Package Candidate", "candidate active phase mismatch")
        require(current.get("next_phase") == "DEV-GATE-05B — Installable Package Candidate", "candidate baseline next phase mismatch")

    boundaries = manifest.get("claim_boundary")
    require(isinstance(boundaries, list), "manifest claim_boundary must be an array")
    require("DEV-GATE-05A CLOSED DOES NOT ESTABLISH SDK RELEASE AUTHORITY OR PUBLICATION" in boundaries, "Gate-05A closure claim boundary missing")
    if advanced:
        require("DEV-GATE-05B CLOSED DOES NOT ESTABLISH REGISTRY OWNERSHIP, A SOFTWARE LICENCE, A SUPPORTED SDK OR SDK PUBLICATION" in boundaries, "Gate-05B claim boundary missing")

    require(EVIDENCE_008.is_file(), "AX-PUB-CI-008 evidence file is missing")
    phase = "DEV-GATE-05C" if advanced else "DEV-GATE-05B"
    print(f"AX_DEV_GATE_05A_MANIFEST_CLOSED_STATE_PASS manifest={manifest.get('manifest_version')} active_phase={phase} sdk_publication=NOT_AUTHORIZED")


if __name__ == "__main__":
    main()
