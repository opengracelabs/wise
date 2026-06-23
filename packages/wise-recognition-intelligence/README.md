# wise-recognition-intelligence

Recognition Intelligence scoring for WISE assets under frozen architecture-v1.0.

## Scope

This package adds deterministic award-based, prize-based, and historical-significance weighting before assets are selected for:

1. Collections
2. Series
3. Commercial products

It is a scoring library only. It does not add governance agents, mutate architecture manifests, or expand the platform source/agent registry.

## Scoring model

Recognition Score =

| Component | Range |
|-----------|-------|
| Awards Weight | 0-40 |
| Historical Importance | 0-30 |
| Citation Volume | 0-20 |
| Cultural Impact | 0-10 |

Assets must score at least 70 to be eligible for collections, series, or commercial products.

## Signals

The local award registry models:

- UNESCO World Heritage List
- Nobel Prize indirect relevance
- Pulitzer Prize photography and journalism archives
- Wildlife Photographer of the Year
- National Geographic Awards
- Smithsonian featured collections
- Wikipedia page views and citation counts
- Academic citation indicators when available

## Tests

```bash
pip install -e packages/wise-recognition-intelligence
pytest tests/recognition -v
```
