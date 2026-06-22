"""RC1 propose endpoints for metadata-service (agents 10 + 13)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from wise_reference.rc1_agents import propose_metadata, propose_quality_review

router = APIRouter(prefix="/v1/rc1", tags=["rc1"])


class MetadataProposeRequest(BaseModel):
    stable_id: str
    preserved_object_ark: str


class QualityProposeRequest(BaseModel):
    stable_id: str
    graph_entity_uri: str


@router.post("/metadata/propose")
def propose_metadata_endpoint(body: MetadataProposeRequest) -> dict:
    return propose_metadata(body.stable_id, preserved_object_ark=body.preserved_object_ark)


@router.post("/quality/propose")
def propose_quality_endpoint(body: QualityProposeRequest) -> dict:
    return propose_quality_review(body.stable_id, graph_entity_uri=body.graph_entity_uri)
