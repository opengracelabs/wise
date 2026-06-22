"""Integration tests for discovery schema migrations."""

import pytest
from alembic.script import ScriptDirectory
from sqlalchemy import text

pytestmark = pytest.mark.integration


def test_discovery_migration_single_head(discovery_alembic_config):
    script = ScriptDirectory.from_config(discovery_alembic_config)
    heads = script.get_heads()
    assert len(heads) == 1
    assert heads[0] == "001_discovery_v1_agent"


def test_approval_status_column_renamed(db_session):
    row = db_session.execute(
        text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'discovery'
              AND table_name = 'records'
              AND column_name = 'approval_status'
            """
        )
    ).scalar()
    assert row == "approval_status"
