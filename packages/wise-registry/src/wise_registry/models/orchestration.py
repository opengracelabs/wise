"""Agent run audit and steward approval queue."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from wise_registry.base import AuditMixin, Base
from wise_registry.enums import RunStatus, StewardTaskStatus


class AgentRun(Base, AuditMixin):
    __tablename__ = "agent_runs"
    __table_args__ = {"schema": "registry"}

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    agent_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("registry.agents.agent_id"),
        nullable=False,
    )
    agent_version: Mapped[str] = mapped_column(String(64), nullable=False, server_default="0.1.0")
    graph_thread_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    trigger_source: Mapped[str] = mapped_column(String(32), nullable=False)
    input_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RunStatus] = mapped_column(nullable=False)
    provenance_event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class StewardTask(Base, AuditMixin):
    """Human approval gate task (orchestration plane)."""

    __tablename__ = "steward_tasks"
    __table_args__ = {"schema": "orchestration"}

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.agent_runs.run_id"),
        nullable=False,
    )
    thread_id: Mapped[str] = mapped_column(String(128), nullable=False)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[StewardTaskStatus] = mapped_column(
        nullable=False,
        server_default=StewardTaskStatus.PENDING.value,
    )
    reviewer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
