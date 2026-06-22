"""Analytics service test fixtures."""

from __future__ import annotations

import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

ROOT = Path(__file__).resolve().parents[2]
for path in (
    ROOT / "services" / "analytics-service" / "src",
    ROOT / "packages" / "wise-demand-intelligence" / "src",
    ROOT / "packages" / "wise-common" / "src",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from wise_analytics.models import Base  # noqa: E402


@pytest.fixture
def analytics_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with SessionLocal() as session:
        yield session
    engine.dispose()
