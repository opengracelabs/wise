"""Shared schema primitives for observability metrics."""

from __future__ import annotations

import re
from enum import StrEnum

WISE_METRIC_ID = re.compile(
    r"^wise\.metric\.(agent|capability|benchmark|audit|cost)\.[a-z0-9]+(?:-[a-z0-9]+)*$"
)


class MetricDomain(StrEnum):
    AGENT = "agent"
    CAPABILITY = "capability"
    BENCHMARK = "benchmark"
    AUDIT = "audit"
    COST = "cost"


class MetricUnit(StrEnum):
    MILLISECONDS = "ms"
    SECONDS = "s"
    RATIO = "ratio"
    COUNT = "count"
    USD = "usd"
    TOKENS = "tokens"
    PERCENT = "percent"
