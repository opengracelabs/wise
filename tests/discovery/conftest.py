"""Fixtures for Source Discovery Agent tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

REGISTRY_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-registry"
REFERENCE_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-reference"
DISCOVERY_ROOT = Path(__file__).resolve().parents[2] / "packages" / "wise-discovery"


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
def discovery_database_url() -> str:
    url = _resolve_test_database_url()
    if not url:
        pytest.skip("WISE_TEST_DATABASE_URL or WISE_DATABASE_URL is not set")
    if not _postgres_reachable(url):
        pytest.skip(f"PostgreSQL not reachable at {url}")
    return url


@pytest.fixture(scope="session")
def registry_alembic_config(discovery_database_url: str) -> Config:
    cfg = Config(str(REGISTRY_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REGISTRY_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = discovery_database_url
    return cfg


@pytest.fixture(scope="session")
def reference_alembic_config(discovery_database_url: str) -> Config:
    cfg = Config(str(REFERENCE_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(REFERENCE_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = discovery_database_url
    return cfg


@pytest.fixture(scope="session")
def discovery_alembic_config(discovery_database_url: str) -> Config:
    cfg = Config(str(DISCOVERY_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(DISCOVERY_ROOT / "migrations"))
    os.environ["WISE_DATABASE_URL"] = discovery_database_url
    return cfg


@pytest.fixture(scope="session")
def migrated_discovery(
    registry_alembic_config: Config,
    reference_alembic_config: Config,
    discovery_alembic_config: Config,
    discovery_database_url: str,
):
    """Apply registry, reference, and discovery migrations."""
    engine = create_engine(discovery_database_url, pool_pre_ping=True)
    with engine.connect() as conn:
        for schema in ("discovery", "quality", "graph", "modeling", "preservation", "species", "registry"):
            conn.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
        conn.commit()
    engine.dispose()

    command.upgrade(registry_alembic_config, "head")
    command.upgrade(reference_alembic_config, "head")
    command.upgrade(discovery_alembic_config, "head")
    yield discovery_database_url


@pytest.fixture
def db_session(migrated_discovery: str):
    engine = create_engine(migrated_discovery, pool_pre_ping=True)
    with Session(engine) as session:
        yield session
        session.rollback()
    engine.dispose()
