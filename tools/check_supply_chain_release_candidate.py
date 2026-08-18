#!/usr/bin/env python3
"""Validate DEV-GATE-03 supply-chain/release-candidate engineering state."""
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
DOC = ROOT / "docs" / "AX-PUB-DEV-005_SUPPLY_CHAIN_RELEASE_CANDIDATE.md"
SECURITY = ROOT / "SECURITY.md"
BUILD = ROOT / "tools" / "build_release_candidate.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-supply-chain-release-candidate.yml"

FORBIDDEN_METADATA = {"pyproject.toml", "setup.py", "setup.cfg", ".pypirc"}
EXPECTED_GENERATED = {
    "release-candidate/AX-PUB-RC-001_BUILD_MANIFEST.json",
    "release-candidate/AX-PUB-RC-001.spdx.json",
}


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


def validate_dist(dist: Path, descriptor: dict[str, Any], findings: list[str]) -> None:
    bundle = dist / "AX-PUB-RC-001.zip"
    digest_file = dist / "AX-PUB-RC-001.sha256"
    manifest_file = dist / "AX-PUB-RC-001_BUILD_MANIFEST.json"
    sbom_file = dist / "AX-PUB-RC-001.spdx.json"
    for path in (bundle, digest_file, manifest_file, sbom_file):
        if not path.is_file():
            findings.append(f"built artifact missing: {path}")
    if findings:
        return

    actual = digest(bundle)
    parts = digest_file.read_text(encoding="utf-8").strip().split()
    if len(parts) != 2 or parts[0] != actual or parts[1] != "AX-PUB-RC-001.zip":
        findings.append("SHA-256 digest file does not match built bundle")

    manifest = load_json(manifest_file, findings)
    if manifest is not None:
        if manifest.get("artifact_id") != "AX-PUB-RC-001":
            findings.append("build manifest artifact_id mismatch")
        if manifest.get("third_party_runtime_dependencies") != []:
            findings.append("build manifest must declare zero third-party runtime dependencies")
        if manifest.get("package_identity_status") != "NOT APPROVED":
            findings.append("build manifest package identity boundary mismatch")
        if manifest.get("registry_status") != "NOT AUTHORIZED":
            findings.append("build manifest registry boundary mismatch")
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
                    findings.append(f"forbidden distribution metadata in bundle: {info.filename}")
    except zipfile.BadZipFile as exc:
        findings.append(f"invalid ZIP bundle: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AX-PUB-DEV-005 / AX-PUB-RC-001 candidate state")
    parser.add_argument("--dist", type=Path)
    args = parser.parse_args()
    findings: list[str] = []

    descriptor = load_json(DESCRIPTOR, findings)
    if descriptor is not None:
        if descriptor.get("artifact_id") != "AX-PUB-RC-001":
            findings.append("release-candidate artifact_id mismatch")
        if descriptor.get("version") != "0.1.0-rc1":
            findings.append("release-candidate version mismatch")
        if descriptor.get("state") != "DEV-GATE-03_CANDIDATE":
            findings.append("release-candidate descriptor must remain DEV-GATE-03_CANDIDATE before closure")
        if descriptor.get("release_candidate_established") is not False:
            findings.append("release candidate must remain not established before closure evidence")
        if descriptor.get("package_identity_status") != "NOT APPROVED":
            findings.append("package identity must remain NOT APPROVED")
        if descriptor.get("registry_status") != "NOT AUTHORIZED":
            findings.append("registry must remain NOT AUTHORIZED")
        if descriptor.get("licence_decided") is not False:
            findings.append("public SDK licence must remain undecided")
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
                    findings.append(f"forbidden package metadata selected: {raw}")

    dev = load_json(DEV005, findings)
    if dev is not None:
        if dev.get("artifact_id") != "AX-PUB-DEV-005":
            findings.append("DEV-005 artifact_id mismatch")
        if dev.get("state") != "DEV-GATE-03_CANDIDATE_NOT_ESTABLISHED":
            findings.append("DEV-GATE-03 machine-readable state must remain candidate/not established")
        if dev.get("release_candidate_established") is not False:
            findings.append("DEV-005 must not establish release candidate before CI evidence")
        if dev.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
            findings.append("DEV-005 SDK publication boundary mismatch")

    for root in (ROOT, ROOT / "sdk-candidate", ROOT / "release-candidate"):
        for forbidden in FORBIDDEN_METADATA:
            matches = list(root.rglob(forbidden)) if root.exists() else []
            if matches:
                findings.append(f"forbidden distribution metadata present: {matches[0].relative_to(ROOT)}")

    require_markers(
        BUILD,
        (
            "ZIP_STORED",
            "SOURCE_DATE_EPOCH",
            "sha256",
            "SPDX-2.3",
            "SDK PUBLICATION NOT AUTHORIZED",
        ),
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
    require_markers(
        SECURITY,
        ("Security",),
        findings,
    )
    require_markers(
        DOC,
        (
            "DEV-GATE-03",
            "AX-PUB-RC-001",
            "SDK PUBLICATION NOT AUTHORIZED",
            "gh attestation verify",
            "SPDX 2.3",
        ),
        findings,
    )

    if args.dist is not None and descriptor is not None:
        dist = args.dist if args.dist.is_absolute() else ROOT / args.dist
        validate_dist(dist, descriptor, findings)

    if findings:
        for item in findings:
            print(f"AX_DEV_GATE_03_CANDIDATE_FAIL: {item}")
        return 1
    print("AX_DEV_GATE_03_CANDIDATE_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
