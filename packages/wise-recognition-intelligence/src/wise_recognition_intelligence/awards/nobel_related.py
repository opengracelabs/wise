"""Nobel Prize indirect relevance signals."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.awards import AwardSignal, first_present, signal_from_registry, text_contains

NOBEL_KEYS = (
    "nobel_prize_refs",
    "nobel_related",
    "associated_nobel_laureates",
)
NOBEL_TEXT_KEYS = (
    "award_tags",
    "awards",
    "associated_people",
    "subject_keywords",
    "description",
)


def detect_nobel_related(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Detect assets with indirect cultural or scientific Nobel relevance."""

    explicit_signal = first_present(asset, NOBEL_KEYS)
    is_nobel_related = bool(explicit_signal) or text_contains(asset, NOBEL_TEXT_KEYS, ("nobel", "laureate"))
    if not is_nobel_related:
        return []

    evidence_uri = first_present(asset, ("nobel_source_uri", "source_uri", "evidence_uri"))
    return [signal_from_registry("nobel_related", evidence_uri=evidence_uri)]
