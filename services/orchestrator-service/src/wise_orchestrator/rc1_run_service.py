"""RC1 pipeline run lifecycle — LangGraph with registry.agent_runs persistence."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_contracts.orchestration import RC1RunResumeRequest, RC1RunStartRequest
from wise_orchestration.checkpointer import create_checkpointer
from wise_orchestration.gates.approval import resume_with_approval
from wise_orchestration.graph import build_rc1_graph
from wise_orchestration.state import PipelineStage, initial_state_for_stonehenge
from wise_registry.enums import RunStatus, StewardTaskStatus
from wise_registry.models import AgentRun, StewardTask

RC1_PIPELINE_AGENT_ID = "wise.agent.source-discovery"


class RC1RunService:
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._checkpointer, self._pool = create_checkpointer(database_url)
        self._graph = build_rc1_graph(checkpointer=self._checkpointer)

    def close(self) -> None:
        self._pool.close()

    def _sync_run_from_state(
        self,
        run: AgentRun,
        snapshot_values: dict[str, Any],
        *,
        interrupted: bool,
    ) -> None:
        run.provenance_event_id = snapshot_values.get("current_provenance_event_id")
        if interrupted:
            run.status = RunStatus.INTERRUPTED
            gate = snapshot_values.get("approval_gate") or {}
            run.output_ref = f"rc1://{run.graph_thread_id}/{gate.get('stage', 'unknown')}"
            return
        stage = snapshot_values.get("current_stage")
        if stage == PipelineStage.COMPLETE.value:
            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.now(UTC)
            report = snapshot_values.get("pipeline_benchmark_report")
            run.output_ref = json.dumps(
                {
                    "stable_id": snapshot_values.get("stable_id"),
                    "provenance_chain": snapshot_values.get("provenance_chain"),
                    "pipeline_benchmark": report,
                },
                default=str,
            )
        elif stage == PipelineStage.FAILED.value:
            run.status = RunStatus.FAILED
            run.completed_at = datetime.now(UTC)

    def start_run(self, session: Session, request: RC1RunStartRequest) -> AgentRun:
        thread_id = str(uuid.uuid4())
        run = AgentRun(
            agent_id=RC1_PIPELINE_AGENT_ID,
            agent_version="0.1.0",
            graph_thread_id=thread_id,
            trigger_source=request.trigger_source,
            input_ref=f"stable_id:{request.stable_id}",
            status=RunStatus.RUNNING,
            created_by="orchestrator-service",
            updated_by="orchestrator-service",
        )
        session.add(run)
        session.flush()

        initial = initial_state_for_stonehenge(
            orchestrator_run_id=str(run.run_id),
            thread_id=thread_id,
        )
        initial["stable_id"] = request.stable_id

        config = {"configurable": {"thread_id": thread_id}}
        try:
            self._graph.invoke(initial, config=config)
            snapshot = self._graph.get_state(config)
            values = snapshot.values or {}
            interrupted = bool(snapshot.next)
            self._sync_run_from_state(run, values, interrupted=interrupted)
            if interrupted:
                session.add(
                    StewardTask(
                        run_id=run.run_id,
                        thread_id=thread_id,
                        agent_id=RC1_PIPELINE_AGENT_ID,
                        status=StewardTaskStatus.PENDING,
                        created_by="orchestrator-service",
                        updated_by="orchestrator-service",
                    )
                )
        except Exception:
            run.status = RunStatus.FAILED
            run.completed_at = datetime.now(UTC)
            session.commit()
            raise

        session.commit()
        session.refresh(run)
        return run

    def resume_run(
        self,
        session: Session,
        thread_id: str,
        request: RC1RunResumeRequest,
    ) -> AgentRun:
        run = session.scalar(select(AgentRun).where(AgentRun.graph_thread_id == thread_id))
        if run is None:
            raise KeyError(f"Unknown thread_id: {thread_id}")

        task = session.scalar(
            select(StewardTask)
            .where(StewardTask.thread_id == thread_id, StewardTask.status == StewardTaskStatus.PENDING)
            .order_by(StewardTask.created_at.desc())
        )
        if task is None:
            raise KeyError(f"No pending steward task for thread_id: {thread_id}")

        task.status = (
            StewardTaskStatus.APPROVED
            if request.decision == "approved"
            else StewardTaskStatus.REJECTED
        )
        task.reviewer_id = request.steward_id
        task.notes = request.rejection_reason
        task.resolved_at = datetime.now(UTC)
        task.updated_by = request.steward_id

        config = {"configurable": {"thread_id": thread_id}}
        resume_with_approval(
            self._graph,
            config,
            decision=request.decision,
            steward_id=request.steward_id,
            rejection_reason=request.rejection_reason,
        )

        snapshot = self._graph.get_state(config)
        values = snapshot.values or {}
        interrupted = bool(snapshot.next)
        self._sync_run_from_state(run, values, interrupted=interrupted)
        if interrupted and request.decision == "approved":
            session.add(
                StewardTask(
                    run_id=run.run_id,
                    thread_id=thread_id,
                    agent_id=RC1_PIPELINE_AGENT_ID,
                    status=StewardTaskStatus.PENDING,
                    created_by="orchestrator-service",
                    updated_by="orchestrator-service",
                )
            )

        session.commit()
        session.refresh(run)
        return run

    def get_run(self, session: Session, thread_id: str) -> AgentRun | None:
        return session.scalar(select(AgentRun).where(AgentRun.graph_thread_id == thread_id))

    def get_graph_state(self, thread_id: str) -> dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        snapshot = self._graph.get_state(config)
        return snapshot.values or {}
