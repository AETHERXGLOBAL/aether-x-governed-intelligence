#!/usr/bin/env python3
"""Validate AX-PUB-CI-014 handoff evidence and authority boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-014_INSTALLABLE_EXTERNAL_EVALUATOR_HANDOFF_VALIDATION.md"
PACK = ROOT / "artifacts" / "AX-PUB-EVAL-PACK-001.json"
REPORT_TEMPLATE = ROOT / "examples" / "external-evaluation" / "AX-PUB-EVAL-REPORT-002.template.json"

PACK_SHA = "5dbac6681909e76a9d844fd5311b3dd3c21e0ac02ecfa27d148348d96b7fc8f2"
ACTIONS_SHA = "9aab68064bf93319056dfb3d75135ab75559a26bad78ff8b949e7297c9e68961"
WHEEL_SHA = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
SDIST_SHA = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"

MARKERS = (
    "AX-PUB-CI-014",
    "Candidate bootstrap PR: #53",
    "Bootstrap merge commit: f25e8c5db41232e29efe201bd202231994a59cdc",
    "Validation PR: #54",
    "Validation head: 8817b4540a8dee4ab0b1e1ad1fcb21c4826d710f",
    "GitHub pull-request merge-test commit: 09a5e6f1d396f23ccd26969559fe5210e6bd7b10",
    "Validation merge commit on main: 584c317c04da4219c8952f67d641ef2edb19c967",
    "Workflow run ID: 32196714529",
    "Workflow run number: 7",
    "Job ID: 95902129022",
    "Run ID: 32196714599",
    "Run number: 199",
    PACK_SHA,
    WHEEL_SHA,
    SDIST_SHA,
    "CPython 3.11 — PASS",
    "CPython 3.12 — PASS",
    "CPython 3.13 — PASS",
    "CPython 3.14 — PASS",
    "Artifact ID: 9346099991",
    ACTIONS_SHA,
    "HANDOFF PACK PASS ≠ HUMAN EXTERNAL EVALUATION",
    "LOCAL REHEARSAL PASS ≠ EXTERNAL-INDEX VALIDATION",
    "CI ARTIFACT ≠ TESTPYPI OR PYPI PUBLICATION",
    "SDK PUBLICATION NOT AUTHORIZED",
)


def fail(message: str) -> None:
    raise SystemExit(f"AX_CI014_EVIDENCE_FAIL: {message}")


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain object")
    return value


def main() -> int:
    if not EVIDENCE.is_file():
        fail("evidence file missing")
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in MARKERS:
        if marker not in text:
            fail(f"evidence missing marker: {marker}")

    pack = load(PACK)
    if pack.get("artifact_id") != "AX-PUB-EVAL-PACK-001" or pack.get("version") != "0.1":
        fail("pack identity mismatch")
    candidate = pack.get("candidate", {})
    if candidate.get("wheel_sha256") != WHEEL_SHA or candidate.get("sdist_sha256") != SDIST_SHA:
        fail("pack candidate artifact identity mismatch")
    report = pack.get("report_contract", {})
    if report.get("final_requires_external_index_used") is not True:
        fail("final external-index requirement missing")
    if report.get("final_requires_independent_human_evaluator") is not True:
        fail("independent human requirement missing")

    state = pack.get("current_state", {})
    for key in (
        "external_registry_validation_established",
        "human_external_evaluation_occurred",
        "external_adoption_established",
        "release_control_readiness_established",
        "registry_ownership_established",
        "public_sdk_licence_granted",
        "supported_sdk_established",
        "sdk_publication_authorized",
    ):
        if state.get(key) is not False:
            fail(f"pack authority boundary changed: {key}")

    template = load(REPORT_TEMPLATE)
    if template.get("report_format") != "AX-PUB-EVAL-REPORT-002" or template.get("record_state") != "TEMPLATE":
        fail("external evaluation template state mismatch")
    if template.get("evaluation", {}).get("external_index_used") is not None:
        fail("template must not pre-claim external index use")
    if template.get("external_adoption_established") is not False:
        fail("template must not pre-claim adoption")
    if template.get("supported_sdk_established") is not False:
        fail("template must not pre-claim supported SDK")
    if template.get("sdk_publication") != "NOT_AUTHORIZED":
        fail("template publication boundary changed")

    print(
        "AX_CI014_EVIDENCE_PASS "
        f"run=32196714529 pack_sha256={PACK_SHA} actions_artifact=9346099991 "
        "runtimes=3.11-3.14 human_evaluation=false external_registry=false "
        "sdk_publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
