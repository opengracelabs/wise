"""Assemble Reference Capability 3 protected area view from database rows."""

from __future__ import annotations

from wise_contracts import (
    ApprovalStatus,
    ConservationMetadata,
    ProtectedAreaIdentifiers,
    ProtectedAreaObjectView,
    ProtectedAreaRegistryEntry,
)
from wise_registry.models import Source
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

from wise_api.assembler_common import (
    assemble_assertion,
    assemble_discovery,
    assemble_graph,
    assemble_metadata,
    assemble_premis_events,
    assemble_preservation,
    assemble_quality,
    provenance_from_dict,
    quality_flags,
    source_registry_ref,
)


def assemble_protected_area_view(
    *,
    source: Source,
    protected_area: ProtectedArea,
    boundary_geojson: dict,
    centroid_geojson: dict,
    discovery: DiscoveryRecord,
    preservation: PreservationObject,
    premis_events: list[PremisEvent],
    metadata: MetadataRecord,
    assertion: EntityAssertion,
    graph_entity: GraphEntity,
    external_links: list[ExternalLink],
    quality: QualityReview,
) -> ProtectedAreaObjectView:
    area_data = protected_area.area_data
    discovery_contract = assemble_discovery(discovery)
    preservation_contract, _ = assemble_preservation(preservation, str(discovery.id))
    premis_contracts = assemble_premis_events(preservation, premis_events)
    metadata_contract = assemble_metadata(metadata, preservation.ark)
    assertion_contract = assemble_assertion(assertion, str(metadata.id))
    graph_contract = assemble_graph(graph_entity, external_links, str(assertion.id))
    quality_contract = assemble_quality(quality)
    quality_data = quality.review_data

    protected_area_contract = ProtectedAreaRegistryEntry(
        id=str(protected_area.id),
        stable_id=protected_area.stable_id,
        status=ApprovalStatus(protected_area.status.value),
        pref_label=protected_area.pref_label,
        designation_type=protected_area.designation_type,
        conservation_metadata=ConservationMetadata(**protected_area.conservation_metadata),
        external_identifiers=ProtectedAreaIdentifiers(**protected_area.external_identifiers),
        boundary_geojson=boundary_geojson,
        centroid_geojson=centroid_geojson,
        evidence=discovery_contract.evidence,
        provenance=provenance_from_dict(area_data["provenance"]),
        graph_entity_id=str(protected_area.graph_entity_id),
    )

    rights_verified, quality_approved, accessibility_compliant = quality_flags(quality_data)
    geospatial_indexed = all(
        score["passed"]
        for score in quality_data.get("dimension_scores", [])
        if score["dimension"] == "geospatial"
    )

    provenance_chain = [
        discovery.discovery_event_id,
        preservation.ingest_event_id,
        *[str(event.id) for event in premis_events],
        metadata.modeling_event_id,
        area_data["provenance"]["event_id"],
        quality_data["provenance"]["event_id"],
    ]

    return ProtectedAreaObjectView(
        stable_id=protected_area.stable_id,
        title=protected_area.pref_label,
        source_registry=source_registry_ref(source),
        protected_area=protected_area_contract,
        discovery=discovery_contract,
        preservation=preservation_contract,
        preservation_events=premis_contracts,
        metadata=metadata_contract,
        entity_assertion=assertion_contract,
        graph_entity=graph_contract,
        quality_review=quality_contract,
        provenance_chain=provenance_chain,
        rights_verified=rights_verified,
        quality_approved=quality_approved,
        accessibility_compliant=accessibility_compliant,
        geospatial_indexed=geospatial_indexed,
    )
