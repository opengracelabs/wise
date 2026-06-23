"""Collection registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_COLLECTION_ID,
)


class CollectionRegistryRecord(GovernedRecord):
    collection_id: str
    display_name: str = Field(min_length=1)
    holder: str = Field(min_length=1)
    description: str | None = None
    dublin_core_profile: str | None = None
    item_entity_ids: list[str] = Field(default_factory=list)
    place_ids: list[str] = Field(default_factory=list)
    europeana_dataset_id: str | None = None
    external_ids: dict[str, str] = Field(default_factory=dict)
    steward_agent_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("collection_id")
    @classmethod
    def validate_collection_id(cls, value: str) -> str:
        if not WISE_COLLECTION_ID.match(value):
            raise ValueError("collection_id must match wise.collection.{slug}")
        return value
