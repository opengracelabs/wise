"""RC17 attribution registry model."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin


class Attribution(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Attribution requirement for a registered asset."""

    __tablename__ = "attributions"
    __table_args__ = {"schema": "registry"}

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.assets.id"),
        nullable=False,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.sources.id"),
        nullable=False,
    )
    license_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.licenses.id"),
        nullable=True,
    )
    rights_status_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("registry.rights_statuses.id"),
        nullable=True,
    )
    display_text: Mapped[str] = mapped_column(String(512), nullable=False)
    credit_line: Mapped[str | None] = mapped_column(String(512), nullable=True)
    attribution_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="attributions")
    source: Mapped["Source"] = relationship(back_populates="attributions")
    license: Mapped["License | None"] = relationship(back_populates="attributions")
    rights_status: Mapped["RightsStatus | None"] = relationship(back_populates="attributions")

    def __repr__(self) -> str:
        return f"<Attribution asset_id={self.asset_id!r} required={self.required!r}>"


from wise_registry.models.asset import Asset  # noqa: E402, F401
from wise_registry.models.license import License  # noqa: E402, F401
from wise_registry.models.rights_status import RightsStatus  # noqa: E402, F401
from wise_registry.models.source import Source  # noqa: E402, F401
