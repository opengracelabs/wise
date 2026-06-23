"""Observability compliance reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from open_grace_observability.validation import MetricValidationContext, validate_metric_cross_registry

if TYPE_CHECKING:
    from open_grace_observability.registries.system import ObservabilitySystem
    from open_grace_observability.schemas import (
        AgentExecutionMetric,
        AuditMetric,
        BenchmarkMetric,
        CapabilityMetric,
        CostMetric,
    )

OBSERVABILITY_REPORT_FILENAME = "observability_compliance_report.json"


@dataclass
class ObservabilityComplianceReport:
    metric_id: str
    domain: str
    display_name: str
    generated_at: str
    validation_passed: bool
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    reference_models: list[str] = field(default_factory=list)
    trace_id: str | None = None

    @property
    def compliant(self) -> bool:
        return self.validation_passed


def _domain(record) -> str:
    metric_id = getattr(record, "metric_id", "")
    parts = metric_id.split(".")
    return parts[2] if len(parts) >= 3 else "unknown"


def _trace_id(record) -> str | None:
    return getattr(record, "trace_id", None)


def generate_observability_report(
    record: (
        AgentExecutionMetric
        | CapabilityMetric
        | BenchmarkMetric
        | AuditMetric
        | CostMetric
    ),
    *,
    context: MetricValidationContext | None = None,
) -> ObservabilityComplianceReport:
    validation = validate_metric_cross_registry(record, context)
    return ObservabilityComplianceReport(
        metric_id=record.metric_id,
        domain=_domain(record),
        display_name=record.display_name,
        generated_at=datetime.now(UTC).isoformat(),
        validation_passed=validation.valid,
        validation_errors=validation.errors,
        validation_warnings=validation.warnings,
        reference_models=list(getattr(record, "reference_models", [])),
        trace_id=_trace_id(record),
    )


def generate_fleet_observability_reports(
    observability: ObservabilitySystem,
    *,
    context: MetricValidationContext | None = None,
) -> list[ObservabilityComplianceReport]:
    reports: list[ObservabilityComplianceReport] = []
    for registry in (
        observability.agent_metrics,
        observability.capability_metrics,
        observability.benchmark_metrics,
        observability.audit_metrics,
        observability.cost_metrics,
    ):
        for record in registry.list():
            reports.append(generate_observability_report(record, context=context))
    return reports


def report_to_dict(report: ObservabilityComplianceReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["compliant"] = report.compliant
    return payload


def write_observability_report(
    report: ObservabilityComplianceReport,
    output_dir: Path,
    *,
    filename: str = OBSERVABILITY_REPORT_FILENAME,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    return path
