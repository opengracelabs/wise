"""Agent run lifecycle — LangGraph invoke, interrupt, resume."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from langgraph.types import Command
from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_contracts.common import ApprovalStatus
from wise_contracts.orchestration import RunResumeRequest, RunStartRequest
from wise_orchestration.checkpointer import create_checkpointer
from wise_orchestration.nodes import CanonicalWriteForbiddenError
from wise_orchestration.registry import get_compiled_graph
from wise_registry.enums import RunStatus, StewardTaskStatus
from wise_registry.models import Agent, AgentRun, StewardTask


class RunService:
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._checkpointer, self._pool = create_checkpointer(database_url)

    def close(self) -> None:
        self._pool.close()

    def start_run(self, session: Session, request: RunStartRequest) -> AgentRun:
        agent = session.scalar(select(Agent).where(Agent.agent_id == request.agent_id))
        if agent is None:
            raise KeyError(f"Unknown agent_id: {request.agent_id}")
        if agent.langgraph_graph_id != request.graph_id:
            raise ValueError(
                f"graph_id {request.graph_id!r} does not match agent graph {agent.langgraph_graph_id!r}"
            )

        thread_id = str(uuid.uuid4())
        run = AgentRun(
            agent_id=agent.agent_id,
            agent_version="0.1.0",
            graph_thread_id=thread_id,
            trigger_source=request.trigger_source,
            input_ref=request.input_ref,
            status=RunStatus.RUNNING,
            created_by="orchestrator-service",
            updated_by="orchestrator-service",
        )
        session.add(run)
        session.flush()

        graph = get_compiled_graph(agent.langgraph_graph_id, checkpointer=self._checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
        initial_state = {
            "run_id": str(run.run_id),
            "thread_id": thread_id,
            "agent_id": agent.agent_id,
            "agent_version": run.agent_version,
            "graph_id": agent.langgraph_graph_id,
            "read_only": agent.read_only,
            "input_ref": request.input_ref,
            "approval_status": ApprovalStatus.PROPOSED.value,
            "errors": [],
        }

        try:
            graph.invoke(initial_state, config=config)
            snapshot = graph.get_state(config)
            values = snapshot.values or {}

            if snapshot.next:
                run.status = RunStatus.INTERRUPTED
                session.add(
                    StewardTask(
                        run_id=run.run_id,
                        thread_id=thread_id,
                        agent_id=agent.agent_id,
                        status=StewardTaskStatus.PENDING,
                        created_by="orchestrator-service",
                        updated_by="orchestrator-service",
                    )
                )
            elif agent.read_only:
                run.status = RunStatus.COMPLETED
                run.output_ref = values.get("output_ref")
                run.completed_at = datetime.now(UTC)
            else:
                run.status = RunStatus.COMPLETED
                run.output_ref = values.get("output_ref")
                run.completed_at = datetime.now(UTC)
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
        request: RunResumeRequest,
    ) -> AgentRun:
        run = session.scalar(
            select(AgentRun).where(AgentRun.graph_thread_id == thread_id)
        )
        if run is None:
            raise KeyError(f"Unknown thread_id: {thread_id}")

        agent = session.scalar(select(Agent).where(Agent.agent_id == run.agent_id))
        if agent is None:
            raise KeyError(f"Agent missing for run: {run.agent_id}")

        task = session.scalar(
            select(StewardTask)
            .where(StewardTask.thread_id == thread_id)
            .order_by(StewardTask.created_at.desc())
        )
        if task is None:
            raise KeyError(f"No steward task for thread_id: {thread_id}")
        if task.status != StewardTaskStatus.PENDING:
            raise ValueError(f"Steward task already resolved: {task.status.value}")

        task.status = (
            StewardTaskStatus.APPROVED
            if request.decision == "approved"
            else StewardTaskStatus.REJECTED
        )
        task.reviewer_id = request.reviewer_id
        task.notes = request.notes
        task.resolved_at = datetime.now(UTC)
        task.updated_by = request.reviewer_id

        graph = get_compiled_graph(agent.langgraph_graph_id, checkpointer=self._checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
        resume_payload = {
            "decision": request.decision,
            "reviewer_id": request.reviewer_id,
            "notes": request.notes,
        }

        try:
            graph.invoke(Command(resume=resume_payload), config=config)
            snapshot = graph.get_state(config)
            values = snapshot.values or {}
        except CanonicalWriteForbiddenError:
            run.status = RunStatus.FAILED
            run.completed_at = datetime.now(UTC)
            session.commit()
            raise

        if request.decision == "rejected":
            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.now(UTC)
        else:
            run.status = RunStatus.COMPLETED
            run.output_ref = values.get("output_ref")
            run.completed_at = datetime.now(UTC)

        session.commit()
        session.refresh(run)
        return run

    def get_run(self, session: Session, thread_id: str) -> AgentRun | None:
        return session.scalar(select(AgentRun).where(AgentRun.graph_thread_id == thread_id))
