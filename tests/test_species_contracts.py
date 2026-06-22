"""Species contract model unit tests."""

from datetime import UTC, datetime

from wise_contracts import (
    ApprovalStatus,
    DarwinCoreOverlay,
    EvidenceOutputProfile,
    GbifExternalIdentifiers,
    ProvenanceRef,
    SpeciesRegistryEntry,
)


def test_species_registry_contract():
    entry = SpeciesRegistryEntry(
        id="test-id",
        stable_id="panthera-leo",
        status=ApprovalStatus.APPROVED,
        species_uri="https://wise.example.org/species/panthera-leo",
        scientific_name="Panthera leo",
        scientific_name_authorship="Linnaeus, 1758",
        taxonomic_rank="species",
        gbif_taxon_key="5219404",
        gbif_usage_key="5219404",
        darwin_core=DarwinCoreOverlay(
            scientific_name="Panthera leo",
            scientific_name_authorship="Linnaeus, 1758",
            taxon_rank="species",
            family="Felidae",
            genus="Panthera",
        ),
        external_identifiers=GbifExternalIdentifiers(
            gbif_taxon_key="5219404",
            wikidata="Q140",
            eol="328450",
        ),
        evidence=EvidenceOutputProfile(
            confidence=0.99,
            evidence_summary="GBIF backbone species",
            method="gbif-backbone-harvest-v1",
            source_registry_refs=["gbif"],
        ),
        provenance=ProvenanceRef(
            event_id="species-registry-panthera-leo",
            event_type="register",
            agent_version="wise-reference/0.2.0",
            event_timestamp=datetime(2026, 6, 22, tzinfo=UTC),
        ),
        source_registry_ref="gbif",
    )
    assert entry.darwin_core.family == "Felidae"
    assert entry.external_identifiers.wikidata == "Q140"
