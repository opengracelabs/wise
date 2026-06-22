"""Assemble heritage object view from database rows."""

from __future__ import annotations

from wise_contracts import HeritageObjectView
from wise_registry.models import Source
from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
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
    quality_flags,
    source_registry_ref,
)


def assemble_object_view(
    *,
    source: Source,
    discovery: DiscoveryRecord,
    preservation: PreservationObject,
    premis_events: list[PremisEvent],
    metadata: MetadataRecord,
    assertion: EntityAssertion,
    graph_entity: GraphEntity,
    external_links: list[ExternalLink],
    quality: QualityReview,
) -> HeritageObjectView:
    discovery_contract = assemble_discovery(discovery)
    preservation_contract, _ = assemble_preservation(preservation, str(discovery.id))
    premis_contracts = assemble_premis_events(preservation, premis_events)
    metadata_contract = assemble_metadata(metadata, preservation.ark)
    assertion_contract = assemble_assertion(assertion, str(metadata.id))
    graph_contract = assemble_graph(graph_entity, external_links, str(assertion.id))
    quality_contract = assemble_quality(quality)
    quality_data = quality.review_data

    rights_verified, quality_approved, accessibility_compliant = quality_flags(quality_data)

    provenance_chain = [
        discovery.discovery_event_id,
        preservation.ingest_event_id,
        *[str(event.id) for event in premis_events],
        metadata.modeling_event_id,
        quality_data["provenance"]["event_id"],
    ]

    return HeritageObjectView(
        stable_id=discovery.stable_id,
        title=discovery.title,
        source_registry=source_registry_ref(source),
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
    )
