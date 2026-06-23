"""Helpers for validating preserved main-branch portfolio JSON."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO_DIR = ROOT / "data" / "portfolio"

RECORD_KEYS = ("assets", "collections", "series", "products", "candidates")


def load_portfolio_records(name: str) -> list[dict]:
    with (PORTFOLIO_DIR / name).open(encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in RECORD_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value

    raise TypeError(f"Unsupported portfolio payload in {name}")


def record_rank(record: dict) -> int:
    for key in ("portfolio_rank", "showcase_rank", "rank"):
        if key in record:
            return int(record[key])
    raise KeyError(f"No rank field found in record: {record.get('title')}")


def assert_ranked(records: list[dict], expected_count: int) -> None:
    assert len(records) == expected_count
    ranks = sorted(record_rank(record) for record in records)
    assert ranks == list(range(1, expected_count + 1))


def assert_score(record: dict, key: str) -> None:
    assert 0 <= record[key] <= 100
