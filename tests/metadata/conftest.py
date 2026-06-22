"""Fixtures for Metadata Agent tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

REGISTRY_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-registry"
METADATA_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-metadata"


def _resolve_test_database_url() -> str | None:
    return os.environ.get("WISE_TEST_DATABASE_URL") or os.environ.get("WISE_DATABASE_URL")


def _postgres_reachable(url: str) -> bool:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def metadata_database_url() -> str:
    url = _resolve_test_database_url()
    if not url:
        pytest.skip("WISE_TEST_DATABASE_URL or WISE_DATABASE_URL is not set")
    if not _postgres_reachable(url):
        pytest.skip(f"PostgreSQL not reachable at {url}")
    return url


@pytest.fixture(scope="session")
def registry_alembic_config(metadata_database_url: str) -> Config:
    cfg = Config(str(REGISTRY_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REGISTRY_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = metadata_database_url
    return cfg


@pytest.fixture(scope="session")
def metadata_alembic_config(metadata_database_url: str) -> Config:
    cfg = Config(str(METADATA_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(METADATA_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = metadata_database_url
    return cfg


@pytest.fixture(scope="session")
def migrated_modeling(
    registry_alembic_config: Config,
    metadata_alembic_config: Config,
    metadata_database_url: str,
):
    """Apply registry and modeling migrations."""
    engine = create_engine(metadata_database_url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS modeling CASCADE"))
        conn.execute(text("DROP SCHEMA IF EXISTS registry CASCADE"))
        conn.commit()
    engine.dispose()

    command.upgrade(registry_alembic_config, "head")
    command.upgrade(metadata_alembic_config, "head")
    yield metadata_database_url


@pytest.fixture
def db_session(migrated_modeling: str):
    engine = create_engine(migrated_modeling, pool_pre_ping=True)
    with Session(engine) as session:
        yield session
        session.rollback()
    engine.dispose()
