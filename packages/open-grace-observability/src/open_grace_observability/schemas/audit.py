"""Audit metric schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AUDIT_ID
from open_grace_observability.schemas.common import WISE_METRIC_ID


class AuditMetric(GovernedRecord):
    metric_id: str
    display_name: str = Field(min_length=1)
    audit_id: str | None = None
    subject_type: Literal["agent", "capability", "model", "benchmark", "standard"]
    subject_id: str = Field(min_length=1)
    metric_kind: Literal["evidence_count", "review_duration", "outcome_score"] = "outcome_score"
    value: float
    unit: str = Field(min_length=1)
    trace_id: str | None = None

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, value: str) -> str:
        if not WISE_METRIC_ID.match(value) or not value.startswith("wise.metric.audit."):
            raise ValueError("metric_id must match wise.metric.audit.{slug}")
        return value

    @field_validator("audit_id")
    @classmethod
    def validate_audit_id(cls, value: str | None) -> str | None:
        if value is not None and not WISE_AUDIT_ID.match(value):
            raise ValueError("audit_id must match wise.audit.{slug}")
        return value
