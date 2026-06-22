# wise-portfolio-intelligence

Portfolio curation and balancing for globally ranked WISE assets.

The package exposes `portfolio_optimizer()` to turn ranked assets into structured:

- `homepage_portfolio.json`
- `collection_portfolio.json`
- `series_portfolio.json`
- `product_portfolio.json`

## Inputs

Each asset carries:

- `global_rank_score`
- `recognition_score`
- `demand_score`
- `commercial_tier`
- `asset_type`
- `category`
- `geography`

`domain` is also accepted. When absent, `category` is used as the domain for diversity
constraints.

## Rules

- Max 20% per domain
- Max 20% per geography
- Max 20% per asset type
- Narrative balance across Heritage, Biodiversity, Geography, Culture, and Climate
- Ranking stabilization to prevent single-category domination
- Every selected asset includes `why_this_asset_was_selected`

This package adds no agents, governance records, ADRs, services, or architecture changes.
