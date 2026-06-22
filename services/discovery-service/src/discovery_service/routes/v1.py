"""Source Discovery Agent v1 endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from wise_discovery.evidence import evidence_profile_to_json
from wise_discovery.schemas.discovery_record import DiscoveryRecordCreate, DiscoveryRecordRead
from wise_discovery.services.agent import (
    check_reachability,
    create_discovery_record,
    lookup_source,
    propagate_rights_posture,
    validate_source,
)
from wise_registry.session import create_session_factory

router = APIRouter(prefix="/v1/discovery", tags=["discovery"])

_session_factory = None


def _factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = create_session_factory()
    return _session_factory


def get_db():
    session = _factory()()
    try:
        yield session
    finally:
        session.close()


class SourceLookupResponse(BaseModel):
    id: UUID
    canonical_name: str
    stable_id: str
    display_name: str
    active: bool


class ReachabilityRequest(BaseModel):
    source_id: UUID | None = None
    canonical_name: str | None = None
    stable_id: str | None = None


class ValidateSourceRequest(BaseModel):
    source_id: UUID | None = None
    canonical_name: str | None = None
    stable_id: str | None = None
    require_license: bool = False


@router.get("/sources/{canonical_name}", response_model=SourceLookupResponse)
def get_source(
    canonical_name: str,
    db: Annotated[Session, Depends(get_db)],
) -> SourceLookupResponse:
    try:
        source = lookup_source(db, canonical_name=canonical_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return SourceLookupResponse(
        id=source.id,
        canonical_name=source.canonical_name,
        stable_id=source.stable_id,
        display_name=source.display_name,
        active=source.active,
    )


@router.post("/sources/validate")
def validate_registered_source(
    body: ValidateSourceRequest,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    try:
        source = lookup_source(
            db,
            source_id=body.source_id,
            canonical_name=body.canonical_name,
            stable_id=body.stable_id,
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    outcome = validate_source(source, require_license=body.require_license)
    return {
        "status": outcome.status,
        "severity": outcome.severity,
        "findings": outcome.findings,
        "evidence": evidence_profile_to_json(outcome.evidence),
    }


@router.post("/sources/reachability")
def probe_reachability(
    body: ReachabilityRequest,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    try:
        source = lookup_source(
            db,
            source_id=body.source_id,
            canonical_name=body.canonical_name,
            stable_id=body.stable_id,
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = check_reachability(source)
    return result.model_dump()


@router.get("/sources/{canonical_name}/rights")
def get_rights_posture(
    canonical_name: str,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    try:
        source = lookup_source(db, canonical_name=canonical_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return propagate_rights_posture(source).model_dump()


@router.post("/records", response_model=DiscoveryRecordRead)
def create_record(
    body: DiscoveryRecordCreate,
    db: Annotated[Session, Depends(get_db)],
    skip_reachability: bool = False,
) -> DiscoveryRecord:
    try:
        record = create_discovery_record(
            db,
            payload=body,
            skip_reachability=skip_reachability,
        )
        db.commit()
    except (KeyError, ValueError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return record
