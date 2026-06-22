"""License Pydantic schemas."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from wise_registry.schemas.audit import AuditFields, AuditFieldsCreate


class LicenseBase(BaseModel):
    code: str = Field(max_length=64)
    uri: HttpUrl | str
    label: str = Field(max_length=255)
    spdx_id: str | None = Field(default=None, max_length=64)
    description: str | None = None


class LicenseCreate(LicenseBase, AuditFieldsCreate):
    pass


class LicenseRead(LicenseBase, AuditFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
