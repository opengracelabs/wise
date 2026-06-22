import pytest

from scoring.enhanced_demand_score import (
    calculate_enhanced_demand_score,
    is_commercializable,
    score_asset,
)


def test_calculates_weighted_final_demand_score():
    result = calculate_enhanced_demand_score(
        recognition_score=80,
        emotional_value=75,
        visual_impact=50,
        market_demand_signal=25,
    )

    assert result.recognition_component == 32
    assert result.emotional_value_component == 15
    assert result.visual_impact_component == 10
    assert result.market_demand_signal_component == 5
    assert result.demand_score == 62
    assert result.commercializable is True
    assert result.rejection_reasons == ()


def test_blocks_commercialization_when_recognition_is_below_gate():
    result = calculate_enhanced_demand_score(
        recognition_score=49.99,
        emotional_value=100,
        visual_impact=100,
        market_demand_signal=100,
    )

    assert is_commercializable(49.99) is False
    assert result.demand_score == pytest.approx(79.996, abs=0.01)
    assert result.commercializable is False
    assert result.rejection_reasons == ("recognition_score_below_commercialization_gate",)


def test_score_asset_accepts_common_json_field_aliases():
    result = score_asset(
        {
            "Recognition Score": 70,
            "Emotional Value": 80,
            "Visual Score": 90,
            "Market Demand Signal": 60,
        }
    )

    assert result.recognition_score == 70
    assert result.visual_impact == 90
    assert result.demand_score == 74


def test_rejects_scores_outside_raw_score_range():
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_enhanced_demand_score(
            recognition_score=101,
            emotional_value=80,
            visual_impact=80,
            market_demand_signal=80,
        )
