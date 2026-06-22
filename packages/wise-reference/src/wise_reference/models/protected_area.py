"""Protected area registry models with PostGIS geometry."""

from __future__ import annotations

import uuid
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from wise_reference.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_reference.enums import ApprovalStatus

APPROVAL_STATUS_ENUM = ENUM(
    ApprovalStatus,
    name="approval_status_enum",
    schema="conservation",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class ProtectedArea(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Canonical protected area with PostGIS boundary geometry."""

    __tablename__ = "protected_areas"
    __table_args__ = (
        UniqueConstraint("stable_id", name="uq_protected_areas_stable_id"),
        {"schema": "conservation"},
    )

    stable_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        APPROVAL_STATUS_ENUM,
        nullable=False,
        server_default=ApprovalStatus.PROPOSED.value,
    )
    pref_label: Mapped[str] = mapped_column(String(512), nullable=False)
    designation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    graph_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("graph.entities.id"),
        nullable=False,
    )
    discovery_record_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("discovery.records.id"),
        nullable=True,
    )
    boundary: Mapped[Any] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326),
        nullable=False,
    )
    centroid: Mapped[Any] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False,
    )
    conservation_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False)
    external_identifiers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    area_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    provenance_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
