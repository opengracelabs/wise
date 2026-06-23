"""Species registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord
from open_grace_knowledge.schemas.common import (
    BackingStoreMetadata,
    WISE_SPECIES_ID,
)


class SpeciesRegistryRecord(GovernedRecord):
    species_id: str
    scientific_name: str = Field(min_length=1)
    common_names: list[str] = Field(default_factory=list)
    taxon_rank: str = Field(min_length=1)
    gbif_taxon_key: int | None = None
    parent_species_id: str | None = None
    place_ids: list[str] = Field(default_factory=list)
    external_ids: dict[str, str] = Field(default_factory=dict)
    steward_agent_id: str | None = None
    backing_stores: list[BackingStoreMetadata] = Field(min_length=1)

    @field_validator("species_id")
    @classmethod
    def validate_species_id(cls, value: str) -> str:
        if not WISE_SPECIES_ID.match(value):
            raise ValueError("species_id must match wise.species.{slug}")
        return value
