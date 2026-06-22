"""Knowledge graph models."""

from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="graph",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class GraphEntity(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "entities"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_graph_entities_stable_id"),
        UniqueConstraint("entity_uri", name="uq_graph_entities_entity_uri"),
        {"schema": "graph"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    label: Mapped[str] = mapped_column(String(512), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_assertion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.entity_assertions.id"),
        nullable=False,
    )
    entity_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    external_links: Mapped[list["ExternalLink"]] = relationship(back_populates="entity")


class ExternalLink(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "external_links"
    __table_args__ = {"schema": "graph"}

    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("graph.entities.id"),
        nullable=False,
    )
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    external_authority: Mapped[str] = mapped_column(String(64), nullable=False)
    external_identifier: Mapped[str] = mapped_column(String(128), nullable=False)
    link_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="sameAs")
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    link_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    entity: Mapped["GraphEntity"] = relationship(back_populates="external_links")
