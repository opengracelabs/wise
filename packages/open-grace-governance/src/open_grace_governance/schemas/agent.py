"""Agent registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import (
    AgentPlane,
    GovernedRecord,
    WISE_AGENT_ID,
)


class AgentRegistryRecord(GovernedRecord):
    agent_id: str
    spec_prefix: str = Field(min_length=1, max_length=4)
    spec_path: str
    display_name: str = Field(min_length=1)
    plane: AgentPlane
    build_phase: int | None = Field(default=None, ge=1, le=15)
    service_binding: str | None = None
    langgraph_graph_id: str = Field(min_length=1)
    output_schema_uri: str = Field(min_length=1)
    evidence_profile: bool = False
    read_only: bool = False

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str) -> str:
        if not WISE_AGENT_ID.match(value):
            raise ValueError("agent_id must match wise.agent.{slug}")
        return value

    @field_validator("langgraph_graph_id")
    @classmethod
    def validate_graph_id(cls, value: str) -> str:
        if not value.replace("-", "").isalnum():
            raise ValueError("langgraph_graph_id must be kebab-case alphanumeric")
        return value
