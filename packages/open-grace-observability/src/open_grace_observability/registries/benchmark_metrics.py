"""Benchmark metric registry."""

from __future__ import annotations

from pathlib import Path

from open_grace_observability.registries.base import MetricRegistry
from open_grace_observability.schemas import BenchmarkMetric


class BenchmarkMetricRegistry(MetricRegistry[BenchmarkMetric]):
    def __init__(self, store_path: Path) -> None:
        super().__init__(
            store_path=store_path,
            model=BenchmarkMetric,
            id_field="metric_id",
            seed_filename="benchmark_metrics.yaml",
            seed_key="benchmark_metrics",
        )

    def for_benchmark(self, benchmark_id: str) -> list[BenchmarkMetric]:
        return [
            record
            for record in self.list()
            if record.benchmark_id == benchmark_id
        ]
