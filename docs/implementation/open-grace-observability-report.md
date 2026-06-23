# Open Grace Observability Report

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-06-23 |
| **Scope** | Runtime v2 instrumentation sprint |

## Summary

Sprint 1 wires OpenTelemetry SDK instrumentation into Open Grace Runtime v2 LangGraph nodes and exposes Prometheus-compatible runtime metrics. The existing `open-grace-observability` stub tracer remains backward compatible when the SDK is absent.

## Instrumented Nodes

| Node | Span name | Metrics emitted |
|------|-----------|-----------------|
| `select_agent` | `runtime.node.select_agent` | node latency histogram |
| `validate_capability` | `runtime.node.validate_capability` | capability gate failures |
| `validate_risk` | `runtime.node.validate_risk` | risk gate failures |
| `select_model` | `runtime.node.select_model` | node latency |
| `execute` | `runtime.node.execute` | execution count, latency |
| `evaluate` | `runtime.node.evaluate` | benchmark score histogram |
| `audit` | `runtime.node.audit` | node latency |
| `persist` | `runtime.node.persist` | execution success rate |

## Metrics

| Metric | Type | Source |
|--------|------|--------|
| `open_grace_runtime_execution_count` | counter | `RuntimeInstrumentation.record_execution_outcome` |
| `open_grace_runtime_execution_success_rate` | gauge | derived from success / total |
| `open_grace_runtime_execution_latency_ms` | gauge / histogram | per-invocation wall time |
| `open_grace_runtime_benchmark_score` | histogram | evaluate node observed values |
| `open_grace_runtime_risk_gate_failures` | counter | `risk_validation` gate failures |
| `open_grace_runtime_capability_gate_failures` | counter | `capability_validation` gate failures |

Definitions added to `packages/open-grace-observability/src/open_grace_observability/data/prometheus/metric_definitions.yaml`.

## Dependencies

- `opentelemetry-api` — default dependency on `open-grace-observability` and `open-grace-runtime`
- `opentelemetry-sdk` — runtime instrumentation (`InMemoryMetricReader`, `MeterProvider`)
- `opentelemetry-exporter-prometheus` — available for production scrape endpoints

## Tests

- `tests/open_grace/test_runtime_instrumentation.py` — 4 tests
- Existing `test_observability_layers.py` and `test_observability_governance_integration.py` unchanged

## Gaps Remaining

| Gap | Priority |
|-----|----------|
| OTLP exporter endpoint configuration | Medium |
| Loki log stream wiring to runtime events | Low |
| Grafana dashboard panels for runtime v2 metrics | Medium |
| Production Prometheus scrape handler | Medium |

## Standards Mapping

| Standard | Improvement |
|----------|-------------|
| OpenTelemetry | SDK default; per-node spans; metric semantic names |
| ISO/IEC 42001 | Performance evaluation via benchmark score metrics |
| ISO/IEC 27001 | Audit node trace correlation via `run_id` |
| NIST AI RMF MEASURE | Benchmark observed values instrumented at runtime |

*Implementation report. Does not modify canonical architecture.*
