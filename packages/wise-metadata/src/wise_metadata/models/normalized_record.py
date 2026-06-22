"""Normalized metadata record model."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import SourceSchema

SOURCE_SCHEMA_ENUM = ENUM(
    SourceSchema,
    name="source_schema_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class NormalizedRecord(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Canonical normalized metadata with preserved source literals."""

    __tablename__ = "normalized_records"
    __table_args__ = {"schema": "modeling"}

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    external_record_id: Mapped[str] = mapped_column(String(512), nullable=False)
    source_schema: Mapped[SourceSchema] = mapped_column(SOURCE_SCHEMA_ENUM, nullable=False)
    source_schema_version: Mapped[str] = mapped_column(String(32), nullable=False, server_default="1.0")
    raw_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    normalized_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    original_literals: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    registry_provenance_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.provenance_events.id"),
        nullable=True,
    )
    normalization_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.provenance_events.id"),
        nullable=True,
    )

    normalization_event: Mapped["ModelingProvenanceEvent | None"] = relationship(
        back_populates="normalized_records",
        foreign_keys=[normalization_event_id],
    )
    mapping_runs: Mapped[list["MappingRun"]] = relationship(back_populates="normalized_record")
    assertion_proposals: Mapped[list["EntityAssertionProposal"]] = relationship(
        back_populates="normalized_record"
    )
    authority_proposals: Mapped[list["AuthorityRecordProposal"]] = relationship(
        back_populates="normalized_record"
    )
    validation_results: Mapped[list["ValidationResult"]] = relationship(
        back_populates="normalized_record"
    )


from wise_metadata.models.authority_record_proposal import AuthorityRecordProposal  # noqa: E402, F401
from wise_metadata.models.entity_assertion_proposal import EntityAssertionProposal  # noqa: E402, F401
from wise_metadata.models.mapping_run import MappingRun  # noqa: E402, F401
from wise_metadata.models.provenance_event import ModelingProvenanceEvent  # noqa: E402, F401
from wise_metadata.models.validation_result import ValidationResult  # noqa: E402, F401
