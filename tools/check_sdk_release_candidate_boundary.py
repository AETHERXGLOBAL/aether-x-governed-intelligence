#!/usr/bin/env python3
"""Fail-closed package-boundary validation for AX-PUB-DEV-008 / Gate-05B."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "sdk-release-candidate" / "python"
SRC_ROOT = PACKAGE_ROOT / "src" / "aetherxglobal" / "governed_intelligence"
ARTIFACT_PATH = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
PYPROJECT = PACKAGE_ROOT / "pyproject.toml"

VALIDATOR_PAIRS = {
    "AX-PUB-REF-001": (
        ROOT / "reference-implementations" / "eav-contract-validator" / "validator.py",
        SRC_ROOT / "_validators" / "eav.py",
    ),
    "AX-PUB-REF-002": (
        ROOT / "reference-implementations" / "point-in-time-knowledge-validator" / "validator.py",
        SRC_ROOT / "_validators" / "point_in_time.py",
    ),
    "AX-PUB-REF-003": (
        ROOT / "reference-implementations" / "agent-tool-authority-validator" / "validator.py",
        SRC_ROOT / "_validators" / "agent_authority.py",
    ),
}

FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "boto3",
    "botocore",
    "ftplib",
    "grpc",
    "httpx",
    "paramiko",
    "requests",
    "smtplib",
    "socket",
    "subprocess",
    "urllib3",
    "websocket",
    "websockets",
}

FORBIDDEN_PUBLIC_NAMES = {
    "execute",
    "authorize",
    "trade",
    "invoke_tool",
    "send",
    "publish",
    "login",
    "authenticate",
    "request",
}

PRIVATE_MARKERS = {
    "aether-x-quantum",
    "aether-x-governance",
    "aether-x-research",
    "aether-intelligence-core",
    "AETHER X Quantum",
    "AX-OS",
}


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_RELEASE_CANDIDATE_BOUNDARY_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path}: {exc}")
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def git_blob_sha1(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def check_artifact() -> dict[str, Any]:
    data = load_json(ARTIFACT_PATH)
    require(data.get("artifact_id") == "AX-PUB-DEV-008", "unexpected package artifact ID")
    require(data.get("parent_decision_artifact") == "AX-PUB-DEV-007", "Gate-05B must remain subordinate to AX-PUB-DEV-007")
    require(data.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication disposition must remain fail-closed")
    require(data.get("distribution_authorized") is False, "distribution must remain unauthorized")
    require(data.get("license_granted") is False, "candidate must not grant a software licence")

    distribution = data.get("distribution", {})
    require(isinstance(distribution, dict), "distribution state must be an object")
    require(distribution.get("name_candidate") == "aetherxglobal-governed-intelligence", "distribution candidate mismatch")
    require(distribution.get("version_candidate") == "0.1.0rc1", "candidate version mismatch")
    require(distribution.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(distribution.get("requires_python") == ">=3.11,<3.15", "requires-python mismatch")
    require(distribution.get("runtime_dependencies") == [], "runtime dependency target must remain empty")
    require(distribution.get("registry_ownership_established") is False, "registry ownership must not be inferred")

    scope = data.get("scope", {})
    require(isinstance(scope, dict), "scope state must be an object")
    require(scope.get("offline_validation_only") is True, "package scope must remain offline validation only")
    for key in (
        "network_allowed",
        "credentials_allowed",
        "authentication_allowed",
        "production_authorization_allowed",
        "tool_invocation_allowed",
        "real_world_execution_allowed",
        "private_repository_runtime_dependency_allowed",
    ):
        require(scope.get(key) is False, f"{key} must remain false")

    require(data.get("runtime_target") == ["3.11", "3.12", "3.13", "3.14"], "runtime target must remain 3.11-3.14")
    return data


def check_pyproject() -> None:
    try:
        data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        fail(f"cannot parse pyproject.toml: {exc}")

    project = data.get("project")
    require(isinstance(project, dict), "pyproject [project] is missing")
    require(project.get("name") == "aetherxglobal-governed-intelligence", "pyproject project name mismatch")
    require(project.get("version") == "0.1.0rc1", "pyproject version mismatch")
    require(project.get("requires-python") == ">=3.11,<3.15", "pyproject requires-python mismatch")
    require(project.get("dependencies") == [], "pyproject must declare zero runtime dependencies")
    require("license" not in project and "license-files" not in project, "licence metadata must not be attached before IP clearance")

    build_system = data.get("build-system")
    require(isinstance(build_system, dict), "pyproject [build-system] is missing")
    require(build_system.get("build-backend") == "hatchling.build", "unexpected build backend")


def check_validator_identity(artifact: dict[str, Any]) -> None:
    expected = artifact.get("validator_source_identity")
    require(isinstance(expected, dict), "validator source identity map is missing")

    for artifact_id, (reference, packaged) in VALIDATOR_PAIRS.items():
        require(reference.is_file(), f"missing reference validator for {artifact_id}")
        require(packaged.is_file(), f"missing packaged validator for {artifact_id}")
        reference_bytes = reference.read_bytes()
        packaged_bytes = packaged.read_bytes()
        require(reference_bytes == packaged_bytes, f"packaged validator drift detected for {artifact_id}")
        digest = git_blob_sha1(packaged_bytes)
        require(digest == expected.get(artifact_id), f"Git blob identity mismatch for {artifact_id}: {digest}")


def iter_package_python() -> list[Path]:
    files = sorted(SRC_ROOT.rglob("*.py"))
    require(files, "package contains no Python source")
    return files


def check_import_boundary(files: list[Path]) -> None:
    stdlib = set(sys.stdlib_module_names)
    for path in files:
        text = path.read_text(encoding="utf-8")
        for marker in PRIVATE_MARKERS:
            require(marker not in text, f"private-project marker {marker!r} found in {path.relative_to(ROOT)}")

        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            fail(f"syntax error in {path.relative_to(ROOT)}: {exc}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    require(root not in FORBIDDEN_IMPORT_ROOTS, f"forbidden runtime import {alias.name} in {path.relative_to(ROOT)}")
                    require(root in stdlib or root == "aetherxglobal", f"third-party runtime import {alias.name} in {path.relative_to(ROOT)}")
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    continue
                if node.module:
                    root = node.module.split(".", 1)[0]
                    require(root not in FORBIDDEN_IMPORT_ROOTS, f"forbidden runtime import {node.module} in {path.relative_to(ROOT)}")
                    require(root in stdlib or root == "aetherxglobal", f"third-party runtime import {node.module} in {path.relative_to(ROOT)}")


def check_public_surface() -> None:
    init_file = SRC_ROOT / "__init__.py"
    text = init_file.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(init_file))
    exported: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__" and isinstance(node.value, (ast.List, ast.Tuple)):
                    for item in node.value.elts:
                        if isinstance(item, ast.Constant) and isinstance(item.value, str):
                            exported.add(item.value)
    require(exported, "public __all__ is missing")
    require(FORBIDDEN_PUBLIC_NAMES.isdisjoint(exported), "execution/network capability leaked into public API")


def check_no_repository_loader() -> None:
    api_text = (SRC_ROOT / "_api.py").read_text(encoding="utf-8")
    require("importlib.util" not in api_text, "release package must not dynamically load repository files")
    require("Path(__file__).resolve().parents" not in api_text, "release package must not derive repository root at runtime")


def main() -> None:
    artifact = check_artifact()
    check_pyproject()
    check_validator_identity(artifact)
    files = iter_package_python()
    check_import_boundary(files)
    check_public_surface()
    check_no_repository_loader()
    print(f"AX_SDK_RELEASE_CANDIDATE_BOUNDARY_PASS python_files={len(files)} runtime_dependencies=0 validators=3")


if __name__ == "__main__":
    main()
