"""Fixtures for Reference Capability 1 tests."""

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
    return os.environ.get("WISE_TEST_DATABASE_URL")


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
def reference_database_url() -> str:
    url = _resolve_test_database_url()
    if not url:
        pytest.skip("WISE_TEST_DATABASE_URL is not set")
    if not _postgres_reachable(url):
        pytest.skip(f"PostgreSQL not reachable at {url}")
    return url


@pytest.fixture(scope="session")
def migrated_reference(reference_database_url: str):
    """Apply registry and reference migrations through RC3."""
    os.environ["WISE_DATABASE_URL"] = reference_database_url

    registry_cfg = Config(str(REGISTRY_ROOT / "alembic.ini"))
    command.upgrade(registry_cfg, "head")

    reference_cfg = Config(str(REFERENCE_ROOT / "alembic.ini"))
    command.upgrade(reference_cfg, "head")

    discovery_cfg = Config(str(DISCOVERY_ROOT / "alembic.ini"))
    command.upgrade(discovery_cfg, "head")

    yield reference_database_url


@pytest.fixture(scope="session")
def migrated_rc1(migrated_reference: str):
    """Backward-compatible alias for RC1 tests."""
    return migrated_reference


@pytest.fixture
def rc1_session(migrated_reference: str):
    engine = create_engine(migrated_reference, pool_pre_ping=True)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def rc3_session(migrated_reference: str):
    engine = create_engine(migrated_reference, pool_pre_ping=True)
    with Session(engine) as session:
        yield session
    engine.dispose()
