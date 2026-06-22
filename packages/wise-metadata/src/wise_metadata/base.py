"""SQLAlchemy declarative base and institutional audit mixins."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Modeling schema declarative base."""


class AuditMixin:
    """Provenance and audit fields required on every modeling table (architecture-v1.0)."""

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
    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="system",
    )
    updated_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="system",
    )
    row_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="1",
    )


class UUIDPrimaryKeyMixin:
    """UUID primary key with PostgreSQL gen_random_uuid() default."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
