"""Capability metric schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AGENT_ID, WISE_CAPABILITY_ID
from open_grace_observability.schemas.common import WISE_METRIC_ID


class CapabilityMetric(GovernedRecord):
    metric_id: str
    display_name: str = Field(min_length=1)
    capability_id: str
    agent_id: str | None = None
    metric_kind: Literal["latency", "success", "error", "coverage"] = "latency"
    value: float
    unit: str = Field(min_length=1)
    trace_id: str | None = None

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, value: str) -> str:
        if not WISE_METRIC_ID.match(value) or not value.startswith("wise.metric.capability."):
            raise ValueError("metric_id must match wise.metric.capability.{slug}")
        return value

    @field_validator("capability_id")
    @classmethod
    def validate_capability_id(cls, value: str) -> str:
        if not WISE_CAPABILITY_ID.match(value):
            raise ValueError("capability_id must match wise.capability.{slug}")
        return value

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str | None) -> str | None:
        if value is not None and not WISE_AGENT_ID.match(value):
            raise ValueError("agent_id must match wise.agent.{slug}")
        return value
