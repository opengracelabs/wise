"""Fixtures for orchestration tests."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture(autouse=True)
def orchestration_inline_mode(monkeypatch):
    """Use inline RC1 clients (no HTTP) for orchestration unit tests."""
    monkeypatch.setenv("WISE_ORCHESTRATION_INLINE", "1")


@pytest.fixture
def orchestration_db_session(migrated_registry: str):
    """Session with full registry migrations including agents and capabilities."""
    engine = create_engine(migrated_registry, pool_pre_ping=True)
    with sessionmaker(bind=engine, autoflush=False)() as session:
        yield session
    engine.dispose()
