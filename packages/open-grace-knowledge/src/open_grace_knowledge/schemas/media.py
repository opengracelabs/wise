"""Media registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_MEDIA_ID,
)


class MediaRegistryRecord(GovernedRecord):
    media_id: str
    display_name: str = Field(min_length=1)
    media_type: str = Field(min_length=1)
    format_mime: str = Field(min_length=1)
    description: str | None = None
    internet_archive_identifier: str | None = None
    iiif_manifest_ref: str | None = None
    collection_id: str | None = None
    entity_ids: list[str] = Field(default_factory=list)
    place_ids: list[str] = Field(default_factory=list)
    prov_activity: str | None = None
    external_ids: dict[str, str] = Field(default_factory=dict)
    steward_agent_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("media_id")
    @classmethod
    def validate_media_id(cls, value: str) -> str:
        if not WISE_MEDIA_ID.match(value):
            raise ValueError("media_id must match wise.media.{slug}")
        return value
