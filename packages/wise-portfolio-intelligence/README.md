# wise-portfolio-intelligence

Portfolio Intelligence selection for WISE assets under frozen architecture-v1.0.

## Scope

This package integrates commercial intelligence into portfolio candidate selection while preserving mission, diversity, collection-balance, and rights constraints.

It is a scoring and selection library only. It does not add governance agents, mutate architecture manifests, modify ADRs, add registry tables, enable payments, add checkout, or collect customer data.

## Inputs

The portfolio input adapter accepts:

- `recognition_score`
- `commercial_appeal_score`
- `commercial_tier`
- `final_selection_score`
- `rights_status`
- country/domain/collection-family metadata used by portfolio balance caps

If commercial fields are not present, the adapter can calculate them with `wise-commercial-intelligence`.

## Selection logic

1. Apply rights gate:
   - `Unknown` and `Restricted` are excluded.
   - `Review Required` may remain in internal candidate lists but is marked `publishable: false`.
2. Score assets with a balanced score:
   - recognition remains the largest factor,
   - commercial appeal influences rank,
   - commercial appeal cannot bypass rights or balance caps.
3. Select items while enforcing country, domain, and collection-family caps.
4. Emit candidate rows for homepage, collections, series, and products.

## Candidate outputs

Packaged sample outputs:

- `src/wise_portfolio_intelligence/outputs/homepage_candidates.json`
- `src/wise_portfolio_intelligence/outputs/collection_candidates.json`
- `src/wise_portfolio_intelligence/outputs/series_candidates.json`
- `src/wise_portfolio_intelligence/outputs/product_candidates.json`

Each selected item includes:

- `recognition_score`
- `commercial_appeal_score`
- `final_selection_score`
- `commercial_tier`
- `portfolio_category`
- `rights_status`
- `why_this_asset_was_selected`

## Tests

```bash
pip install -e packages/wise-commercial-intelligence -e packages/wise-portfolio-intelligence
pytest tests/portfolio -v
```
