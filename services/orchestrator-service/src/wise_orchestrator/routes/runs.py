"""Agent run invoke and resume API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wise_contracts.orchestration import AgentRunRecord, RunResumeRequest, RunStartRequest
from wise_orchestrator.database import get_db
from wise_orchestrator.dependencies import get_run_service
from wise_orchestrator.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"])


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
def start_run(
    request: RunStartRequest,
    session: Session = Depends(get_db),
    run_service: RunService = Depends(get_run_service),
) -> AgentRunRecord:
    try:
        run = run_service.start_run(session, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_record(run)


@router.get("/{thread_id}", response_model=AgentRunRecord)
def get_run(
    thread_id: str,
    session: Session = Depends(get_db),
    run_service: RunService = Depends(get_run_service),
) -> AgentRunRecord:
    run = run_service.get_run(session, thread_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Unknown thread_id: {thread_id}")
    return _to_record(run)


@router.post("/{thread_id}/resume", response_model=AgentRunRecord)
def resume_run(
    thread_id: str,
    request: RunResumeRequest,
    session: Session = Depends(get_db),
    run_service: RunService = Depends(get_run_service),
) -> AgentRunRecord:
    try:
        run = run_service.resume_run(session, thread_id, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return _to_record(run)
