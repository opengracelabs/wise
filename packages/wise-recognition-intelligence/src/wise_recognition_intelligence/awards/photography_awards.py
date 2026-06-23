"""Photography, editorial-selection, and featured-collection signals."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.awards import AwardSignal, first_present, signal_from_registry, text_contains

NATIONAL_GEOGRAPHIC_KEYS = (
    "national_geographic_awards",
    "natgeo_awards",
    "national_geographic_featured",
)
SMITHSONIAN_KEYS = (
    "smithsonian_featured_collection",
    "smithsonian_featured",
)
MAJOR_PHOTOGRAPHY_KEYS = (
    "photography_awards",
    "major_photography_awards",
)
TEXT_KEYS = (
    "award_tags",
    "awards",
    "featured_collections",
    "editorial_selections",
    "description",
)


def detect_photography_awards(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Detect National Geographic, Smithsonian, and major photography recognition."""

    signals: list[AwardSignal] = []

    if first_present(asset, NATIONAL_GEOGRAPHIC_KEYS) or text_contains(
        asset,
        TEXT_KEYS,
        ("national geographic", "natgeo"),
    ):
        signals.append(
            signal_from_registry(
                "national_geographic",
                evidence_uri=first_present(asset, ("national_geographic_source_uri", "source_uri", "evidence_uri")),
            )
        )

    if first_present(asset, SMITHSONIAN_KEYS) or text_contains(asset, TEXT_KEYS, ("smithsonian",)):
        signals.append(
            signal_from_registry(
                "smithsonian_featured",
                evidence_uri=first_present(asset, ("smithsonian_source_uri", "source_uri", "evidence_uri")),
            )
        )

    if first_present(asset, MAJOR_PHOTOGRAPHY_KEYS) or text_contains(
        asset,
        TEXT_KEYS,
        ("sony world photography", "world press photo", "hasselblad award", "major photography award"),
    ):
        signals.append(
            signal_from_registry(
                "major_photography_award",
                evidence_uri=first_present(asset, ("photography_award_source_uri", "source_uri", "evidence_uri")),
            )
        )

    return signals
