"""RC6 analytics event tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from wise_analytics.repository import aggregate_insights, create_event
from wise_analytics.schemas import EventCreate


def _event(
    *,
    type: str = "page_view",
    entity_id: str = "big-cats-of-the-world",
    entity_type: str = "collection",
    session_id: str = "anon_test_session",
    metadata: dict | None = None,
) -> EventCreate:
    return EventCreate(
        type=type,
        entity_id=entity_id,
        entity_type=entity_type,
        timestamp=datetime(2026, 6, 22, 12, 0, tzinfo=UTC),
        session_id=session_id,
        metadata=metadata or {},
    )


def test_event_schema_validation_accepts_allowed_event():
    payload = _event(metadata={"dwell_time": 12.5, "referrer": "https://example.org", "device_type": "desktop"})

    assert payload.type == "page_view"
    assert payload.metadata.dwell_time == 12.5


def test_event_schema_validation_rejects_extra_metadata():
    with pytest.raises(ValidationError):
        _event(metadata={"email": "person@example.org"})


def test_anonymous_session_behavior_rejects_personal_identifier():
    with pytest.raises(ValidationError):
        _event(session_id="person@example.org")

    with pytest.raises(ValidationError):
        _event(session_id="customer_123")


def test_event_persistence(analytics_session):
    event = create_event(analytics_session, _event(metadata={"dwell_time": 7}))
    analytics_session.commit()

    assert event.id is not None
    assert event.entity_id == "big-cats-of-the-world"
    assert event.event_metadata["dwell_time"] == 7


def test_insights_aggregation(analytics_session):
    events = [
        _event(type="page_view", entity_id="big-cats-of-the-world", entity_type="collection", metadata={"dwell_time": 20}),
        _event(type="collection_click", entity_id="big-cats-of-the-world", entity_type="collection"),
        _event(type="page_view", entity_id="endangered-earth", entity_type="series", metadata={"dwell_time": 9}),
        _event(type="series_click", entity_id="endangered-earth", entity_type="series"),
        _event(type="species_click", entity_id="panthera-leo", entity_type="species"),
        _event(type="cta_click", entity_id="big-cats-of-the-world", entity_type="collection:yes"),
        _event(type="cta_click", entity_id="endangered-earth", entity_type="series:maybe"),
    ]
    for payload in events:
        create_event(analytics_session, payload)
    analytics_session.commit()

    insights = aggregate_insights(analytics_session)

    assert insights.top_viewed_collections[0].entity_id == "big-cats-of-the-world"
    assert insights.top_clicked_species[0].entity_id == "panthera-leo"
    assert insights.top_series_engagement[0].entity_id == "endangered-earth"
    assert insights.cta_response_conversion_rate.yes == 1
    assert insights.cta_response_conversion_rate.maybe == 1
    assert insights.cta_response_conversion_rate.no == 0
