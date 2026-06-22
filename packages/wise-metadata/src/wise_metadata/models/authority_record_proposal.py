"""Authority record proposals."""

from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import AssertionStatus, AuthorityEntityType, AuthorityMatchMethod

ASSERTION_STATUS_ENUM = ENUM(
    AssertionStatus,
    name="assertion_status_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)
AUTHORITY_ENTITY_TYPE_ENUM = ENUM(
    AuthorityEntityType,
    name="authority_entity_type_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)
AUTHORITY_MATCH_METHOD_ENUM = ENUM(
    AuthorityMatchMethod,
    name="authority_match_method_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class AuthorityRecordProposal(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Authority reconciliation candidate pending steward approval."""

    __tablename__ = "authority_record_proposals"
    __table_args__ = {"schema": "modeling"}

    normalized_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("modeling.normalized_records.id"),
        nullable=False,
    )
    entity_type: Mapped[AuthorityEntityType] = mapped_column(
        AUTHORITY_ENTITY_TYPE_ENUM,
        nullable=False,
    )
    provisional_uri: Mapped[str] = mapped_column(String(512), nullable=False)
    pref_label: Mapped[str] = mapped_column(String(512), nullable=False)
    alt_labels: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")
    external_scheme: Mapped[str] = mapped_column(String(64), nullable=False)
    external_id: Mapped[str] = mapped_column(String(128), nullable=False)
    link_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="exactMatch")
    match_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    match_method: Mapped[AuthorityMatchMethod] = mapped_column(
        AUTHORITY_MATCH_METHOD_ENUM,
        nullable=False,
    )
    status: Mapped[AssertionStatus] = mapped_column(
        ASSERTION_STATUS_ENUM,
        nullable=False,
        server_default=AssertionStatus.PROPOSED.value,
    )
    skos_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)

    normalized_record: Mapped["NormalizedRecord"] = relationship(back_populates="authority_proposals")


from wise_metadata.models.normalized_record import NormalizedRecord  # noqa: E402, F401
