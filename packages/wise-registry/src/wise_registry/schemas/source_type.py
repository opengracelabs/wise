"""SourceType Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class SourceTypeBase(BaseModel):
    code: str = Field(max_length=64)
    label: str = Field(max_length=255)
    description: str | None = None


class SourceTypeCreate(SourceTypeBase, AuditFieldsCreate):
    pass


class SourceTypeRead(SourceTypeBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
