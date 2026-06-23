"""SQLAlchemy declarative base and shared mixins."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    pass


class GovernedMixin:
    lifecycle_stage: Mapped[str] = mapped_column(String(32), nullable=False, default="proposal")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    steward_actor: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reference_models: Mapped[list] = mapped_column(JSON, nullable=False, default=list)


class JsonPayloadMixin:
    """Stores the full pydantic record as JSON for round-trip fidelity."""

    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
