"""Governance metrics for generated Portfolio Intelligence outputs.

This is implementation reporting only. It does not modify governance records,
architecture documents, ADRs, agents, or registries.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from wise_portfolio_intelligence import (
    BALANCED_GLOBAL_PORTFOLIO_DOMAINS,
    RIGHTS_STATUS_APPROVED,
    RIGHTS_STATUS_RESTRICTED,
    RIGHTS_STATUS_REVIEW_REQUIRED,
    RIGHTS_STATUS_UNKNOWN,
)

PORTFOLIO_GOVERNANCE_REPORT_FILENAME = "portfolio_governance_report.json"
MAX_CONCENTRATION_SHARE = 0.20

PRODUCT_CATEGORIES = (
    "Homepage Assets",
    "Collection Candidates",
    "Series Candidates",
    "Product Candidates",
)

_CANDIDATE_OUTPUT_KEYS = (
    "homepage_candidates",
    "collection_candidates",
    "series_candidates",
    "product_candidates",
    "archive_only",
)

_FIELD_ALIASES = {
    "country": (
        "country",
        "Country",
        "source_country",
        "sourceCountry",
        "region",
        "Region",
    ),
    "domain": (
        "domain",
        "Domain",
    ),
    "collection_family": (
        "collection_family",
        "collectionFamily",
        "Collection Family",
        "collection_id",
        "collectionId",
        "family",
    ),
    "narrative": (
        "narrative",
        "Narrative",
        "narrative_theme",
        "narrativeTheme",
        "story_theme",
        "storyTheme",
        "theme",
    ),
    "product": (
        "product",
        "Product",
        "product_category",
        "productCategory",
        "portfolio_category",
        "commercial_tier",
        "commercialTier",
        "asset_type",
        "assetType",
    ),
    "rights_status": (
        "rights_status",
        "rightsStatus",
        "Rights Status",
        "rc17_rights_status",
        "rc17RightsStatus",
    ),
}

_RIGHTS_STATUS_ALIASES = {
    "approved": RIGHTS_STATUS_APPROVED,
    "eligible": RIGHTS_STATUS_APPROVED,
    "cleared": RIGHTS_STATUS_APPROVED,
    "publishable": RIGHTS_STATUS_APPROVED,
    "review required": RIGHTS_STATUS_REVIEW_REQUIRED,
    "review": RIGHTS_STATUS_REVIEW_REQUIRED,
    "candidate only": RIGHTS_STATUS_REVIEW_REQUIRED,
    "needs review": RIGHTS_STATUS_REVIEW_REQUIRED,
    "restricted": RIGHTS_STATUS_RESTRICTED,
    "blocked": RIGHTS_STATUS_RESTRICTED,
    "excluded": RIGHTS_STATUS_RESTRICTED,
    "unknown": RIGHTS_STATUS_UNKNOWN,
    "": RIGHTS_STATUS_UNKNOWN,
}


@dataclass(frozen=True)
class PortfolioGovernanceReport:
    """Quality, balance, diversity, and representation metrics."""

    asset_count: int
    diversity_score: float
    representation_score: float
    concentration_risk_score: float
    coverage_score: float
    portfolio_health_score: float
    publishable_asset_percentage: float
    blocked_asset_percentage: float
    review_required_percentage: float
    distributions: dict[str, dict[str, Any]]
    diversity_metrics: dict[str, Any]
    rights_summary: dict[str, Any]
    publishable_assets: list[dict[str, Any]]
    blocked_assets: list[dict[str, Any]]
    rights_bottlenecks: list[dict[str, Any]]
    overrepresented_areas: list[dict[str, Any]]
    underrepresented_areas: list[dict[str, Any]]
    concentration_risks: list[dict[str, Any]]
    recommended_portfolio_adjustments: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def diversity_score(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return normalized distribution diversity across required dimensions."""
    distributions = _build_distributions(_coerce_assets(assets))
    entropy_scores = [
        _normalized_entropy(distribution["counts"])
        for distribution in distributions.values()
        if distribution["total"] > 0
    ]
    return _round_score(_average(entropy_scores))


def representation_score(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return balance and representation quality across portfolio dimensions."""
    normalized_assets = _coerce_assets(assets)
    distributions = _build_distributions(normalized_assets)
    scores = [
        _target_representation_score(
            distributions["domain"]["counts"],
            BALANCED_GLOBAL_PORTFOLIO_DOMAINS,
        ),
        _target_representation_score(
            distributions["product"]["counts"],
            PRODUCT_CATEGORIES,
        ),
        _normalized_entropy(distributions["geographic"]["counts"]),
        _normalized_entropy(distributions["collection_family"]["counts"]),
        _normalized_entropy(distributions["narrative"]["counts"]),
    ]
    return _round_score(_average(scores))


def concentration_risk_score(
    assets: Iterable[Mapping[str, Any]],
    *,
    max_concentration_share: float = MAX_CONCENTRATION_SHARE,
) -> float:
    """Return a 0-100 concentration risk score, where 100 is highest risk."""
    if max_concentration_share <= 0 or max_concentration_share > 1:
        raise ValueError("max_concentration_share must be greater than 0 and no more than 1")

    distributions = _build_distributions(_coerce_assets(assets))
    dimension_scores = [
        _dimension_concentration_risk(distributions[dimension]["counts"], max_concentration_share)
        for dimension in ("geographic", "domain", "collection_family")
        if distributions[dimension]["total"] > 0
    ]
    return _round_score(max(dimension_scores, default=0.0))


def coverage_score(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return coverage across required global domains and product surfaces."""
    distributions = _build_distributions(_coerce_assets(assets))
    scores = [
        _coverage_ratio(distributions["domain"]["counts"], BALANCED_GLOBAL_PORTFOLIO_DOMAINS),
        _coverage_ratio(distributions["product"]["counts"], PRODUCT_CATEGORIES),
        _freeform_coverage_score(distributions["geographic"]["counts"], target_unique=5),
        _freeform_coverage_score(distributions["collection_family"]["counts"], target_unique=5),
        _freeform_coverage_score(distributions["narrative"]["counts"], target_unique=4),
    ]
    return _round_score(_average(scores))


def portfolio_health_score(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return the blended portfolio health score, where 100 is healthiest."""
    normalized_assets = _coerce_assets(assets)
    diversity = diversity_score(normalized_assets)
    representation = representation_score(normalized_assets)
    concentration_risk = concentration_risk_score(normalized_assets)
    coverage = coverage_score(normalized_assets)
    return _round_score(
        (diversity * 0.30)
        + (representation * 0.25)
        + ((100.0 - concentration_risk) * 0.25)
        + (coverage * 0.20)
    )


def publishable_asset_percentage(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return percentage of assets with approved rights status."""
    normalized_assets = _coerce_assets(assets)
    return _rights_percentage(normalized_assets, {RIGHTS_STATUS_APPROVED})


def blocked_asset_percentage(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return percentage of assets blocked by restricted or unknown rights."""
    normalized_assets = _coerce_assets(assets)
    return _rights_percentage(normalized_assets, {RIGHTS_STATUS_RESTRICTED, RIGHTS_STATUS_UNKNOWN})


def review_required_percentage(assets: Iterable[Mapping[str, Any]]) -> float:
    """Return percentage of assets requiring rights review before publication."""
    normalized_assets = _coerce_assets(assets)
    return _rights_percentage(normalized_assets, {RIGHTS_STATUS_REVIEW_REQUIRED})


def generate_portfolio_governance_report(
    assets: Iterable[Mapping[str, Any]] | Mapping[str, Any],
    *,
    max_concentration_share: float = MAX_CONCENTRATION_SHARE,
) -> PortfolioGovernanceReport:
    """Generate a complete portfolio governance report."""
    if max_concentration_share <= 0 or max_concentration_share > 1:
        raise ValueError("max_concentration_share must be greater than 0 and no more than 1")

    normalized_assets = _coerce_assets(assets)
    distributions = _build_distributions(normalized_assets)
    overrepresented = _overrepresented_areas(distributions, max_concentration_share)
    underrepresented = _underrepresented_areas(distributions)
    concentration_risks = [
        area for area in overrepresented if area["dimension"] in {"geographic", "domain", "collection_family"}
    ]
    diversity = diversity_score(normalized_assets)
    representation = representation_score(normalized_assets)
    concentration_risk = concentration_risk_score(
        normalized_assets,
        max_concentration_share=max_concentration_share,
    )
    coverage = coverage_score(normalized_assets)
    rights_summary = _rights_summary(normalized_assets)
    health = _round_score(
        (diversity * 0.30)
        + (representation * 0.25)
        + ((100.0 - concentration_risk) * 0.25)
        + (coverage * 0.20)
    )

    return PortfolioGovernanceReport(
        asset_count=len(normalized_assets),
        diversity_score=diversity,
        representation_score=representation,
        concentration_risk_score=concentration_risk,
        coverage_score=coverage,
        portfolio_health_score=health,
        publishable_asset_percentage=rights_summary["publishable_asset_percentage"],
        blocked_asset_percentage=rights_summary["blocked_asset_percentage"],
        review_required_percentage=rights_summary["review_required_percentage"],
        distributions=distributions,
        diversity_metrics=_diversity_metrics(distributions),
        rights_summary=rights_summary,
        publishable_assets=_rights_assets(normalized_assets, {RIGHTS_STATUS_APPROVED}),
        blocked_assets=_rights_assets(
            normalized_assets,
            {RIGHTS_STATUS_RESTRICTED, RIGHTS_STATUS_UNKNOWN},
        ),
        rights_bottlenecks=_rights_bottlenecks(rights_summary),
        overrepresented_areas=overrepresented,
        underrepresented_areas=underrepresented,
        concentration_risks=concentration_risks,
        recommended_portfolio_adjustments=_recommend_adjustments(
            overrepresented=overrepresented,
            underrepresented=underrepresented,
            concentration_risks=concentration_risks,
        ),
    )


def write_portfolio_governance_report(
    assets: Iterable[Mapping[str, Any]] | Mapping[str, Any],
    output_dir: str | Path,
    *,
    max_concentration_share: float = MAX_CONCENTRATION_SHARE,
) -> PortfolioGovernanceReport:
    """Generate and write ``portfolio_governance_report.json``."""
    report = generate_portfolio_governance_report(
        assets,
        max_concentration_share=max_concentration_share,
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / PORTFOLIO_GOVERNANCE_REPORT_FILENAME).write_text(
        json.dumps(report.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def load_portfolio_assets(path: str | Path) -> list[dict[str, Any]]:
    """Load a portfolio JSON list, assets wrapper, or candidate-output object."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return _coerce_assets(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="Portfolio JSON list, assets wrapper, or candidate-output object")
    parser.add_argument(
        "--output-dir",
        default=".",
        help=f"Directory for {PORTFOLIO_GOVERNANCE_REPORT_FILENAME}",
    )
    args = parser.parse_args(argv)

    write_portfolio_governance_report(load_portfolio_assets(args.input_json), args.output_dir)
    return 0


def _coerce_assets(assets: Iterable[Mapping[str, Any]] | Mapping[str, Any]) -> list[dict[str, Any]]:
    if isinstance(assets, Mapping):
        if isinstance(assets.get("assets"), list):
            return [dict(asset) for asset in assets["assets"]]
        if any(key in assets for key in _CANDIDATE_OUTPUT_KEYS):
            flattened: list[dict[str, Any]] = []
            for key in _CANDIDATE_OUTPUT_KEYS:
                values = assets.get(key, [])
                if isinstance(values, list):
                    flattened.extend(dict(asset) for asset in values)
            return flattened
        raise ValueError("Portfolio mapping must contain assets or candidate output lists")
    return [dict(asset) for asset in assets]


def _build_distributions(assets: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    dimensions = {
        "geographic": Counter(_field_value(asset, "country") for asset in assets),
        "domain": Counter(_field_value(asset, "domain") for asset in assets),
        "collection_family": Counter(_field_value(asset, "collection_family") for asset in assets),
        "narrative": Counter(_field_value(asset, "narrative") for asset in assets),
        "product": Counter(_field_value(asset, "product") for asset in assets),
    }
    return {
        dimension: _distribution_payload(counts)
        for dimension, counts in dimensions.items()
    }


def _distribution_payload(counts: Counter[str]) -> dict[str, Any]:
    counts.pop("unknown", None)
    total = sum(counts.values())
    shares = {
        value: _round_score((count / total) * 100) if total else 0.0
        for value, count in counts.most_common()
    }
    return {
        "total": total,
        "unique_count": len(counts),
        "counts": dict(counts.most_common()),
        "share_percent": shares,
    }


def _field_value(asset: Mapping[str, Any], canonical_name: str) -> str:
    portfolio_inputs = asset.get("portfolio_inputs")
    if isinstance(portfolio_inputs, Mapping):
        nested = _read_alias(portfolio_inputs, canonical_name)
        if nested is not None:
            return _normalize_text(nested)

    value = _read_alias(asset, canonical_name)
    if value is not None:
        return _normalize_text(value)
    return "unknown"


def _read_alias(asset: Mapping[str, Any], canonical_name: str) -> Any:
    for alias in _FIELD_ALIASES[canonical_name]:
        if alias in asset and asset[alias] not in (None, ""):
            return asset[alias]
    return None


def _overrepresented_areas(
    distributions: Mapping[str, Mapping[str, Any]],
    max_concentration_share: float,
) -> list[dict[str, Any]]:
    threshold_percent = max_concentration_share * 100
    areas: list[dict[str, Any]] = []
    for dimension, distribution in distributions.items():
        for value, share in distribution["share_percent"].items():
            if share > threshold_percent:
                areas.append(
                    {
                        "dimension": dimension,
                        "value": value,
                        "share_percent": share,
                        "threshold_percent": threshold_percent,
                    }
                )
    return areas


def _underrepresented_areas(distributions: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    areas: list[dict[str, Any]] = []
    areas.extend(
        _missing_expected_values(
            "domain",
            distributions["domain"]["counts"],
            BALANCED_GLOBAL_PORTFOLIO_DOMAINS,
        )
    )
    areas.extend(
        _missing_expected_values(
            "product",
            distributions["product"]["counts"],
            PRODUCT_CATEGORIES,
        )
    )
    if distributions["geographic"]["unique_count"] < 5:
        areas.append(
            {
                "dimension": "geographic",
                "value": "global_distribution",
                "status": "below_target_unique_count",
                "observed_unique_count": distributions["geographic"]["unique_count"],
                "target_unique_count": 5,
            }
        )
    if distributions["narrative"]["unique_count"] < 4:
        areas.append(
            {
                "dimension": "narrative",
                "value": "narrative_distribution",
                "status": "below_target_unique_count",
                "observed_unique_count": distributions["narrative"]["unique_count"],
                "target_unique_count": 4,
            }
        )
    return areas


def _diversity_metrics(distributions: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    entropy_by_dimension = {
        dimension: _round_score(_normalized_entropy(distribution["counts"]))
        for dimension, distribution in distributions.items()
    }
    return {
        "method": "normalized_entropy_0_to_100",
        "by_dimension": entropy_by_dimension,
        "average": _round_score(_average(list(entropy_by_dimension.values()))),
    }


def _rights_percentage(assets: Sequence[Mapping[str, Any]], statuses: set[str]) -> float:
    if not assets:
        return 0.0
    count = sum(1 for asset in assets if _rights_status(asset) in statuses)
    return _round_score((count / len(assets)) * 100)


def _rights_summary(assets: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    counts = Counter(_rights_status(asset) for asset in assets)
    total = len(assets)
    return {
        "total": total,
        "counts": {
            RIGHTS_STATUS_APPROVED: counts.get(RIGHTS_STATUS_APPROVED, 0),
            RIGHTS_STATUS_REVIEW_REQUIRED: counts.get(RIGHTS_STATUS_REVIEW_REQUIRED, 0),
            RIGHTS_STATUS_RESTRICTED: counts.get(RIGHTS_STATUS_RESTRICTED, 0),
            RIGHTS_STATUS_UNKNOWN: counts.get(RIGHTS_STATUS_UNKNOWN, 0),
        },
        "publishable_asset_percentage": _rights_percentage(assets, {RIGHTS_STATUS_APPROVED}),
        "blocked_asset_percentage": _rights_percentage(
            assets,
            {RIGHTS_STATUS_RESTRICTED, RIGHTS_STATUS_UNKNOWN},
        ),
        "review_required_percentage": _rights_percentage(assets, {RIGHTS_STATUS_REVIEW_REQUIRED}),
    }


def _rights_assets(assets: Sequence[Mapping[str, Any]], statuses: set[str]) -> list[dict[str, Any]]:
    return [
        _asset_summary(asset, rights_status)
        for asset in assets
        if (rights_status := _rights_status(asset)) in statuses
    ]


def _rights_bottlenecks(rights_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    total = rights_summary["total"]
    if total == 0:
        return []

    bottlenecks: list[dict[str, Any]] = []
    for rights_status, recommendation in (
        (
            RIGHTS_STATUS_REVIEW_REQUIRED,
            "Resolve rights review before promoting candidate-only assets to publishable surfaces.",
        ),
        (
            RIGHTS_STATUS_RESTRICTED,
            "Remove restricted assets from publishable portfolio consideration.",
        ),
        (
            RIGHTS_STATUS_UNKNOWN,
            "Complete rights discovery before considering unknown-rights assets.",
        ),
    ):
        count = rights_summary["counts"].get(rights_status, 0)
        if count:
            bottlenecks.append(
                {
                    "rights_status": rights_status,
                    "count": count,
                    "share_percent": _round_score((count / total) * 100),
                    "recommendation": recommendation,
                }
            )
    return bottlenecks


def _asset_summary(asset: Mapping[str, Any], rights_status: str) -> dict[str, Any]:
    portfolio_inputs = asset.get("portfolio_inputs") if isinstance(asset.get("portfolio_inputs"), Mapping) else {}
    return {
        "id": asset.get("id") or asset.get("asset_id") or asset.get("assetId"),
        "rights_status": rights_status,
        "portfolio_category": asset.get("portfolio_category"),
        "domain": asset.get("domain") or portfolio_inputs.get("domain"),
        "country": asset.get("country") or portfolio_inputs.get("country") or asset.get("region"),
        "collection_family": asset.get("collection_family") or portfolio_inputs.get("collection_family"),
    }


def _rights_status(asset: Mapping[str, Any]) -> str:
    portfolio_inputs = asset.get("portfolio_inputs")
    if isinstance(portfolio_inputs, Mapping):
        nested = _read_alias(portfolio_inputs, "rights_status")
        if nested is not None:
            return _normalize_rights_status(nested)

    value = _read_alias(asset, "rights_status")
    if value is not None:
        return _normalize_rights_status(value)
    return RIGHTS_STATUS_UNKNOWN


def _normalize_rights_status(value: Any) -> str:
    return _RIGHTS_STATUS_ALIASES.get(_normalize_text(value), RIGHTS_STATUS_UNKNOWN)


def _missing_expected_values(
    dimension: str,
    counts: Mapping[str, int],
    expected_values: Iterable[str],
) -> list[dict[str, Any]]:
    present = set(counts)
    return [
        {
            "dimension": dimension,
            "value": expected,
            "status": "missing_expected_coverage",
        }
        for expected in expected_values
        if _normalize_text(expected) not in present
    ]


def _recommend_adjustments(
    *,
    overrepresented: Sequence[Mapping[str, Any]],
    underrepresented: Sequence[Mapping[str, Any]],
    concentration_risks: Sequence[Mapping[str, Any]],
) -> list[str]:
    recommendations: list[str] = []
    for risk in concentration_risks:
        recommendations.append(
            "Reduce selection weight for "
            f"{risk['dimension']} '{risk['value']}' until it falls at or below "
            f"{risk['threshold_percent']}%."
        )
    for area in underrepresented:
        if area.get("status") == "missing_expected_coverage":
            recommendations.append(
                f"Add or promote candidates covering {area['dimension']} '{area['value']}'."
            )
        elif area.get("status") == "below_target_unique_count":
            recommendations.append(
                f"Increase {area['dimension']} variety from {area['observed_unique_count']} "
                f"to at least {area['target_unique_count']} distinct values."
            )
    if not recommendations and not overrepresented:
        recommendations.append("Portfolio is balanced against current governance metrics; maintain monitoring.")
    return list(dict.fromkeys(recommendations))


def _normalized_entropy(counts: Mapping[str, int]) -> float:
    total = sum(counts.values())
    unique = len(counts)
    if total == 0 or unique <= 1:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log(probability)
    return (entropy / math.log(unique)) * 100


def _target_representation_score(counts: Mapping[str, int], expected_values: Iterable[str]) -> float:
    expected = tuple(_normalize_text(value) for value in expected_values)
    if not expected:
        return 0.0
    total = sum(counts.values())
    if total == 0:
        return 0.0
    ideal_share = 1 / len(expected)
    total_variation = 0.0
    for expected_value in expected:
        observed_share = counts.get(expected_value, 0) / total
        total_variation += abs(observed_share - ideal_share)
    unexpected_share = sum(
        count / total for value, count in counts.items() if value not in expected
    )
    total_variation += unexpected_share
    return max(0.0, (1 - (total_variation / 2)) * 100)


def _dimension_concentration_risk(
    counts: Mapping[str, int],
    max_concentration_share: float,
) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    top_share = max(counts.values()) / total
    if top_share <= max_concentration_share:
        return 0.0
    return ((top_share - max_concentration_share) / (1 - max_concentration_share)) * 100


def _coverage_ratio(counts: Mapping[str, int], expected_values: Iterable[str]) -> float:
    expected = {_normalize_text(value) for value in expected_values}
    if not expected:
        return 0.0
    present = set(counts)
    return (len(expected & present) / len(expected)) * 100


def _freeform_coverage_score(counts: Mapping[str, int], *, target_unique: int) -> float:
    if target_unique <= 0:
        return 0.0
    return min(len(counts) / target_unique, 1.0) * 100


def _normalize_text(value: Any) -> str:
    return " ".join(str(value).strip().lower().replace("-", " ").replace("_", " ").split())


def _average(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _round_score(value: float) -> float:
    return round(value, 2)


if __name__ == "__main__":
    raise SystemExit(main())
