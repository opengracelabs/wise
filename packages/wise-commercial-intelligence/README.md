# wise-commercial-intelligence

Commercial Intelligence scoring for WISE assets under frozen architecture-v1.0.

## Scope

This package measures commercial desirability separately from recognition score and historical importance.

Inputs:

- `recognition_score`
- `award_tags`
- `historical_significance_level`
- optional asset metadata that helps score visual, emotional, education, tourism, and gift demand

It is a scoring library only. It does not add governance agents, mutate architecture manifests, add registry tables, or alter Architecture v1.0.

## Scoring dimensions

`commercial_appeal_score` is a 0-100 composite:

| Dimension | Range |
|-----------|-------|
| Visual Impact | 0-25 |
| Emotional Connection | 0-25 |
| Educational Demand | 0-20 |
| Tourism Interest | 0-15 |
| Giftability | 0-15 |

`final_selection_score` combines recognition and commercial appeal while preserving their separation:

```text
final_selection_score = round((recognition_score * 0.40) + (commercial_appeal_score * 0.60))
```

## Commercial tiers

| Tier | Rule |
|------|------|
| Icon Product | `final_selection_score >= 85` and `commercial_appeal_score >= 80` |
| Strong Product | `final_selection_score >= 70` and `commercial_appeal_score >= 65` |
| Educational Product | `educational_demand >= 14` or `final_selection_score >= 55` |
| Archive Only | Everything else |

## Output

```json
{
  "recognition_score": 92,
  "commercial_appeal_score": 88,
  "final_selection_score": 90,
  "commercial_tier": "Icon Product"
}
```

Additional diagnostic fields include the five-dimension `commercial_breakdown`.

## Sample rankings

Sample ranking inputs are provided in `src/wise_commercial_intelligence/samples/sample_rankings.json`.
Expected ranked output rows are provided in `src/wise_commercial_intelligence/samples/sample_rankings_output.json`.

## Tests

```bash
pip install -e packages/wise-commercial-intelligence
pytest tests/commercial -v
```
