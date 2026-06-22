"""Platform capability registry model (03-canonical-architecture §4)."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from wise_registry.base import AuditMixin, Base
from wise_registry.enums import AgentPlane, CapabilityRole


class Capability(Base, AuditMixin):
    __tablename__ = "capabilities"
    __table_args__ = {"schema": "registry"}

    capability_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    canonical_section: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    build_phase: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plane: Mapped[AgentPlane] = mapped_column(nullable=False)
    contract_producer: Mapped[str | None] = mapped_column(String(512), nullable=True)
    contract_consumer: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default="active")


class CapabilityAgent(Base, AuditMixin):
    __tablename__ = "capability_agents"
    __table_args__ = {"schema": "registry"}

    capability_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("registry.capabilities.capability_id"),
        primary_key=True,
    )
    agent_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("registry.agents.agent_id"),
        primary_key=True,
    )
    role: Mapped[CapabilityRole] = mapped_column(nullable=False)


class CapabilityService(Base, AuditMixin):
    __tablename__ = "capability_services"
    __table_args__ = {"schema": "registry"}

    capability_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("registry.capabilities.capability_id"),
        primary_key=True,
    )
    service_name: Mapped[str] = mapped_column(String(128), primary_key=True)
    base_url_env: Mapped[str] = mapped_column(String(128), nullable=False)
    health_path: Mapped[str] = mapped_column(String(64), nullable=False, server_default="/health")
