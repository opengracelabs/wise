# wise-global-ranking

Global asset ranking system for WISE reference assets.

This package ranks assets on a 0-100 `global_rank_score` using:

- Demand Score, supplied by the prior demand system
- Recognition Score, including awards and prizes
- Emotional Score
- Visual Impact Score
- Historical Importance Score

The package classifies each ranked asset into one of four tiers:

| Tier | Classification | Entry rule |
|------|----------------|------------|
| Tier 1 | ICONIC GLOBAL HERITAGE | UNESCO, award/prize recognition, and high demand |
| Tier 2 | HIGH CULTURAL VALUE | Historically important or widely recognized |
| Tier 3 | EDUCATIONAL VALUE | Useful, but low commercial demand |
| Tier 4 | ARCHIVAL ONLY | No commercial or product use |

Only Tier 1 and Tier 2 assets are eligible for Series, Products, and Marketplace entry.

## Output

The package output artifact is:

```text
global_ranked_assets.json
```

## Usage

```python
from wise_global_ranking import GlobalRankingInput, rank_assets

ranked_assets = rank_assets([
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
        awards_prizes=["UNESCO World Heritage inscription"],
    )
])
```
