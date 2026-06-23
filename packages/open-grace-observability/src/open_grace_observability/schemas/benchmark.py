"""Benchmark metric schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AGENT_ID, WISE_BENCHMARK_ID
from open_grace_observability.schemas.common import WISE_METRIC_ID


class BenchmarkMetric(GovernedRecord):
    metric_id: str
    display_name: str = Field(min_length=1)
    benchmark_id: str
    agent_id: str | None = None
    metric_kind: Literal["observed", "threshold", "delta"] = "observed"
    observed_value: float
    unit: str = Field(min_length=1)
    passed: bool | None = None
    trace_id: str | None = None

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, value: str) -> str:
        if not WISE_METRIC_ID.match(value) or not value.startswith("wise.metric.benchmark."):
            raise ValueError("metric_id must match wise.metric.benchmark.{slug}")
        return value

    @field_validator("benchmark_id")
    @classmethod
    def validate_benchmark_id(cls, value: str) -> str:
        if not WISE_BENCHMARK_ID.match(value):
            raise ValueError("benchmark_id must match wise.benchmark.{slug}")
        return value

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str | None) -> str | None:
        if value is not None and not WISE_AGENT_ID.match(value):
            raise ValueError("agent_id must match wise.agent.{slug}")
        return value
