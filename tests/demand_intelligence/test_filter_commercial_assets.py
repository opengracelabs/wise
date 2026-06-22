import json

from filter_commercial_assets import (
    COMMERCIAL_READY_FILENAME,
    REJECTED_ASSETS_FILENAME,
    filter_commercial_assets,
    load_assets,
    write_commercial_asset_outputs,
)


def test_filter_passes_assets_with_recognition_at_or_above_70():
    result = filter_commercial_assets(
        [
            {
                "id": "recognized",
                "recognition_score": 70,
                "emotional_value": 10,
                "visual_impact": 10,
                "market_demand_signal": 10,
            }
        ]
    )

    assert [asset["id"] for asset in result.commercial_ready_assets] == ["recognized"]
    assert result.rejected_assets == []


def test_filter_passes_assets_with_high_demand_and_visual_scores():
    result = filter_commercial_assets(
        [
            {
                "id": "high-demand-visual",
                "recognition_score": 55,
                "demand_score": 85,
                "visual_score": 25,
            }
        ]
    )

    assert [asset["id"] for asset in result.commercial_ready_assets] == ["high-demand-visual"]
    assert result.commercial_ready_assets[0]["demand_intelligence"]["score_source"] == "precomputed"


def test_filter_rejects_high_demand_assets_below_recognition_gate():
    result = filter_commercial_assets(
        [
            {
                "id": "blocked",
                "recognition_score": 49,
                "demand_score": 99,
                "visual_score": 90,
            }
        ]
    )

    assert result.commercial_ready_assets == []
    assert result.rejected_assets[0]["id"] == "blocked"
    assert result.rejected_assets[0]["archival_only"] is True
    assert "recognition_score_below_commercialization_gate" in result.rejected_assets[0][
        "rejection_reasons"
    ]


def test_filter_rejects_assets_that_miss_readiness_thresholds():
    result = filter_commercial_assets(
        [
            {
                "id": "not-ready",
                "recognition_score": 69,
                "demand_score": 79,
                "visual_score": 100,
            }
        ]
    )

    assert result.commercial_ready_assets == []
    assert result.rejected_assets[0]["archival_only"] is True
    assert "commercial_readiness_threshold_not_met" in result.rejected_assets[0][
        "rejection_reasons"
    ]


def test_write_commercial_asset_outputs_creates_expected_json_files(tmp_path):
    result = write_commercial_asset_outputs(
        [
            {
                "id": "ready",
                "recognition_score": 72,
                "emotional_value": 10,
                "visual_impact": 10,
                "market_demand_signal": 10,
            },
            {
                "id": "archival",
                "recognition_score": 45,
                "emotional_value": 100,
                "visual_impact": 100,
                "market_demand_signal": 100,
            },
        ],
        tmp_path,
    )

    commercial_ready = json.loads((tmp_path / COMMERCIAL_READY_FILENAME).read_text())
    rejected = json.loads((tmp_path / REJECTED_ASSETS_FILENAME).read_text())

    assert [asset["id"] for asset in commercial_ready] == ["ready"]
    assert [asset["id"] for asset in rejected] == ["archival"]
    assert result.commercial_ready_assets == commercial_ready
    assert result.rejected_assets == rejected


def test_load_assets_accepts_assets_wrapper(tmp_path):
    input_file = tmp_path / "assets.json"
    input_file.write_text(json.dumps({"assets": [{"id": "wrapped"}]}))

    assert load_assets(input_file) == [{"id": "wrapped"}]
