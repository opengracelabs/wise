"""Database session dependency for api-service."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from wise_reference.session import create_session_factory

from wise_api.settings import ApiSettings

settings = ApiSettings()
SessionLocal = create_session_factory(settings.database_url)


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
