"""RC6 demand telemetry schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

EventType = Literal[
    "page_view",
    "collection_click",
    "series_click",
    "species_click",
    "cta_click",
]


class EventMetadata(BaseModel):
    """Allowed anonymous event metadata fields."""

    model_config = ConfigDict(extra="forbid")

    dwell_time: float | None = Field(default=None, ge=0, le=86_400)
    referrer: str | None = Field(default=None, max_length=512)
    device_type: str | None = Field(default=None, max_length=64)

    @field_validator("referrer", "device_type")
    @classmethod
    def reject_obvious_personal_data(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if "@" in value:
            raise ValueError("personal identifiers are not allowed in telemetry metadata")
        return value


class EventCreate(BaseModel):
    """Anonymous telemetry event accepted by POST /api/events."""

    model_config = ConfigDict(extra="forbid")

    type: EventType
    entity_id: str = Field(min_length=1, max_length=256)
    entity_type: str = Field(min_length=1, max_length=128)
    timestamp: datetime
    session_id: str = Field(min_length=8, max_length=128)
    metadata: EventMetadata = Field(default_factory=EventMetadata)

    @field_validator("entity_id", "entity_type", "session_id")
    @classmethod
    def reject_personal_identifiers(cls, value: str) -> str:
        if "@" in value:
            raise ValueError("personal identifiers are not allowed in telemetry fields")
        return value

    @model_validator(mode="after")
    def require_anonymous_session(self) -> "EventCreate":
        if not self.session_id.startswith("anon_"):
            raise ValueError("session_id must be anonymous and start with 'anon_'")
        return self


class EventRead(BaseModel):
    id: int
    type: EventType
    entity_id: str
    entity_type: str
    timestamp: datetime
    session_id: str
    metadata: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InsightItem(BaseModel):
    entity_id: str
    entity_type: str
    views: int = 0
    clicks: int = 0
    cta_clicks: int = 0
    dwell_time: float = 0
    engagement_score: float = 0


class CtaResponseConversion(BaseModel):
    yes: int = 0
    maybe: int = 0
    no: int = 0
    total: int = 0


class InsightsResponse(BaseModel):
    top_viewed_collections: list[InsightItem]
    top_clicked_species: list[InsightItem]
    top_series_engagement: list[InsightItem]
    cta_response_conversion_rate: CtaResponseConversion
    source: Literal["user_events", "synthetic_fallback"] = "user_events"
