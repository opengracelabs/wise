"""Persistence tests for open-grace-registry-db."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from open_grace_registry_db import RegistryDatabase, export_all_json, seed_all_from_yaml, sync_json_store


@pytest.fixture
def memory_db():
    db = RegistryDatabase.create("sqlite:///:memory:")
    db.create_tables()
    return db


def test_seed_all_from_yaml(memory_db):
    counts = seed_all_from_yaml(memory_db)
    assert counts["agents"] >= 10
    assert counts["capabilities"] >= 4
    assert counts["risks"] >= 5
    assert counts["standards"] >= 4
    assert counts["benchmarks"] >= 4
    assert counts["models"] >= 3
    assert counts.get("knowledge", 0) >= 5


def test_export_json_round_trip(memory_db, tmp_path):
    seed_all_from_yaml(memory_db)
    written = export_all_json(memory_db, tmp_path)
    assert (tmp_path / "agent_registry.json").is_file()
    agents_payload = json.loads((tmp_path / "agent_registry.json").read_text())
    assert len(agents_payload["entries"]) >= 10
    assert "agents" in written


def test_sync_json_store(memory_db, tmp_path):
    seed_all_from_yaml(memory_db)
    export_all_json(memory_db, tmp_path)

    fresh = RegistryDatabase.create("sqlite:///:memory:")
    fresh.create_tables()
    counts = sync_json_store(fresh, tmp_path)
    assert counts["agents"] >= 10
    assert counts["capabilities"] >= 4


def test_alembic_upgrade_head(tmp_path):
    pytest.importorskip("alembic")
    from alembic import command
    from alembic.config import Config

    db_path = tmp_path / "migrate.db"
    url = f"sqlite:///{db_path}"
    pkg_root = Path(__file__).resolve().parents[2] / "packages" / "open-grace-registry-db"
    ini = pkg_root / "alembic.ini"
    cfg = Config(str(ini))
    cfg.set_main_option("script_location", str(pkg_root / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url)
    command.upgrade(cfg, "head")

    db = RegistryDatabase.create(url)
    seed_all_from_yaml(db)
    with db.session() as session:
        from open_grace_registry_db.models import AgentEntry
        from sqlalchemy import select

        rows = session.scalars(select(AgentEntry)).all()
        assert len(rows) >= 10
