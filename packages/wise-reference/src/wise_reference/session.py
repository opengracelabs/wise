"""Database session factory."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    return os.environ.get(
        "WISE_DATABASE_URL",
        os.environ.get(
            "WISE_TEST_DATABASE_URL",
            os.environ.get(
                "DATABASE_URL",
                "postgresql+psycopg://wise:wise@localhost:5432/wise",
            ),
        ),
    )


def create_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    url = database_url or get_database_url()
    engine = create_engine(url, pool_pre_ping=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
