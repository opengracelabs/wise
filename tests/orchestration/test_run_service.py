"""Integration tests for LangGraph run lifecycle."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import select

from wise_contracts.orchestration import RunResumeRequest, RunStartRequest
from wise_orchestration.validation import RegistryValidationError, validate_registry_alignment
from wise_orchestrator.run_service import RunService
from wise_registry.enums import RunStatus, StewardTaskStatus
from wise_registry.models import Agent, StewardTask


@pytest.fixture
def run_service(registry_database_url: str):
    service = RunService(registry_database_url)
    yield service
    service.close()


@pytest.mark.integration
def test_human_approval_gate_blocks_canonical_write_until_resume(
    orchestration_db_session,
    run_service: RunService,
):
    session = orchestration_db_session
    request = RunStartRequest(
        graph_id="source-discovery",
        agent_id="wise.agent.source-discovery",
        trigger_source="api",
    )
    run = run_service.start_run(session, request)
    assert run.status == RunStatus.INTERRUPTED

    task = session.scalar(select(StewardTask).where(StewardTask.thread_id == run.graph_thread_id))
    assert task is not None
    assert task.status == StewardTaskStatus.PENDING

    resumed = run_service.resume_run(
        session,
        run.graph_thread_id,
        RunResumeRequest(decision="approved", reviewer_id="steward-1"),
    )
    assert resumed.status == RunStatus.COMPLETED
    assert resumed.output_ref is not None
    assert resumed.output_ref.startswith("canonical://")


@pytest.mark.integration
def test_governance_agent_completes_without_canonical_write(
    orchestration_db_session,
    run_service: RunService,
):
    session = orchestration_db_session
    run = run_service.start_run(
        session,
        RunStartRequest(
            graph_id="standards",
            agent_id="wise.agent.standards",
            trigger_source="api",
        ),
    )
    assert run.status == RunStatus.COMPLETED
    assert run.output_ref is not None
    assert run.output_ref.startswith("governance-report://")

    tasks = session.scalars(
        select(StewardTask).where(StewardTask.thread_id == run.graph_thread_id)
    ).all()
    assert tasks == []


@pytest.mark.integration
def test_validation_fails_when_agent_removed_from_database(
    orchestration_db_session,
):
    session = orchestration_db_session
    agent = session.scalar(select(Agent).where(Agent.agent_id == "wise.agent.benchmark"))
    session.delete(agent)
    session.commit()

    with pytest.raises(RegistryValidationError, match="Agent ID mismatch"):
        validate_registry_alignment(session)
