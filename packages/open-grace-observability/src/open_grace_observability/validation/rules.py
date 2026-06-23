"""Cross-registry validation for observability metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from open_grace_governance.validation.rules import ValidationResult
from open_grace_observability.reference_models import OBSERVABILITY_REFERENCE_MODEL_BY_SLUG
from open_grace_observability.schemas import (
    AgentExecutionMetric,
    AuditMetric,
    BenchmarkMetric,
    CapabilityMetric,
    CostMetric,
)

if TYPE_CHECKING:
    from open_grace_agent_registry import AgentRegistry, CapabilityRegistry
    from open_grace_audit import AuditRegistry
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_observability.registries.system import ObservabilitySystem


def validate_observability_reference_models(record, errors: list[str]) -> None:
    slugs = getattr(record, "reference_models", []) or []
    for slug in slugs:
        if slug not in OBSERVABILITY_REFERENCE_MODEL_BY_SLUG:
            errors.append(f"unknown observability reference model slug: {slug}")


def validate_agent_metric(record: AgentExecutionMetric) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_observability_reference_models(record, errors)

    if record.metric_kind == "success" and record.unit != "ratio" and record.value > 1:
        warnings.append("success metric value > 1 with non-ratio unit")

    if record.trace_id and "opentelemetry" not in record.reference_models:
        warnings.append("trace_id set without opentelemetry reference model")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_capability_metric(record: CapabilityMetric) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_observability_reference_models(record, errors)
    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_benchmark_metric(record: BenchmarkMetric) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_observability_reference_models(record, errors)

    if record.passed is False and record.metric_kind == "observed":
        warnings.append("benchmark observation marked as not passed")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_audit_metric(record: AuditMetric) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_observability_reference_models(record, errors)
    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def validate_cost_metric(record: CostMetric) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    validate_observability_reference_models(record, errors)

    if record.token_count is None and record.cost_kind == "inference":
        warnings.append("inference cost without token_count")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


_VALIDATORS = {
    AgentExecutionMetric: validate_agent_metric,
    CapabilityMetric: validate_capability_metric,
    BenchmarkMetric: validate_benchmark_metric,
    AuditMetric: validate_audit_metric,
    CostMetric: validate_cost_metric,
}


def validate_metric_entry(record) -> ValidationResult:
    validator = _VALIDATORS.get(type(record))
    if validator is None:
        return ValidationResult(
            valid=False,
            errors=[f"no metric validator for {type(record).__name__}"],
        )
    return validator(record)


@dataclass
class MetricValidationContext:
    observability: ObservabilitySystem
    agents: AgentRegistry | None = None
    capabilities: CapabilityRegistry | None = None
    benchmarks: BenchmarkRegistry | None = None
    audits: AuditRegistry | None = None


def validate_metric_cross_registry(
    record,
    context: MetricValidationContext | None = None,
) -> ValidationResult:
    base = validate_metric_entry(record)
    if context is None:
        return base

    errors = list(base.errors)
    warnings = list(base.warnings)

    if isinstance(record, AgentExecutionMetric):
        if context.agents and context.agents.get(record.agent_id) is None:
            errors.append(f"unknown agent_id: {record.agent_id}")

    if isinstance(record, CapabilityMetric):
        if context.capabilities and context.capabilities.get(record.capability_id) is None:
            errors.append(f"unknown capability_id: {record.capability_id}")
        if record.agent_id and context.agents and context.agents.get(record.agent_id) is None:
            errors.append(f"unknown agent_id: {record.agent_id}")

    if isinstance(record, BenchmarkMetric):
        if context.benchmarks and context.benchmarks.get(record.benchmark_id) is None:
            errors.append(f"unknown benchmark_id: {record.benchmark_id}")
        if record.agent_id and context.agents and context.agents.get(record.agent_id) is None:
            errors.append(f"unknown agent_id: {record.agent_id}")

    if isinstance(record, AuditMetric):
        if record.audit_id and context.audits and context.audits.get(record.audit_id) is None:
            errors.append(f"unknown audit_id: {record.audit_id}")
        if record.subject_type == "agent" and context.agents:
            if context.agents.get(record.subject_id) is None:
                errors.append(f"unknown subject agent: {record.subject_id}")
        if record.subject_type == "capability" and context.capabilities:
            if context.capabilities.get(record.subject_id) is None:
                errors.append(f"unknown subject capability: {record.subject_id}")
        if record.subject_type == "benchmark" and context.benchmarks:
            if context.benchmarks.get(record.subject_id) is None:
                errors.append(f"unknown subject benchmark: {record.subject_id}")

    if isinstance(record, CostMetric):
        if record.agent_id and context.agents and context.agents.get(record.agent_id) is None:
            errors.append(f"unknown agent_id: {record.agent_id}")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)
