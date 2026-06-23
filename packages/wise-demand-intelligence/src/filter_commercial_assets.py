"""Filter scored assets into commercial-ready and archival-only outputs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from scoring.enhanced_demand_score import (
    COMMERCIAL_RECOGNITION_GATE,
    score_asset,
)

COMMERCIAL_READY_FILENAME = "commercial_ready_assets.json"
REJECTED_ASSETS_FILENAME = "rejected_assets.json"

COMMERCIAL_READY_RECOGNITION_THRESHOLD = 70.0
COMMERCIAL_READY_DEMAND_THRESHOLD = 80.0
COMMERCIAL_READY_VISUAL_THRESHOLD = 25.0

_DEMAND_SCORE_ALIASES = (
    "demand_score",
    "demandScore",
    "Demand Score",
    "Final Demand Score",
)

_VISUAL_SCORE_ALIASES = (
    "visual_score",
    "visualScore",
    "visual_impact",
    "visualImpact",
    "Visual Score",
    "Visual Impact",
)

_RECOGNITION_SCORE_ALIASES = (
    "recognition_score",
    "recognitionScore",
    "recognition",
    "Recognition Score",
    "RecognitionScore",
)


@dataclass(frozen=True)
class CommercialAssetFilterResult:
    """Commercial filter outputs."""

    commercial_ready_assets: list[dict[str, Any]]
    rejected_assets: list[dict[str, Any]]


def filter_commercial_assets(assets: Iterable[Mapping[str, Any]]) -> CommercialAssetFilterResult:
    """Split assets using recognition, demand, and visual readiness thresholds.

    An asset can pass only when it is commercializable. The pass rule is:

    * Recognition Score >= 70, or
    * Demand Score >= 80 and Visual Score >= 25

    Assets rejected by either the recognition gate or readiness thresholds are
    retained for archival-only use.
    """
    commercial_ready_assets: list[dict[str, Any]] = []
    rejected_assets: list[dict[str, Any]] = []

    for asset in assets:
        evaluated_asset = dict(asset)
        rejection_reasons: list[str] = []

        try:
            score_payload = _score_payload(evaluated_asset)
            evaluated_asset["demand_intelligence"] = score_payload
            recognition_score = score_payload["recognition_score"]
            demand_score = score_payload["demand_score"]
            visual_score = score_payload["visual_impact"]
            commercializable = score_payload["commercializable"]
            rejection_reasons.extend(score_payload["rejection_reasons"])
        except (KeyError, ValueError) as exc:
            recognition_score = _read_optional_score(evaluated_asset, _RECOGNITION_SCORE_ALIASES)
            demand_score = _read_optional_score(evaluated_asset, _DEMAND_SCORE_ALIASES)
            visual_score = _read_optional_score(evaluated_asset, _VISUAL_SCORE_ALIASES)
            commercializable = bool(
                recognition_score is not None and recognition_score >= COMMERCIAL_RECOGNITION_GATE
            )
            rejection_reasons.append(f"demand_score_unavailable:{exc}")
            if not commercializable:
                rejection_reasons.append("recognition_score_below_commercialization_gate")

        passes_threshold = _passes_commercial_thresholds(
            recognition_score=recognition_score,
            demand_score=demand_score,
            visual_score=visual_score,
        )

        if commercializable and passes_threshold:
            evaluated_asset["commercial_ready"] = True
            commercial_ready_assets.append(evaluated_asset)
            continue

        if not passes_threshold:
            rejection_reasons.append("commercial_readiness_threshold_not_met")

        evaluated_asset["commercial_ready"] = False
        evaluated_asset["archival_only"] = True
        evaluated_asset["rejection_reasons"] = _dedupe_reasons(rejection_reasons)
        rejected_assets.append(evaluated_asset)

    return CommercialAssetFilterResult(
        commercial_ready_assets=commercial_ready_assets,
        rejected_assets=rejected_assets,
    )


def write_commercial_asset_outputs(
    assets: Iterable[Mapping[str, Any]],
    output_dir: str | Path,
) -> CommercialAssetFilterResult:
    """Filter assets and write commercial-ready and archival-only JSON outputs."""
    result = filter_commercial_assets(assets)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    (destination / COMMERCIAL_READY_FILENAME).write_text(
        json.dumps(result.commercial_ready_assets, indent=2) + "\n",
        encoding="utf-8",
    )
    (destination / REJECTED_ASSETS_FILENAME).write_text(
        json.dumps(result.rejected_assets, indent=2) + "\n",
        encoding="utf-8",
    )
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
        help="Directory for commercial_ready_assets.json and rejected_assets.json",
    )
    args = parser.parse_args(argv)

    write_commercial_asset_outputs(load_assets(args.input_json), args.output_dir)
    return 0


def _score_payload(asset: Mapping[str, Any]) -> dict[str, Any]:
    try:
        return score_asset(asset).to_dict()
    except KeyError:
        demand_score = _read_optional_score(asset, _DEMAND_SCORE_ALIASES)
        recognition_score = _read_optional_score(asset, _RECOGNITION_SCORE_ALIASES)
        visual_score = _read_optional_score(asset, _VISUAL_SCORE_ALIASES)
        if demand_score is None or recognition_score is None or visual_score is None:
            raise

        rejection_reasons: list[str] = []
        commercializable = recognition_score >= COMMERCIAL_RECOGNITION_GATE
        if not commercializable:
            rejection_reasons.append("recognition_score_below_commercialization_gate")

        return {
            "recognition_score": recognition_score,
            "visual_impact": visual_score,
            "demand_score": demand_score,
            "commercializable": commercializable,
            "rejection_reasons": tuple(rejection_reasons),
            "score_source": "precomputed",
        }


def _passes_commercial_thresholds(
    *,
    recognition_score: float | None,
    demand_score: float | None,
    visual_score: float | None,
) -> bool:
    return bool(
        (recognition_score is not None and recognition_score >= COMMERCIAL_READY_RECOGNITION_THRESHOLD)
        or (
            demand_score is not None
            and demand_score >= COMMERCIAL_READY_DEMAND_THRESHOLD
            and visual_score is not None
            and visual_score >= COMMERCIAL_READY_VISUAL_THRESHOLD
        )
    )


def _read_optional_score(asset: Mapping[str, Any], aliases: tuple[str, ...]) -> float | None:
    for alias in aliases:
        if alias in asset:
            try:
                score = float(asset[alias])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{alias} must be a numeric score") from exc
            if score < 0 or score > 100:
                raise ValueError(f"{alias} must be between 0 and 100")
            return score
    return None


def _dedupe_reasons(rejection_reasons: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(rejection_reasons))


if __name__ == "__main__":
    raise SystemExit(main())
