"""Unit tests for authority proposer."""

from wise_metadata.enums import AuthorityEntityType
from wise_metadata.services.authority_proposer import propose_from_normalized


def test_propose_wikidata_authority():
    normalized = {
        "dcterms:title": "Stonehenge",
        "wikidata:entity": "Q16476",
    }
    proposals = propose_from_normalized(
        normalized,
        source_canonical_name="wikidata",
        source_registry_ref="https://wise.example/registry/source/wikidata",
    )
    assert len(proposals) == 1
    assert proposals[0].entity_type == AuthorityEntityType.PLACE
    assert proposals[0].external_scheme == "wikidata"
    assert proposals[0].external_id == "Q16476"
    assert proposals[0].evidence["confidence"] == 1.0


def test_propose_unesco_authority():
    normalized = {
        "dcterms:title": "Stonehenge",
        "dcterms:identifier": "373",
    }
    proposals = propose_from_normalized(
        normalized,
        source_canonical_name="unesco",
        source_registry_ref="https://wise.example/registry/source/unesco",
    )
    assert proposals[0].external_scheme == "unesco.whc"
