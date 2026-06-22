"""Pulitzer Prize recognition signals."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.awards import AwardSignal, first_present, signal_from_registry, text_contains

PULITZER_KEYS = (
    "pulitzer_prize_refs",
    "pulitzer_winner",
    "pulitzer_finalist",
)
PULITZER_TEXT_KEYS = (
    "award_tags",
    "awards",
    "prizes",
    "description",
)


def detect_pulitzer(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Detect Pulitzer photography or journalism archive recognition."""

    explicit_signal = first_present(asset, PULITZER_KEYS)
    is_pulitzer = bool(explicit_signal) or text_contains(asset, PULITZER_TEXT_KEYS, ("pulitzer",))
    if not is_pulitzer:
        return []

    evidence_uri = first_present(asset, ("pulitzer_source_uri", "source_uri", "evidence_uri"))
    return [signal_from_registry("pulitzer", evidence_uri=evidence_uri)]
