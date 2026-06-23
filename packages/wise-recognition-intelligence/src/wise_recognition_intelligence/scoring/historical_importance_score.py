"""Historical-importance scoring for recognition intelligence."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Iterable, Mapping

SIGNIFICANCE_LEVEL_SCORES = {
    "global": 30,
    "world": 30,
    "civilizational": 30,
    "high": 24,
    "major": 24,
    "national": 20,
    "regional": 16,
    "moderate": 16,
    "local": 10,
    "limited": 6,
    "unknown": 0,
}


def clamp_score(value: float | int, lower: int, upper: int) -> int:
    """Clamp and round a score into an integer range."""

    return max(lower, min(upper, round(float(value))))


def infer_historical_significance_level(score: int) -> str:
    """Map a numeric historical score to a significance level."""

    if score >= 26:
        return "global"
    if score >= 20:
        return "high"
    if score >= 12:
        return "moderate"
    return "limited"


def _asset_year(asset: Mapping[str, Any]) -> int | None:
    for key in ("year", "date_created", "created_year", "event_year", "period_start_year"):
        value = asset.get(key)
        if value in (None, ""):
            continue
        if isinstance(value, int):
            return value
        text = str(value)
        for token in text.replace("/", "-").split("-"):
            token = token.strip()
            if token.lstrip("-").isdigit():
                return int(token)
    return None


def _age_bonus(asset: Mapping[str, Any]) -> int:
    year = _asset_year(asset)
    if year is None:
        return 0

    current_year = datetime.now(tz=UTC).year
    age = current_year - year
    if age >= 1000:
        return 8
    if age >= 250:
        return 6
    if age >= 100:
        return 4
    if age >= 50:
        return 2
    return 0


def score_historical_importance(asset: Mapping[str, Any], award_tags: Iterable[str] = ()) -> int:
    """Score historical importance on a 0-30 scale."""

    explicit_score = asset.get("historical_importance_score")
    if explicit_score is not None:
        return clamp_score(explicit_score, 0, 30)

    explicit_level = str(asset.get("historical_significance_level", "unknown")).lower()
    base_score = SIGNIFICANCE_LEVEL_SCORES.get(explicit_level, 0)

    tags = set(award_tags)
    if "unesco_world_heritage" in tags:
        base_score = max(base_score, SIGNIFICANCE_LEVEL_SCORES["global"])
    elif {"pulitzer_prize", "nobel_related"} & tags:
        base_score = max(base_score, SIGNIFICANCE_LEVEL_SCORES["high"])
    elif {"national_geographic_award", "smithsonian_featured_collection", "wildlife_photographer_of_the_year"} & tags:
        base_score = max(base_score, SIGNIFICANCE_LEVEL_SCORES["moderate"])

    if asset.get("documented_historical_event") or asset.get("primary_source"):
        base_score = max(base_score, SIGNIFICANCE_LEVEL_SCORES["major"])

    return clamp_score(base_score + _age_bonus(asset), 0, 30)
