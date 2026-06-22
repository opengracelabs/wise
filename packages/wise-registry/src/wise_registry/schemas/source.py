"""Source Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.enums import TrustLevel
from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class SourceBase(BaseModel):
    canonical_name: str = Field(max_length=128)
    display_name: str = Field(max_length=255)
    source_type_id: UUID
    homepage_url: str = Field(max_length=512)
    api_url: str | None = Field(default=None, max_length=512)
    license_id: UUID | None = None
    trust_level: TrustLevel = TrustLevel.UNVERIFIED
    active: bool = True


class SourceCreate(SourceBase, AuditFieldsCreate):
    pass


class SourceUpdate(BaseModel):
    display_name: str | None = Field(default=None, max_length=255)
    homepage_url: str | None = Field(default=None, max_length=512)
    api_url: str | None = Field(default=None, max_length=512)
    license_id: UUID | None = None
    trust_level: TrustLevel | None = None
    active: bool | None = None
    updated_by: str = Field(default="system", max_length=255)


class SourceRead(SourceBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
