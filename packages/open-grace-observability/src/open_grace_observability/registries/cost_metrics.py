"""Cost metric registry."""

from __future__ import annotations

from pathlib import Path

from open_grace_observability.registries.base import MetricRegistry
from open_grace_observability.schemas import CostMetric


class CostMetricRegistry(MetricRegistry[CostMetric]):
    def __init__(self, store_path: Path) -> None:
        super().__init__(
            store_path=store_path,
            model=CostMetric,
            id_field="metric_id",
            seed_filename="cost_metrics.yaml",
            seed_key="cost_metrics",
        )
