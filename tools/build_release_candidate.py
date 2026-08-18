#!/usr/bin/env python3
"""Build AX-PUB-RC-001 as a deterministic, non-published engineering bundle.

The build uses only the Python standard library and the public repository source set
declared in release-candidate/AX-PUB-RC-001.json. It does not publish a package.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR_PATH = ROOT / "release-candidate" / "AX-PUB-RC-001.json"
DEFAULT_EPOCH = 315532800  # 1980-01-01T00:00:00Z; ZIP-compatible deterministic fallback.
BUNDLE_ROOT = "AX-PUB-RC-001"


def json_bytes(data: Any) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_descriptor() -> dict[str, Any]:
    data = json.loads(DESCRIPTOR_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("release-candidate descriptor must be a JSON object")
    return data


def source_epoch() -> int:
    raw = os.environ.get("SOURCE_DATE_EPOCH")
    if raw is None:
        return DEFAULT_EPOCH
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("SOURCE_DATE_EPOCH must be an integer") from exc
    return max(value, DEFAULT_EPOCH)


def zip_datetime(epoch: int) -> tuple[int, int, int, int, int, int]:
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    year = max(dt.year, 1980)
    second = dt.second - (dt.second % 2)  # ZIP timestamps use 2-second resolution.
    return (year, dt.month, dt.day, dt.hour, dt.minute, second)


def validate_source_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"source path escapes repository: {raw}")
    full = ROOT / path
    if not full.is_file():
        raise FileNotFoundError(f"declared source file is missing: {raw}")
    if full.is_symlink():
        raise ValueError(f"symlink source is not allowed: {raw}")
    return full


def build_manifest(descriptor: dict[str, Any], source_files: list[str], epoch: int) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for raw in source_files:
        path = validate_source_path(raw)
        payload = path.read_bytes()
        files.append({
            "path": raw,
            "sha256": sha256_bytes(payload),
            "size_bytes": len(payload),
        })
    return {
        "artifact_id": "AX-PUB-RC-001",
        "artifact_version": descriptor.get("version"),
        "type": "DETERMINISTIC_RELEASE_CANDIDATE_BUILD_MANIFEST",
        "source_date_epoch": epoch,
        "source_files": files,
        "third_party_runtime_dependencies": descriptor.get("third_party_runtime_dependencies", []),
        "package_identity_status": descriptor.get("package_identity_status"),
        "registry_status": descriptor.get("registry_status"),
        "licence_decided": descriptor.get("licence_decided"),
        "sdk_publication_disposition": descriptor.get("sdk_publication_disposition"),
    }


def spdx_sbom(descriptor: dict[str, Any], epoch: int) -> dict[str, Any]:
    created = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "AX-PUB-RC-001 engineering release candidate SBOM",
        "documentNamespace": "https://github.com/AETHERXGLOBAL/aether-x-governed-intelligence/spdx/AX-PUB-RC-001/0.1.0-rc1",
        "creationInfo": {
            "created": created,
            "creators": [
                "Organization: AETHER X GLOBAL",
                "Tool: AX-PUB-DEV-005 build_release_candidate.py",
            ],
        },
        "packages": [
            {
                "name": "AX-PUB-RC-001",
                "SPDXID": "SPDXRef-Package-AX-PUB-RC-001",
                "versionInfo": str(descriptor.get("version")),
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "comment": "Non-published engineering release candidate. No software reuse licence is asserted by this SBOM.",
            }
        ],
        "relationships": [
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": "SPDXRef-Package-AX-PUB-RC-001",
            }
        ],
    }


def write_zip(output: Path, entries: dict[str, bytes], epoch: int) -> None:
    timestamp = zip_datetime(epoch)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(f"{BUNDLE_ROOT}/{name}", date_time=timestamp)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, entries[name])


def build(output_dir: Path) -> dict[str, Any]:
    descriptor = load_descriptor()
    if descriptor.get("artifact_id") != "AX-PUB-RC-001":
        raise ValueError("unexpected release-candidate artifact_id")
    if descriptor.get("sdk_publication_disposition") != "SDK PUBLICATION NOT AUTHORIZED":
        raise ValueError("build must fail closed when SDK publication boundary changes")
    if descriptor.get("package_identity_status") != "NOT APPROVED":
        raise ValueError("build requires package identity to remain NOT APPROVED")
    if descriptor.get("registry_status") != "NOT AUTHORIZED":
        raise ValueError("build requires registry status to remain NOT AUTHORIZED")
    if descriptor.get("licence_decided") is not False:
        raise ValueError("build requires public SDK licence to remain undecided")

    raw_sources = descriptor.get("source_files")
    if not isinstance(raw_sources, list) or not raw_sources or not all(isinstance(item, str) for item in raw_sources):
        raise ValueError("source_files must be a non-empty string array")
    source_files = sorted(set(raw_sources))
    if len(source_files) != len(raw_sources):
        raise ValueError("source_files must not contain duplicates")

    forbidden = set(descriptor.get("forbidden_distribution_metadata", []))
    for raw in source_files:
        if Path(raw).name in forbidden:
            raise ValueError(f"forbidden distribution metadata selected: {raw}")

    epoch = source_epoch()
    manifest = build_manifest(descriptor, source_files, epoch)
    sbom = spdx_sbom(descriptor, epoch)

    entries: dict[str, bytes] = {}
    for raw in source_files:
        entries[raw] = validate_source_path(raw).read_bytes()
    entries["release-candidate/AX-PUB-RC-001_BUILD_MANIFEST.json"] = json_bytes(manifest)
    entries["release-candidate/AX-PUB-RC-001.spdx.json"] = json_bytes(sbom)

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = output_dir / "AX-PUB-RC-001.zip"
    manifest_path = output_dir / "AX-PUB-RC-001_BUILD_MANIFEST.json"
    sbom_path = output_dir / "AX-PUB-RC-001.spdx.json"
    digest_path = output_dir / "AX-PUB-RC-001.sha256"

    write_zip(bundle_path, entries, epoch)
    manifest_path.write_bytes(json_bytes(manifest))
    sbom_path.write_bytes(json_bytes(sbom))
    digest = sha256_path(bundle_path)
    digest_path.write_text(f"{digest}  AX-PUB-RC-001.zip\n", encoding="utf-8")

    result = {
        "artifact_id": "AX-PUB-RC-001",
        "version": descriptor.get("version"),
        "bundle": str(bundle_path.relative_to(ROOT) if bundle_path.is_relative_to(ROOT) else bundle_path),
        "sha256": digest,
        "source_files": len(source_files),
        "bundle_entries": len(entries),
        "source_date_epoch": epoch,
    }
    print(
        "AX_RELEASE_CANDIDATE_BUILD_PASS "
        f"sha256={digest} source_files={len(source_files)} bundle_entries={len(entries)}"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic AX-PUB-RC-001 engineering bundle")
    parser.add_argument("--output-dir", default="dist", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    build(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
