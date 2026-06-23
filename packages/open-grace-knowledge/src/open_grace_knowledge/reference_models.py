"""Knowledge-domain reference model profiles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeReferenceModelProfile:
    slug: str
    display_name: str
    domain: str
    knowledge_use: str


KNOWLEDGE_REFERENCE_MODELS: tuple[KnowledgeReferenceModelProfile, ...] = (
    KnowledgeReferenceModelProfile(
        slug="wikidata",
        display_name="Wikidata",
        domain="linked_open_data",
        knowledge_use="Entity authority, same-as linking, and schema conformance",
    ),
    KnowledgeReferenceModelProfile(
        slug="gbif",
        display_name="GBIF",
        domain="biodiversity",
        knowledge_use="Taxonomic keys, Darwin Core occurrence binding, species validation",
    ),
    KnowledgeReferenceModelProfile(
        slug="europeana",
        display_name="Europeana",
        domain="cultural_heritage",
        knowledge_use="Collection metadata, rights statements, and aggregation profiles",
    ),
    KnowledgeReferenceModelProfile(
        slug="internet-archive",
        display_name="Internet Archive",
        domain="digital_preservation",
        knowledge_use="Fixity, format migration, and long-term media access",
    ),
    KnowledgeReferenceModelProfile(
        slug="cidoc-crm",
        display_name="CIDOC CRM",
        domain="museum_heritage",
        knowledge_use="Heritage object typing, provenance events, and museum semantics",
    ),
    KnowledgeReferenceModelProfile(
        slug="dublin-core",
        display_name="Dublin Core",
        domain="metadata",
        knowledge_use="Collection description, resource typing, and cataloging profiles",
    ),
    KnowledgeReferenceModelProfile(
        slug="skos",
        display_name="SKOS",
        domain="controlled_vocabulary",
        knowledge_use="Concept schemes, broader/narrower relations, and taxonomy graphs",
    ),
    KnowledgeReferenceModelProfile(
        slug="prov-o",
        display_name="PROV-O",
        domain="provenance",
        knowledge_use="Activity agents, derivation chains, and audit evidence linkage",
    ),
)

KNOWLEDGE_REFERENCE_MODEL_BY_SLUG = {
    profile.slug: profile for profile in KNOWLEDGE_REFERENCE_MODELS
}
