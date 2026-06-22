"""Source type reference model."""

from __future__ import annotations

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin


class SourceType(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Classification of registered sources (authority, media repository, geospatial)."""

    __tablename__ = "source_types"
    __table_args__ = (
        UniqueConstraint("code", name="uq_source_types_code"),
        {"schema": "registry"},
    )

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    sources: Mapped[list["Source"]] = relationship(back_populates="source_type")

    def __repr__(self) -> str:
        return f"<SourceType code={self.code!r}>"


from wise_registry.models.source import Source  # noqa: E402, F401
