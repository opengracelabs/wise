"""Unit tests for provenance chain validation."""

from __future__ import annotations

from uuid import uuid4

import pytest

from wise_registry.provenance import ProvenanceChainError, validate_chain, validate_event_link


def _event(
    *,
    source_id=None,
    previous_event_id=None,
    event_id=None,
):
    """Minimal stand-in for ProvenanceEvent in unit tests."""

    class Stub:
        pass

    stub = Stub()
    stub.id = event_id or uuid4()
    stub.source_id = source_id or uuid4()
    stub.previous_event_id = previous_event_id
    return stub


def test_validate_event_link_accepts_no_previous():
    source_id = uuid4()
    validate_event_link(source_id, uuid4(), None, None)


def test_validate_event_link_accepts_valid_previous():
    source_id = uuid4()
    previous = _event(source_id=source_id)
    event_id = uuid4()
    validate_event_link(source_id, event_id, previous.id, previous)


def test_validate_event_link_rejects_self_reference():
    source_id = uuid4()
    event_id = uuid4()
    previous = _event(source_id=source_id, event_id=event_id)
    with pytest.raises(ProvenanceChainError, match="same event"):
        validate_event_link(source_id, event_id, event_id, previous)


def test_validate_event_link_rejects_missing_previous():
    source_id = uuid4()
    missing_id = uuid4()
    with pytest.raises(ProvenanceChainError, match="does not reference an existing event"):
        validate_event_link(source_id, uuid4(), missing_id, None)


def test_validate_event_link_rejects_source_mismatch():
    previous = _event(source_id=uuid4())
    with pytest.raises(ProvenanceChainError, match="same source_id"):
        validate_event_link(uuid4(), uuid4(), previous.id, previous)


def test_validate_chain_accepts_linear_chain():
    source_id = uuid4()
    first = _event(source_id=source_id)
    second = _event(source_id=source_id, previous_event_id=first.id)
    third = _event(source_id=source_id, previous_event_id=second.id)
    validate_chain([first, second, third])


def test_validate_chain_rejects_cycle():
    source_id = uuid4()
    a = _event(source_id=source_id)
    b = _event(source_id=source_id, previous_event_id=a.id)
    c = _event(source_id=source_id, previous_event_id=b.id)
    a.previous_event_id = c.id
    with pytest.raises(ProvenanceChainError, match="cycle detected"):
        validate_chain([a, b, c])


def test_validate_chain_rejects_mixed_sources():
    first = _event()
    second = _event(previous_event_id=first.id)
    with pytest.raises(ProvenanceChainError, match="same source_id"):
        validate_chain([first, second])


def test_validate_chain_rejects_broken_link():
    source_id = uuid4()
    missing_id = uuid4()
    event = _event(source_id=source_id, previous_event_id=missing_id)
    with pytest.raises(ProvenanceChainError, match="unknown previous_event_id"):
        validate_chain([event])
