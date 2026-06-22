"""Award and prize signal detection for recognition scoring."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class AwardSignal:
    """Normalized award or editorial-recognition signal."""

    tag: str
    source: str
    weight: int
    label: str
    evidence_uri: str | None = None
    confidence: float = 1.0


def load_award_registry() -> dict[str, Any]:
    """Load the local award scoring registry bundled with the package."""

    registry_path = resources.files("wise_recognition_intelligence.datasets").joinpath("award_registry.json")
    return json.loads(registry_path.read_text(encoding="utf-8"))


def registry_source(source_key: str) -> Mapping[str, Any]:
    """Return registry metadata for a source key."""

    return load_award_registry()["sources"][source_key]


def first_present(asset: Mapping[str, Any], keys: Iterable[str]) -> Any:
    """Return the first non-empty asset value for any known key."""

    for key in keys:
        value = asset.get(key)
        if value not in (None, "", [], {}, ()):
            return value
    return None


def as_list(value: Any) -> list[Any]:
    """Normalize scalar, tuple, set, or list values into a list."""

    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple | set):
        return list(value)
    return [value]


def text_contains(asset: Mapping[str, Any], keys: Iterable[str], tokens: Iterable[str]) -> bool:
    """Check whether any configured field contains one of the tokens."""

    lowered_tokens = tuple(token.lower() for token in tokens)
    for key in keys:
        for value in as_list(asset.get(key)):
            if isinstance(value, Mapping):
                value = " ".join(str(part) for part in value.values())
            text = str(value).lower()
            if any(token in text for token in lowered_tokens):
                return True
    return False


def signal_from_registry(
    source_key: str,
    *,
    evidence_uri: str | None = None,
    confidence: float = 1.0,
) -> AwardSignal:
    """Build an AwardSignal from a bundled registry source."""

    source = registry_source(source_key)
    return AwardSignal(
        tag=str(source["tag"]),
        source=source_key,
        weight=int(source["weight"]),
        label=str(source["label"]),
        evidence_uri=evidence_uri,
        confidence=confidence,
    )


from wise_recognition_intelligence.awards.nobel_related import detect_nobel_related
from wise_recognition_intelligence.awards.photography_awards import detect_photography_awards
from wise_recognition_intelligence.awards.pulitzer import detect_pulitzer
from wise_recognition_intelligence.awards.unesco_world_heritage import detect_unesco_world_heritage
from wise_recognition_intelligence.awards.wildlife_conservation_awards import (
    detect_wildlife_conservation_awards,
)

__all__ = [
    "AwardSignal",
    "as_list",
    "detect_nobel_related",
    "detect_photography_awards",
    "detect_pulitzer",
    "detect_unesco_world_heritage",
    "detect_wildlife_conservation_awards",
    "first_present",
    "load_award_registry",
    "registry_source",
    "signal_from_registry",
    "text_contains",
]
