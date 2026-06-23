"""Heritage registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_HERITAGE_ID,
)


class HeritageRegistryRecord(GovernedRecord):
    heritage_id: str
    display_name: str = Field(min_length=1)
    heritage_type: str = Field(min_length=1)
    description: str | None = None
    unesco_id: str | None = None
    place_id: str | None = None
    cidoc_class: str | None = None
    collection_ids: list[str] = Field(default_factory=list)
    entity_ids: list[str] = Field(default_factory=list)
    external_ids: dict[str, str] = Field(default_factory=dict)
    steward_agent_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("heritage_id")
    @classmethod
    def validate_heritage_id(cls, value: str) -> str:
        if not WISE_HERITAGE_ID.match(value):
            raise ValueError("heritage_id must match wise.heritage.{slug}")
        return value
