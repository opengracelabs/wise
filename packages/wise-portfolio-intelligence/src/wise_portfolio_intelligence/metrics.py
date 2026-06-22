"""Portfolio governance metrics derived from committed portfolio outputs."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from wise_portfolio_intelligence.models import NARRATIVE_CATEGORIES

PORTFOLIO_OUTPUT_FILES: tuple[str, ...] = (
    "homepage_portfolio.json",
    "collection_portfolio.json",
    "series_portfolio.json",
    "product_portfolio.json",
)

METRIC_VERSION = "wise-portfolio-intelligence-metrics/0.1.0"
EXPECTED_GEOGRAPHIES: tuple[str, ...] = (
    "Africa",
    "Arctic",
    "Asia",
    "Europe",
    "North America",
    "Oceania",
    "South America",
)


def load_portfolio_outputs(package_root: Path) -> dict[str, dict[str, Any]]:
    """Load portfolio output JSON files from the package root."""

    return {
        output_file: json.loads((package_root / output_file).read_text(encoding="utf-8"))
        for output_file in PORTFOLIO_OUTPUT_FILES
    }


def build_portfolio_metrics(portfolios: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Calculate governance metrics from existing portfolio output artifacts."""

    portfolio_metrics = {
        output_file: _metrics_for_assets(portfolio["assets"])
        for output_file, portfolio in portfolios.items()
    }
    all_assets = [
        asset
        for portfolio in portfolios.values()
        for asset in portfolio["assets"]
    ]
    aggregate_metrics = _metrics_for_assets(all_assets)
    aggregate_metrics["unique_asset_count"] = len({asset["stable_id"] for asset in all_assets})
    aggregate_metrics["selection_count"] = len(all_assets)

    representation = _representation_summary(all_assets)

    return {
        "metrics_version": METRIC_VERSION,
        "source_portfolios": list(portfolios),
        "score_direction": {
            "diversity_score": "higher_is_better",
            "geographic_balance_score": "higher_is_better",
            "domain_balance_score": "higher_is_better",
            "asset_type_balance_score": "higher_is_better",
            "narrative_balance_score": "higher_is_better",
            "concentration_risk_score": "lower_is_better",
        },
        "aggregate_metrics": aggregate_metrics,
        "portfolio_metrics": portfolio_metrics,
        "representation": representation,
        "portfolio_risks": _portfolio_risks(aggregate_metrics, representation),
        "recommended_additions": _recommended_additions(representation),
    }


def build_metrics_from_package(package_root: Path) -> dict[str, Any]:
    """Load committed portfolio outputs and calculate metrics."""

    return build_portfolio_metrics(load_portfolio_outputs(package_root))


def _metrics_for_assets(assets: list[dict[str, Any]]) -> dict[str, Any]:
    geographic_balance = _balance_score(
        Counter(asset["geography"] for asset in assets),
        expected_values=EXPECTED_GEOGRAPHIES,
    )
    domain_balance = _balance_score(
        Counter(asset["domain"] for asset in assets),
        expected_values=NARRATIVE_CATEGORIES,
    )
    asset_type_balance = _balance_score(Counter(asset["asset_type"] for asset in assets))
    narrative_balance = _balance_score(
        Counter(asset["category"] for asset in assets),
        expected_values=NARRATIVE_CATEGORIES,
    )
    diversity_score = round(
        (geographic_balance + domain_balance + asset_type_balance + narrative_balance) / 4,
        2,
    )

    return {
        "diversity_score": diversity_score,
        "geographic_balance_score": geographic_balance,
        "domain_balance_score": domain_balance,
        "asset_type_balance_score": asset_type_balance,
        "narrative_balance_score": narrative_balance,
        "concentration_risk_score": _concentration_risk_score(
            Counter(asset["stable_id"] for asset in assets)
        ),
        "distributions": {
            "geography": dict(sorted(Counter(asset["geography"] for asset in assets).items())),
            "domain": dict(sorted(Counter(asset["domain"] for asset in assets).items())),
            "asset_type": dict(sorted(Counter(asset["asset_type"] for asset in assets).items())),
            "narrative": dict(sorted(Counter(asset["category"] for asset in assets).items())),
        },
    }


def _balance_score(
    counts: Counter[str],
    *,
    expected_values: tuple[str, ...] | None = None,
) -> float:
    """Score even representation on a 0-100 scale."""

    values = tuple(expected_values or counts.keys())
    if not values:
        return 0.0

    total = sum(counts.values())
    if total == 0:
        return 0.0

    ideal = total / len(values)
    max_deviation = total * 2 * (len(values) - 1) / len(values)
    if max_deviation == 0:
        return 100.0

    observed_deviation = sum(abs(counts.get(value, 0) - ideal) for value in values)
    return round(max(0.0, (1 - observed_deviation / max_deviation) * 100), 2)


def _concentration_risk_score(asset_counts: Counter[str]) -> float:
    """Return Herfindahl-Hirschman concentration risk on a 0-100 scale."""

    total = sum(asset_counts.values())
    if total == 0:
        return 0.0
    return round(sum((count / total) ** 2 for count in asset_counts.values()) * 100, 2)


def _representation_summary(assets: list[dict[str, Any]]) -> dict[str, Any]:
    geographies = Counter(asset["geography"] for asset in assets)
    domains = Counter(asset["domain"] for asset in assets)

    return {
        "top_represented_regions": _top_represented(geographies),
        "underrepresented_regions": _underrepresented(
            geographies,
            expected_values=EXPECTED_GEOGRAPHIES,
        ),
        "top_represented_domains": _top_represented(domains),
        "underrepresented_domains": _underrepresented(
            domains,
            expected_values=NARRATIVE_CATEGORIES,
        ),
    }


def _top_represented(counts: Counter[str], *, limit: int = 5) -> list[dict[str, Any]]:
    total = sum(counts.values())
    return [
        {"name": name, "count": count, "share": round(count / total, 2)}
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _underrepresented(
    counts: Counter[str],
    *,
    expected_values: tuple[str, ...],
) -> list[dict[str, Any]]:
    total = sum(counts.values())
    if not expected_values or total == 0:
        return []

    target_share = 1 / len(expected_values)
    threshold = target_share * 0.75
    return [
        {
            "name": name,
            "count": counts.get(name, 0),
            "share": round(counts.get(name, 0) / total, 2),
            "target_share": round(target_share, 2),
        }
        for name in sorted(expected_values)
        if counts.get(name, 0) / total < threshold
    ]


def _portfolio_risks(
    aggregate_metrics: dict[str, Any],
    representation: dict[str, Any],
) -> list[str]:
    risks: list[str] = []
    if aggregate_metrics["concentration_risk_score"] > 25:
        risks.append("Asset concentration risk exceeds low-risk threshold.")
    if aggregate_metrics["narrative_balance_score"] < 90:
        risks.append("Narrative balance is below target across required story categories.")
    if aggregate_metrics["geographic_balance_score"] < 90:
        risks.append("Geographic balance is below target.")
    if representation["underrepresented_regions"]:
        risks.append("One or more represented regions fall below target share.")
    if representation["underrepresented_domains"]:
        risks.append("One or more represented domains fall below target share.")
    if not risks:
        risks.append("No material representation risk detected in current portfolio outputs.")
    return risks


def _recommended_additions(representation: dict[str, Any]) -> list[str]:
    recommendations: list[str] = []

    for region in representation["underrepresented_regions"]:
        recommendations.append(f"Add candidate assets from {region['name']} to improve geographic balance.")
    for domain in representation["underrepresented_domains"]:
        recommendations.append(f"Add candidate assets in {domain['name']} to improve domain balance.")

    if not recommendations:
        recommendations.append(
            "Maintain current five-narrative balance; add future candidates only if they preserve the 20% caps."
        )
        recommendations.append(
            "Prioritize alternate high-ranking assets from new geographies before repeating existing regions."
        )

    return recommendations
