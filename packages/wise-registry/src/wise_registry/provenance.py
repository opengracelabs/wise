"""Provenance chain validation for registry provenance events."""

from __future__ import annotations

from uuid import UUID

from wise_registry.models.provenance_event import ProvenanceEvent


class ProvenanceChainError(ValueError):
    """Raised when a provenance chain fails integrity checks."""


def validate_event_link(
    source_id: UUID,
    event_id: UUID | None,
    previous_event_id: UUID | None,
    previous_event: ProvenanceEvent | None,
) -> None:
    """Validate that an event may link to a previous event in the chain."""
    if previous_event_id is None:
        return

    if event_id is not None and previous_event_id == event_id:
        raise ProvenanceChainError("previous_event_id cannot reference the same event")

    if previous_event is None:
        raise ProvenanceChainError(
            f"previous_event_id {previous_event_id} does not reference an existing event"
        )

    if previous_event.id != previous_event_id:
        raise ProvenanceChainError("previous_event does not match previous_event_id")

    if previous_event.source_id != source_id:
        raise ProvenanceChainError(
            "previous_event_id must reference an event for the same source_id"
        )


def _walk_previous_chain(
    event: ProvenanceEvent,
    events_by_id: dict[UUID, ProvenanceEvent],
) -> None:
    """Follow previous_event_id pointers and raise if a cycle is detected."""
    visited: set[UUID] = {event.id}
    current = event

    while current.previous_event_id is not None:
        if current.previous_event_id in visited:
            raise ProvenanceChainError(
                f"cycle detected at event {current.id} -> {current.previous_event_id}"
            )
        previous = events_by_id.get(current.previous_event_id)
        if previous is None:
            raise ProvenanceChainError(
                f"broken chain: event {current.id} references missing "
                f"previous_event_id {current.previous_event_id}"
            )
        if previous.source_id != current.source_id:
            raise ProvenanceChainError(
                f"chain source mismatch: event {current.id} and previous "
                f"{previous.id} belong to different sources"
            )
        visited.add(current.previous_event_id)
        current = previous


def validate_chain(events: list[ProvenanceEvent]) -> None:
    """Validate provenance chain integrity: same source, no cycles, no broken links."""
    if not events:
        return

    events_by_id = {event.id: event for event in events}
    source_ids = {event.source_id for event in events}
    if len(source_ids) > 1:
        raise ProvenanceChainError("all events in a chain must share the same source_id")

    for event in events:
        if event.previous_event_id is not None and event.previous_event_id == event.id:
            raise ProvenanceChainError(f"event {event.id} cannot reference itself")

        if event.previous_event_id is not None and event.previous_event_id not in events_by_id:
            raise ProvenanceChainError(
                f"event {event.id} references unknown previous_event_id "
                f"{event.previous_event_id}"
            )

        _walk_previous_chain(event, events_by_id)
