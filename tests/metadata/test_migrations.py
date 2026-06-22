"""Integration tests for modeling schema migrations."""

import pytest
from sqlalchemy import func, select, text

from wise_metadata.models import SchemaMapping

pytestmark = pytest.mark.integration


def test_modeling_schema_exists(db_session):
    result = db_session.execute(
        text(
            """
            SELECT schema_name FROM information_schema.schemata
            WHERE schema_name = 'modeling'
            """
        )
    ).scalar()
    assert result == "modeling"


def test_seed_schema_mappings_present(db_session):
    count = db_session.scalar(select(func.count()).select_from(SchemaMapping))
    assert count >= 16


def test_seed_mappings_cover_rc1_sources(db_session):
    names = {
        row[0]
        for row in db_session.execute(
            text(
                """
                SELECT DISTINCT source_canonical_name
                FROM modeling.schema_mappings
                """
            )
        )
    }
    assert {"unesco", "wikidata", "wikimedia-commons", "openstreetmap"}.issubset(names)
