# Commercial + Portfolio Intelligence Integration Report

## Scope

This implementation integrates `wise-commercial-intelligence` with a new pure-library package, `wise-portfolio-intelligence`, so commercial appeal can influence candidate ranking without bypassing mission, diversity, collection-family, or rights constraints.

No governance agents, Architecture v1.0 documents, ADRs, registry tables, payments, checkout flows, or customer-data collection were added or modified.

## Scoring changes

Portfolio selection now accepts these commercial-intelligence fields:

- `recognition_score`
- `commercial_appeal_score`
- `commercial_tier`
- `final_selection_score`

If commercial fields are absent, the portfolio adapter can calculate them through `wise-commercial-intelligence`. Portfolio ranking uses a mission-first balanced score:

```text
balanced_portfolio_score =
  recognition_score * 0.45
  + historical_significance_weight * 0.20
  + final_selection_score * 0.20
  + commercial_appeal_score * 0.15
```

Commercial appeal therefore influences ordering, but recognition and historical significance remain dominant.

## Selection logic

Candidate selection runs in this order:

1. Normalize commercial and portfolio input fields.
2. Apply rights gating.
3. Rank candidates by balanced portfolio score.
4. Select candidates while enforcing diversity and portfolio-balance caps:
   - country cap,
   - domain cap,
   - collection-family cap.
5. Emit candidate outputs for:
   - `homepage_candidates.json`
   - `collection_candidates.json`
   - `series_candidates.json`
   - `product_candidates.json`

Because caps are applied during final selection, a high commercial score can improve an asset's rank within the eligible pool but cannot override country, domain, or collection-family balance.

## Rights gating behavior

The rights gate is intentionally a placeholder library gate, not a governance change.

| Rights status | Behavior |
|---------------|----------|
| `Unknown` | Excluded from candidate outputs |
| `Restricted` | Excluded from candidate outputs |
| `Review Required` | May remain in internal candidate outputs but is marked `publishable: false` |
| Other statuses | Considered publishable by this placeholder gate |

The candidate output schema includes `rights_status` and `publishable` so downstream publication workflows can keep review-required assets out of public surfaces.

## Output schema

Each selected item includes:

- `recognition_score`
- `commercial_appeal_score`
- `final_selection_score`
- `commercial_tier`
- `portfolio_category`
- `rights_status`
- `why_this_asset_was_selected`

Diagnostic fields also include `publishable`, country/domain/family fields, and `balanced_portfolio_score`.

## Tests run

Focused verification commands:

```bash
python3 -m pytest --confcutdir="tests/portfolio" "tests/portfolio" -v
python3 -m pytest --confcutdir="tests/portfolio" "tests/test_smoke.py::test_wise_portfolio_intelligence_imports" -v
```

The test suite covers:

- commercial score integration,
- fallback commercial scoring when portfolio inputs lack commercial fields,
- commercial score inability to override diversity caps,
- exclusion of `Unknown` and `Restricted` rights assets,
- `Review Required` assets marked as not publishable,
- output schema consistency for generated and packaged candidate outputs.

## Known gaps

- Rights handling is a placeholder and does not yet call canonical rights validation services.
- Diversity cap values are library configuration defaults, not steward-approved production policy.
- Candidate JSON files are packaged sample outputs, not production deployment artifacts.
- No payment, checkout, product analytics, or customer data flows are implemented.

## Recommended next release

For the next release, add a steward-reviewed configuration layer for portfolio caps and rights-status mappings, then connect the package to approved orchestration surfaces without changing agent definitions or registry schema.
