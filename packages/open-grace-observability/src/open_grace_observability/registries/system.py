"""Observability system coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from open_grace_governance.lifecycle import LifecycleStage
from open_grace_observability.registries import (
    AgentMetricRegistry,
    AuditMetricRegistry,
    BenchmarkMetricRegistry,
    CapabilityMetricRegistry,
    CostMetricRegistry,
)
from open_grace_observability.schemas import AgentExecutionMetric


@dataclass
class ObservabilitySystem:
    """Open Grace Observability Framework v1 — five governed metric registries."""

    agent_metrics: AgentMetricRegistry
    capability_metrics: CapabilityMetricRegistry
    benchmark_metrics: BenchmarkMetricRegistry
    audit_metrics: AuditMetricRegistry
    cost_metrics: CostMetricRegistry

    @classmethod
    def create(cls, root: Path | None = None) -> ObservabilitySystem:
        base = root or Path.cwd() / ".open-grace-observability"
        base.mkdir(parents=True, exist_ok=True)
        return cls(
            agent_metrics=AgentMetricRegistry(base / "agent_metrics.json"),
            capability_metrics=CapabilityMetricRegistry(base / "capability_metrics.json"),
            benchmark_metrics=BenchmarkMetricRegistry(base / "benchmark_metrics.json"),
            audit_metrics=AuditMetricRegistry(base / "audit_metrics.json"),
            cost_metrics=CostMetricRegistry(base / "cost_metrics.json"),
        )

    def seed_all(self) -> dict[str, int]:
        return {
            "agent_metrics": self.agent_metrics.seed_from_yaml(),
            "capability_metrics": self.capability_metrics.seed_from_yaml(),
            "benchmark_metrics": self.benchmark_metrics.seed_from_yaml(),
            "audit_metrics": self.audit_metrics.seed_from_yaml(),
            "cost_metrics": self.cost_metrics.seed_from_yaml(),
        }

    def summary(self) -> dict[str, int]:
        return {
            "agent_metrics": len(self.agent_metrics.list()),
            "capability_metrics": len(self.capability_metrics.list()),
            "benchmark_metrics": len(self.benchmark_metrics.list()),
            "audit_metrics": len(self.audit_metrics.list()),
            "cost_metrics": len(self.cost_metrics.list()),
        }

    def get_by_id(self, metric_id: str):
        if metric_id.startswith("wise.metric.agent."):
            return self.agent_metrics.get(metric_id)
        if metric_id.startswith("wise.metric.capability."):
            return self.capability_metrics.get(metric_id)
        if metric_id.startswith("wise.metric.benchmark."):
            return self.benchmark_metrics.get(metric_id)
        if metric_id.startswith("wise.metric.audit."):
            return self.audit_metrics.get(metric_id)
        if metric_id.startswith("wise.metric.cost."):
            return self.cost_metrics.get(metric_id)
        return None

    def record_agent_execution(
        self,
        *,
        agent_id: str,
        metric_kind: str,
        value: float,
        unit: str,
        display_name: str | None = None,
        execution_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        steward_actor: str | None = None,
    ) -> AgentExecutionMetric:
        slug = agent_id.rsplit(".", maxsplit=1)[-1]
        suffix = uuid4().hex[:8]
        metric_id = f"wise.metric.agent.{slug}-{metric_kind}-{suffix}"
        entry = AgentExecutionMetric(
            metric_id=metric_id,
            display_name=display_name or f"{agent_id} {metric_kind}",
            agent_id=agent_id,
            execution_id=execution_id,
            metric_kind=metric_kind,  # type: ignore[arg-type]
            value=value,
            unit=unit,
            trace_id=trace_id,
            span_id=span_id,
            lifecycle_stage=LifecycleStage.AUDIT,
            steward_actor=steward_actor,
            reference_models=["opentelemetry", "prometheus"],
        )
        return self.agent_metrics.record(entry)
