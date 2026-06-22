"""Reference Capability 3 end-to-end acceptance tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from wise_api.area_repository import get_protected_area_object
from wise_api.main import app


@pytest.mark.e2e
def test_protected_area_aggregate(rc3_session: Session):
    view = get_protected_area_object(rc3_session, "everglades-national-park")
    assert view.stable_id == "everglades-national-park"
    assert view.source_registry.stable_id == "ramsar"
    assert view.rights_verified is True
    assert view.quality_approved is True
    assert view.geospatial_indexed is True
    assert len(view.provenance_chain) >= 4
    assert view.graph_entity.external_links[0].external_identifier == "Q212174"
    assert view.protected_area.conservation_metadata.iucn_category == "II"


@pytest.mark.e2e
def test_api_area_endpoint(rc3_session: Session):
    from wise_api import database

    def override_db():
        yield rc3_session

    app.dependency_overrides[database.get_db] = override_db
    client = TestClient(app)
    response = client.get("/v1/areas/everglades-national-park")
    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Everglades National Park"
    assert payload["preservation"]["ark"] == "ark:/99999/374/everglades-national-park/"
    assert payload["protected_area"]["external_identifiers"]["ramsar"] == "374"
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_map_area_endpoint(rc3_session: Session):
    from wise_api import database

    def override_db():
        yield rc3_session

    app.dependency_overrides[database.get_db] = override_db
    client = TestClient(app)
    response = client.get("/v1/map/areas/everglades-national-park")
    assert response.status_code == 200
    payload = response.json()
    assert payload["stable_id"] == "everglades-national-park"
    assert payload["boundary_geojson"]["type"] in ("Polygon", "MultiPolygon")
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_map_bbox_search_endpoint(rc3_session: Session):
    from wise_api import database

    def override_db():
        yield rc3_session

    app.dependency_overrides[database.get_db] = override_db
    client = TestClient(app)
    response = client.get("/v1/map/search", params={"bbox": "-82.0,25.0,-80.0,26.0"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1
    assert any(item["stable_id"] == "everglades-national-park" for item in payload["areas"])
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_public_area_page_served():
    client = TestClient(app)
    response = client.get("/areas/everglades-national-park")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")
    assert response.status_code == 200
    assert "Everglades" in response.text
