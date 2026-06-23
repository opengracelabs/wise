"""Capability compliance reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from open_grace_governance.capabilities.benchmarking import (
    CapabilityBenchmarkResult,
    evaluate_capability_benchmarks,
)
from open_grace_governance.capabilities.validation import (
    CapabilityValidationContext,
    validate_capability_framework,
)
from open_grace_governance.schemas.capability_framework import CapabilityFrameworkRecord

if TYPE_CHECKING:
    from open_grace_benchmarking import BenchmarkRegistry
    from open_grace_governance.capabilities.registry import CapabilityFrameworkRegistry
    from open_grace_governance.registries import RiskRegistry, StandardsRegistry
    from open_grace_agent_registry import ModelRegistry

CAPABILITY_REPORT_FILENAME = "capability_compliance_report.json"


@dataclass
class CapabilityComplianceReport:
    capability_id: str
    name: str
    owner: str
    generated_at: str
    validation_passed: bool
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    benchmark_passed: bool | None = None
    benchmark_failures: list[str] = field(default_factory=list)
    linked_agents: list[str] = field(default_factory=list)

    @property
    def compliant(self) -> bool:
        if not self.validation_passed:
            return False
        if self.benchmark_passed is False:
            return False
        return True


def generate_capability_report(
    record: CapabilityFrameworkRecord,
    *,
    context: CapabilityValidationContext,
    benchmark_registry: BenchmarkRegistry,
    observed_values: dict[str, float] | None = None,
    linked_agents: list[str] | None = None,
) -> CapabilityComplianceReport:
    validation = validate_capability_framework(record, context)
    benchmark_passed: bool | None = None
    benchmark_failures: list[str] = []

    if observed_values is not None:
        bench_result = evaluate_capability_benchmarks(
            record, benchmark_registry, observed_values
        )
        benchmark_passed = bench_result.passed
        benchmark_failures = bench_result.failures

    return CapabilityComplianceReport(
        capability_id=record.id,
        name=record.name,
        owner=record.owner,
        generated_at=datetime.now(UTC).isoformat(),
        validation_passed=validation.valid,
        validation_errors=validation.errors,
        validation_warnings=validation.warnings,
        benchmark_passed=benchmark_passed,
        benchmark_failures=benchmark_failures,
        linked_agents=linked_agents or [],
    )


def generate_fleet_capability_reports(
    framework: CapabilityFrameworkRegistry,
    *,
    context: CapabilityValidationContext,
    benchmark_registry: BenchmarkRegistry,
    observed_values_by_capability: dict[str, dict[str, float]] | None = None,
) -> list[CapabilityComplianceReport]:
    reports: list[CapabilityComplianceReport] = []
    observed = observed_values_by_capability or {}
    for record in framework.list():
        reports.append(
            generate_capability_report(
                record,
                context=context,
                benchmark_registry=benchmark_registry,
                observed_values=observed.get(record.id),
                linked_agents=framework.agents_for_capability(record.id),
            )
        )
    return reports


def report_to_dict(report: CapabilityComplianceReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["compliant"] = report.compliant
    return payload


def write_capability_report(
    report: CapabilityComplianceReport,
    output_dir: Path,
    *,
    filename: str = CAPABILITY_REPORT_FILENAME,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    return path
