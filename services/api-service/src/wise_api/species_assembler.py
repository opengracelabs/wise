"""Assemble Reference Capability 2 species view from database rows."""

from __future__ import annotations

from wise_contracts import (
    ApprovalStatus,
    DarwinCoreOverlay,
    GbifExternalIdentifiers,
    SpeciesObjectView,
    SpeciesRegistryEntry,
    TaxonomicBackboneNode,
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
    QualityReview,
    SpeciesRegistryEntry as SpeciesRegistryRow,
    TaxonomicBackboneNode as BackboneRow,
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


def assemble_species_view(
    *,
    source: Source,
    species_registry: SpeciesRegistryRow,
    backbone_nodes: list[BackboneRow],
    discovery: DiscoveryRecord,
    preservation: PreservationObject,
    premis_events: list[PremisEvent],
    metadata: MetadataRecord,
    assertion: EntityAssertion,
    graph_entity: GraphEntity,
    external_links: list[ExternalLink],
    quality: QualityReview,
) -> SpeciesObjectView:
    registry_data = species_registry.registry_data
    discovery_contract = assemble_discovery(discovery)
    preservation_contract, _ = assemble_preservation(preservation, str(discovery.id))
    premis_contracts = assemble_premis_events(preservation, premis_events)
    metadata_contract = assemble_metadata(metadata, preservation.ark)
    assertion_contract = assemble_assertion(assertion, str(metadata.id))
    graph_contract = assemble_graph(graph_entity, external_links, str(assertion.id))
    quality_contract = assemble_quality(quality)
    quality_data = quality.review_data

    species_contract = SpeciesRegistryEntry(
        id=str(species_registry.id),
        stable_id=species_registry.stable_id,
        status=ApprovalStatus(species_registry.status.value),
        species_uri=species_registry.species_uri,
        scientific_name=species_registry.scientific_name,
        scientific_name_authorship=species_registry.scientific_name_authorship,
        taxonomic_rank=species_registry.taxonomic_rank,
        gbif_taxon_key=species_registry.gbif_taxon_key,
        gbif_usage_key=species_registry.gbif_usage_key,
        darwin_core=DarwinCoreOverlay(**registry_data["darwin_core"]),
        external_identifiers=GbifExternalIdentifiers(**registry_data["external_identifiers"]),
        evidence=discovery_contract.evidence,
        provenance=provenance_from_dict(registry_data["provenance"]),
        source_registry_ref=registry_data["source_registry_ref"],
    )

    backbone_contracts = [
        TaxonomicBackboneNode(
            id=str(node.id),
            gbif_usage_key=node.gbif_usage_key,
            scientific_name=node.scientific_name,
            taxonomic_rank=node.taxonomic_rank,
            parent_usage_key=node.parent_usage_key,
            status=ApprovalStatus(node.status.value),
            kingdom=node.kingdom,
            phylum=node.phylum,
            class_=node.taxonomic_class,
            order=node.taxonomic_order,
            family=node.family,
            genus=node.genus,
        )
        for node in sorted(backbone_nodes, key=lambda n: n.gbif_usage_key)
    ]

    rights_verified, quality_approved, accessibility_compliant = quality_flags(quality_data)

    provenance_chain = [
        discovery.discovery_event_id,
        registry_data["provenance"]["event_id"],
        preservation.ingest_event_id,
        *[str(event.id) for event in premis_events],
        metadata.modeling_event_id,
        quality_data["provenance"]["event_id"],
    ]

    return SpeciesObjectView(
        stable_id=species_registry.stable_id,
        scientific_name=species_registry.scientific_name,
        common_name=discovery.title,
        source_registry=source_registry_ref(source),
        species_registry=species_contract,
        taxonomic_backbone=backbone_contracts,
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
