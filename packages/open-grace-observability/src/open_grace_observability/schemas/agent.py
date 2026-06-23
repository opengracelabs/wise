"""Agent execution metric schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AGENT_ID
from open_grace_observability.schemas.common import WISE_METRIC_ID


class AgentExecutionMetric(GovernedRecord):
    metric_id: str
    display_name: str = Field(min_length=1)
    agent_id: str
    execution_id: str | None = None
    metric_kind: Literal["latency", "success", "error", "throughput"] = "latency"
    value: float
    unit: str = Field(min_length=1)
    trace_id: str | None = None
    span_id: str | None = None

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, value: str) -> str:
        if not WISE_METRIC_ID.match(value) or not value.startswith("wise.metric.agent."):
            raise ValueError("metric_id must match wise.metric.agent.{slug}")
        return value

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str) -> str:
        if not WISE_AGENT_ID.match(value):
            raise ValueError("agent_id must match wise.agent.{slug}")
        return value
