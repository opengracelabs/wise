"""Risk registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import (
    GovernedRecord,
    MitAffectedParty,
    MitCausalSource,
    MitHarmType,
    MitRiskDomain,
    MitRiskIntent,
    MitRiskTiming,
    RiskSeverity,
    WISE_RISK_ID,
    _SEVERITY_ORDINAL,
)


class RiskRegistryRecord(GovernedRecord):
    risk_id: str
    display_name: str = Field(min_length=1)
    severity: RiskSeverity
    framework: str = Field(min_length=1)
    control_id: str = Field(min_length=1)
    mitigation: str = Field(min_length=1)
    agent_id: str | None = None
    capability_id: str | None = None
    risk_domain: MitRiskDomain
    harm_type: MitHarmType
    affected_party: MitAffectedParty
    causal_source: MitCausalSource
    intent: MitRiskIntent
    timing: MitRiskTiming
    residual_risk: RiskSeverity
    evidence: str = Field(min_length=1)

    @field_validator("risk_id")
    @classmethod
    def validate_risk_id(cls, value: str) -> str:
        if not WISE_RISK_ID.match(value):
            raise ValueError("risk_id must match wise.risk.{slug}")
        return value

    @field_validator("framework")
    @classmethod
    def validate_framework(cls, value: str) -> str:
        allowed = {"nist-ai-rmf", "iso-42001", "iso-27001", "mit-ai-risk"}
        if value not in allowed:
            raise ValueError(f"framework must be one of {sorted(allowed)}")
        return value

    @field_validator("residual_risk")
    @classmethod
    def validate_residual_risk(cls, value: str, info) -> str:
        severity = info.data.get("severity")
        if severity is not None and _SEVERITY_ORDINAL[value] > _SEVERITY_ORDINAL[severity]:
            raise ValueError("residual_risk cannot exceed severity")
        return value
