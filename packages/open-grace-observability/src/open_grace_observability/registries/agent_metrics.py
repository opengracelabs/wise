"""Agent execution metric registry."""

from __future__ import annotations

from pathlib import Path

from open_grace_observability.registries.base import MetricRegistry
from open_grace_observability.schemas import AgentExecutionMetric


class AgentMetricRegistry(MetricRegistry[AgentExecutionMetric]):
    def __init__(self, store_path: Path) -> None:
        super().__init__(
            store_path=store_path,
            model=AgentExecutionMetric,
            id_field="metric_id",
            seed_filename="agent_metrics.yaml",
            seed_key="agent_metrics",
        )
