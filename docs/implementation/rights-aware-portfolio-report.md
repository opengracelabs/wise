# Rights-Aware Portfolio Selection Implementation Report

**Scope:** Portfolio Intelligence implementation only  
**Architecture status:** Architecture v1.0 remains frozen

## Summary

Rights-aware portfolio selection integrates future RC17-style `rights_status`
signals into portfolio candidate selection and portfolio governance reporting.

This implementation does not modify:

- Governance records
- Architecture documents
- ADRs
- Agent Registry
- Capability Registry

## Portfolio Eligibility Rules

| Rights status | Portfolio behavior |
|---------------|--------------------|
| `Approved` | Eligible and publishable |
| `Review Required` | Candidate only; not publishable |
| `Restricted` | Excluded from candidate outputs |
| `Unknown` | Excluded from candidate outputs |

Missing rights status is treated as `Unknown` so candidate selection remains
conservative until rights discovery is complete.

## Candidate Output Support

The portfolio candidate payloads now include rights metadata in:

- `homepage_candidates.json`
- `collection_candidates.json`
- `series_candidates.json`
- `product_candidates.json`

Each candidate includes:

- `rights_status`
- `rights_eligibility`
- `rights_publishable`
- `portfolio_inputs.rights_status`

`Review Required` assets are retained only as non-publishable candidates.
Homepage-eligible review-required assets are downgraded to product candidates
until rights review is complete.

## Governance Metrics

`portfolio_governance_report.json` now includes:

- `publishable_asset_percentage`
- `blocked_asset_percentage`
- `review_required_percentage`
- `rights_summary`
- `publishable_assets`
- `blocked_assets`
- `rights_bottlenecks`

## Publishable Assets

Publishable assets are assets with `rights_status = Approved`. These can be
used on publishable surfaces subject to the existing portfolio balance rules.

## Blocked Assets

Blocked assets are assets with `rights_status = Restricted` or
`rights_status = Unknown`. These are excluded from candidate outputs and
reported as rights bottlenecks when present in report inputs.

## Rights Bottlenecks

Rights bottlenecks identify rights states that prevent publication or promotion:

- `Review Required` — resolve rights review before promoting candidate-only
  assets to publishable surfaces.
- `Restricted` — remove restricted assets from publishable portfolio
  consideration.
- `Unknown` — complete rights discovery before considering assets for portfolio
  selection.

## Tests

Tests cover:

- Approved assets flowing into publishable candidate outputs
- Review-required assets becoming candidate-only and non-publishable
- Restricted and unknown assets being excluded
- Rights-aware governance percentages
- Publishable/blocked asset report sections
- Rights bottleneck reporting
