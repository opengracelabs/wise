# Portfolio Governance Metrics Implementation Report

**Authority:** Architecture v1.0 remains frozen (ADR-011)  
**Scope:** `packages/wise-portfolio-intelligence/src/wise_portfolio_intelligence/governance/` implementation reporting only

## Summary

Portfolio Governance Metrics measure the quality, balance, diversity, and
representation of generated portfolios. The implementation produces
`portfolio_governance_report.json` from portfolio candidate outputs or raw asset
lists.

This change does not modify:

- Governance records
- Architecture documents
- ADRs
- Agent Registry
- Capability Registry

## Metrics

The report includes five top-level scores:

1. `diversity_score` — normalized entropy across geographic, domain, collection
   family, narrative, and product distributions.
2. `representation_score` — balance against expected portfolio domains and
   product surfaces, plus evenness across free-form dimensions.
3. `concentration_risk_score` — highest observed concentration risk above the
   20% threshold.
4. `coverage_score` — coverage of global portfolio goals, product surfaces,
   geographic spread, collection-family spread, and narrative variety.
5. `portfolio_health_score` — blended health score using diversity,
   representation, inverse concentration risk, and coverage.

## Measured Distributions

The governance report records distributions for:

- Geographic distribution
- Domain distribution
- Collection family distribution
- Narrative distribution
- Product distribution

Each distribution includes total measured items, unique count, raw counts, and
share percentages.

## Overrepresented Areas

An area is overrepresented when its share exceeds the 20% concentration
threshold. This applies across all measured dimensions, with concentration-risk
tracking focused on geographic, domain, and collection-family dimensions.

## Underrepresented Areas

Underrepresented areas include:

- Missing global portfolio domains:
  - Heritage
  - Biodiversity
  - Protected Areas
  - Art
  - Historical Maps
  - Cultural Traditions
- Missing product surfaces:
  - Homepage Assets
  - Collection Candidates
  - Series Candidates
  - Product Candidates
- Geographic variety below five distinct values
- Narrative variety below four distinct values

## Diversity Metrics

Diversity is calculated with normalized entropy. A portfolio with values spread
evenly across a dimension scores higher than a portfolio dominated by one value.
The final diversity score is the average entropy score across the measured
dimensions with data.

## Concentration Risks

Concentration risk is scored from 0 to 100, where 0 means no measured dimension
exceeds the 20% cap and 100 means a dimension is fully concentrated in one value.
The report includes concrete risk entries for any geography, domain, or
collection family above the cap.

## Recommended Portfolio Adjustments

The report generates recommendations from detected risks and coverage gaps:

- Reduce selection weight for overrepresented geography, domain, or collection
  family values.
- Add or promote candidates for missing global portfolio domains.
- Add or promote candidates for missing product surfaces.
- Increase geographic and narrative variety when unique-count targets are not
  met.

## Output

The report writer creates:

```text
portfolio_governance_report.json
```

The JSON report includes overrepresented areas, underrepresented areas,
diversity metrics, concentration risks, recommended adjustments, and the five
top-level scores.
