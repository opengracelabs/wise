"""Schema mapping crosswalk schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_metadata.enums import MappingTarget
from wise_metadata.schemas.audit import AuditFields, AuditFieldsCreate


class SchemaMappingCreate(BaseModel):
    """Define source field → ontology term crosswalk rule."""

    source_canonical_name: str = Field(max_length=128)
    source_field_path: str = Field(max_length=512)
    mapping_target: MappingTarget
    target_term: str = Field(max_length=256)
    crm_class: str | None = Field(default=None, max_length=64)
    transform_rule: str = Field(default="direct", max_length=64)
    priority: int = Field(default=100, ge=0)
    active: bool = True
    audit: AuditFieldsCreate = Field(default_factory=AuditFieldsCreate)


class SchemaMappingRead(BaseModel):
    """Read schema mapping rule."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_canonical_name: str
    source_field_path: str
    mapping_target: MappingTarget
    target_term: str
    crm_class: str | None
    transform_rule: str
    priority: int
    active: bool
    audit: AuditFields
