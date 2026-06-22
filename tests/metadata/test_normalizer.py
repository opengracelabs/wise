"""Unit tests for metadata normalizer."""

from wise_metadata.enums import SourceSchema
from wise_metadata.services.normalizer import normalize_metadata


def test_normalize_unesco_whc():
    raw = {
        "id_no": "373",
        "site": "Stonehenge, Avebury and Associated Sites",
        "short_description": "Prehistoric monument",
        "latitude": 51.1789,
        "longitude": -1.8262,
    }
    normalized, literals, lang = normalize_metadata(SourceSchema.UNESCO_WHC, raw)
    assert normalized["dcterms:title"] == raw["site"]
    assert normalized["crm:E27_Site"] is True
    assert literals["site"] == raw["site"]
    assert lang == "en"


def test_normalize_wikidata():
    raw = {
        "id": "Q16476",
        "labels": {"en": {"value": "Stonehenge"}},
        "descriptions": {"en": {"value": "Prehistoric monument"}},
    }
    normalized, literals, _lang = normalize_metadata(SourceSchema.WIKIDATA, raw)
    assert normalized["dcterms:identifier"] == "Q16476"
    assert normalized["dcterms:title"] == "Stonehenge"
    assert "id" in literals


def test_normalize_wikimedia_commons():
    raw = {
        "title": "File:Stonehenge.jpg",
        "artist": "Example Photographer",
        "license": "https://creativecommons.org/licenses/by-sa/2.0/",
    }
    normalized, _literals, _lang = normalize_metadata(SourceSchema.WIKIMEDIA_COMMONS, raw)
    assert normalized["crm:E73_Information_Object"] is True
    assert "creativecommons.org" in normalized["dcterms:rights"]


def test_normalize_openstreetmap():
    raw = {
        "type": "node",
        "id": 123,
        "lat": 51.17,
        "lon": -1.82,
        "tags": {"name": "Stonehenge", "wikidata": "Q16476"},
    }
    normalized, _literals, _lang = normalize_metadata(SourceSchema.OPENSTREETMAP, raw)
    assert normalized["crm:E53_Place"] is True
    assert normalized["osm:wikidata"] == "Q16476"
