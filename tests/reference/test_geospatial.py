"""Geospatial query tests for map service repository."""

from __future__ import annotations

import pytest

from wise_api.area_repository import (
    ProtectedAreaNotFoundError,
    get_map_area,
    get_protected_area_object,
    search_protected_areas_by_bbox,
)


@pytest.mark.integration
def test_get_protected_area_aggregate(rc3_session):
    view = get_protected_area_object(rc3_session, "everglades-national-park")
    assert view.stable_id == "everglades-national-park"
    assert view.source_registry.stable_id == "ramsar"
    assert view.protected_area.external_identifiers.ramsar == "374"
    assert view.geospatial_indexed is True
    assert view.protected_area.boundary_geojson["type"] in ("Polygon", "MultiPolygon")
    assert view.entity_assertion.evidence.confidence >= 0.9


@pytest.mark.integration
def test_map_area_feature(rc3_session):
    feature = get_map_area(rc3_session, "everglades-national-park")
    assert feature.pref_label == "Everglades National Park"
    assert feature.centroid_geojson["type"] == "Point"
    assert len(feature.centroid_geojson["coordinates"]) == 2


@pytest.mark.integration
def test_bbox_search_returns_everglades(rc3_session):
    result = search_protected_areas_by_bbox(
        rc3_session,
        min_lon=-82.0,
        min_lat=25.0,
        max_lon=-80.0,
        max_lat=26.0,
    )
    assert result.count >= 1
    assert result.bbox == [-82.0, 25.0, -80.0, 26.0]
    assert any(area.stable_id == "everglades-national-park" for area in result.areas)


@pytest.mark.integration
def test_bbox_search_empty_outside_extent(rc3_session):
    result = search_protected_areas_by_bbox(
        rc3_session,
        min_lon=0.0,
        min_lat=50.0,
        max_lon=1.0,
        max_lat=51.0,
    )
    assert result.count == 0


@pytest.mark.integration
def test_map_area_not_found(rc3_session):
    with pytest.raises(ProtectedAreaNotFoundError):
        get_map_area(rc3_session, "nonexistent-area")
