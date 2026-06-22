"""Registry provenance event helpers for discovery agent."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from wise_registry.enums import ProvenanceEventType
from wise_registry.models.provenance_event import ProvenanceEvent
from wise_registry.provenance import validate_event_link

AGENT_VERSION = "discovery-agent@1.0.0"


def _latest_source_event(session: Session, source_id: UUID) -> ProvenanceEvent | None:
    return session.scalar(
        select(ProvenanceEvent)
        .where(ProvenanceEvent.source_id == source_id)
        .order_by(ProvenanceEvent.event_timestamp.desc())
    )


def append_provenance_event(
    session: Session,
    *,
    source_id: UUID,
    event_type: ProvenanceEventType = ProvenanceEventType.HARVEST,
    evidence_uris: list[str],
    actor: str = AGENT_VERSION,
    notes: str | None = None,
    previous_event_id: UUID | None = None,
) -> ProvenanceEvent:
    """Append a registry provenance event, preserving previous_event_id chain."""
    previous_event: ProvenanceEvent | None = None
    if previous_event_id is None:
        previous_event = _latest_source_event(session, source_id)
        previous_event_id = previous_event.id if previous_event else None
    else:
        previous_event = session.get(ProvenanceEvent, previous_event_id)

    validate_event_link(source_id, None, previous_event_id, previous_event)

    event = ProvenanceEvent(
        source_id=source_id,
        event_type=event_type,
        event_timestamp=datetime.now(timezone.utc),
        actor=actor,
        evidence_uris=evidence_uris,
        notes=notes,
        previous_event_id=previous_event_id,
        created_by=AGENT_VERSION,
        updated_by=AGENT_VERSION,
    )
    session.add(event)
    session.flush()
    return event
