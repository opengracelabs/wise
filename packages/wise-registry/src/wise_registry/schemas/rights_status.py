"""RightsStatus Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class RightsStatusBase(BaseModel):
    code: str = Field(max_length=64)
    uri: HttpUrl | str
    label: str = Field(max_length=255)
    description: str | None = None


class RightsStatusCreate(RightsStatusBase, AuditFieldsCreate):
    pass


class RightsStatusRead(RightsStatusBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
