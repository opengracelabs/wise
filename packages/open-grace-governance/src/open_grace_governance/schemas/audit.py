"""Audit registry schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_AUDIT_ID


class AuditRegistryRecord(GovernedRecord):
    audit_id: str
    display_name: str = Field(min_length=1)
    subject_type: Literal["agent", "capability", "model", "benchmark", "standard"]
    subject_id: str = Field(min_length=1)
    evidence_ref: str = Field(min_length=1)
    trace_id: str | None = None
    outcome: Literal["pass", "fail", "conditional"] = "pass"
    reviewer_id: str | None = None

    @field_validator("audit_id")
    @classmethod
    def validate_audit_id(cls, value: str) -> str:
        if not WISE_AUDIT_ID.match(value):
            raise ValueError("audit_id must match wise.audit.{slug}")
        return value
