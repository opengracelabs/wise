"""SQLAlchemy models for Open Grace governed registries."""

from __future__ import annotations

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from open_grace_registry_db.base import Base, GovernedMixin, JsonPayloadMixin


class AgentEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_agents"

    agent_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class CapabilityEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_capabilities"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)


class AgentCapabilityBinding(Base):
    __tablename__ = "open_grace_agent_capability_bindings"
    __table_args__ = (UniqueConstraint("agent_id", "capability_class_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    capability_class_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)


class KnowledgeEntry(Base, GovernedMixin, JsonPayloadMixin):
    """Unified knowledge registry — entity, species, place, heritage, collection, media, kg."""

    __tablename__ = "open_grace_knowledge"

    entry_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    knowledge_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)


class RiskEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_risks"

    risk_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class BenchmarkEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_benchmarks"

    benchmark_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class AuditEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_audits"

    audit_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class StandardEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_standards"

    standard_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class ModelEntry(Base, GovernedMixin, JsonPayloadMixin):
    __tablename__ = "open_grace_models"

    model_id: Mapped[str] = mapped_column(String(128), primary_key=True)


class ExecutionEntry(Base, JsonPayloadMixin):
    __tablename__ = "open_grace_executions"

    run_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    agent_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
