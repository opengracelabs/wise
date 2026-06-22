"""Balanced portfolio selection for assets, collections, and series.

Architecture v1.0 remains frozen. This module implements ADR-011-compatible
selection logic only; it does not add governance records, agents, registries, or
canonical architecture changes.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

HOMEPAGE_CANDIDATES_FILENAME = "homepage_candidates.json"
COLLECTION_CANDIDATES_FILENAME = "collection_candidates.json"
SERIES_CANDIDATES_FILENAME = "series_candidates.json"
PRODUCT_CANDIDATES_FILENAME = "product_candidates.json"

CATEGORY_HOMEPAGE_ASSET = "Homepage Assets"
CATEGORY_COLLECTION_CANDIDATE = "Collection Candidates"
CATEGORY_SERIES_CANDIDATE = "Series Candidates"
CATEGORY_PRODUCT_CANDIDATE = "Product Candidates"
CATEGORY_ARCHIVE_ONLY = "Archive Only"

RIGHTS_STATUS_APPROVED = "Approved"
RIGHTS_STATUS_REVIEW_REQUIRED = "Review Required"
RIGHTS_STATUS_RESTRICTED = "Restricted"
RIGHTS_STATUS_UNKNOWN = "Unknown"

RIGHTS_ELIGIBILITY_ELIGIBLE = "eligible"
RIGHTS_ELIGIBILITY_CANDIDATE_ONLY = "candidate_only"
RIGHTS_ELIGIBILITY_EXCLUDED = "excluded"

BALANCED_GLOBAL_PORTFOLIO_DOMAINS = (
    "heritage",
    "biodiversity",
    "protected areas",
    "art",
    "historical maps",
    "cultural traditions",
)

MAX_CONCENTRATION_SHARE = 0.20

_FIELD_ALIASES = {
    "recognition_score": (
        "recognition_score",
        "recognitionScore",
        "recognition",
        "Recognition Score",
    ),
    "demand_score": (
        "demand_score",
        "demandScore",
        "Demand Score",
        "portfolio_demand_score",
    ),
    "commercial_tier": (
        "commercial_tier",
        "commercialTier",
        "Commercial Tier",
        "tier",
    ),
    "asset_type": (
        "asset_type",
        "assetType",
        "Asset Type",
        "type",
    ),
    "domain": (
        "domain",
        "Domain",
    ),
    "region": (
        "region",
        "Region",
    ),
    "country": (
        "country",
        "Country",
        "source_country",
        "sourceCountry",
    ),
    "collection_family": (
        "collection_family",
        "collectionFamily",
        "Collection Family",
        "collection_id",
        "collectionId",
        "family",
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

_COMMERCIAL_TIER_SCORES = {
    "homepage": 100.0,
    "premium": 100.0,
    "tier_1": 100.0,
    "tier 1": 100.0,
    "high": 90.0,
    "collection": 85.0,
    "series": 80.0,
    "standard": 70.0,
    "tier_2": 70.0,
    "tier 2": 70.0,
    "product": 65.0,
    "mid": 60.0,
    "low": 40.0,
    "tier_3": 40.0,
    "tier 3": 40.0,
    "archive": 0.0,
    "archive only": 0.0,
    "archival": 0.0,
    "restricted": 0.0,
    "noncommercial": 0.0,
    "non-commercial": 0.0,
    "none": 0.0,
}

_ARCHIVE_TIERS = {
    "archive",
    "archive only",
    "archival",
    "restricted",
    "noncommercial",
    "non-commercial",
    "none",
}

_ASSET_TYPES = {"asset", "image", "object", "place", "map", "media"}
_COLLECTION_TYPES = {"collection", "collection candidate", "set"}
_SERIES_TYPES = {"series", "series candidate", "sequence"}


@dataclass(frozen=True)
class PortfolioAsset:
    """Normalized asset with portfolio selection metadata."""

    source: dict[str, Any]
    recognition_score: float
    demand_score: float
    commercial_tier: str
    commercial_tier_score: float
    asset_type: str
    domain: str
    region: str
    country: str | None
    collection_family: str | None
    rights_status: str
    rights_eligibility: str
    rights_publishable: bool
    portfolio_priority_score: float
    category: str
    concentration_keys: dict[str, str]
    selection_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable asset payload with portfolio metadata."""
        payload = dict(self.source)
        payload["portfolio_priority_score"] = self.portfolio_priority_score
        payload["portfolio_category"] = self.category
        payload["rights_status"] = self.rights_status
        payload["rights_eligibility"] = self.rights_eligibility
        payload["rights_publishable"] = self.rights_publishable
        payload["portfolio_inputs"] = {
            "recognition_score": self.recognition_score,
            "demand_score": self.demand_score,
            "commercial_tier": self.commercial_tier,
            "asset_type": self.asset_type,
            "domain": self.domain,
            "region": self.region,
            "country": self.country,
            "collection_family": self.collection_family,
            "rights_status": self.rights_status,
        }
        payload["selection_notes"] = list(self.selection_notes)
        return payload


@dataclass(frozen=True)
class PortfolioSelectionResult:
    """Balanced candidate outputs plus archive-only assets."""

    homepage_candidates: list[dict[str, Any]]
    collection_candidates: list[dict[str, Any]]
    series_candidates: list[dict[str, Any]]
    product_candidates: list[dict[str, Any]]
    archive_only: list[dict[str, Any]]

    def to_dict(self) -> dict[str, list[dict[str, Any]]]:
        return asdict(self)


def calculate_portfolio_priority_score(
    *,
    recognition_score: float,
    demand_score: float,
    commercial_tier: str | int | float,
    domain: str,
) -> float:
    """Calculate the portfolio priority score on a 0-100 scale.

    Recognition and demand carry the highest weight. Commercial tier contributes
    merchandising readiness, and the domain term favors the six stated global
    portfolio goals without excluding other domains.
    """
    recognition = _coerce_score(recognition_score, "recognition_score")
    demand = _coerce_score(demand_score, "demand_score")
    tier_score = _commercial_tier_score(commercial_tier)
    domain_alignment = 100.0 if _normalize_text(domain) in BALANCED_GLOBAL_PORTFOLIO_DOMAINS else 0.0

    return round(
        (recognition * 0.40)
        + (demand * 0.40)
        + (tier_score * 0.15)
        + (domain_alignment * 0.05),
        2,
    )


def select_portfolio(
    assets: Iterable[Mapping[str, Any]],
    *,
    max_concentration_share: float = MAX_CONCENTRATION_SHARE,
    portfolio_limit: int | None = None,
) -> PortfolioSelectionResult:
    """Select a balanced global portfolio from candidate assets.

    Concentration controls are enforced across the selected portfolio. Missing
    concentration values are ignored, except `region` is used as a country proxy
    when no country field is available because `region` is a required input.
    """
    if max_concentration_share <= 0 or max_concentration_share > 1:
        raise ValueError("max_concentration_share must be greater than 0 and no more than 1")

    normalized_assets = [_normalize_asset(asset) for asset in assets]
    archive_assets = [asset for asset in normalized_assets if asset.category == CATEGORY_ARCHIVE_ONLY]
    candidates = sorted(
        (asset for asset in normalized_assets if asset.category != CATEGORY_ARCHIVE_ONLY),
        key=lambda asset: asset.portfolio_priority_score,
        reverse=True,
    )

    target_size = portfolio_limit or len(candidates)
    if target_size < 0:
        raise ValueError("portfolio_limit must be non-negative")
    concentration_cap = _concentration_cap(target_size, max_concentration_share)

    selected: list[PortfolioAsset] = []
    concentration_counts: dict[str, dict[str, int]] = {
        "country": {},
        "domain": {},
        "collection_family": {},
    }
    concentrated_archive: list[dict[str, Any]] = []

    for candidate in candidates:
        if len(selected) >= target_size:
            concentrated_archive.append(
                _archive_payload(candidate, "portfolio_limit_reached")
            )
            continue

        if _would_over_concentrate(candidate, concentration_counts, concentration_cap):
            concentrated_archive.append(
                _archive_payload(candidate, "over_concentration_limit")
            )
            continue

        selected.append(candidate)
        _increment_concentration_counts(candidate, concentration_counts)

    return _build_selection_result(
        selected=selected,
        archive_assets=[asset.to_dict() for asset in archive_assets] + concentrated_archive,
    )


def write_portfolio_outputs(
    assets: Iterable[Mapping[str, Any]],
    output_dir: str | Path,
    *,
    max_concentration_share: float = MAX_CONCENTRATION_SHARE,
    portfolio_limit: int | None = None,
) -> PortfolioSelectionResult:
    """Select the portfolio and write the four required candidate JSON outputs."""
    result = select_portfolio(
        assets,
        max_concentration_share=max_concentration_share,
        portfolio_limit=portfolio_limit,
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    _write_json(destination / HOMEPAGE_CANDIDATES_FILENAME, result.homepage_candidates)
    _write_json(destination / COLLECTION_CANDIDATES_FILENAME, result.collection_candidates)
    _write_json(destination / SERIES_CANDIDATES_FILENAME, result.series_candidates)
    _write_json(destination / PRODUCT_CANDIDATES_FILENAME, result.product_candidates)
    return result


def load_assets(path: str | Path) -> list[dict[str, Any]]:
    """Load assets from a JSON list or an object containing an ``assets`` list."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [dict(asset) for asset in payload]
    if isinstance(payload, dict) and isinstance(payload.get("assets"), list):
        return [dict(asset) for asset in payload["assets"]]
    raise ValueError("Input JSON must be a list of assets or an object with an assets list")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="JSON list of assets, or object with an assets list")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for portfolio candidate JSON outputs",
    )
    parser.add_argument(
        "--portfolio-limit",
        type=int,
        default=None,
        help="Maximum selected portfolio size before category splitting",
    )
    args = parser.parse_args(argv)

    write_portfolio_outputs(
        load_assets(args.input_json),
        args.output_dir,
        portfolio_limit=args.portfolio_limit,
    )
    return 0


def _normalize_asset(asset: Mapping[str, Any]) -> PortfolioAsset:
    source = dict(asset)
    recognition_score = _read_required_score(source, "recognition_score")
    demand_score = _read_required_score(source, "demand_score")
    commercial_tier = str(_read_required(source, "commercial_tier"))
    asset_type = _normalize_text(str(_read_required(source, "asset_type")))
    domain = _normalize_text(str(_read_required(source, "domain")))
    region = str(_read_required(source, "region")).strip()
    country = _read_optional_text(source, "country") or region
    collection_family = _read_optional_text(source, "collection_family")
    rights_status = _normalize_rights_status(_read_optional_text(source, "rights_status"))
    rights_eligibility = _rights_eligibility(rights_status)
    rights_publishable = rights_status == RIGHTS_STATUS_APPROVED
    priority_score = calculate_portfolio_priority_score(
        recognition_score=recognition_score,
        demand_score=demand_score,
        commercial_tier=commercial_tier,
        domain=domain,
    )
    category, notes = _assign_category(
        recognition_score=recognition_score,
        demand_score=demand_score,
        commercial_tier=commercial_tier,
        asset_type=asset_type,
        portfolio_priority_score=priority_score,
        rights_status=rights_status,
    )

    return PortfolioAsset(
        source=source,
        recognition_score=recognition_score,
        demand_score=demand_score,
        commercial_tier=commercial_tier,
        commercial_tier_score=_commercial_tier_score(commercial_tier),
        asset_type=asset_type,
        domain=domain,
        region=region,
        country=country,
        collection_family=collection_family,
        rights_status=rights_status,
        rights_eligibility=rights_eligibility,
        rights_publishable=rights_publishable,
        portfolio_priority_score=priority_score,
        category=category,
        concentration_keys=_concentration_keys(
            country=country,
            domain=domain,
            collection_family=collection_family,
        ),
        selection_notes=notes,
    )


def _assign_category(
    *,
    recognition_score: float,
    demand_score: float,
    commercial_tier: str,
    asset_type: str,
    portfolio_priority_score: float,
    rights_status: str,
) -> tuple[str, tuple[str, ...]]:
    if rights_status in {RIGHTS_STATUS_RESTRICTED, RIGHTS_STATUS_UNKNOWN}:
        return CATEGORY_ARCHIVE_ONLY, ("rights_status_excluded",)

    tier = _normalize_text(commercial_tier)
    if tier in _ARCHIVE_TIERS:
        return CATEGORY_ARCHIVE_ONLY, ("commercial_tier_archive_only",)
    if portfolio_priority_score < 50 or recognition_score < 35 or demand_score < 35:
        return CATEGORY_ARCHIVE_ONLY, ("portfolio_priority_below_candidate_floor",)

    rights_notes: tuple[str, ...] = ()
    review_required = rights_status == RIGHTS_STATUS_REVIEW_REQUIRED
    if review_required:
        rights_notes = ("rights_review_required_not_publishable",)

    if asset_type in _COLLECTION_TYPES and portfolio_priority_score >= 60:
        return CATEGORY_COLLECTION_CANDIDATE, rights_notes
    if asset_type in _SERIES_TYPES and portfolio_priority_score >= 60:
        return CATEGORY_SERIES_CANDIDATE, rights_notes
    if asset_type in _ASSET_TYPES and recognition_score >= 75 and demand_score >= 75:
        if review_required:
            return CATEGORY_PRODUCT_CANDIDATE, rights_notes
        return CATEGORY_HOMEPAGE_ASSET, ()
    if portfolio_priority_score >= 60:
        return CATEGORY_PRODUCT_CANDIDATE, rights_notes
    return CATEGORY_ARCHIVE_ONLY, ("portfolio_priority_below_product_floor",)


def _build_selection_result(
    *,
    selected: list[PortfolioAsset],
    archive_assets: list[dict[str, Any]],
) -> PortfolioSelectionResult:
    homepage_candidates: list[dict[str, Any]] = []
    collection_candidates: list[dict[str, Any]] = []
    series_candidates: list[dict[str, Any]] = []
    product_candidates: list[dict[str, Any]] = []

    for asset in selected:
        payload = asset.to_dict()
        if asset.category == CATEGORY_HOMEPAGE_ASSET:
            homepage_candidates.append(payload)
        elif asset.category == CATEGORY_COLLECTION_CANDIDATE:
            collection_candidates.append(payload)
        elif asset.category == CATEGORY_SERIES_CANDIDATE:
            series_candidates.append(payload)
        elif asset.category == CATEGORY_PRODUCT_CANDIDATE:
            product_candidates.append(payload)
        else:
            archive_assets.append(payload)

    return PortfolioSelectionResult(
        homepage_candidates=homepage_candidates,
        collection_candidates=collection_candidates,
        series_candidates=series_candidates,
        product_candidates=product_candidates,
        archive_only=archive_assets,
    )


def _would_over_concentrate(
    candidate: PortfolioAsset,
    concentration_counts: dict[str, dict[str, int]],
    concentration_cap: int,
) -> bool:
    for dimension, value in candidate.concentration_keys.items():
        if concentration_counts[dimension].get(value, 0) + 1 > concentration_cap:
            return True
    return False


def _increment_concentration_counts(
    candidate: PortfolioAsset,
    concentration_counts: dict[str, dict[str, int]],
) -> None:
    for dimension, value in candidate.concentration_keys.items():
        concentration_counts[dimension][value] = concentration_counts[dimension].get(value, 0) + 1


def _archive_payload(asset: PortfolioAsset, reason: str) -> dict[str, Any]:
    payload = asset.to_dict()
    notes = payload.get("selection_notes", [])
    payload["portfolio_category"] = CATEGORY_ARCHIVE_ONLY
    payload["selection_notes"] = list(dict.fromkeys([*notes, reason]))
    return payload


def _concentration_cap(target_size: int, max_concentration_share: float) -> int:
    if target_size == 0:
        return 0
    return max(1, math.floor(target_size * max_concentration_share))


def _concentration_keys(
    *,
    country: str | None,
    domain: str,
    collection_family: str | None,
) -> dict[str, str]:
    keys = {"domain": domain}
    if country:
        keys["country"] = _normalize_text(country)
    if collection_family:
        keys["collection_family"] = _normalize_text(collection_family)
    return keys


def _read_required_score(asset: Mapping[str, Any], canonical_name: str) -> float:
    return _coerce_score(_read_required(asset, canonical_name), canonical_name)


def _read_required(asset: Mapping[str, Any], canonical_name: str) -> Any:
    for alias in _FIELD_ALIASES[canonical_name]:
        if alias in asset:
            return asset[alias]
    aliases = ", ".join(_FIELD_ALIASES[canonical_name])
    raise KeyError(f"Missing {canonical_name}; accepted fields: {aliases}")


def _read_optional_text(asset: Mapping[str, Any], canonical_name: str) -> str | None:
    for alias in _FIELD_ALIASES[canonical_name]:
        if alias in asset and asset[alias] is not None:
            value = str(asset[alias]).strip()
            return value or None
    return None


def _coerce_score(value: Any, field_name: str) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a numeric score") from exc
    if score < 0 or score > 100:
        raise ValueError(f"{field_name} must be between 0 and 100")
    return score


def _commercial_tier_score(value: str | int | float) -> float:
    if isinstance(value, int | float):
        return _coerce_score(value, "commercial_tier")
    normalized = _normalize_text(str(value))
    if normalized in _COMMERCIAL_TIER_SCORES:
        return _COMMERCIAL_TIER_SCORES[normalized]
    return 50.0


def _normalize_rights_status(value: str | None) -> str:
    if value is None:
        return RIGHTS_STATUS_UNKNOWN
    normalized = _normalize_text(value)
    return _RIGHTS_STATUS_ALIASES.get(normalized, RIGHTS_STATUS_UNKNOWN)


def _rights_eligibility(rights_status: str) -> str:
    if rights_status == RIGHTS_STATUS_APPROVED:
        return RIGHTS_ELIGIBILITY_ELIGIBLE
    if rights_status == RIGHTS_STATUS_REVIEW_REQUIRED:
        return RIGHTS_ELIGIBILITY_CANDIDATE_ONLY
    return RIGHTS_ELIGIBILITY_EXCLUDED


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().replace("-", " ").replace("_", " ").split())


def _write_json(path: Path, payload: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
