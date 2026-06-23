"""Enhanced demand scoring for commercial asset selection.

Architecture v1.0 remains frozen: this module is a pure scoring helper and does
not mutate registries, metadata schemas, or orchestration contracts.

Raw score inputs use a 0-100 scale. The final demand score is a weighted 0-100
score composed of:

* Recognition Score component: 0-40
* Emotional Value component: 0-20
* Visual Impact component: 0-20
* Market Demand Signal component: 0-20

The commercialization gate uses the raw recognition score: if Recognition Score
is below 50, the asset cannot be commercialized regardless of the final demand
score.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

RAW_SCORE_MIN = 0.0
RAW_SCORE_MAX = 100.0
COMMERCIAL_RECOGNITION_GATE = 50.0

RECOGNITION_COMPONENT_MAX = 40.0
EMOTIONAL_VALUE_COMPONENT_MAX = 20.0
VISUAL_IMPACT_COMPONENT_MAX = 20.0
MARKET_DEMAND_SIGNAL_COMPONENT_MAX = 20.0

UNESCO_AUTHORITY_HIERARCHY = (
    "unesco_world_heritage_and_programme_records",
    "national_and_regional_heritage_authorities",
    "accredited_museums_libraries_archives_and_research_institutions",
    "peer_reviewed_or_formally_published_scholarly_sources",
    "recognized_editorial_sources_with_documented_fact_checking",
)

SMITHSONIAN_CURATION_PRINCIPLES = (
    "verified_provenance",
    "cultural_and_historical_context",
    "public_education_value",
    "rights_and_stewardship_clarity",
    "preservation_first_selection",
)

NATIONAL_GEOGRAPHIC_EDITORIAL_SELECTION_RULES = (
    "visual_distinctiveness",
    "clear_human_or_natural_story",
    "geographic_and_cultural_specificity",
    "factual_accuracy",
    "ethical_context_and_non_extractive_framing",
)

_FIELD_ALIASES = {
    "recognition_score": (
        "recognition_score",
        "recognitionScore",
        "recognition",
        "Recognition Score",
        "RecognitionScore",
    ),
    "emotional_value": (
        "emotional_value",
        "emotionalValue",
        "emotional_score",
        "emotionalScore",
        "Emotional Value",
        "Emotional Score",
    ),
    "visual_impact": (
        "visual_impact",
        "visualImpact",
        "visual_score",
        "visualScore",
        "Visual Impact",
        "Visual Score",
    ),
    "market_demand_signal": (
        "market_demand_signal",
        "marketDemandSignal",
        "market_score",
        "marketScore",
        "Market Demand Signal",
        "Market Score",
    ),
}


@dataclass(frozen=True)
class EnhancedDemandScore:
    """Weighted demand score and commercialization gate outcome."""

    recognition_score: float
    emotional_value: float
    visual_impact: float
    market_demand_signal: float
    recognition_component: float
    emotional_value_component: float
    visual_impact_component: float
    market_demand_signal_component: float
    demand_score: float
    commercializable: bool
    rejection_reasons: tuple[str, ...]
    authority_hierarchy: tuple[str, ...] = UNESCO_AUTHORITY_HIERARCHY
    curation_principles: tuple[str, ...] = SMITHSONIAN_CURATION_PRINCIPLES
    editorial_selection_rules: tuple[str, ...] = NATIONAL_GEOGRAPHIC_EDITORIAL_SELECTION_RULES

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable score payload."""
        payload = asdict(self)
        for key, value in payload.items():
            if isinstance(value, tuple):
                payload[key] = list(value)
        return payload


def is_commercializable(recognition_score: float) -> bool:
    """Return whether the raw recognition score clears the commercialization gate."""
    return _coerce_raw_score(recognition_score, "recognition_score") >= COMMERCIAL_RECOGNITION_GATE


def calculate_enhanced_demand_score(
    *,
    recognition_score: float,
    emotional_value: float,
    visual_impact: float,
    market_demand_signal: float,
) -> EnhancedDemandScore:
    """Calculate the final demand score using the v1.0 weighted formula."""
    recognition = _coerce_raw_score(recognition_score, "recognition_score")
    emotional = _coerce_raw_score(emotional_value, "emotional_value")
    visual = _coerce_raw_score(visual_impact, "visual_impact")
    market = _coerce_raw_score(market_demand_signal, "market_demand_signal")

    recognition_component = _weighted_component(recognition, RECOGNITION_COMPONENT_MAX)
    emotional_component = _weighted_component(emotional, EMOTIONAL_VALUE_COMPONENT_MAX)
    visual_component = _weighted_component(visual, VISUAL_IMPACT_COMPONENT_MAX)
    market_component = _weighted_component(market, MARKET_DEMAND_SIGNAL_COMPONENT_MAX)
    demand_score = round(
        recognition_component + emotional_component + visual_component + market_component,
        2,
    )

    rejection_reasons: list[str] = []
    commercializable = recognition >= COMMERCIAL_RECOGNITION_GATE
    if not commercializable:
        rejection_reasons.append("recognition_score_below_commercialization_gate")

    return EnhancedDemandScore(
        recognition_score=recognition,
        emotional_value=emotional,
        visual_impact=visual,
        market_demand_signal=market,
        recognition_component=recognition_component,
        emotional_value_component=emotional_component,
        visual_impact_component=visual_component,
        market_demand_signal_component=market_component,
        demand_score=demand_score,
        commercializable=commercializable,
        rejection_reasons=tuple(rejection_reasons),
    )


def score_asset(asset: Mapping[str, Any]) -> EnhancedDemandScore:
    """Calculate an enhanced demand score from an asset-like mapping.

    The helper accepts common snake_case, camelCase, and title-case field names
    so JSON feeds can be scored without ad hoc pre-normalization.
    """
    return calculate_enhanced_demand_score(
        recognition_score=_read_score(asset, "recognition_score"),
        emotional_value=_read_score(asset, "emotional_value"),
        visual_impact=_read_score(asset, "visual_impact"),
        market_demand_signal=_read_score(asset, "market_demand_signal"),
    )


def _weighted_component(raw_score: float, component_max: float) -> float:
    return round((raw_score / RAW_SCORE_MAX) * component_max, 2)


def _read_score(asset: Mapping[str, Any], canonical_name: str) -> float:
    for alias in _FIELD_ALIASES[canonical_name]:
        if alias in asset:
            return _coerce_raw_score(asset[alias], canonical_name)
    aliases = ", ".join(_FIELD_ALIASES[canonical_name])
    raise KeyError(f"Missing {canonical_name}; accepted fields: {aliases}")


def _coerce_raw_score(value: Any, field_name: str) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a numeric score") from exc

    if score < RAW_SCORE_MIN or score > RAW_SCORE_MAX:
        raise ValueError(f"{field_name} must be between 0 and 100")
    return score
