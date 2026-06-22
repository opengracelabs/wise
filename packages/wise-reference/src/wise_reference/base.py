"""SQLAlchemy declarative base and audit mixins."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Multi-schema declarative base for RC1 tables."""


class AuditMixin:
    """Provenance and audit fields (architecture-v1.0)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_by: Mapped[str] = mapped_column(String(255), nullable=False, server_default="system")
    updated_by: Mapped[str] = mapped_column(String(255), nullable=False, server_default="system")
    row_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
