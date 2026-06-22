"""Registry read API."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_contracts.orchestration import (
    AgentRegistryEntry,
    CapabilityAgentLink,
    CapabilityRegistryEntry,
)
from wise_orchestrator.database import get_db
from wise_registry.models import Agent, Capability, CapabilityAgent

router = APIRouter(prefix="/registry", tags=["registry"])


@router.get("/agents", response_model=list[AgentRegistryEntry])
def list_agents(session: Session = Depends(get_db)) -> list[AgentRegistryEntry]:
    agents = session.scalars(select(Agent).order_by(Agent.spec_prefix)).all()
    return [
        AgentRegistryEntry(
            agent_id=a.agent_id,
            spec_prefix=a.spec_prefix,
            spec_path=a.spec_path,
            display_name=a.display_name,
            plane=a.plane.value,
            build_phase=a.build_phase,
            service_binding=a.service_binding,
            langgraph_graph_id=a.langgraph_graph_id,
            output_schema_uri=a.output_schema_uri,
            evidence_profile=a.evidence_profile,
            read_only=a.read_only,
            status=a.status.value,
        )
        for a in agents
    ]


@router.get("/capabilities", response_model=list[CapabilityRegistryEntry])
def list_capabilities(session: Session = Depends(get_db)) -> list[CapabilityRegistryEntry]:
    caps = session.scalars(select(Capability).order_by(Capability.build_phase.nulls_last())).all()
    return [
        CapabilityRegistryEntry(
            capability_id=c.capability_id,
            canonical_section=c.canonical_section,
            display_name=c.display_name,
            build_phase=c.build_phase,
            plane=c.plane.value,
            contract_producer=c.contract_producer,
            contract_consumer=c.contract_consumer,
            status=c.status,
        )
        for c in caps
    ]


@router.get("/capability-agents", response_model=list[CapabilityAgentLink])
def list_capability_agents(session: Session = Depends(get_db)) -> list[CapabilityAgentLink]:
    links = session.scalars(select(CapabilityAgent)).all()
    return [
        CapabilityAgentLink(
            capability_id=link.capability_id,
            agent_id=link.agent_id,
            role=link.role.value,
        )
        for link in links
    ]
