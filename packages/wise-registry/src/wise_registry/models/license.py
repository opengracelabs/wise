"""License reference model (Creative Commons, ODbL)."""

from __future__ import annotations

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin


class License(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """Machine-readable license URI registry (Creative Commons, ODbL)."""

    __tablename__ = "licenses"
    __table_args__ = (
        UniqueConstraint("code", name="uq_licenses_code"),
        UniqueConstraint("uri", name="uq_licenses_uri"),
        {"schema": "registry"},
    )

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    uri: Mapped[str] = mapped_column(String(512), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    spdx_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    sources: Mapped[list["Source"]] = relationship(back_populates="license")
    assets: Mapped[list["Asset"]] = relationship(back_populates="license")
    attributions: Mapped[list["Attribution"]] = relationship(back_populates="license")

    def __repr__(self) -> str:
        return f"<License code={self.code!r}>"


from wise_registry.models.source import Source  # noqa: E402, F401
from wise_registry.models.asset import Asset  # noqa: E402, F401
from wise_registry.models.attribution import Attribution  # noqa: E402, F401
