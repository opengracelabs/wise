"""Cost metric schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator, model_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AGENT_ID, WISE_MODEL_ID
from open_grace_observability.schemas.common import WISE_METRIC_ID


class CostMetric(GovernedRecord):
    metric_id: str
    display_name: str = Field(min_length=1)
    agent_id: str | None = None
    model_id: str | None = None
    cost_kind: Literal["inference", "embedding", "storage", "egress"] = "inference"
    cost_usd: float = Field(ge=0)
    token_count: int | None = Field(default=None, ge=0)
    unit: str = "usd"
    trace_id: str | None = None

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, value: str) -> str:
        if not WISE_METRIC_ID.match(value) or not value.startswith("wise.metric.cost."):
            raise ValueError("metric_id must match wise.metric.cost.{slug}")
        return value

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str | None) -> str | None:
        if value is not None and not WISE_AGENT_ID.match(value):
            raise ValueError("agent_id must match wise.agent.{slug}")
        return value

    @field_validator("model_id")
    @classmethod
    def validate_model_id(cls, value: str | None) -> str | None:
        if value is not None and not WISE_MODEL_ID.match(value):
            raise ValueError("model_id must match wise.model.{slug}")
        return value

    @model_validator(mode="after")
    def require_subject(self) -> CostMetric:
        if not self.agent_id and not self.model_id:
            raise ValueError("at least one of agent_id or model_id is required")
        return self
