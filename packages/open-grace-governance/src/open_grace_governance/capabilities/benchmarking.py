"""Capability-level benchmark evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from open_grace_governance.schemas.capability_framework import CapabilityFrameworkRecord

if TYPE_CHECKING:
    from open_grace_benchmarking import BenchmarkRegistry, BenchmarkEvaluation


@dataclass
class CapabilityBenchmarkResult:
    capability_id: str
    capability_name: str
    passed: bool
    evaluations: list[BenchmarkEvaluation] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)


def evaluate_capability_benchmarks(
    record: CapabilityFrameworkRecord,
    benchmark_registry: BenchmarkRegistry,
    observed_values: dict[str, float],
) -> CapabilityBenchmarkResult:
    from open_grace_benchmarking import evaluate_benchmark

    evaluations: list[BenchmarkEvaluation] = []
    failures: list[str] = []

    for benchmark_id in record.benchmark_set:
        bench = benchmark_registry.get(benchmark_id)
        if bench is None:
            failures.append(f"missing benchmark definition: {benchmark_id}")
            continue
        if benchmark_id not in observed_values:
            failures.append(f"missing observed value for: {benchmark_id}")
            continue
        result = evaluate_benchmark(bench, observed_values[benchmark_id])
        evaluations.append(result)
        if not result.passed:
            failures.append(f"{benchmark_id}: {result.reason}")

    return CapabilityBenchmarkResult(
        capability_id=record.id,
        capability_name=record.name,
        passed=not failures and len(evaluations) == len(record.benchmark_set),
        evaluations=evaluations,
        failures=failures,
    )
