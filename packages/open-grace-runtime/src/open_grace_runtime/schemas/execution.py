"""Runtime execution schemas."""

from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from open_grace_governance.schemas.common import utc_now

WISE_EXECUTION_RUN_ID = re.compile(r"^wise\.execution\.[a-z0-9]+(?:-[a-z0-9]+)*$")
WISE_BENCHMARK_RUN_ID = re.compile(r"^wise\.benchmark-run\.[a-z0-9]+(?:-[a-z0-9]+)*$")


class ExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class GateResult(BaseModel):
    gate_name: str = Field(min_length=1)
    passed: bool
    errors: list[str] = Field(default_factory=list)


class ExecutionRecord(BaseModel):
    run_id: str
    agent_id: str
    model_id: str | None = None
    capability_class_ids: list[str] = Field(default_factory=list)
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None
    gate_results: list[GateResult] = Field(default_factory=list)
    output_ref: str | None = None
    audit_id: str | None = None

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, value: str) -> str:
        if not WISE_EXECUTION_RUN_ID.match(value):
            raise ValueError("run_id must match wise.execution.{slug}")
        return value


class BenchmarkRunRecord(BaseModel):
    benchmark_run_id: str
    run_id: str
    agent_id: str
    capability_class_id: str
    benchmark_id: str
    passed: bool
    observed_value: float
    reason: str = Field(min_length=1)
    recorded_at: datetime = Field(default_factory=utc_now)

    @field_validator("benchmark_run_id")
    @classmethod
    def validate_benchmark_run_id(cls, value: str) -> str:
        if not WISE_BENCHMARK_RUN_ID.match(value):
            raise ValueError("benchmark_run_id must match wise.benchmark-run.{slug}")
        return value

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, value: str) -> str:
        if not WISE_EXECUTION_RUN_ID.match(value):
            raise ValueError("run_id must match wise.execution.{slug}")
        return value
