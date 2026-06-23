# wise-demand-intelligence

Demand Intelligence scoring and commercial readiness filters for WISE (architecture-v1.0).

## Capabilities

1. Enhanced demand scoring from raw recognition, emotional, visual, and market signals.
2. Recognition commercialization gate: assets with recognition score below 50 cannot be commercialized.
3. Commercial-ready filtering with archival rejection output.

## Tests

```bash
PYTHONPATH=packages/wise-demand-intelligence/src pytest tests/demand_intelligence -v
```
