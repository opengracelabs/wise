"""Wildlife conservation and natural-history award signals."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.awards import AwardSignal, first_present, signal_from_registry, text_contains

WILDLIFE_KEYS = (
    "wildlife_photographer_of_the_year_refs",
    "wildlife_conservation_awards",
    "wildlife_awards",
)
WILDLIFE_TEXT_KEYS = (
    "award_tags",
    "awards",
    "prizes",
    "description",
)


def detect_wildlife_conservation_awards(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Detect Wildlife Photographer of the Year and conservation-award signals."""

    explicit_signal = first_present(asset, WILDLIFE_KEYS)
    is_wildlife_award = bool(explicit_signal) or text_contains(
        asset,
        WILDLIFE_TEXT_KEYS,
        ("wildlife photographer of the year", "wildlife conservation award"),
    )
    if not is_wildlife_award:
        return []

    evidence_uri = first_present(asset, ("wildlife_award_source_uri", "source_uri", "evidence_uri"))
    return [signal_from_registry("wildlife_photographer", evidence_uri=evidence_uri)]
