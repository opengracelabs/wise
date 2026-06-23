"""Rights-aware portfolio gating tests."""

from wise_portfolio_intelligence import (
    PortfolioSelectionConfig,
    RIGHTS_ELIGIBILITY_CANDIDATE_ONLY,
    RIGHTS_ELIGIBILITY_ELIGIBLE,
    RIGHTS_ELIGIBILITY_EXCLUDED,
    RIGHTS_STATUS_APPROVED,
    RIGHTS_STATUS_RESTRICTED,
    RIGHTS_STATUS_REVIEW_REQUIRED,
    RIGHTS_STATUS_UNKNOWN,
    normalize_rights_status,
    read_rights_status,
    rights_eligibility,
    rights_gate,
    select_portfolio_candidates,
)


def test_normalize_rights_status_maps_aliases_to_canonical_labels():
    assert normalize_rights_status("approved") == RIGHTS_STATUS_APPROVED
    assert normalize_rights_status("Open") == RIGHTS_STATUS_APPROVED
    assert normalize_rights_status("review") == RIGHTS_STATUS_REVIEW_REQUIRED
    assert normalize_rights_status("blocked") == RIGHTS_STATUS_RESTRICTED
    assert normalize_rights_status(None) == RIGHTS_STATUS_UNKNOWN


def test_rights_eligibility_matches_canonical_statuses():
    assert rights_eligibility(RIGHTS_STATUS_APPROVED) == RIGHTS_ELIGIBILITY_ELIGIBLE
    assert rights_eligibility(RIGHTS_STATUS_REVIEW_REQUIRED) == RIGHTS_ELIGIBILITY_CANDIDATE_ONLY
    assert rights_eligibility(RIGHTS_STATUS_RESTRICTED) == RIGHTS_ELIGIBILITY_EXCLUDED
    assert rights_eligibility(RIGHTS_STATUS_UNKNOWN) == RIGHTS_ELIGIBILITY_EXCLUDED


def test_rights_gate_excludes_blocked_statuses():
    restricted = rights_gate("Restricted")
    unknown = rights_gate("Unknown")

    assert restricted.excluded is True
    assert restricted.publishable is False
    assert restricted.eligibility == RIGHTS_ELIGIBILITY_EXCLUDED
    assert unknown.excluded is True


def test_rights_gate_allows_review_required_candidates_only():
    decision = rights_gate("Review Required")

    assert decision.excluded is False
    assert decision.publishable is False
    assert decision.eligibility == RIGHTS_ELIGIBILITY_CANDIDATE_ONLY


def test_read_rights_status_supports_rc17_field_alias():
    asset = {"id": "rc17-asset", "rc17_rights_status": "Review Required"}

    assert read_rights_status(asset) == RIGHTS_STATUS_REVIEW_REQUIRED


def test_selected_candidates_include_rights_eligibility_metadata():
    selected = select_portfolio_candidates(
        [
            {
                "id": "approved-asset",
                "recognition_score": 90,
                "commercial_appeal_score": 88,
                "commercial_tier": "Icon Product",
                "final_selection_score": 89,
                "historical_significance_level": "global",
                "portfolio_category": "homepage",
                "rights_status": "Approved",
            },
            {
                "id": "review-asset",
                "recognition_score": 85,
                "commercial_appeal_score": 70,
                "commercial_tier": "Strong Product",
                "final_selection_score": 77,
                "historical_significance_level": "high",
                "portfolio_category": "homepage",
                "rights_status": "Review Required",
            },
        ],
        PortfolioSelectionConfig(max_items=2, portfolio_category="homepage"),
    )

    by_id = {asset["id"]: asset for asset in selected}
    assert by_id["approved-asset"]["rights_status"] == RIGHTS_STATUS_APPROVED
    assert by_id["approved-asset"]["rights_eligibility"] == RIGHTS_ELIGIBILITY_ELIGIBLE
    assert by_id["approved-asset"]["publishable"] is True
    assert by_id["review-asset"]["rights_eligibility"] == RIGHTS_ELIGIBILITY_CANDIDATE_ONLY
    assert by_id["review-asset"]["publishable"] is False
