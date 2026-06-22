"""Shared audit field schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuditFields(BaseModel):
    """Provenance and audit fields present on every registry entity."""

    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    created_by: str = Field(max_length=255)
    updated_by: str = Field(max_length=255)
    row_version: int = Field(ge=1)


class AuditFieldsCreate(BaseModel):
    """Optional audit overrides on create (defaults to system principal)."""

    created_by: str = Field(default="system", max_length=255)
    updated_by: str = Field(default="system", max_length=255)
