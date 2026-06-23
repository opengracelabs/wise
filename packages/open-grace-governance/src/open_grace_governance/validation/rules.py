"""Cross-registry validation rules."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.reference_models import REFERENCE_MODEL_BY_SLUG
from open_grace_governance.schemas import (
    AgentRegistryRecord,
    AuditRegistryRecord,
    BenchmarkRegistryRecord,
    CapabilityFrameworkRecord,
    CapabilityRegistryRecord,
    ModelRegistryRecord,
    RiskRegistryRecord,
    StandardsRegistryRecord,
)


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _require_publication_fields(record: BaseModel, errors: list[str]) -> None:
    stage = getattr(record, "lifecycle_stage", None)
    if stage != LifecycleStage.PUBLICATION:
        return
    steward = getattr(record, "steward_actor", None)
    if not steward:
        errors.append("steward_actor required at publication stage")


def validate_reference_models(record: BaseModel, errors: list[str]) -> None:
    slugs = getattr(record, "reference_models", []) or []
    for slug in slugs:
        if slug not in REFERENCE_MODEL_BY_SLUG:
            errors.append(f"unknown reference model slug: {slug}")


def validate_agent_record(record: AgentRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.plane == "constitutional" and not record.read_only:
        warnings.append("constitutional agents should be read_only")
    if record.read_only and record.service_binding:
        warnings.append("read_only agents typically have no service_binding")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_capability_framework_record(record: CapabilityFrameworkRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if not record.benchmark_set:
        errors.append("benchmark_set must not be empty")
    if not record.approved_models:
        errors.append("approved_models must not be empty")
    if not record.required_standards:
        errors.append("required_standards must not be empty")
    if not record.risk_profile:
        errors.append("risk_profile must not be empty")
    if not record.audit_requirements:
        errors.append("audit_requirements must not be empty")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_capability_record(record: CapabilityRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)
    return ValidationResult(valid=not errors, errors=errors)


def validate_standards_record(record: StandardsRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.reference_model_slug not in REFERENCE_MODEL_BY_SLUG:
        errors.append(f"reference_model_slug not in catalog: {record.reference_model_slug}")

    return ValidationResult(valid=not errors, errors=errors)


_MIT_FRAMEWORKS = frozenset({"mit-ai-risk", "nist-ai-rmf"})


def validate_risk_record(record: RiskRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if not record.agent_id and not record.capability_id:
        errors.append("risk must reference agent_id or capability_id")

    if record.framework in _MIT_FRAMEWORKS and "mit-ai-risk" not in record.reference_models:
        warnings.append("MIT-aligned framework should declare mit-ai-risk reference model")

    if record.lifecycle_stage == LifecycleStage.PUBLICATION:
        if not record.evidence.strip():
            errors.append("evidence required at publication stage")
        if record.framework == "mit-ai-risk" and not record.mitigation.strip():
            errors.append("mit-ai-risk framework requires documented mitigation")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_benchmark_record(record: BenchmarkRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.threshold_min is None and record.threshold_max is None:
        errors.append("benchmark requires at least one threshold")

    return ValidationResult(valid=not errors, errors=errors)


def validate_audit_record(record: AuditRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_reference_models(record, errors)

    if not record.evidence_ref:
        errors.append("audit requires evidence_ref")

    return ValidationResult(valid=not errors, errors=errors)


def validate_model_record(record: ModelRegistryRecord) -> ValidationResult:
    errors: list[str] = []
    validate_reference_models(record, errors)
    _require_publication_fields(record, errors)

    if record.safety_tier == "restricted" and "constitutional" in record.allowed_planes:
        errors.append("restricted models cannot serve constitutional plane")

    return ValidationResult(valid=not errors, errors=errors)


_VALIDATORS = {
  AgentRegistryRecord: validate_agent_record,
  CapabilityRegistryRecord: validate_capability_record,
  CapabilityFrameworkRecord: validate_capability_framework_record,
  StandardsRegistryRecord: validate_standards_record,
  RiskRegistryRecord: validate_risk_record,
  BenchmarkRegistryRecord: validate_benchmark_record,
  AuditRegistryRecord: validate_audit_record,
  ModelRegistryRecord: validate_model_record,
}


def validate_entry(record: BaseModel) -> ValidationResult:
    validator = _VALIDATORS.get(type(record))
    if validator is None:
        return ValidationResult(valid=False, errors=[f"no validator for {type(record).__name__}"])
    return validator(record)
