"""Rights status reference model (RightsStatements.org)."""

from __future__ import annotations

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from wise_registry.base import AuditMixin, Base, UUIDPrimaryKeyMixin


class RightsStatus(Base, UUIDPrimaryKeyMixin, AuditMixin):
    """RightsStatements.org machine-readable rights category."""

    __tablename__ = "rights_statuses"
    __table_args__ = (
        UniqueConstraint("code", name="uq_rights_statuses_code"),
        UniqueConstraint("uri", name="uq_rights_statuses_uri"),
        {"schema": "registry"},
    )

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    uri: Mapped[str] = mapped_column(String(512), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<RightsStatus code={self.code!r}>"
