"""OpenTelemetry instrumentation layer (API or lightweight stub)."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import Any, Iterator
from uuid import uuid4

try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.trace import Span, Tracer

    _OTEL_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised when otel extra absent
    _OTEL_AVAILABLE = False
    otel_trace = None  # type: ignore[assignment]
    Span = Any  # type: ignore[misc, assignment]
    Tracer = Any  # type: ignore[misc, assignment]


@dataclass
class SpanContext:
    trace_id: str
    span_id: str
    attributes: dict[str, str | int | float | bool] = field(default_factory=dict)


@dataclass
class _StubSpan:
    context: SpanContext

    def set_attribute(self, key: str, value: str | int | float | bool) -> None:
        self.context.attributes[key] = value

    def end(self) -> None:
        return None


class StubTracer:
    """In-memory tracer when opentelemetry-api is not installed."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.spans: list[SpanContext] = []

    def start_span(self, name: str, *, attributes: dict[str, Any] | None = None) -> _StubSpan:
        trace_id = uuid4().hex
        span_id = uuid4().hex[:16]
        ctx = SpanContext(trace_id=trace_id, span_id=span_id)
        if attributes:
            for key, value in attributes.items():
                if isinstance(value, (str, int, float, bool)):
                    ctx.attributes[key] = value
        self.spans.append(ctx)
        return _StubSpan(context=ctx)


def get_tracer(name: str = "open-grace-observability") -> Tracer | StubTracer:
    if _OTEL_AVAILABLE:
        return otel_trace.get_tracer(name)
    return StubTracer(name)


def current_span_context() -> SpanContext | None:
    if _OTEL_AVAILABLE:
        span = otel_trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.is_valid:
            return SpanContext(
                trace_id=format(ctx.trace_id, "032x"),
                span_id=format(ctx.span_id, "016x"),
            )
        return None
    return None


@contextlib.contextmanager
def trace_agent_execution(
    agent_id: str,
    *,
    execution_id: str | None = None,
    tracer_name: str = "open-grace-observability",
) -> Iterator[SpanContext | Span]:
    """Start a span for an agent execution, yielding trace context for metric correlation."""
    tracer = get_tracer(tracer_name)
    span_name = f"agent.execution.{agent_id.rsplit('.', 1)[-1]}"
    attributes = {"agent.id": agent_id}
    if execution_id:
        attributes["execution.id"] = execution_id

    if _OTEL_AVAILABLE:
        with tracer.start_as_current_span(span_name, attributes=attributes) as span:
            yield span
    else:
        stub_tracer = tracer
        span = stub_tracer.start_span(span_name, attributes=attributes)
        try:
            yield span.context
        finally:
            span.end()


def metric_attributes_from_span(span_context: SpanContext | Span | None) -> dict[str, str]:
    if span_context is None:
        return {}
    if isinstance(span_context, SpanContext):
        return {
            "trace_id": span_context.trace_id,
            "span_id": span_context.span_id,
        }
    if _OTEL_AVAILABLE:
        ctx = span_context.get_span_context()
        if ctx and ctx.is_valid:
            return {
                "trace_id": format(ctx.trace_id, "032x"),
                "span_id": format(ctx.span_id, "016x"),
            }
    return {}
