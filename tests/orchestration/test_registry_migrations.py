"""Integration tests for agent and capability registry migrations."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from wise_orchestration.manifest_loader import CANONICAL_AGENT_COUNT, CANONICAL_CAPABILITY_COUNT
from wise_orchestration.validation import validate_registry_alignment
from wise_registry.models import Agent, Capability

SEED_ACTOR = "wise-orchestration-seed"


@pytest.mark.integration
def test_orchestration_schema_tables_exist(orchestration_db_session: Session):
    db_session = orchestration_db_session
    result = db_session.execute(
        text(
            """
            SELECT table_name, table_schema
            FROM information_schema.tables
            WHERE table_schema IN ('registry', 'orchestration')
            ORDER BY table_schema, table_name
            """
        )
    )
    tables = {(row[1], row[0]) for row in result}
    assert ("registry", "agents") in tables
    assert ("registry", "capabilities") in tables
    assert ("registry", "capability_agents") in tables
    assert ("registry", "agent_runs") in tables
    assert ("orchestration", "steward_tasks") in tables


@pytest.mark.integration
def test_canonical_agents_seeded(orchestration_db_session: Session):
    db_session = orchestration_db_session
    count = db_session.scalar(select(func.count()).select_from(Agent))
    assert count == CANONICAL_AGENT_COUNT

    standards = db_session.scalar(select(Agent).where(Agent.agent_id == "wise.agent.standards"))
    benchmark = db_session.scalar(select(Agent).where(Agent.agent_id == "wise.agent.benchmark"))
    assert standards is not None and standards.read_only is True
    assert benchmark is not None and benchmark.read_only is True
    assert standards.created_by == SEED_ACTOR


@pytest.mark.integration
def test_canonical_capabilities_seeded(orchestration_db_session: Session):
    db_session = orchestration_db_session
    count = db_session.scalar(select(func.count()).select_from(Capability))
    assert count == CANONICAL_CAPABILITY_COUNT


@pytest.mark.integration
def test_startup_registry_validation_passes(orchestration_db_session: Session):
    db_session = orchestration_db_session
    validate_registry_alignment(db_session)
