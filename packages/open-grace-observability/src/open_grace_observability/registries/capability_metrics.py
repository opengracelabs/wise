"""Capability metric registry."""

from __future__ import annotations

from pathlib import Path

from open_grace_observability.registries.base import MetricRegistry
from open_grace_observability.schemas import CapabilityMetric


class CapabilityMetricRegistry(MetricRegistry[CapabilityMetric]):
    def __init__(self, store_path: Path) -> None:
        super().__init__(
            store_path=store_path,
            model=CapabilityMetric,
            id_field="metric_id",
            seed_filename="capability_metrics.yaml",
            seed_key="capability_metrics",
        )

    def for_capability(self, capability_id: str) -> list[CapabilityMetric]:
        return [
            record
            for record in self.list()
            if record.capability_id == capability_id
        ]
