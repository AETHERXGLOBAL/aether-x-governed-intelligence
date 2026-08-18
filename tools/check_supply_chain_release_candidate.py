#!/usr/bin/env python3
"""Validate DEV-GATE-03 supply-chain/release-candidate governance state.

Gate-03 historically prohibited all package-distribution metadata because no
later SDK packaging gate existed. The closed Gate-05A decision now permits one
bounded Gate-05B package-candidate metadata file under stronger fail-closed
controls. This checker therefore preserves the Gate-03 prohibition everywhere
except the exact Gate-05B pyproject path when the later governance state is
machine-verifiably active and publication remains unauthorized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / "release-candidate" / "AX-PUB-RC-001.json"
DEV005 = ROOT / "artifacts" / "AX-PUB-DEV-005.json"
DEV007 = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
DEV008 = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
DOC = ROOT / "docs" / "AX-PUB-DEV-005_SUPPLY_CHAIN_RELEASE_CANDIDATE.md"
EVIDENCE = ROOT / "evidence" / "AX-PUB-CI-006_SUPPLY_CHAIN_RELEASE_CANDIDATE_VALIDATION.md"
SECURITY = ROOT / "SECURITY.md"
BUILD = ROOT / "tools" / "build_release_candidate.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-supply-chain-release-candidate.yml"

FORBIDDEN_METADATA = {"pyproject.toml", "setup.py", "setup.cfg", ".pypirc"}
GATE05B_PYPROJECT = ROOT / "sdk-release-candidate" / "python" / "pyproject.toml"
EXPECTED_GENERATED = {
    "release-candidate/AX-PUB-RC-001_BUILD_MANIFEST.json",
    "release-candidate/AX-PUB-RC-001.spdx.json",
}
EXPECTED_DIGEST = "8444e7c01621f3d63019b407d9379bc82176f892dce64760cc93e84064ac8c21"
EXPECTED_SOURCE_DATE_EPOCH = 1787064230


def load_json(path: Path, findings: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(data, dict):
        findings.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return data


def require_markers(path: Path, markers: tuple[str, ...], findings: list[str]) -> None:
    if not path.is_file():
        findings.append(f"missing file: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            findings.append(f"{path.relative_to(ROOT)} missing marker: {marker}")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def gate05b_metadata_allowlist(findings: list[str]) -> set[Path]:
    """Return the single later-gate metadata path only under proven Gate-05B state."""
    if not DEV008.exists():
        return set()

    dev007 = load_json(DEV007, findings)
    dev008 = load_json(DEV008, findings)
    if dev007 is None or dev008 is None:
        return set()

    valid = True
    phases = dev007.get("gate_05_phases")
    if not isinstance(phases, dict):
        findings.append("Gate-05B metadata present but DEV-007 gate_05_phases is missing")
        valid = False
    else:
        if phases.get("DEV-GATE-05A") != "CLOSED":
            findings.append("Gate-05B metadata requires DEV-GATE-05A=CLOSED")
            valid = False
        if phases.get("DEV-GATE-05B") != "ACTIVE_ENGINEERING_OBJECTIVE":
            findings.append("Gate-05B metadata requires DEV-GATE-05B=ACTIVE_ENGINEERING_OBJECTIVE")
            valid = False

    if dev007.get("publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
        findings.append("Gate-05B metadata requires parent SDK publication to remain NOT AUTHORIZED")
        valid = False
    if dev007.get("release_authorized") is not False:
        findings.append("Gate-05B metadata requires parent release_authorized=false")
        valid = False

    if dev008.get("artifact_id") != "AX-PUB-DEV-008":
        findings.append("Gate-05B metadata requires AX-PUB-DEV-008")
        valid = False
    if dev008.get("parent_decision_artifact") != "AX-PUB-DEV-007":
        findings.append("Gate-05B metadata parent decision mismatch")
        valid = False
    if dev008.get("phase") != "DEV-GATE-05B":
        findings.append("Gate-05B metadata phase mismatch")
        valid = False
    if dev008.get("publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
        findings.append("Gate-05B metadata requires SDK PUBLICATION NOT AUTHORIZED")
        valid = False
    if dev008.get("distribution_authorized") is not False:
        findings.append("Gate-05B metadata requires distribution_authorized=false")
        valid = False
    if dev008.get("license_granted") is not False:
        findings.append("Gate-05B metadata requires license_granted=false")
        valid = False
    if dev008.get("supported_sdk_established") is not False:
        findings.append("Gate-05B metadata requires supported_sdk_established=false")
        valid = False

    distribution = dev008.get("distribution")
    if not isinstance(distribution, dict):
        findings.append("Gate-05B metadata requires DEV-008 distribution state")
        valid = False
    else:
        if distribution.get("registry_ownership_established") is not False:
            findings.append("Gate-05B metadata requires registry ownership to remain unestablished")
            valid = False
        if distribution.get("registry_publication_authorized") is not False:
            findings.append("Gate-05B metadata requires registry publication to remain unauthorized")
            valid = False

    return {GATE05B_PYPROJECT} if valid else set()


def validate_dist(dist: Path, descriptor: dict[str, Any], findings: list[str]) -> None:
    bundle = dist / "AX-PUB-RC-001.zip"
    digest_file = dist / "AX-PUB-RC-001.sha256"
    manifest_file = dist / "AX-PUB-RC-001_BUILD_MANIFEST.json"
    sbom_file = dist / "AX-PUB-RC-001.spdx.json"
    for path in (bundle, digest_file, manifest_file, sbom_file):
        if not path.is_file():
            findings.append(f"built artifact missing: {path}")
    if any(not path.is_file() for path in (bundle, digest_file, manifest_file, sbom_file)):
        return

    actual = digest(bundle)
    parts = digest_file.read_text(encoding="utf-8").strip().split()
    if len(parts) != 2 or parts[0] != actual or parts[1] != "AX-PUB-RC-001.zip":
        findings.append("SHA-256 digest file does not match built bundle")
    if descriptor.get("release_candidate_established") is True and actual != descriptor.get("verified_build_digest"):
        findings.append("built bundle digest does not match verified closed-state digest")

    manifest = load_json(manifest_file, findings)
    if manifest is not None:
        if manifest.get("artifact_id") != "AX-PUB-RC-001":
            findings.append("build manifest artifact_id mismatch")
        if manifest.get("artifact_version") != "0.1.0-rc1":
            findings.append("build manifest artifact version mismatch")
        if manifest.get("third_party_runtime_dependencies") != []:
            findings.append("build manifest must declare zero third-party runtime dependencies")
        if manifest.get("package_identity_status") != "NOT APPROVED":
            findings.append("build manifest package identity boundary mismatch")
        if manifest.get("registry_status") != "NOT AUTHORIZED":
            findings.append("build manifest registry boundary mismatch")
        if descriptor.get("release_candidate_established") is True and manifest.get("source_date_epoch") != descriptor.get("verified_source_date_epoch"):
            findings.append("build manifest source_date_epoch does not match verified closed-state epoch")
        observed_sources = [item.get("path") for item in manifest.get("source_files", []) if isinstance(item, dict)]
        if observed_sources != sorted(descriptor.get("source_files", [])):
            findings.append("build manifest source set mismatch")

    sbom = load_json(sbom_file, findings)
    if sbom is not None:
        if sbom.get("spdxVersion") != "SPDX-2.3":
            findings.append("SBOM must declare SPDX-2.3")
        packages = sbom.get("packages")
        if not isinstance(packages, list) or len(packages) != 1:
            findings.append("SBOM must describe exactly the bounded engineering candidate")
        else:
            package = packages[0]
            if not isinstance(package, dict):
                findings.append("SBOM package entry invalid")
            else:
                if package.get("name") != "AX-PUB-RC-001":
                    findings.append("SBOM candidate name mismatch")
                if package.get("versionInfo") != "0.1.0-rc1":
                    findings.append("SBOM candidate version mismatch")
                if package.get("licenseConcluded") != "NOASSERTION" or package.get("licenseDeclared") != "NOASSERTION":
                    findings.append("SBOM must not invent software licence terms")

    expected = {f"AX-PUB-RC-001/{path}" for path in descriptor.get("source_files", [])}
    expected |= {f"AX-PUB-RC-001/{path}" for path in EXPECTED_GENERATED}
    try:
        with zipfile.ZipFile(bundle, "r") as archive:
            names = set(archive.namelist())
            if names != expected:
                findings.append("bundle entry inventory mismatch")
            for info in archive.infolist():
                mode = (info.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    findings.append(f"symlink entry is not allowed: {info.filename}")
                if Path(info.filename).name in FORBIDDEN_METADATA:
                    findings.append(f"forbidden distribution metadata in Gate-03 bundle: {info.filename}")
    except zipfile.BadZipFile as exc:
        findings.append(f"invalid ZIP bundle: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AX-PUB-DEV-005 / AX-PUB-RC-001 Gate-03 state")
    parser.add_argument("--dist", type=Path)
    args = parser.parse_args()
    findings: list[str] = []

    descriptor = load_json(DESCRIPTOR, findings)
    dev = load_json(DEV005, findings)

    state = dev.get("state") if dev is not None else None
    closed = state == "DEV-GATE-03_CLOSED"
    candidate = state == "DEV-GATE-03_CANDIDATE_NOT_ESTABLISHED"
    if dev is not None and not (closed or candidate):
        findings.append("DEV-005 state must be candidate/not-established or closed")

    if descriptor is not None:
        if descriptor.get("artifact_id") != "AX-PUB-RC-001":
            findings.append("release-candidate artifact_id mismatch")
        if descriptor.get("version") != "0.1.0-rc1":
            findings.append("release-candidate version mismatch")
        if descriptor.get("package_identity_status") != "NOT APPROVED":
            findings.append("package identity must remain NOT APPROVED")
        if descriptor.get("registry_status") != "NOT AUTHORIZED":
            findings.append("registry must remain NOT AUTHORIZED")
        if descriptor.get("licence_decided") is not False:
            findings.append("Gate-03 public SDK licence state must remain undecided")
        if descriptor.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("SDK publication disposition mismatch")
        if descriptor.get("third_party_runtime_dependencies") != []:
            findings.append("candidate must declare zero third-party runtime dependencies")
        if descriptor.get("artifact_upload_scope") != "CI_ONLY":
            findings.append("release candidate artifact upload must remain CI_ONLY")
        sources = descriptor.get("source_files")
        if not isinstance(sources, list) or not sources:
            findings.append("source_files must be a non-empty array")
        else:
            if len(sources) != len(set(sources)):
                findings.append("source_files contains duplicates")
            for raw in sources:
                if not isinstance(raw, str):
                    findings.append("source_files must contain strings only")
                    continue
                path = Path(raw)
                if path.is_absolute() or ".." in path.parts:
                    findings.append(f"source path escapes repository: {raw}")
                    continue
                if not (ROOT / path).is_file():
                    findings.append(f"declared source file missing: {raw}")
                if path.name in FORBIDDEN_METADATA:
                    findings.append(f"forbidden package metadata selected into Gate-03 bundle: {raw}")

        if closed:
            if descriptor.get("state") != "DEV-GATE-03_VALIDATED":
                findings.append("closed Gate-03 requires validated release-candidate descriptor state")
            if descriptor.get("release_candidate_established") is not True:
                findings.append("closed Gate-03 requires release_candidate_established=true")
            if descriptor.get("verified_build_digest") != EXPECTED_DIGEST:
                findings.append("closed Gate-03 verified build digest mismatch")
            if descriptor.get("verified_source_date_epoch") != EXPECTED_SOURCE_DATE_EPOCH:
                findings.append("closed Gate-03 verified source epoch mismatch")
            closure = descriptor.get("closure_evidence")
            if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
                findings.append("closed Gate-03 descriptor must cite AX-PUB-CI-006 v1.1")
        elif candidate:
            if descriptor.get("state") != "DEV-GATE-03_CANDIDATE":
                findings.append("candidate Gate-03 requires candidate descriptor state")
            if descriptor.get("release_candidate_established") is not False:
                findings.append("release candidate must remain not established before closure evidence")

    if dev is not None:
        if dev.get("artifact_id") != "AX-PUB-DEV-005":
            findings.append("DEV-005 artifact_id mismatch")
        if dev.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("DEV-005 SDK publication boundary mismatch")
        if closed:
            if dev.get("release_candidate_established") is not True:
                findings.append("closed DEV-005 must establish the bounded release candidate")
            if dev.get("verified_build_digest") != EXPECTED_DIGEST:
                findings.append("DEV-005 verified build digest mismatch")
            if dev.get("verified_source_date_epoch") != EXPECTED_SOURCE_DATE_EPOCH:
                findings.append("DEV-005 verified source epoch mismatch")
            for field in (
                "build_provenance_attestation_verified",
                "sbom_attestation_verified",
                "deterministic_rebuild_verified",
                "extracted_bundle_validation_verified",
            ):
                if dev.get(field) is not True:
                    findings.append(f"closed DEV-005 requires {field}=true")
            closure = dev.get("closure_evidence")
            if not isinstance(closure, dict) or closure.get("id") != "AX-PUB-CI-006" or closure.get("version") != "1.1":
                findings.append("closed DEV-005 must cite AX-PUB-CI-006 v1.1")
            if dev.get("next_gate") != "DEV-GATE-04 — External Evaluation Readiness":
                findings.append("closed DEV-005 next gate mismatch")
        elif candidate:
            if dev.get("release_candidate_established") is not False:
                findings.append("DEV-005 must not establish release candidate before CI evidence")

    allowed_later_metadata = gate05b_metadata_allowlist(findings)
    for root in (ROOT, ROOT / "sdk-candidate", ROOT / "release-candidate"):
        for forbidden in FORBIDDEN_METADATA:
            matches = list(root.rglob(forbidden)) if root.exists() else []
            for match in matches:
                if match.resolve() in {path.resolve() for path in allowed_later_metadata}:
                    continue
                findings.append(f"forbidden distribution metadata present outside authorized Gate-05B candidate: {match.relative_to(ROOT)}")

    require_markers(
        BUILD,
        ("ZIP_STORED", "SOURCE_DATE_EPOCH", "sha256", "SPDX-2.3", "SDK PUBLICATION NOT AUTHORIZED"),
        findings,
    )
    require_markers(
        WORKFLOW,
        (
            "actions/checkout@v6",
            "actions/setup-python@v6",
            "actions/attest@v4",
            "actions/upload-artifact@v6",
            "id-token: write",
            "attestations: write",
            "gh attestation verify",
            "retention-days: 7",
        ),
        findings,
    )
    require_markers(SECURITY, ("Security",), findings)

    if closed:
        require_markers(
            EVIDENCE,
            (
                "AX-PUB-CI-006",
                "`1.1`",
                "32150126557",
                EXPECTED_DIGEST,
                "SDK PUBLICATION NOT AUTHORIZED",
            ),
            findings,
        )
        require_markers(
            DOC,
            (
                "DEV-GATE-03 CLOSED",
                "RELEASE-CANDIDATE VALIDATED",
                "AX-PUB-CI-006",
                EXPECTED_DIGEST,
                "SDK PUBLICATION NOT AUTHORIZED",
            ),
            findings,
        )
    else:
        require_markers(
            DOC,
            ("DEV-GATE-03", "AX-PUB-RC-001", "SDK PUBLICATION NOT AUTHORIZED", "gh attestation verify", "SPDX 2.3"),
            findings,
        )

    if args.dist is not None and descriptor is not None:
        dist = args.dist if args.dist.is_absolute() else ROOT / args.dist
        validate_dist(dist, descriptor, findings)

    if findings:
        prefix = "AX_DEV_GATE_03_CLOSED_FAIL" if closed else "AX_DEV_GATE_03_CANDIDATE_FAIL"
        for item in findings:
            print(f"{prefix}: {item}")
        return 1

    if closed:
        print("AX_DEV_GATE_03_CLOSED_STATE_PASS")
    else:
        print("AX_DEV_GATE_03_CANDIDATE_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
