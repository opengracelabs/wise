"""RC17 attribution registry Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class AttributionBase(BaseModel):
    asset_id: UUID
    source_id: UUID
    license_id: UUID | None = None
    rights_status_id: UUID | None = None
    display_text: str = Field(max_length=512)
    credit_line: str | None = Field(default=None, max_length=512)
    attribution_uri: str | None = Field(default=None, max_length=512)
    required: bool = True
    sort_order: int = 0
    notes: str | None = None


class AttributionCreate(AttributionBase, AuditFieldsCreate):
    pass


class AttributionUpdate(BaseModel):
    display_text: str | None = Field(default=None, max_length=512)
    credit_line: str | None = Field(default=None, max_length=512)
    attribution_uri: str | None = Field(default=None, max_length=512)
    required: bool | None = None
    sort_order: int | None = None
    notes: str | None = None
    updated_by: str = Field(default="system", max_length=255)


class AttributionRead(AttributionBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
