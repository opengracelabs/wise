"""RC1 propose endpoints for knowledge-graph-service."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from wise_reference.rc1_agents import propose_graph_entity

router = APIRouter(prefix="/v1/rc1", tags=["rc1"])


class GraphProposeRequest(BaseModel):
    stable_id: str
    entity_assertion_id: str


@router.post("/graph/propose")
def propose_graph_endpoint(body: GraphProposeRequest) -> dict:
    return propose_graph_entity(body.stable_id, entity_assertion_id=body.entity_assertion_id)
