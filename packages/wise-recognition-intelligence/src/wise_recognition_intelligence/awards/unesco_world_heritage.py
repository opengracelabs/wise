"""UNESCO World Heritage recognition signals."""

from __future__ import annotations

from typing import Any, Mapping

from wise_recognition_intelligence.awards import AwardSignal, first_present, signal_from_registry, text_contains

UNESCO_IDENTIFIER_KEYS = (
    "unesco_world_heritage_id",
    "unesco_whc_id",
    "world_heritage_id",
)
UNESCO_TEXT_KEYS = (
    "award_tags",
    "awards",
    "authority_links",
    "external_identifiers",
    "source_registry_refs",
)


def detect_unesco_world_heritage(asset: Mapping[str, Any]) -> list[AwardSignal]:
    """Detect UNESCO World Heritage authority on an asset."""

    identifier = first_present(asset, UNESCO_IDENTIFIER_KEYS)
    is_unesco = identifier is not None or text_contains(
        asset,
        UNESCO_TEXT_KEYS,
        ("unesco", "world heritage", "unesco-whc"),
    )
    if not is_unesco:
        return []

    evidence_uri = first_present(asset, ("unesco_source_uri", "source_uri", "evidence_uri"))
    return [signal_from_registry("unesco_world_heritage", evidence_uri=evidence_uri)]
