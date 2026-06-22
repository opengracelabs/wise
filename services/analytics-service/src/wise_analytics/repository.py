"""Persistence and aggregation for RC6 demand telemetry."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session
from wise_demand_intelligence import insights_from_user_events

from wise_analytics.models import UserEvent
from wise_analytics.schemas import CtaResponseConversion, EventCreate, InsightItem, InsightsResponse

CLICK_TYPES = {"collection_click", "series_click", "species_click"}


def create_event(db: Session, payload: EventCreate) -> UserEvent:
    event = UserEvent(
        type=payload.type,
        entity_id=payload.entity_id,
        entity_type=payload.entity_type,
        timestamp=payload.timestamp,
        session_id=payload.session_id,
        event_metadata=payload.metadata.model_dump(exclude_none=True),
    )
    db.add(event)
    db.flush()
    db.refresh(event)
    return event


def list_events(db: Session) -> list[UserEvent]:
    return list(db.scalars(select(UserEvent)))


def aggregate_insights(db: Session) -> InsightsResponse:
    events = list_events(db)
    if not events:
        return InsightsResponse(
            top_viewed_collections=[],
            top_clicked_species=[],
            top_series_engagement=[],
            cta_response_conversion_rate=CtaResponseConversion(),
            source="user_events",
        )

    return InsightsResponse(
        top_viewed_collections=_rank(events, entity_type="collection", ranking="views"),
        top_clicked_species=_rank(events, entity_type="species", ranking="clicks"),
        top_series_engagement=_rank(events, entity_type="series", ranking="engagement"),
        cta_response_conversion_rate=_cta_response_conversion(events),
        source="user_events",
    )


def _rank(events: Iterable[UserEvent], *, entity_type: str, ranking: str) -> list[InsightItem]:
    grouped: dict[str, InsightItem] = {}

    for event in events:
        normalized_type = _base_entity_type(event.entity_type)
        if normalized_type != entity_type:
            continue

        item = grouped.setdefault(
            event.entity_id,
            InsightItem(entity_id=event.entity_id, entity_type=normalized_type),
        )
        item.views += 1 if event.type == "page_view" else 0
        item.clicks += 1 if event.type in CLICK_TYPES else 0
        item.cta_clicks += 1 if event.type == "cta_click" else 0
        item.dwell_time += float((event.event_metadata or {}).get("dwell_time", 0) or 0)

    for item in grouped.values():
        item.engagement_score = _engagement_score_from_adapter(events, item.entity_type, item.entity_id)

    key_name = {
        "views": "views",
        "clicks": "clicks",
        "engagement": "engagement_score",
    }[ranking]
    return sorted(grouped.values(), key=lambda item: getattr(item, key_name), reverse=True)[:10]


def _cta_response_conversion(events: Iterable[UserEvent]) -> CtaResponseConversion:
    counts = defaultdict(int)
    for event in events:
        if event.type != "cta_click":
            continue
        response = _response_from_entity_type(event.entity_type)
        if response in {"yes", "maybe", "no"}:
            counts[response] += 1

    total = counts["yes"] + counts["maybe"] + counts["no"]
    return CtaResponseConversion(
        yes=counts["yes"],
        maybe=counts["maybe"],
        no=counts["no"],
        total=total,
    )


def _base_entity_type(entity_type: str) -> str:
    return entity_type.split(":", 1)[0]


def _response_from_entity_type(entity_type: str) -> str | None:
    parts = entity_type.split(":", 1)
    if len(parts) != 2:
        return None
    return parts[1]


def _engagement_score_from_adapter(events: Iterable[UserEvent], entity_type: str, entity_id: str) -> float:
    for insight in insights_from_user_events(events):
        if insight.entity_type == entity_type and insight.entity_id == entity_id:
            return insight.engagement_score
    return 0
