"""Shared audit field schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditFields(BaseModel):
    """Provenance and audit fields present on every discovery entity."""

    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    created_by: str = Field(max_length=255)
    updated_by: str = Field(max_length=255)
    row_version: int = Field(ge=1)


class AuditFieldsCreate(BaseModel):
    """Optional audit overrides on create."""

    created_by: str = Field(default="discovery-agent@1.0.0", max_length=255)
    updated_by: str = Field(default="discovery-agent@1.0.0", max_length=255)
