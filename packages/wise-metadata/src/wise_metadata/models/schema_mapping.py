"""Schema mapping crosswalk rules."""

from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from wise_metadata.base import AuditMixin, Base, UUIDPrimaryKeyMixin
from wise_metadata.enums import MappingTarget

MAPPING_TARGET_ENUM = ENUM(
    MappingTarget,
    name="mapping_target_enum",
    schema="modeling",
    create_type=False,
    values_callable=lambda enum: [member.value for member in enum],
)


class SchemaMapping(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Source field → ontology term crosswalk rule."""

    __tablename__ = "schema_mappings"
    __table_args__ = (
        UniqueConstraint(
            "source_canonical_name",
            "source_field_path",
            "mapping_target",
            "target_term",
            name="uq_schema_mappings_crosswalk",
        ),
        {"schema": "modeling"},
    )

    source_canonical_name: Mapped[str] = mapped_column(String(128), nullable=False)
    source_field_path: Mapped[str] = mapped_column(String(512), nullable=False)
    mapping_target: Mapped[MappingTarget] = mapped_column(MAPPING_TARGET_ENUM, nullable=False)
    target_term: Mapped[str] = mapped_column(String(256), nullable=False)
    crm_class: Mapped[str | None] = mapped_column(String(64), nullable=True)
    transform_rule: Mapped[str] = mapped_column(String(64), nullable=False, server_default="direct")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default="100")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
