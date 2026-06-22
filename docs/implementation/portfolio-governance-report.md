# Portfolio Governance Metrics Report

**Scope:** Portfolio quality and representation metrics generated from existing
`packages/wise-portfolio-intelligence/*_portfolio.json` outputs.

**Architecture boundary:** No architecture, governance, or ADR changes. This report
documents implementation-level portfolio metrics only.

## Source outputs

- `homepage_portfolio.json`
- `collection_portfolio.json`
- `series_portfolio.json`
- `product_portfolio.json`

## Aggregate metrics

| Metric | Score | Direction |
|--------|-------|-----------|
| Diversity Score | 91.67 | Higher is better |
| Geographic Balance Score | 66.67 | Higher is better |
| Domain Balance Score | 100.00 | Higher is better |
| Asset Type Balance Score | 100.00 | Higher is better |
| Narrative Balance Score | 100.00 | Higher is better |
| Concentration Risk Score | 20.00 | Lower is better |

The current outputs contain 20 total portfolio selections across 5 unique assets.
Each portfolio contains one asset per required narrative category and one asset per
represented domain and asset type. Geographic balance is lower because the current
portfolio outputs do not include Africa or Arctic coverage.

## Top represented regions

All represented regions are balanced at 20% of aggregate selections:

| Region | Count | Share |
|--------|-------|-------|
| Asia | 4 | 20% |
| Europe | 4 | 20% |
| North America | 4 | 20% |
| Oceania | 4 | 20% |
| South America | 4 | 20% |

## Underrepresented regions

| Region | Count | Share | Target Share |
|--------|-------|-------|--------------|
| Africa | 0 | 0% | 14% |
| Arctic | 0 | 0% | 14% |

## Top represented domains

All represented domains are balanced at 20% of aggregate selections:

| Domain | Count | Share |
|--------|-------|-------|
| Biodiversity | 4 | 20% |
| Climate | 4 | 20% |
| Culture | 4 | 20% |
| Geography | 4 | 20% |
| Heritage | 4 | 20% |

## Underrepresented domains

None detected in the current portfolio outputs. Every represented domain meets the
current equal-share target.

## Portfolio risks

- Geographic balance is below target.
- Africa and Arctic are absent from the measured output set.
- Concentration risk is low at 20.00 because no single asset exceeds the portfolio
  optimizer's 20% representation pattern across the measured output set.
- Future risk could emerge if new outputs repeat the same geography, domain, asset
  type, or narrative without adding offsetting selections.

## Recommended additions

- Add candidate assets from Africa to improve geographic balance.
- Add candidate assets from Arctic to improve geographic balance.
- When expanding beyond five assets per portfolio, add candidates that improve
  global coverage without increasing any single domain, geography, or asset type
  above its diversity threshold.

## Generated artifact

The machine-readable metrics artifact is:

```text
packages/wise-portfolio-intelligence/portfolio_metrics.json
```
