"""Database session helpers for Source Discovery Agent."""

from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    url = os.environ.get("WISE_DATABASE_URL")
    if not url:
        raise RuntimeError("WISE_DATABASE_URL is not set")
    return url


def create_session_factory(url: str | None = None) -> sessionmaker[Session]:
    engine = create_engine(url or get_database_url(), pool_pre_ping=True)
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_session(url: str | None = None) -> Generator[Session, None, None]:
    factory = create_session_factory(url)
    session = factory()
    try:
        yield session
    finally:
        session.close()
