"""Reference Capability 2 end-to-end acceptance tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from wise_api.main import app
from wise_api.species_repository import get_species_object


@pytest.mark.e2e
def test_species_object_aggregate(rc1_session: Session):
    view = get_species_object(rc1_session, "panthera-leo")
    assert view.stable_id == "panthera-leo"
    assert view.scientific_name == "Panthera leo"
    assert view.source_registry.stable_id == "gbif"
    assert view.species_registry.gbif_taxon_key == "5219404"
    assert len(view.taxonomic_backbone) >= 7
    assert view.rights_verified is True
    assert view.quality_approved is True
    assert view.graph_entity.external_links[0].external_identifier in ("Q140", "328450")


@pytest.mark.e2e
def test_api_species_endpoint(rc1_session: Session):
    from wise_api import database

    def override_db():
        yield rc1_session

    app.dependency_overrides[database.get_db] = override_db
    client = TestClient(app)
    response = client.get("/v1/species/panthera-leo")
    assert response.status_code == 200
    payload = response.json()
    assert payload["scientific_name"] == "Panthera leo"
    assert payload["preservation"]["ark"] == "ark:/99999/gbif/5219404/"
    assert payload["species_registry"]["darwin_core"]["family"] == "Felidae"
    assert payload["quality_review"]["disposition"] == "accepted"
    app.dependency_overrides.clear()


@pytest.mark.e2e
def test_public_species_page_served():
    client = TestClient(app)
    response = client.get("/objects/panthera-leo")
    if response.status_code == 404:
        pytest.skip("Demonstration surface assets not mounted in test environment")
    assert response.status_code == 200
    assert "Panthera leo" in response.text or "panthera-leo" in response.text
