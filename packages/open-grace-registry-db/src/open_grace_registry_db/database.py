"""Database session factory and schema management."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from open_grace_registry_db.base import Base
from open_grace_registry_db import models as _models  # noqa: F401 — register tables


def default_database_url() -> str:
    return os.environ.get("OPEN_GRACE_DATABASE_URL", "sqlite:///./open-grace-registry.db")


class RegistryDatabase:
    """SQLAlchemy-backed Open Grace registry store."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    @classmethod
    def create(cls, url: str | None = None) -> RegistryDatabase:
        db_url = url or default_database_url()
        connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
        engine = create_engine(db_url, future=True, connect_args=connect_args)
        return cls(engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
