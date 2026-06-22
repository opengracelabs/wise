"""Resolve Source Registry entries from pipeline references."""

from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from wise_registry.models import Source


def resolve_source(session: Session, registry_ref: str) -> Source:
    """Look up a source by stable_id alias or canonical_name."""
    return session.scalars(
        select(Source).where(
            or_(
                Source.stable_id == registry_ref,
                Source.canonical_name == registry_ref,
            )
        )
    ).one()
