"""Entity registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_ENTITY_ID,
)


class EntityRegistryRecord(GovernedRecord):
    entity_id: str
    display_name: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    description: str | None = None
    external_ids: dict[str, str] = Field(default_factory=dict)
    same_as: list[str] = Field(default_factory=list)
    steward_agent_id: str | None = None
    capability_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("entity_id")
    @classmethod
    def validate_entity_id(cls, value: str) -> str:
        if not WISE_ENTITY_ID.match(value):
            raise ValueError("entity_id must match wise.entity.{slug}")
        return value
