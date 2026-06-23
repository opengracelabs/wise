"""Benchmark registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import BenchmarkMetric, GovernedRecord, WISE_BENCHMARK_ID


class BenchmarkRegistryRecord(GovernedRecord):
    benchmark_id: str
    display_name: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    metric: BenchmarkMetric
    threshold_min: float | None = None
    threshold_max: float | None = None
    unit: str = Field(min_length=1)
    gold_dataset_ref: str | None = None

    @field_validator("benchmark_id")
    @classmethod
    def validate_benchmark_id(cls, value: str) -> str:
        if not WISE_BENCHMARK_ID.match(value):
            raise ValueError("benchmark_id must match wise.benchmark.{slug}")
        return value

    @field_validator("threshold_max")
    @classmethod
    def validate_thresholds(cls, value: float | None, info) -> float | None:
        minimum = info.data.get("threshold_min")
        if minimum is not None and value is not None and value < minimum:
            raise ValueError("threshold_max must be >= threshold_min")
        return value
