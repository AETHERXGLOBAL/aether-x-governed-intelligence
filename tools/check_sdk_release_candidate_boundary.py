#!/usr/bin/env python3
"""Fail-closed boundary validation for AX-PUB-DEV-008 / DEV-GATE-05B.

The checker accepts either the published engineering-candidate state or the
AX-PUB-CI-009-backed closed state. Closed state is accepted only when the exact
validated distribution identities and verification evidence are present.
"""
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
EVIDENCE_PATH = ROOT / "evidence" / "AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md"
PYPROJECT = PACKAGE_ROOT / "pyproject.toml"

EXPECTED_WHEEL = "aetherxglobal_governed_intelligence-0.1.0rc1-py3-none-any.whl"
EXPECTED_WHEEL_SHA256 = "bd3c3bfc7306c9b45659e3e0533ea1ac24b065a4c577f08cbe987cc10a4d1fac"
EXPECTED_SDIST = "aetherxglobal_governed_intelligence-0.1.0rc1.tar.gz"
EXPECTED_SDIST_SHA256 = "2736a2d10827bd42cb048c6ceacbffc6d18402028e9db673813a95c474d86b99"
EXPECTED_ACTIONS_ARTIFACT_SHA256 = "9b2e050d59146e2b768cb5f9468b2035c078aa1abbb4e0fd0ac4148e8d58d4a2"

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


def check_parent_gate() -> str:
    parent = load_json(PARENT_ARTIFACT)
    require(parent.get("artifact_id") == "AX-PUB-DEV-007", "parent Gate-05 artifact ID mismatch")
    phases = parent.get("gate_05_phases")
    require(isinstance(phases, dict), "parent Gate-05 phase state missing")
    require(phases.get("DEV-GATE-05A") == "CLOSED", "Gate-05B requires Gate-05A=CLOSED")
    b_state = phases.get("DEV-GATE-05B")
    require(b_state in {"ACTIVE_ENGINEERING_OBJECTIVE", "CLOSED"}, "Gate-05B parent state invalid")
    if b_state == "ACTIVE_ENGINEERING_OBJECTIVE":
        require(phases.get("DEV-GATE-05C") == "NOT_ESTABLISHED", "candidate Gate-05B must not pre-promote Gate-05C")
    else:
        require(phases.get("DEV-GATE-05C") == "ACTIVE_ENGINEERING_OBJECTIVE", "closed Gate-05B must advance Gate-05C")
        require(parent.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "closed Gate-05B parent next phase mismatch")
        package_evidence = parent.get("installable_package_closure_evidence")
        require(isinstance(package_evidence, dict), "closed Gate-05B parent closure evidence missing")
        require(package_evidence.get("id") == "AX-PUB-CI-009", "closed Gate-05B parent must cite AX-PUB-CI-009")
    require(phases.get("DEV-GATE-05D") == "NOT_AUTHORIZED", "Gate-05D must remain unauthorized")
    require(parent.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "parent publication boundary changed")
    require(parent.get("release_authorized") is False, "parent release authority must remain false")
    return b_state


def check_closed_evidence(data: dict[str, Any]) -> None:
    require(data.get("phase_state") == "CLOSED", "closed Gate-05B requires phase_state=CLOSED")
    require(data.get("next_phase") == "DEV-GATE-05C — Distribution & External Validation", "closed Gate-05B next phase mismatch")

    build = data.get("build")
    require(isinstance(build, dict), "build state missing")
    require(build.get("reproducibility_evidence_established") is True, "closed Gate-05B requires reproducibility evidence")

    verification = data.get("verification")
    require(isinstance(verification, dict), "closed Gate-05B verification state missing")
    required_verification = {
        "package_boundary": "VERIFIED",
        "deterministic_double_build": "VERIFIED",
        "wheel_metadata_inventory": "VERIFIED",
        "wheel_install": "VERIFIED",
        "sdist_build": "VERIFIED",
        "sdist_to_wheel_byte_identity": "VERIFIED",
        "installed_package_tests": "VERIFIED",
        "runtime_matrix": "VERIFIED_CPTHON_3_11_TO_3_14",
        "artifact_inventory": "VERIFIED",
        "artifact_digests": "VERIFIED",
        "ci_artifact_retention": "VERIFIED_7_DAYS",
        "inherited_gate_03": "PRESERVED",
        "inherited_gate_04": "PRESERVED",
        "inherited_gate_05a": "PRESERVED",
        "public_manifest": "PRESERVED",
        "publication": "NOT_AUTHORIZED",
    }
    for key, expected in required_verification.items():
        require(verification.get(key) == expected, f"closed Gate-05B verification mismatch for {key}")

    identity = data.get("verified_distribution_identity")
    require(isinstance(identity, dict), "verified distribution identity missing")
    wheel = identity.get("wheel")
    sdist = identity.get("sdist")
    actions = identity.get("actions_artifact")
    require(isinstance(wheel, dict) and isinstance(sdist, dict) and isinstance(actions, dict), "verified distribution identity incomplete")
    require(wheel.get("filename") == EXPECTED_WHEEL, "verified wheel filename mismatch")
    require(wheel.get("sha256") == EXPECTED_WHEEL_SHA256, "verified wheel digest mismatch")
    require(sdist.get("filename") == EXPECTED_SDIST, "verified sdist filename mismatch")
    require(sdist.get("sha256") == EXPECTED_SDIST_SHA256, "verified sdist digest mismatch")
    require(actions.get("id") == 9337474216, "Actions artifact ID mismatch")
    require(actions.get("name") == "ax-pub-dev-008-3267c66681e417bf5eb0f8a384e8c2d992d266c0", "Actions artifact name mismatch")
    require(actions.get("sha256") == EXPECTED_ACTIONS_ARTIFACT_SHA256, "Actions artifact digest mismatch")
    require(actions.get("retention_days") == 7, "Actions artifact retention mismatch")

    closure = data.get("closure_evidence")
    require(isinstance(closure, dict), "closed Gate-05B closure_evidence missing")
    expected_closure = {
        "id": "AX-PUB-CI-009",
        "version": "1.0",
        "path": "evidence/AX-PUB-CI-009_INSTALLABLE_PACKAGE_CANDIDATE_VALIDATION.md",
        "published_baseline_commit": "774abcce340c3fbaf3481ab5244ee1d41b88243c",
        "verification_head_commit": "63477bb11124aebbad4034587a366d5ef882b3c2",
        "verification_merge_commit": "3267c66681e417bf5eb0f8a384e8c2d992d266c0",
        "verification_pr": 36,
        "workflow_run_id": 32171606094,
        "workflow_run_number": 19,
        "job_id": 95823835258,
        "governance_workflow_run_id": 32171606079,
        "governance_workflow_run_number": 168,
        "conclusion": "SUCCESS",
        "source_date_epoch": 1787076737,
    }
    for key, expected in expected_closure.items():
        require(closure.get(key) == expected, f"closed Gate-05B closure evidence mismatch for {key}")
    require(closure.get("verified_runtime_matrix") == ["3.11", "3.12", "3.13", "3.14"], "closed Gate-05B runtime evidence mismatch")

    require(EVIDENCE_PATH.is_file(), "AX-PUB-CI-009 evidence file missing")
    evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
    for token in (
        "AX-PUB-CI-009",
        "774abcce340c3fbaf3481ab5244ee1d41b88243c",
        "63477bb11124aebbad4034587a366d5ef882b3c2",
        "3267c66681e417bf5eb0f8a384e8c2d992d266c0",
        "32171606094",
        "95823835258",
        EXPECTED_WHEEL_SHA256,
        EXPECTED_SDIST_SHA256,
        EXPECTED_ACTIONS_ARTIFACT_SHA256,
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(token in evidence, f"AX-PUB-CI-009 missing token: {token}")


def check_artifact(parent_b_state: str) -> tuple[dict[str, Any], bool]:
    data = load_json(ARTIFACT_PATH)
    require(data.get("artifact_id") == "AX-PUB-DEV-008", "unexpected package artifact ID")
    require(data.get("version") == "0.1", "unexpected Gate-05B artifact version")
    require(data.get("parent_decision_artifact") == "AX-PUB-DEV-007", "Gate-05B must remain subordinate to AX-PUB-DEV-007")
    require(data.get("parent_phase_state") == "DEV-GATE-05A CLOSED", "Gate-05A closure state mismatch")
    require(data.get("gate") == "DEV-GATE-05" and data.get("phase") == "DEV-GATE-05B", "Gate-05B identity mismatch")
    require(data.get("publication_disposition") == "SDK PUBLICATION NOT AUTHORIZED", "publication disposition must remain fail-closed")
    require(data.get("distribution_authorized") is False, "distribution must remain unauthorized")
    require(data.get("license_granted") is False, "Gate-05B must not grant a software licence")
    require(data.get("supported_sdk_established") is False, "Gate-05B must not establish a supported SDK")

    closed = data.get("phase_state") == "CLOSED"
    if parent_b_state == "CLOSED":
        require(closed, "parent closes Gate-05B but DEV-008 is not closed")
        check_closed_evidence(data)
    else:
        require(not closed, "DEV-008 may not close before parent Gate-05 state advances")
        build_candidate = data.get("build")
        require(isinstance(build_candidate, dict), "candidate build state missing")
        require(build_candidate.get("reproducibility_evidence_established") is False, "candidate must not pre-claim reproducibility evidence")

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
    return data, closed


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
    parent_b_state = check_parent_gate()
    artifact, closed = check_artifact(parent_b_state)
    check_pyproject()
    check_namespace_boundary()
    check_validator_identity(artifact)
    files = iter_package_python()
    check_import_boundary(files)
    check_public_surface()
    check_no_repository_loader()
    marker = "AX_SDK_RELEASE_CANDIDATE_CLOSED_STATE_PASS" if closed else "AX_SDK_RELEASE_CANDIDATE_BOUNDARY_PASS"
    print(f"{marker} python_files={len(files)} runtime_dependencies=0 validators=3 namespace=PEP420")


if __name__ == "__main__":
    main()
