"""Protected area repository — aggregates RC3 pipeline records and geospatial queries."""

from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from wise_contracts import MapAreaSummary, MapSearchResult, ProtectedAreaIdentifiers, ProtectedAreaObjectView
from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
    ProtectedArea,
    QualityReview,
)

from wise_api.area_assembler import assemble_protected_area_view
from wise_api.source_lookup import resolve_source


class ProtectedAreaNotFoundError(LookupError):
    """Raised when no approved RC3 protected area exists for the stable identifier."""


def _geojson_pair(session: Session, area_id) -> tuple[dict, dict]:
    row = session.execute(
        text(
            """
            SELECT
                ST_AsGeoJSON(boundary)::json AS boundary_geojson,
                ST_AsGeoJSON(centroid)::json AS centroid_geojson
            FROM conservation.protected_areas
            WHERE id = :area_id
            """
        ),
        {"area_id": str(area_id)},
    ).one()
    return row.boundary_geojson, row.centroid_geojson


def get_protected_area_object(session: Session, stable_id: str) -> ProtectedAreaObjectView:
    protected_area = session.scalars(
        select(ProtectedArea).where(ProtectedArea.stable_id == stable_id)
    ).one_or_none()
    if protected_area is None:
        raise ProtectedAreaNotFoundError(f"Protected area not found: {stable_id}")

    discovery = session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == stable_id)
    ).one()

    preservation = session.scalars(
        select(PreservationObject).where(PreservationObject.stable_id == stable_id)
    ).one()

    metadata = session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == stable_id)
    ).one()

    assertion = session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()

    graph_entity = session.scalars(
        select(GraphEntity).where(GraphEntity.stable_id == stable_id)
    ).one()

    quality = session.scalars(
        select(QualityReview).where(QualityReview.graph_entity_id == graph_entity.id)
    ).one()

    source = resolve_source(session, discovery.source_registry_ref)

    premis_events = session.scalars(
        select(PremisEvent)
        .where(PremisEvent.preservation_object_id == preservation.id)
        .order_by(PremisEvent.event_timestamp)
    ).all()

    external_links = session.scalars(
        select(ExternalLink).where(ExternalLink.entity_id == graph_entity.id)
    ).all()

    boundary_geojson, centroid_geojson = _geojson_pair(session, protected_area.id)

    return assemble_protected_area_view(
        source=source,
        protected_area=protected_area,
        boundary_geojson=boundary_geojson,
        centroid_geojson=centroid_geojson,
        discovery=discovery,
        preservation=preservation,
        premis_events=premis_events,
        metadata=metadata,
        assertion=assertion,
        graph_entity=graph_entity,
        external_links=external_links,
        quality=quality,
    )


def get_map_area(session: Session, stable_id: str) -> MapAreaSummary:
    row = session.execute(
        text(
            """
            SELECT
                stable_id,
                pref_label,
                designation_type,
                external_identifiers,
                ST_AsGeoJSON(centroid)::json AS centroid_geojson,
                ST_AsGeoJSON(boundary)::json AS boundary_geojson
            FROM conservation.protected_areas
            WHERE stable_id = :stable_id AND status = 'approved'
            """
        ),
        {"stable_id": stable_id},
    ).one_or_none()
    if row is None:
        raise ProtectedAreaNotFoundError(f"Protected area not found: {stable_id}")

    return MapAreaSummary(
        stable_id=row.stable_id,
        pref_label=row.pref_label,
        designation_type=row.designation_type,
        centroid_geojson=row.centroid_geojson,
        boundary_geojson=row.boundary_geojson,
        external_identifiers=ProtectedAreaIdentifiers(**row.external_identifiers),
    )


def search_protected_areas_by_bbox(
    session: Session,
    *,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> MapSearchResult:
    rows = session.execute(
        text(
            """
            SELECT
                stable_id,
                pref_label,
                designation_type,
                external_identifiers,
                ST_AsGeoJSON(centroid)::json AS centroid_geojson,
                ST_AsGeoJSON(boundary)::json AS boundary_geojson
            FROM conservation.protected_areas
            WHERE status = 'approved'
              AND boundary && ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326)
              AND ST_Intersects(
                    boundary,
                    ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326)
                  )
            ORDER BY pref_label
            """
        ),
        {
            "min_lon": min_lon,
            "min_lat": min_lat,
            "max_lon": max_lon,
            "max_lat": max_lat,
        },
    ).all()

    areas = [
        MapAreaSummary(
            stable_id=row.stable_id,
            pref_label=row.pref_label,
            designation_type=row.designation_type,
            centroid_geojson=row.centroid_geojson,
            boundary_geojson=row.boundary_geojson,
            external_identifiers=ProtectedAreaIdentifiers(**row.external_identifiers),
        )
        for row in rows
    ]

    return MapSearchResult(
        count=len(areas),
        bbox=[min_lon, min_lat, max_lon, max_lat],
        areas=areas,
    )
