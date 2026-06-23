"""Standards registry schema."""

from __future__ import annotations

from pydantic import Field, field_validator

from open_grace_governance.schemas.common import GovernedRecord, WISE_STANDARD_ID


class StandardsRegistryRecord(GovernedRecord):
    standard_id: str
    display_name: str = Field(min_length=1)
    binding_uri: str = Field(min_length=1)
    schema_family: str = Field(min_length=1)
    conformance_level: str = Field(default="binding")
    reference_model_slug: str = Field(min_length=1)

    @field_validator("standard_id")
    @classmethod
    def validate_standard_id(cls, value: str) -> str:
        if not WISE_STANDARD_ID.match(value):
            raise ValueError("standard_id must match wise.standard.{slug}")
        return value
