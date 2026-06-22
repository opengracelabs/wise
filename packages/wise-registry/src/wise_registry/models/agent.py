"""Canonical agent registry model (23-benchmark-agent.md §5.4)."""

from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from wise_registry.base import AuditMixin, Base
from wise_registry.enums import AgentPlane, AgentStatus


class Agent(Base, AuditMixin):
    __tablename__ = "agents"
    __table_args__ = {"schema": "registry"}

    agent_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    spec_prefix: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    spec_path: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    plane: Mapped[AgentPlane] = mapped_column(nullable=False)
    build_phase: Mapped[int | None] = mapped_column(Integer, nullable=True)
    service_binding: Mapped[str | None] = mapped_column(String(128), nullable=True)
    langgraph_graph_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    output_schema_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    evidence_profile: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    read_only: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    status: Mapped[AgentStatus] = mapped_column(
        nullable=False,
        server_default=AgentStatus.REGISTERED.value,
    )
