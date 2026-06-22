"""RC1 propose endpoints for discovery-service."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from wise_reference.rc1_agents import propose_discovery_record
from wise_registry.session import create_session_factory

router = APIRouter(prefix="/v1/rc1", tags=["rc1"])

_session_factory = None


def _factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = create_session_factory()
    return _session_factory


class DiscoveryProposeRequest(BaseModel):
    stable_id: str


def get_db():
    session = _factory()()
    try:
        yield session
    finally:
        session.close()


@router.post("/discovery/propose")
def propose_discovery(
    body: DiscoveryProposeRequest,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    return propose_discovery_record(body.stable_id, db)
