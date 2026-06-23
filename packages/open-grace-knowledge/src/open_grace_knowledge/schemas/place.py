"""Place registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_PLACE_ID,
)


class PlaceRegistryRecord(GovernedRecord):
    place_id: str
    display_name: str = Field(min_length=1)
    place_type: str = Field(min_length=1)
    description: str | None = None
    geometry_ref: str | None = None
    parent_place_id: str | None = None
    external_ids: dict[str, str] = Field(default_factory=dict)
    steward_agent_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("place_id")
    @classmethod
    def validate_place_id(cls, value: str) -> str:
        if not WISE_PLACE_ID.match(value):
            raise ValueError("place_id must match wise.place.{slug}")
        return value
