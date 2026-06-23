"""Reference asset inputs for the committed global ranking artifact."""

from __future__ import annotations

from wise_global_ranking.models import GlobalRankingInput
from wise_global_ranking.scoring import build_global_ranking_output


REFERENCE_ASSETS: tuple[GlobalRankingInput, ...] = (
    GlobalRankingInput(
        stable_id="stonehenge",
        title="Stonehenge",
        asset_type="heritage_site",
        demand_score=94,
        recognition_score=96,
        emotional_score=92,
        visual_impact_score=98,
        historical_importance_score=100,
        unesco_whc_id="373",
        awards_prizes=("UNESCO World Heritage inscription",),
        recognition_evidence_uris=(
            "https://whc.unesco.org/en/list/373/",
            "https://www.wikidata.org/wiki/Q39671",
        ),
        metadata={
            "source_registry_refs": ["unesco", "wikidata"],
            "source_asset": "data/reference/unesco/stonehenge-373.json",
        },
    ),
    GlobalRankingInput(
        stable_id="everglades-national-park",
        title="Everglades National Park",
        asset_type="protected_area",
        demand_score=96,
        recognition_score=90,
        emotional_score=88,
        visual_impact_score=93,
        historical_importance_score=88,
        unesco_whc_id="76",
        awards_prizes=(
            "UNESCO World Heritage inscription",
            "Ramsar Wetland of International Importance",
        ),
        recognition_evidence_uris=(
            "https://whc.unesco.org/en/list/76/",
            "https://www.wikidata.org/wiki/Q212174",
        ),
        metadata={
            "source_registry_refs": ["ramsar", "unesco-whc", "wikidata", "geonames"],
            "source_asset": "data/reference/ramsar/everglades-374.json",
        },
    ),
    GlobalRankingInput(
        stable_id="panthera-leo",
        title="Panthera leo",
        asset_type="species",
        demand_score=96,
        recognition_score=88,
        emotional_score=90,
        visual_impact_score=94,
        historical_importance_score=78,
        awards_prizes=("GBIF backbone taxon recognition",),
        recognition_evidence_uris=(
            "https://www.gbif.org/species/5219404",
            "https://www.wikidata.org/wiki/Q140",
        ),
        metadata={
            "source_registry_refs": ["gbif", "wikidata", "eol"],
            "source_asset": "data/reference/gbif/panthera-leo-5219404.json",
        },
    ),
)


def build_reference_global_ranking_output() -> dict:
    """Build the global ranking artifact for all committed reference assets."""

    return build_global_ranking_output(REFERENCE_ASSETS)
