# wise-portfolio-intelligence

Portfolio Intelligence selects a balanced, high-value mix of WISE assets,
collections, and series while preserving Architecture v1.0 boundaries.

This package follows ADR-011 by remaining implementation-only:

- no governance changes
- no new agents
- no registry expansion
- no orchestration contract changes

## Inputs

Each asset should include:

- `recognition_score`
- `demand_score`
- `commercial_tier`
- `asset_type`
- `domain`
- `region`

For concentration controls, `country` and `collection_family` are also accepted.
If `country` is absent, `region` is used for the country cap.

## Outputs

The portfolio writer emits:

- `homepage_candidates.json`
- `collection_candidates.json`
- `series_candidates.json`
- `product_candidates.json`

Archive-only assets remain available in the in-memory result but are not written
as a required output file.

## Tests

```bash
PYTHONPATH=packages/wise-portfolio-intelligence/src pytest tests/portfolio_intelligence -v
```
