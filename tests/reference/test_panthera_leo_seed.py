"""Panthera leo Reference Capability 2 seed and schema tests."""

from __future__ import annotations

import pytest
from sqlalchemy import select, text

from wise_reference.models import (
    DiscoveryRecord,
    EntityAssertion,
    ExternalLink,
    GraphEntity,
    MetadataRecord,
    PremisEvent,
    PreservationObject,
    QualityReview,
    SpeciesBackboneLink,
    SpeciesRegistryEntry,
    TaxonomicBackboneNode,
)


@pytest.mark.integration
def test_panthera_leo_species_registry(rc1_session):
    entry = rc1_session.scalars(
        select(SpeciesRegistryEntry).where(SpeciesRegistryEntry.stable_id == "panthera-leo")
    ).one()
    assert entry.status.value == "approved"
    assert entry.gbif_taxon_key == "5219404"
    assert entry.scientific_name == "Panthera leo"
    assert entry.taxonomic_rank == "species"


@pytest.mark.integration
def test_panthera_leo_taxonomic_backbone(rc1_session):
    species = rc1_session.scalars(
        select(SpeciesRegistryEntry).where(SpeciesRegistryEntry.stable_id == "panthera-leo")
    ).one()
    links = rc1_session.scalars(
        select(SpeciesBackboneLink).where(SpeciesBackboneLink.species_registry_id == species.id)
    ).all()
    assert len(links) >= 7
    species_node = rc1_session.scalars(
        select(TaxonomicBackboneNode).where(TaxonomicBackboneNode.gbif_usage_key == "5219404")
    ).one()
    assert species_node.scientific_name == "Panthera leo"
    assert species_node.family == "Felidae"


@pytest.mark.integration
def test_panthera_leo_discovery_record(rc1_session):
    record = rc1_session.scalars(
        select(DiscoveryRecord).where(DiscoveryRecord.stable_id == "panthera-leo")
    ).one()
    assert record.source_registry_ref == "gbif"
    assert record.external_identifiers["wikidata"] == "Q140"
    assert record.external_identifiers["eol"] == "328450"


@pytest.mark.integration
def test_panthera_leo_darwin_core_assertion(rc1_session):
    metadata = rc1_session.scalars(
        select(MetadataRecord).where(MetadataRecord.stable_id == "panthera-leo")
    ).one()
    assertion = rc1_session.scalars(
        select(EntityAssertion).where(EntityAssertion.metadata_record_id == metadata.id)
    ).one()
    assert assertion.entity_type == "dwc:Taxon"
    assert assertion.assertion_data["descriptive_overlay"]["dwc:scientificName"] == "Panthera leo"


@pytest.mark.integration
def test_panthera_leo_graph_links(rc1_session):
    entity = rc1_session.scalars(
        select(GraphEntity).where(GraphEntity.stable_id == "panthera-leo")
    ).one()
    links = rc1_session.scalars(
        select(ExternalLink).where(ExternalLink.entity_id == entity.id)
    ).all()
    authorities = {link.external_authority: link.external_identifier for link in links}
    assert authorities["wikidata"] == "Q140"
    assert authorities["eol"] == "328450"


@pytest.mark.integration
def test_panthera_leo_quality_approved(rc1_session):
    review = rc1_session.scalars(
        select(QualityReview).where(QualityReview.entity_uri.like("%panthera-leo%"))
    ).one()
    assert review.status.value == "approved"
    assert review.disposition == "accepted"


@pytest.mark.integration
def test_panthera_leo_full_pipeline_linked(rc1_session):
    row = rc1_session.execute(
        text(
            """
            SELECT s.gbif_taxon_key, p.ark, g.entity_type, q.disposition
            FROM species.registry_entries s
            JOIN discovery.records d ON d.id = s.discovery_record_id
            JOIN preservation.objects p ON p.discovery_record_id = d.id
            JOIN modeling.metadata_records m ON m.preservation_object_id = p.id
            JOIN modeling.entity_assertions ea ON ea.metadata_record_id = m.id
            JOIN graph.entities g ON g.entity_assertion_id = ea.id
            JOIN quality.reviews q ON q.graph_entity_id = g.id
            WHERE s.stable_id = 'panthera-leo'
            """
        )
    ).one()
    assert row.gbif_taxon_key == "5219404"
    assert row.ark == "ark:/99999/gbif/5219404/"
    assert row.entity_type == "dwc:Taxon"
    assert row.disposition == "accepted"
