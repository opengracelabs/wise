"""Audit metric registry."""

from __future__ import annotations

from pathlib import Path

from open_grace_observability.registries.base import MetricRegistry
from open_grace_observability.schemas import AuditMetric


class AuditMetricRegistry(MetricRegistry[AuditMetric]):
    def __init__(self, store_path: Path) -> None:
        super().__init__(
            store_path=store_path,
            model=AuditMetric,
            id_field="metric_id",
            seed_filename="audit_metrics.yaml",
            seed_key="audit_metrics",
        )

    def for_subject(self, subject_id: str) -> list[AuditMetric]:
        return [
            record
            for record in self.list()
            if record.subject_id == subject_id
        ]
