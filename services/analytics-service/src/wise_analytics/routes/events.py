"""Telemetry ingestion routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from wise_analytics.database import get_db
from wise_analytics.repository import aggregate_insights, create_event
from wise_analytics.schemas import EventCreate, EventRead, InsightsResponse

router = APIRouter(tags=["analytics"])


@router.post("/api/events", response_model=EventRead, status_code=201)
def post_event(payload: EventCreate, db: Annotated[Session, Depends(get_db)]) -> EventRead:
    event = create_event(db, payload)
    db.commit()
    return EventRead(
        id=event.id,
        type=event.type,
        entity_id=event.entity_id,
        entity_type=event.entity_type,
        timestamp=event.timestamp,
        session_id=event.session_id,
        metadata=event.event_metadata,
        created_at=event.created_at,
    )


@router.get("/admin/insights", response_model=InsightsResponse)
def get_admin_insights(db: Annotated[Session, Depends(get_db)]) -> InsightsResponse:
    return aggregate_insights(db)
