"""Risk registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, RiskSeverity, WISE_RISK_ID


class RiskRegistryRecord(GovernedRecord):
    risk_id: str
    display_name: str = Field(min_length=1)
    severity: RiskSeverity
    framework: str = Field(min_length=1)
    control_id: str = Field(min_length=1)
    mitigation: str = Field(min_length=1)
    agent_id: str | None = None
    capability_id: str | None = None

    @field_validator("risk_id")
    @classmethod
    def validate_risk_id(cls, value: str) -> str:
        if not WISE_RISK_ID.match(value):
            raise ValueError("risk_id must match wise.risk.{slug}")
        return value

    @field_validator("framework")
    @classmethod
    def validate_framework(cls, value: str) -> str:
        allowed = {"nist-ai-rmf", "iso-42001", "iso-27001"}
        if value not in allowed:
            raise ValueError(f"framework must be one of {sorted(allowed)}")
        return value
