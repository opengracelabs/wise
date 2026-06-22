"""Demand insight aggregation for real and synthetic telemetry inputs."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping, Protocol


class UserEventLike(Protocol):
    type: str
    entity_id: str
    entity_type: str
    event_metadata: Mapping[str, object]


@dataclass(frozen=True)
class DemandInsight:
    entity_id: str
    entity_type: str
    views: int
    clicks: int
    cta_clicks: int
    dwell_time: float
    engagement_score: float


@dataclass(frozen=True)
class SyntheticFallback:
    reason: str
    insights: tuple[DemandInsight, ...]


def insights_from_user_events(events: Iterable[UserEventLike]) -> tuple[DemandInsight, ...]:
    grouped: dict[tuple[str, str], dict[str, float]] = defaultdict(
        lambda: {"views": 0, "clicks": 0, "cta_clicks": 0, "dwell_time": 0}
    )

    for event in events:
        entity_type = event.entity_type.split(":", 1)[0]
        bucket = grouped[(entity_type, event.entity_id)]
        bucket["views"] += 1 if event.type == "page_view" else 0
        bucket["clicks"] += 1 if event.type in {"collection_click", "series_click", "species_click"} else 0
        bucket["cta_clicks"] += 1 if event.type == "cta_click" else 0
        bucket["dwell_time"] += float(event.event_metadata.get("dwell_time", 0) or 0)

    return tuple(
        sorted(
            (
                DemandInsight(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    views=int(values["views"]),
                    clicks=int(values["clicks"]),
                    cta_clicks=int(values["cta_clicks"]),
                    dwell_time=values["dwell_time"],
                    engagement_score=round(
                        values["clicks"]
                        + values["dwell_time"]
                        + (values["cta_clicks"] / values["views"] if values["views"] else 0),
                        2,
                    ),
                )
                for (entity_type, entity_id), values in grouped.items()
            ),
            key=lambda item: item.engagement_score,
            reverse=True,
        )
    )


def synthetic_demo_insights(reason: str = "no user_events available") -> SyntheticFallback:
    return SyntheticFallback(
        reason=reason,
        insights=(
            DemandInsight(
                entity_id="big-cats-of-the-world",
                entity_type="collection",
                views=1,
                clicks=1,
                cta_clicks=1,
                dwell_time=12,
                engagement_score=14,
            ),
            DemandInsight(
                entity_id="endangered-earth",
                entity_type="series",
                views=1,
                clicks=1,
                cta_clicks=0,
                dwell_time=8,
                engagement_score=9,
            ),
        ),
    )
