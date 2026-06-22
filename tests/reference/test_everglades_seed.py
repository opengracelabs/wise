"""Reference Capability 3 Everglades seed and geospatial tests."""

from __future__ import annotations

import pytest
from sqlalchemy import select, text

from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PreservationObject,
    ProtectedArea,
    QualityReview,
)


@pytest.mark.integration
def test_everglades_discovery_record(rc3_session):
    record = rc3_session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == "everglades-national-park")
    ).one()
    assert record.status.value == "approved"
    assert record.source_registry_ref == "ramsar"
    assert record.external_identifiers["ramsar"] == "374"
    assert record.external_identifiers["wikidata"] == "Q212174"
    assert record.external_identifiers["unesco_whc"] == "76"
    assert record.external_identifiers["geonames"] == "4157029"


@pytest.mark.integration
def test_everglades_protected_area_postgis(rc3_session):
    area = rc3_session.scalars(
        select(ProtectedArea).where(ProtectedArea.stable_id == "everglades-national-park")
    ).one()
    assert area.status.value == "approved"
    assert area.designation_type == "national_park"
    assert area.conservation_metadata["iucn_category"] == "II"
    assert area.conservation_metadata["area_hectares"] == 610493

    row = rc3_session.execute(
        text(
            """
            SELECT
                ST_GeometryType(boundary) AS boundary_type,
                ST_SRID(boundary) AS boundary_srid,
                ST_GeometryType(centroid) AS centroid_type,
                ST_SRID(centroid) AS centroid_srid,
                ST_Area(boundary::geography) > 0 AS has_area
            FROM conservation.protected_areas
            WHERE stable_id = 'everglades-national-park'
            """
        )
    ).one()
    assert row.boundary_type == "ST_MultiPolygon"
    assert row.boundary_srid == 4326
    assert row.centroid_type == "ST_Point"
    assert row.centroid_srid == 4326
    assert row.has_area is True


@pytest.mark.integration
def test_everglades_spatial_gist_index(rc3_session):
    indexes = rc3_session.execute(
        text(
            """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = 'conservation'
              AND tablename = 'protected_areas'
              AND indexname LIKE '%gist%'
            """
        )
    ).all()
    index_names = {row.indexname for row in indexes}
    assert "ix_protected_areas_boundary_gist" in index_names
    assert "ix_protected_areas_centroid_gist" in index_names


@pytest.mark.integration
def test_everglades_entity_assertion_conservation_metadata(rc3_session):
    metadata = rc3_session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == "everglades-national-park")
    ).one()
    assertion = rc3_session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()
    assert assertion.entity_type == "crm:E27_Site"
    assert assertion.assertion_data["conservation_metadata"]["iucn_category"] == "II"
    assert assertion.assertion_data["evidence"]["confidence"] >= 0.9


@pytest.mark.integration
def test_everglades_quality_review_geospatial_dimension(rc3_session):
    review = rc3_session.scalars(
        select(QualityReview).where(QualityReview.entity_uri.like("%everglades%"))
    ).one()
    assert review.disposition == "accepted"
    geospatial = next(
        score
        for score in review.review_data["dimension_scores"]
        if score["dimension"] == "geospatial"
    )
    assert geospatial["passed"] is True


@pytest.mark.integration
def test_everglades_bbox_spatial_search(rc3_session):
    rows = rc3_session.execute(
        text(
            """
            SELECT stable_id
            FROM conservation.protected_areas
            WHERE status = 'approved'
              AND ST_Intersects(
                    boundary,
                    ST_MakeEnvelope(-82.0, 25.0, -80.0, 26.0, 4326)
                  )
            """
        )
    ).all()
    stable_ids = {row.stable_id for row in rows}
    assert "everglades-national-park" in stable_ids
