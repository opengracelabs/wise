"""Capability registry schema."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import AgentPlane, GovernedRecord, WISE_CAPABILITY_ID


class CapabilityRegistryRecord(GovernedRecord):
    capability_id: str
    canonical_section: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    build_phase: int | None = Field(default=None, ge=1, le=15)
    plane: AgentPlane
    contract_producer: str | None = None
    contract_consumer: str | None = None
    status: Literal["active", "deprecated"] = "active"

    @field_validator("capability_id")
    @classmethod
    def validate_capability_id(cls, value: str) -> str:
        if not WISE_CAPABILITY_ID.match(value):
            raise ValueError("capability_id must match wise.capability.{slug}")
        return value
