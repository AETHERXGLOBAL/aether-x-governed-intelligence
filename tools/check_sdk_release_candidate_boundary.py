#!/usr/bin/env python3
"""Fail-closed boundary validation for AX-PUB-DEV-008 / DEV-GATE-05B."""
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
NAMESPACE_ROOT = PACKAGE_ROOT / "src" / "aetherxglobal"
SRC_ROOT = NAMESPACE_ROOT / "governed_intelligence"
ARTIFACT_PATH = ROOT / "artifacts" / "AX-PUB-DEV-008.json"
PARENT_ARTIFACT = ROOT / "artifacts" / "AX-PUB-DEV-007.json"
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
    "aiohttp", "boto3", "botocore", "ftplib", "grpc", "httpx", "paramiko",
    "requests", "smtplib", "socket", "subprocess", "urllib3", "websocket", "websockets",
}

FORBIDDEN_PUBLIC_NAMES = {
    "execute", "authorize", "trade", "invoke_tool", "send", "publish",
    "login", "authenticate", "request",
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
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def git_blob_sha1(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def check_parent_gate() -> None:
    parent = load_json(PARENT_ARTIFACT)
    require(parent.get("artifact_id") == "AX-PUB-DEV-007", "parent Gate-05A artifact ID mismatch")
    phases = parent.get("gate_05_phases")
    require(isinstance(phases, dict), "parent Gate-05 phase state missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "Gate-05B may not proceed before Gate-05A is closed")
    require(phases.get("DEV-GATE-05B") == "ACTIVE_ENGINEERING_OBJECTIVE", "Gate-05B is not the active engineering objective")
    require(parent.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "parent publication boundary changed")
    require(parent.get("release_authorized") is False, "parent release authority must remain false")


def check_artifact() -> dict[str, Any]:
    data = load_json(ARTIFACT_PATH)
    require(data.get("artifact_id") == "AX-PUB-DEV-008", "unexpected package artifact ID")
    require(data.get("version") == "0.1", "unexpected Gate-05B artifact version")
    require(data.get("parent_decision_artifact") == "AX-PUB-DEV-007", "Gate-05B must remain subordinate to AX-PUB-DEV-007")
    require(data.get("parent_phase_state") == "DEV-GATE-05A CLOSED", "Gate-05A closure state mismatch")
    require(data.get("gate") == "DEV-GATE-05" and data.get("phase") == "DEV-GATE-05B", "Gate-05B identity mismatch")
    require(data.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication disposition must remain fail-closed")
    require(data.get("distribution_authorized") is False, "distribution must remain unauthorized")
    require(data.get("license_granted") is False, "candidate must not grant a software licence")
    require(data.get("supported_sdk_established") is False, "candidate must not establish a supported SDK")

    distribution = data.get("distribution")
    require(isinstance(distribution, dict), "distribution state must be an object")
    require(distribution.get("name_candidate") == "aetherxglobal-governed-intelligence", "distribution candidate mismatch")
    require(distribution.get("version_candidate") == "0.1.0rc1", "candidate version mismatch")
    require(distribution.get("import_namespace") == "aetherxglobal.governed_intelligence", "import namespace mismatch")
    require(distribution.get("company_namespace_model") == "PEP_420_IMPLICIT_NAMESPACE", "company namespace must remain PEP 420")
    require(distribution.get("top_level_company_init_allowed") is False, "top-level company __init__ must remain prohibited")
    require(distribution.get("requires_python") == ">=3.11,<3.15", "requires-python mismatch")
    require(distribution.get("runtime_dependencies") == [], "runtime dependency target must remain empty")
    require(distribution.get("public_registry") == "PyPI", "canonical registry mismatch")
    require(distribution.get("staging_registry") == "TestPyPI", "staging registry mismatch")
    require(distribution.get("registry_ownership_established") is False, "registry ownership must not be inferred")
    require(distribution.get("registry_publication_authorized") is False, "registry publication must remain unauthorized")

    build = data.get("build")
    require(isinstance(build, dict), "build state must be an object")
    require(build.get("backend") == "hatchling" and build.get("backend_version") == "1.31.0", "build backend candidate mismatch")
    require(build.get("frontend") == "build" and build.get("frontend_version") == "1.5.0", "build frontend candidate mismatch")
    require(build.get("canonical_source_date_epoch") == 1787076737, "canonical build epoch mismatch")
    for key in (
        "wheel_required", "sdist_required", "double_build_required",
        "byte_identical_rebuild_required", "exact_distribution_testing_required",
        "ci_artifact_evidence_required",
    ):
        require(build.get(key) is True, f"build control {key} must remain required")
    require(build.get("ci_artifact_retention_days") == 7, "CI artifact retention must remain 7 days")
    require(build.get("reproducibility_evidence_established") is False, "candidate must not pre-claim reproducibility evidence")

    require(data.get("runtime_target") == ["3.11", "3.12", "3.13", "3.14"], "runtime target must remain CPython 3.11-3.14")

    scope = data.get("scope")
    require(isinstance(scope, dict), "scope state must be an object")
    require(scope.get("offline_validation_only") is True, "package scope must remain offline validation only")
    for key in (
        "network_allowed", "credentials_allowed", "authentication_allowed",
        "production_authorization_allowed", "tool_invocation_allowed",
        "real_world_execution_allowed", "private_repository_runtime_dependency_allowed",
    ):
        require(scope.get(key) is False, f"{key} must remain false")

    public_api = data.get("public_api")
    require(isinstance(public_api, dict), "public_api state must be an object")
    require(public_api.get("module") == "aetherxglobal.governed_intelligence", "public API module mismatch")
    require(public_api.get("execution_capability_exposed") is False, "execution capability must not be exposed")
    require(public_api.get("network_capability_exposed") is False, "network capability must not be exposed")
    require(public_api.get("supported_contract_ids") == ["AX-PUB-SPEC-002", "AX-PUB-SPEC-003", "AX-PUB-SPEC-004"], "contract inventory mismatch")

    blockers = data.get("hard_blockers_retained")
    require(isinstance(blockers, list), "hard blocker list missing")
    required_blockers = {
        "IP_AND_COPYRIGHT_CLEARANCE",
        "PACKAGE_NAME_LIVE_AVAILABILITY_AND_OWNERSHIP",
        "BRANCH_OR_REPOSITORY_RULESET_PROTECTION",
        "PROTECTED_PYPI_RELEASE_ENVIRONMENT",
        "HUMAN_EXTERNAL_EVALUATION",
        "FINAL_RELEASE_EVIDENCE_PACK",
        "EXPLICIT_RELEASE_AUTHORITY",
    }
    require(required_blockers <= set(blockers), "one or more release hard blockers were removed")
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
    require(build_system.get("requires") == ["hatchling==1.31.0"], "build backend must remain exactly pinned for Gate-05B")

    hatch = data.get("tool", {}).get("hatch", {}) if isinstance(data.get("tool"), dict) else {}
    require(isinstance(hatch, dict), "Hatch configuration missing")


def check_namespace_boundary() -> None:
    require(NAMESPACE_ROOT.is_dir(), "company namespace directory is missing")
    require(not (NAMESPACE_ROOT / "__init__.py").exists(), "PEP 420 company namespace must not contain top-level __init__.py")
    require((SRC_ROOT / "__init__.py").is_file(), "governed_intelligence package __init__.py is missing")


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
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules = [node.module]
            else:
                continue
            for module in modules:
                root = module.split(".", 1)[0]
                require(root not in FORBIDDEN_IMPORT_ROOTS, f"forbidden runtime import {module} in {path.relative_to(ROOT)}")
                require(root in stdlib or root == "aetherxglobal", f"third-party runtime import {module} in {path.relative_to(ROOT)}")


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

    api_text = (SRC_ROOT / "_api.py").read_text(encoding="utf-8")
    require('SDK_VERSION = "0.1.0rc1"' in api_text, "SDK_VERSION must match package candidate metadata")


def check_no_repository_loader() -> None:
    api_text = (SRC_ROOT / "_api.py").read_text(encoding="utf-8")
    require("importlib.util" not in api_text, "release package must not dynamically load repository files")
    require("Path(__file__).resolve().parents" not in api_text, "release package must not derive repository root at runtime")


def main() -> None:
    check_parent_gate()
    artifact = check_artifact()
    check_pyproject()
    check_namespace_boundary()
    check_validator_identity(artifact)
    files = iter_package_python()
    check_import_boundary(files)
    check_public_surface()
    check_no_repository_loader()
    print(
        "AX_SDK_RELEASE_CANDIDATE_BOUNDARY_PASS "
        f"python_files={len(files)} runtime_dependencies=0 validators=3 namespace=PEP420"
    )


if __name__ == "__main__":
    main()
