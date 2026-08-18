#!/usr/bin/env python3
"""AETHER X public SDK candidate facade — DEV-GATE-02 candidate.

Repository-local, non-distributable candidate surface over the three declared
public reference contract paths. This module is not an authorized package,
production API, execution runtime, or supported SDK.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Mapping

ROOT = Path(__file__).resolve().parents[2]
SDK_CANDIDATE_VERSION = "0.1.0-candidate"


class ErrorCategory(str, Enum):
    CONTRACT_INVALID = "AXDEV-CONTRACT-INVALID"
    VERSION_UNSUPPORTED = "AXDEV-VERSION-UNSUPPORTED"
    EVIDENCE_INSUFFICIENT = "AXDEV-EVIDENCE-INSUFFICIENT"
    AUTHORITY_UNESTABLISHED = "AXDEV-AUTHORITY-UNESTABLISHED"
    AUTHORITY_INACTIVE = "AXDEV-AUTHORITY-INACTIVE"
    AUTHORITY_SCOPE_VIOLATION = "AXDEV-AUTHORITY-SCOPE-VIOLATION"
    TEMPORAL_CUTOFF_VIOLATION = "AXDEV-TEMPORAL-CUTOFF-VIOLATION"
    PROVENANCE_INCOMPLETE = "AXDEV-PROVENANCE-INCOMPLETE"
    CONFLICT_UNRESOLVED = "AXDEV-CONFLICT-UNRESOLVED"
    VERIFICATION_FAILED = "AXDEV-VERIFICATION-FAILED"
    VERIFICATION_INCONCLUSIVE = "AXDEV-VERIFICATION-INCONCLUSIVE"
    EXECUTION_NOT_VERIFIED = "AXDEV-EXECUTION-NOT-VERIFIED"
    UNSUPPORTED_OPERATION = "AXDEV-UNSUPPORTED-OPERATION"


@dataclass(frozen=True)
class CandidateFinding:
    category: ErrorCategory
    source_code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        data = asdict(self)
        data["category"] = self.category.value
        return data


@dataclass(frozen=True)
class ValidationResult:
    contract_id: str
    contract_version: str
    reference_validator_id: str | None
    valid: bool
    findings: tuple[CandidateFinding, ...]
    candidate_version: str = SDK_CANDIDATE_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_version": self.candidate_version,
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "reference_validator_id": self.reference_validator_id,
            "valid": self.valid,
            "findings": [finding.as_dict() for finding in self.findings],
            "claim_boundary": "SDK CANDIDATE RESULT DOES NOT ESTABLISH PRODUCTION AUTHORITY OR PRODUCT IMPLEMENTATION",
        }


@dataclass(frozen=True)
class _ContractDescriptor:
    contract_id: str
    version: str
    schema_id: str
    reference_validator_id: str
    module_path: str
    validator_function: str


_CONTRACTS: dict[str, _ContractDescriptor] = {
    "AX-PUB-SPEC-002": _ContractDescriptor(
        contract_id="AX-PUB-SPEC-002",
        version="1.0",
        schema_id="AX-PUB-SCHEMA-001",
        reference_validator_id="AX-PUB-REF-001",
        module_path="reference-implementations/eav-contract-validator/validator.py",
        validator_function="validate_bundle",
    ),
    "AX-PUB-SPEC-003": _ContractDescriptor(
        contract_id="AX-PUB-SPEC-003",
        version="1.0",
        schema_id="AX-PUB-SCHEMA-002",
        reference_validator_id="AX-PUB-REF-002",
        module_path="reference-implementations/point-in-time-knowledge-validator/validator.py",
        validator_function="validate_envelope",
    ),
    "AX-PUB-SPEC-004": _ContractDescriptor(
        contract_id="AX-PUB-SPEC-004",
        version="1.0",
        schema_id="AX-PUB-SCHEMA-003",
        reference_validator_id="AX-PUB-REF-003",
        module_path="reference-implementations/agent-tool-authority-validator/validator.py",
        validator_function="validate_envelope",
    ),
}

_AUTHORITY_UNESTABLISHED = {
    "AX-EAV-EXEC-AUTHORITY",
    "AX-AGT-GRANT-CONTEXT",
    "AX-AGT-INVOKE-GRANT",
}

_AUTHORITY_INACTIVE = {
    "AX-EAV-EXEC-AUTHORITY-INACTIVE",
    "AX-EAV-EXEC-AFTER-EXPIRY",
    "AX-EAV-EXEC-BEFORE-GRANT",
    "AX-AGT-INVOKE-AUTHORITY-INACTIVE",
    "AX-AGT-INVOKE-BEFORE-GRANT",
    "AX-AGT-INVOKE-AFTER-GRANT",
}

_AUTHORITY_SCOPE = {
    "AX-EAV-EXEC-DECISION-MISMATCH",
    "AX-EAV-EXEC-PRINCIPAL",
    "AX-EAV-EXEC-ACTION",
    "AX-EAV-EXEC-SCOPE",
    "AX-AGT-GRANT-PRINCIPAL-MISMATCH",
    "AX-AGT-GRANT-CONTEXT-PRINCIPAL",
    "AX-AGT-GRANT-TOOL-MISMATCH",
    "AX-AGT-GRANT-ACTION-MISMATCH",
    "AX-AGT-GRANT-TOOL-SCOPE",
    "AX-AGT-GRANT-ACTION-SCOPE",
    "AX-AGT-GRANT-RESOURCE-SCOPE",
    "AX-AGT-GRANT-PARAM-SCOPE",
    "AX-AGT-GRANT-PROPOSAL-RESOURCE",
    "AX-AGT-INVOKE-PRINCIPAL",
    "AX-AGT-INVOKE-TOOL",
    "AX-AGT-INVOKE-ACTION",
    "AX-AGT-INVOKE-RESOURCE",
    "AX-AGT-PARAM-REQUIRED",
    "AX-AGT-PARAM-ALLOWED-VALUES",
    "AX-AGT-PARAM-MINIMUM",
    "AX-AGT-PARAM-MAXIMUM",
    "AX-AGT-GRANT-INVOCATION-LIMIT",
    "AX-AGT-GRANT-SINGLE-USE",
}

_PROVENANCE_INCOMPLETE = {
    "AX-PTK-SOURCE-REFERENCE",
    "AX-PTK-SUPERSEDES-REFERENCE",
    "AX-PTK-SUPERSEDED-BY-REFERENCE",
    "AX-PTK-TRANSFORMATION-INPUT-REF",
    "AX-PTK-TRANSFORMATION-OUTPUT-REF",
    "AX-PTK-TRANSFORMATION-REFERENCE",
}

_EXECUTION_NOT_VERIFIED = {
    "AX-EAV-OUTCOME-NOT-PASSED",
    "AX-EAV-OUTCOME-VERIFICATION",
}


@lru_cache(maxsize=None)
def _load_validator(descriptor: _ContractDescriptor) -> Callable[[dict[str, Any]], list[Any]]:
    path = ROOT / descriptor.module_path
    module_name = f"ax_sdk_candidate_{descriptor.reference_validator_id.lower().replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load public reference validator: {descriptor.reference_validator_id}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    validator = getattr(module, descriptor.validator_function, None)
    if not callable(validator):
        raise RuntimeError(f"public reference validator entrypoint missing: {descriptor.reference_validator_id}")
    return validator


def _category_for_source_code(code: str) -> ErrorCategory:
    if code in _AUTHORITY_UNESTABLISHED:
        return ErrorCategory.AUTHORITY_UNESTABLISHED
    if code in _AUTHORITY_INACTIVE:
        return ErrorCategory.AUTHORITY_INACTIVE
    if code in _AUTHORITY_SCOPE:
        return ErrorCategory.AUTHORITY_SCOPE_VIOLATION
    if code.startswith("AX-PTK-FUTURE-") or code == "AX-PTK-REPRODUCIBILITY-CUTOFF":
        return ErrorCategory.TEMPORAL_CUTOFF_VIOLATION
    if code in _PROVENANCE_INCOMPLETE:
        return ErrorCategory.PROVENANCE_INCOMPLETE
    if code in _EXECUTION_NOT_VERIFIED:
        return ErrorCategory.EXECUTION_NOT_VERIFIED
    return ErrorCategory.CONTRACT_INVALID


def _unsupported_result(contract_id: str, version: str, category: ErrorCategory, code: str, message: str) -> ValidationResult:
    return ValidationResult(
        contract_id=contract_id,
        contract_version=version,
        reference_validator_id=None,
        valid=False,
        findings=(CandidateFinding(category=category, source_code=code, path="$", message=message),),
    )


def supported_contracts() -> tuple[Mapping[str, str], ...]:
    """Return the bounded candidate contract inventory without implying package support."""
    return tuple(
        {
            "contract_id": item.contract_id,
            "contract_version": item.version,
            "schema_id": item.schema_id,
            "reference_validator_id": item.reference_validator_id,
        }
        for item in _CONTRACTS.values()
    )


def validate(contract_id: str, payload: Any, *, version: str = "1.0") -> ValidationResult:
    """Validate one declared public contract through the bounded candidate facade.

    Validation findings are returned as data. This function performs no network,
    tool, credential, product, brokerage, or real-world execution.
    """
    descriptor = _CONTRACTS.get(contract_id)
    if descriptor is None:
        return _unsupported_result(
            contract_id,
            version,
            ErrorCategory.UNSUPPORTED_OPERATION,
            "AX-SDK-CANDIDATE-CONTRACT-UNSUPPORTED",
            "contract is outside the declared DEV-GATE-02 candidate surface",
        )
    if version != descriptor.version:
        return _unsupported_result(
            contract_id,
            version,
            ErrorCategory.VERSION_UNSUPPORTED,
            "AX-SDK-CANDIDATE-VERSION-UNSUPPORTED",
            f"supported candidate contract version is {descriptor.version}",
        )

    validator = _load_validator(descriptor)
    source_findings = validator(payload)
    findings = tuple(
        CandidateFinding(
            category=_category_for_source_code(str(finding.code)),
            source_code=str(finding.code),
            path=str(finding.path),
            message=str(finding.message),
        )
        for finding in source_findings
    )
    return ValidationResult(
        contract_id=descriptor.contract_id,
        contract_version=descriptor.version,
        reference_validator_id=descriptor.reference_validator_id,
        valid=not findings,
        findings=findings,
    )


def validate_eav(payload: Any, *, version: str = "1.0") -> ValidationResult:
    return validate("AX-PUB-SPEC-002", payload, version=version)


def validate_point_in_time(payload: Any, *, version: str = "1.0") -> ValidationResult:
    return validate("AX-PUB-SPEC-003", payload, version=version)


def validate_agent_authority(payload: Any, *, version: str = "1.0") -> ValidationResult:
    return validate("AX-PUB-SPEC-004", payload, version=version)


__all__ = [
    "SDK_CANDIDATE_VERSION",
    "ErrorCategory",
    "CandidateFinding",
    "ValidationResult",
    "supported_contracts",
    "validate",
    "validate_eav",
    "validate_point_in_time",
    "validate_agent_authority",
]
