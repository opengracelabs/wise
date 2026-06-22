"""RC1 propose endpoints for preservation-service."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from wise_reference.rc1_agents import propose_preservation

router = APIRouter(prefix="/v1/rc1", tags=["rc1"])


class PreservationProposeRequest(BaseModel):
    stable_id: str
    discovery_record_id: str


@router.post("/preservation/propose")
def propose_preservation_endpoint(body: PreservationProposeRequest) -> dict:
    return propose_preservation(
        body.stable_id,
        discovery_record_id=body.discovery_record_id,
    )
