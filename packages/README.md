# packages/

Shared Python libraries consumed by `services/` and `apps/`.

| Package | Purpose |
|---------|---------|
| `wise-common` | Configuration, logging, HTTP client utilities |
| `wise-contracts` | Canonical layer interface contracts (03 §7) |
| `wise-registry` | Source Registry + Agent/Capability Registry — models, migrations, schemas |
| `wise-orchestration` | LangGraph graphs, approval gates, manifest validation (Phase 0) |
| `wise-reference` | Reference Capability 1 domain schemas |
| `wise-metadata` | Metadata Agent v1 — modeling schema, normalization, mapping, validation |
| `wise-recognition-intelligence` | Award, prize, and historical-significance scoring for asset inclusion |

Install locally for development:

```bash
pip install -e packages/wise-common -e packages/wise-contracts -e packages/wise-registry \
  -e packages/wise-orchestration -e packages/wise-metadata -e packages/wise-reference \
  -e packages/wise-recognition-intelligence
```
