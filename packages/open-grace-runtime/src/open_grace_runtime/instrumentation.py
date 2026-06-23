"""OpenTelemetry instrumentation for Open Grace Runtime v2 LangGraph nodes."""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

from open_grace_observability.layers.opentelemetry import (
    SpanContext,
    get_tracer,
    metric_attributes_from_span,
    trace_agent_execution,
)

try:
    from opentelemetry import metrics as otel_metrics
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    _OTEL_SDK_AVAILABLE = True
except ImportError:  # pragma: no cover
    _OTEL_SDK_AVAILABLE = False
    otel_metrics = None  # type: ignore[assignment]


@dataclass
class RuntimeMetricsSnapshot:
    execution_count: int = 0
    execution_success_count: int = 0
    execution_latency_ms_total: float = 0.0
    benchmark_scores: list[float] = field(default_factory=list)
    risk_gate_failures: int = 0
    capability_gate_failures: int = 0
    node_latencies_ms: dict[str, float] = field(default_factory=dict)

    @property
    def execution_success_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.execution_success_count / self.execution_count

    @property
    def execution_latency_ms(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.execution_latency_ms_total / self.execution_count

    @property
    def benchmark_score(self) -> float | None:
        if not self.benchmark_scores:
            return None
        return sum(self.benchmark_scores) / len(self.benchmark_scores)


class RuntimeInstrumentation:
    """Collects runtime execution metrics and optional OTel SDK instruments."""

    def __init__(self) -> None:
        self.snapshot = RuntimeMetricsSnapshot()
        self._reader: Any | None = None
        self._span_exporter: Any | None = None
        self._meter = None
        self._counters: dict[str, Any] = {}
        self._histograms: dict[str, Any] = {}
        self._configure_sdk()

    def _configure_sdk(self) -> None:
        if not _OTEL_SDK_AVAILABLE:
            return
        resource = Resource.create({"service.name": "open-grace-runtime"})
        span_exporter = InMemorySpanExporter()
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
        get_tracer("open-grace-runtime")  # ensure API tracer registered

        reader = InMemoryMetricReader()
        meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
        meter = meter_provider.get_meter("open-grace-runtime")
        self._reader = reader
        self._span_exporter = span_exporter
        self._meter = meter
        self._counters = {
            "execution_count": meter.create_counter(
                "open_grace_runtime_execution_count",
                description="Total runtime graph invocations",
            ),
            "risk_gate_failures": meter.create_counter(
                "open_grace_runtime_risk_gate_failures",
                description="Risk gate failures",
            ),
            "capability_gate_failures": meter.create_counter(
                "open_grace_runtime_capability_gate_failures",
                description="Capability gate failures",
            ),
        }
        self._histograms = {
            "execution_latency_ms": meter.create_histogram(
                "open_grace_runtime_execution_latency_ms",
                unit="ms",
                description="End-to-end execution latency",
            ),
            "node_latency_ms": meter.create_histogram(
                "open_grace_runtime_node_latency_ms",
                unit="ms",
                description="Per-node execution latency",
            ),
            "benchmark_score": meter.create_histogram(
                "open_grace_runtime_benchmark_score",
                description="Observed benchmark scores",
            ),
        }

    @contextmanager
    def trace_execution(
        self,
        *,
        agent_id: str,
        run_id: str,
    ) -> Iterator[SpanContext | Any]:
        start = time.perf_counter()
        with trace_agent_execution(agent_id, execution_id=run_id) as span:
            yield span
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.snapshot.execution_latency_ms_total += elapsed_ms
        attrs = {"agent_id": agent_id, "run_id": run_id}
        if self._histograms:
            self._histograms["execution_latency_ms"].record(elapsed_ms, attrs)

    @contextmanager
    def trace_node(self, node_name: str, *, agent_id: str, run_id: str) -> Iterator[None]:
        tracer = get_tracer("open-grace-runtime")
        start = time.perf_counter()
        span_name = f"runtime.node.{node_name}"
        if hasattr(tracer, "start_as_current_span"):
            with tracer.start_as_current_span(span_name, attributes={"agent.id": agent_id, "run.id": run_id}):
                try:
                    yield
                finally:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    self.snapshot.node_latencies_ms[node_name] = elapsed_ms
                    if self._histograms:
                        self._histograms["node_latency_ms"].record(
                            elapsed_ms,
                            {"node": node_name, "agent_id": agent_id},
                        )
        else:
            span = tracer.start_span(span_name, attributes={"agent.id": agent_id, "run.id": run_id})
            try:
                yield
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                self.snapshot.node_latencies_ms[node_name] = elapsed_ms
                span.end()

    def record_execution_outcome(
        self,
        *,
        agent_id: str,
        run_id: str,
        success: bool,
        halted: bool,
        gate_results: list[dict],
        benchmark_evaluations: list[dict] | None = None,
        span: SpanContext | Any | None = None,
    ) -> None:
        self.snapshot.execution_count += 1
        if success and not halted:
            self.snapshot.execution_success_count += 1

        attrs = {"agent_id": agent_id, "run_id": run_id}
        trace_attrs = metric_attributes_from_span(span)
        attrs.update(trace_attrs)

        if self._counters:
            self._counters["execution_count"].add(1, attrs)

        for gate in gate_results:
            if gate.get("passed"):
                continue
            name = gate.get("gate_name", "")
            if name == "risk_validation":
                self.snapshot.risk_gate_failures += 1
                if self._counters:
                    self._counters["risk_gate_failures"].add(1, attrs)
            elif name == "capability_validation":
                self.snapshot.capability_gate_failures += 1
                if self._counters:
                    self._counters["capability_gate_failures"].add(1, attrs)

        for row in benchmark_evaluations or []:
            value = float(row.get("observed_value", 0))
            self.snapshot.benchmark_scores.append(value)
            if self._histograms:
                self._histograms["benchmark_score"].record(
                    value,
                    {"benchmark_id": row.get("benchmark_id", ""), "agent_id": agent_id},
                )

    def prometheus_samples(self) -> list[dict[str, Any]]:
        snap = self.snapshot
        labels = {}
        samples: list[dict[str, Any]] = [
            {"name": "open_grace_runtime_execution_count", "value": snap.execution_count, "labels": labels},
            {
                "name": "open_grace_runtime_execution_success_rate",
                "value": snap.execution_success_rate,
                "labels": labels,
            },
            {
                "name": "open_grace_runtime_execution_latency_ms",
                "value": snap.execution_latency_ms,
                "labels": labels,
            },
            {
                "name": "open_grace_runtime_risk_gate_failures",
                "value": snap.risk_gate_failures,
                "labels": labels,
            },
            {
                "name": "open_grace_runtime_capability_gate_failures",
                "value": snap.capability_gate_failures,
                "labels": labels,
            },
        ]
        if snap.benchmark_score is not None:
            samples.append(
                {
                    "name": "open_grace_runtime_benchmark_score",
                    "value": snap.benchmark_score,
                    "labels": labels,
                }
            )
        return samples


_GLOBAL_INSTRUMENTATION = RuntimeInstrumentation()


def get_runtime_instrumentation() -> RuntimeInstrumentation:
    return _GLOBAL_INSTRUMENTATION
