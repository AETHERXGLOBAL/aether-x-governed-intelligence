#!/usr/bin/env python3
"""Fail-closed validator for AX-PUB-API-001 Python SDK public API contract candidate."""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "sdk-release-candidate" / "python"
SRC = SDK_ROOT / "src"
PYPROJECT = SDK_ROOT / "pyproject.toml"
CONTRACT = ROOT / "artifacts" / "AX-PUB-API-001.json"
DOC = ROOT / "docs" / "AX-PUB-API-001_PYTHON_SDK_PUBLIC_API_CONTRACT.md"


def fail(message: str) -> None:
    raise SystemExit(f"AX_SDK_PUBLIC_API_CONTRACT_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def parameter_contract(fn: Any) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    signature = inspect.signature(fn)
    for parameter in signature.parameters.values():
        item: dict[str, Any] = {
            "name": parameter.name,
            "kind": parameter.kind.name,
            "required": parameter.default is inspect.Parameter.empty,
        }
        if parameter.default is not inspect.Parameter.empty:
            item["default"] = parameter.default
        result.append(item)
    return result


def main() -> int:
    contract = load_json(CONTRACT)
    require(contract.get("artifact_id") == "AX-PUB-API-001", "artifact identity mismatch")
    require(contract.get("version") == "0.1", "contract version mismatch")
    require(contract.get("state") == "DEV_GATE_05C_API_CONTRACT_CANDIDATE", "contract state mismatch")
    require(contract.get("support_commitment_established") is False, "support commitment must remain false")
    require(contract.get("stable_api_guarantee_established") is False, "stable API guarantee must remain false")
    require(contract.get("sdk_publication_authorized") is False, "SDK publication must remain unauthorized")

    require(PYPROJECT.is_file(), "candidate pyproject missing")
    with PYPROJECT.open("rb") as handle:
        pyproject = tomllib.load(handle)
    project = pyproject.get("project")
    require(isinstance(project, dict), "pyproject [project] missing")
    require(project.get("name") == contract.get("sdk_distribution_candidate"), "distribution name mismatch")
    require(project.get("version") == contract.get("sdk_version_candidate"), "candidate version mismatch")
    require(project.get("requires-python") == contract.get("requires_python"), "Requires-Python mismatch")
    require(project.get("dependencies") == [], "candidate must preserve zero runtime dependencies")

    sys.path.insert(0, str(SRC))
    try:
        sdk = importlib.import_module("aetherxglobal.governed_intelligence")
    finally:
        try:
            sys.path.remove(str(SRC))
        except ValueError:
            pass

    require(sdk.__name__ == contract.get("import_namespace"), "import namespace mismatch")
    require(sdk.__version__ == contract.get("sdk_version_candidate"), "__version__ mismatch")
    require(sdk.SDK_VERSION == contract.get("sdk_version_candidate"), "SDK_VERSION mismatch")

    expected_exports = contract.get("public_exports")
    require(isinstance(expected_exports, list), "public_exports must be an array")
    require(list(sdk.__all__) == expected_exports, "exact top-level public export inventory changed")
    for name in expected_exports:
        require(hasattr(sdk, name), f"declared public export missing: {name}")

    callable_contracts = contract.get("callable_contracts")
    require(isinstance(callable_contracts, dict), "callable_contracts missing")
    for name, spec in callable_contracts.items():
        require(hasattr(sdk, name), f"public callable missing: {name}")
        fn = getattr(sdk, name)
        require(callable(fn), f"declared callable is not callable: {name}")
        require(isinstance(spec, dict), f"callable contract must be object: {name}")
        require(parameter_contract(fn) == spec.get("parameters"), f"parameter contract changed: {name}")

    public_types = contract.get("public_types")
    require(isinstance(public_types, dict), "public_types missing")

    for type_name in ("Finding", "ValidationResult"):
        spec = public_types.get(type_name)
        require(isinstance(spec, dict), f"type contract missing: {type_name}")
        cls = getattr(sdk, type_name)
        require(dataclasses.is_dataclass(cls), f"{type_name} must remain a dataclass")
        params = getattr(cls, "__dataclass_params__", None)
        require(params is not None and params.frozen is True, f"{type_name} must remain frozen")
        actual_fields = [field.name for field in dataclasses.fields(cls)]
        require(actual_fields == spec.get("fields"), f"{type_name} field inventory/order changed")
        for method in spec.get("methods", []):
            require(callable(getattr(cls, method, None)), f"{type_name}.{method} missing")

    error_spec = public_types.get("ErrorCategory")
    require(isinstance(error_spec, dict), "ErrorCategory contract missing")
    actual_error_values = [item.value for item in sdk.ErrorCategory]
    require(actual_error_values == error_spec.get("values"), "ErrorCategory value inventory/order changed")
    require(all(isinstance(item.value, str) for item in sdk.ErrorCategory), "ErrorCategory values must remain strings")

    inventory = [dict(item) for item in sdk.supported_contracts()]
    require(inventory == contract.get("supported_contract_inventory"), "supported contract inventory changed")

    unsupported_contract = sdk.validate("AX-PUB-SPEC-999", {}, version="1.0")
    require(unsupported_contract.valid is False, "unsupported contract must fail closed")
    require(len(unsupported_contract.findings) == 1, "unsupported contract must return one explicit finding")
    require(
        unsupported_contract.findings[0].category == sdk.ErrorCategory.UNSUPPORTED_OPERATION,
        "unsupported contract category changed",
    )
    require(
        unsupported_contract.findings[0].source_code == "AX-SDK-RC-CONTRACT-UNSUPPORTED",
        "unsupported contract source code changed",
    )

    unsupported_version = sdk.validate("AX-PUB-SPEC-002", {}, version="999.0")
    require(unsupported_version.valid is False, "unsupported version must fail closed")
    require(len(unsupported_version.findings) == 1, "unsupported version must return one explicit finding")
    require(
        unsupported_version.findings[0].category == sdk.ErrorCategory.VERSION_UNSUPPORTED,
        "unsupported version category changed",
    )
    require(
        unsupported_version.findings[0].source_code == "AX-SDK-RC-VERSION-UNSUPPORTED",
        "unsupported version source code changed",
    )

    first = unsupported_contract.as_dict()
    second = sdk.validate("AX-PUB-SPEC-999", {}, version="1.0").as_dict()
    require(first == second, "identical candidate validation must remain deterministic")

    forbidden_exports = {
        "execute",
        "authorize",
        "invoke_tool",
        "trade",
        "send",
        "publish",
        "login",
        "authenticate",
        "request",
        "client",
        "session",
    }
    require(forbidden_exports.isdisjoint(set(sdk.__all__)), "execution/network capability leaked into public exports")

    require(DOC.is_file(), "public API contract document missing")
    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "AX-PUB-API-001",
        "DEV-GATE-05C API CONTRACT CANDIDATE",
        "Requires-Python: >=3.11,<3.15",
        "AXDEV-UNSUPPORTED-OPERATION",
        "STABLE 1.0 GUARANTEE",
        "SDK PUBLICATION NOT AUTHORIZED",
    ):
        require(marker in doc, f"API contract document missing marker: {marker}")

    runtime = f"{sys.version_info.major}.{sys.version_info.minor}"
    require(runtime in contract.get("verified_runtime_target", []), f"runtime {runtime} outside declared target matrix")

    print(
        "AX_SDK_PUBLIC_API_CONTRACT_PASS "
        f"runtime={runtime} exports={len(expected_exports)} contracts={len(inventory)} "
        "support=NOT_ESTABLISHED publication=NOT_AUTHORIZED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
