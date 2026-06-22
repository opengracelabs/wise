"""RC1 pipeline orchestration API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wise_contracts.orchestration import AgentRunRecord, RC1RunResumeRequest, RC1RunStartRequest
from wise_orchestrator.database import get_db
from wise_orchestrator.dependencies import get_rc1_run_service
from wise_orchestrator.rc1_run_service import RC1RunService

router = APIRouter(prefix="/rc1/runs", tags=["rc1"])


def _to_record(run) -> AgentRunRecord:
    return AgentRunRecord(
        run_id=run.run_id,
        agent_id=run.agent_id,
        agent_version=run.agent_version,
        graph_thread_id=run.graph_thread_id,
        trigger_source=run.trigger_source,
        input_ref=run.input_ref,
        output_ref=run.output_ref,
        status=run.status.value,
        provenance_event_id=run.provenance_event_id,
        started_at=run.started_at,
        completed_at=run.completed_at,
    )


@router.post("", response_model=AgentRunRecord, status_code=201)
def start_rc1_run(
    request: RC1RunStartRequest,
    session: Session = Depends(get_db),
    rc1_service: RC1RunService = Depends(get_rc1_run_service),
) -> AgentRunRecord:
    try:
        run = rc1_service.start_run(session, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_record(run)


@router.get("/{thread_id}", response_model=AgentRunRecord)
def get_rc1_run(
    thread_id: str,
    session: Session = Depends(get_db),
    rc1_service: RC1RunService = Depends(get_rc1_run_service),
) -> AgentRunRecord:
    run = rc1_service.get_run(session, thread_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Unknown thread_id: {thread_id}")
    return _to_record(run)


@router.get("/{thread_id}/state")
def get_rc1_graph_state(
    thread_id: str,
    rc1_service: RC1RunService = Depends(get_rc1_run_service),
) -> dict:
    return rc1_service.get_graph_state(thread_id)


@router.post("/{thread_id}/resume", response_model=AgentRunRecord)
def resume_rc1_run(
    thread_id: str,
    request: RC1RunResumeRequest,
    session: Session = Depends(get_db),
    rc1_service: RC1RunService = Depends(get_rc1_run_service),
) -> AgentRunRecord:
    try:
        run = rc1_service.resume_run(session, thread_id, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_record(run)
