"""Reference Capability 1 end-to-end acceptance tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from wise_api.main import app
from wise_api.repository import get_heritage_object


@pytest.mark.e2e
def test_heritage_object_aggregate(rc1_session: Session):
    view = get_heritage_object(rc1_session, "stonehenge")
    assert view.stable_id == "stonehenge"
    # The canonical UNESCO source (registry seed 002) has canonical_name "unesco"
    # and stable_id "unesco-whc"; the discovery record's source_registry_ref
    # "unesco" resolves via canonical_name, so the resolved stable_id is "unesco-whc"
    # (cf. tests/discovery/test_agent_integration.py and registry seed 002).
    assert view.source_registry.stable_id == "unesco-whc"
    assert view.rights_verified is True
    assert view.quality_approved is True
    assert view.accessibility_compliant is True
    assert len(view.provenance_chain) >= 4
    assert view.graph_entity.external_links[0].external_identifier == "Q39671"


@pytest.mark.e2e
def test_api_object_endpoint(rc1_session: Session, monkeypatch):
    from wise_api import database

    def override_db():
        yield rc1_session

    app.dependency_overrides[database.get_db] = override_db
    client = TestClient(app)
    response = client.get("/v1/objects/stonehenge")
    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Stonehenge"
    assert payload["preservation"]["ark"] == "ark:/99999/373/stonehenge/"
    assert payload["quality_review"]["disposition"] == "accepted"
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_public_object_page_served():
    client = TestClient(app)
    response = client.get("/objects/stonehenge")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")
    assert response.status_code == 200
    assert "Stonehenge" in response.text
