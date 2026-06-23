"""Cross-registry validation for capability framework records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_governance.reference_models import REFERENCE_MODEL_BY_SLUG
from open_grace_governance.schemas.capability_framework import CapabilityFrameworkRecord
from open_grace_governance.validation.rules import ValidationResult, validate_reference_models

if TYPE_CHECKING:
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_governance.registries import RiskRegistry, StandardsRegistry
    from open_grace_agent_registry import ModelRegistry

FRAMEWORK_REFERENCE_MODELS = frozenset(
    {"unesco", "gbif", "wikidata", "nist-ai-rmf", "iso-42001"}
)


@dataclass
class CapabilityValidationContext:
    benchmarks: BenchmarkRegistry
    models: ModelRegistry
    standards: StandardsRegistry
    risks: RiskRegistry


def validate_capability_framework(
    record: CapabilityFrameworkRecord,
    context: CapabilityValidationContext | None = None,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    validate_reference_models(record, errors)
    for slug in record.reference_models:
        if slug not in FRAMEWORK_REFERENCE_MODELS:
            warnings.append(f"reference model {slug} outside framework catalog")

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

    if context is None:
        return ValidationResult(valid=not errors, errors=errors, warnings=warnings)

    for benchmark_id in record.benchmark_set:
        if context.benchmarks.get(benchmark_id) is None:
            errors.append(f"unknown benchmark: {benchmark_id}")

    for model_id in record.approved_models:
        model = context.models.get(model_id)
        if model is None:
            errors.append(f"unknown model: {model_id}")
        elif model.lifecycle_stage != LifecycleStage.PUBLICATION:
            errors.append(f"model not published: {model_id}")

    for standard_id in record.required_standards:
        standard = context.standards.get(standard_id)
        if standard is None:
            errors.append(f"unknown standard: {standard_id}")
        elif standard.lifecycle_stage != LifecycleStage.PUBLICATION:
            errors.append(f"standard not published: {standard_id}")

    for risk_id in record.risk_profile:
        risk = context.risks.get(risk_id)
        if risk is None:
            errors.append(f"unknown risk: {risk_id}")
        elif risk.lifecycle_stage != LifecycleStage.PUBLICATION:
            errors.append(f"risk not published: {risk_id}")

    for slug in record.reference_models:
        if slug not in REFERENCE_MODEL_BY_SLUG:
            errors.append(f"unknown reference model slug: {slug}")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)
