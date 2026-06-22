"""Fixtures for Source Registry tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

REGISTRY_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-registry"


def _resolve_test_database_url() -> str | None:
    return os.environ.get("WISE_TEST_DATABASE_URL")


def _postgres_reachable(url: str) -> bool:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except OSError:
        return False
    except Exception:
        return False


@pytest.fixture(scope="session")
def registry_database_url() -> str:
    """PostgreSQL URL for integration tests."""
    url = _resolve_test_database_url()
    if not url:
        pytest.skip("WISE_TEST_DATABASE_URL is not set")
    if not _postgres_reachable(url):
        pytest.skip(f"PostgreSQL not reachable at {url}")
    return url


@pytest.fixture(scope="session")
def alembic_config(registry_database_url: str) -> Config:
    """Alembic configuration for wise-registry migrations."""
    cfg = Config(str(REGISTRY_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REGISTRY_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = registry_database_url
    return cfg


@pytest.fixture(scope="session")
def migrated_registry(alembic_config: Config, registry_database_url: str):
    """Apply all Source Registry migrations (schema + seed data)."""
    engine = create_engine(registry_database_url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS orchestration CASCADE"))
        conn.execute(text("DROP SCHEMA IF EXISTS registry CASCADE"))
        conn.commit()
    engine.dispose()
    command.upgrade(alembic_config, "head")
    yield registry_database_url


@pytest.fixture
def db_session(migrated_registry: str):
    """SQLAlchemy session against migrated registry schema."""
    engine = create_engine(migrated_registry, pool_pre_ping=True)
    with Session(engine) as session:
        yield session
    engine.dispose()
