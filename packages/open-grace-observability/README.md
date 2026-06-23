# open-grace-observability

Open Grace Observability Framework v1 — governed metric registries, OpenTelemetry
instrumentation helpers, and static Prometheus/Grafana/Loki definitions.

## Metric domains

| Domain | Schema | ID pattern |
|--------|--------|------------|
| Agent execution | `AgentExecutionMetric` | `wise.metric.agent.{slug}` |
| Capability | `CapabilityMetric` | `wise.metric.capability.{slug}` |
| Benchmark | `BenchmarkMetric` | `wise.metric.benchmark.{slug}` |
| Audit | `AuditMetric` | `wise.metric.audit.{slug}` |
| Cost | `CostMetric` | `wise.metric.cost.{slug}` |

## Quick start

```python
from pathlib import Path
from open_grace_observability import ObservabilitySystem

system = ObservabilitySystem.create(Path(".open-grace-observability"))
system.seed_all()
```

## Governance integration

`GovernanceSystem.create()` provisions a nested `ObservabilitySystem`. Use
`record_agent_metric()`, `validate_metric_context()`, and `observability_reports()`
on the governance coordinator.

## Observability layers (v1)

- **OpenTelemetry** — trace/metric context helpers (stub when `opentelemetry-api` absent)
- **Prometheus** — metric definitions + exposition text helper
- **Grafana** — static dashboard JSON under `data/grafana/`
- **Loki** — label schemas and log stream definitions under `data/loki/`

## Tests

```bash
pip install -e packages/open-grace-observability -q
pytest tests/open_grace/test_observability_*.py -q
```
