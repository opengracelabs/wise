"""Database session factory."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    """Resolve database URL from WISE_DATABASE_URL or WISE_TEST_DATABASE_URL."""
    return os.environ.get(
        "WISE_DATABASE_URL",
        os.environ.get(
            "WISE_TEST_DATABASE_URL",
            "postgresql+psycopg://wise:wise@localhost:5432/wise",
        ),
    )


def create_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    """Create a SQLAlchemy session factory."""
    url = database_url or get_database_url()
    engine = create_engine(url, pool_pre_ping=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_engine_from_env(database_url: str | None = None):
    """Create SQLAlchemy engine."""
    url = database_url or get_database_url()
    return create_engine(url, pool_pre_ping=True)
