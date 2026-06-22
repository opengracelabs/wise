"""Metadata normalization from registered source payloads."""

from __future__ import annotations

from typing import Any

from wise_metadata.enums import SourceSchema

AGENT_VERSION = "metadata-agent@1.0.0"


def _extract_literals(payload: dict, paths: list[str]) -> dict[str, Any]:
    """Preserve original source literals at dotted paths."""
    literals: dict[str, Any] = {}
    for path in paths:
        value = _get_path(payload, path)
        if value is not None:
            literals[path] = value
    return literals


def _get_path(payload: dict, path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def normalize_unesco_whc(raw: dict) -> tuple[dict, dict, str | None]:
    """Normalize UNESCO World Heritage site metadata."""
    literals = _extract_literals(
        raw,
        ["id_no", "site", "short_description", "date_inscribed", "latitude", "longitude"],
    )
    normalized = {
        "dcterms:identifier": str(raw.get("id_no", "")),
        "dcterms:title": raw.get("site"),
        "dcterms:description": raw.get("short_description"),
        "crm:E27_Site": True,
        "geo:lat": raw.get("latitude"),
        "geo:long": raw.get("longitude"),
        "unesco:date_inscribed": raw.get("date_inscribed"),
    }
    return normalized, literals, "en"


def normalize_wikidata(raw: dict) -> tuple[dict, dict, str | None]:
    """Normalize Wikidata entity metadata."""
    literals = _extract_literals(raw, ["id", "labels.en.value", "descriptions.en.value", "claims.P625"])
    label = _get_path(raw, "labels.en.value") or _get_path(raw, "labels.en")
    description = _get_path(raw, "descriptions.en.value") or _get_path(raw, "descriptions.en")
    normalized = {
        "dcterms:identifier": raw.get("id"),
        "dcterms:title": label,
        "dcterms:description": description,
        "wikidata:entity": raw.get("id"),
    }
    coords = _get_path(raw, "claims.P625")
    if coords:
        normalized["geo:coordinates"] = coords
    return normalized, literals, "en"


def normalize_wikimedia_commons(raw: dict) -> tuple[dict, dict, str | None]:
    """Normalize Wikimedia Commons file metadata."""
    literals = _extract_literals(
        raw,
        ["title", "artist", "license", "license_short_name", "width", "height"],
    )
    normalized = {
        "dcterms:identifier": raw.get("title"),
        "dcterms:title": raw.get("title"),
        "dcterms:creator": raw.get("artist"),
        "dcterms:rights": raw.get("license"),
        "crm:E73_Information_Object": True,
        "commons:width": raw.get("width"),
        "commons:height": raw.get("height"),
    }
    return normalized, literals, "en"


def normalize_openstreetmap(raw: dict) -> tuple[dict, dict, str | None]:
    """Normalize OpenStreetMap element metadata."""
    literals = _extract_literals(raw, ["id", "type", "tags.name", "tags.wikidata", "lat", "lon"])
    tags = raw.get("tags") or {}
    normalized = {
        "dcterms:identifier": f"{raw.get('type')}/{raw.get('id')}",
        "dcterms:title": tags.get("name"),
        "osm:type": raw.get("type"),
        "osm:id": raw.get("id"),
        "geo:lat": raw.get("lat"),
        "geo:long": raw.get("lon"),
        "osm:wikidata": tags.get("wikidata"),
        "crm:E53_Place": True,
    }
    return normalized, literals, tags.get("name:en") and "en" or None


_NORMALIZERS = {
    SourceSchema.UNESCO_WHC: normalize_unesco_whc,
    SourceSchema.WIKIDATA: normalize_wikidata,
    SourceSchema.WIKIMEDIA_COMMONS: normalize_wikimedia_commons,
    SourceSchema.OPENSTREETMAP: normalize_openstreetmap,
}


def normalize_metadata(source_schema: SourceSchema, raw_payload: dict) -> tuple[dict, dict, str | None]:
    """Normalize raw source metadata; preserve original literals."""
    normalizer = _NORMALIZERS.get(source_schema)
    if normalizer is None:
        raise ValueError(f"Unsupported source schema: {source_schema}")
    return normalizer(raw_payload)
