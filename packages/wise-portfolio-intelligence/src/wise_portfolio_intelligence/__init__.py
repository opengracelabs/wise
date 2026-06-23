"""Portfolio Intelligence selection for WISE assets."""

from wise_portfolio_intelligence.adapters.commercial_input import (
    PortfolioCandidate,
    adapt_commercial_portfolio_input,
)
from wise_portfolio_intelligence.constants import (
    BALANCED_GLOBAL_PORTFOLIO_DOMAINS,
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
)
from wise_portfolio_intelligence.governance import (
    PORTFOLIO_GOVERNANCE_REPORT_FILENAME,
    PortfolioGovernanceReport,
    blocked_asset_percentage,
    concentration_risk_score,
    coverage_score,
    diversity_score,
    generate_portfolio_governance_report,
    load_portfolio_assets,
    portfolio_health_score,
    publishable_asset_percentage,
    representation_score,
    review_required_percentage,
    write_portfolio_governance_report,
)
from wise_portfolio_intelligence.selection.portfolio_selector import (
    PortfolioSelectionConfig,
    select_candidate_outputs,
    select_portfolio_candidates,
)
from wise_portfolio_intelligence.selection.rights_gate import (
    RightsDecision,
    rights_gate,
)

__version__ = "0.1.0"

__all__ = [
    "BALANCED_GLOBAL_PORTFOLIO_DOMAINS",
    "PORTFOLIO_GOVERNANCE_REPORT_FILENAME",
    "PortfolioCandidate",
    "PortfolioGovernanceReport",
    "PortfolioSelectionConfig",
    "RIGHTS_ELIGIBILITY_CANDIDATE_ONLY",
    "RIGHTS_ELIGIBILITY_ELIGIBLE",
    "RIGHTS_ELIGIBILITY_EXCLUDED",
    "RIGHTS_STATUS_APPROVED",
    "RIGHTS_STATUS_RESTRICTED",
    "RIGHTS_STATUS_REVIEW_REQUIRED",
    "RIGHTS_STATUS_UNKNOWN",
    "RightsDecision",
    "__version__",
    "adapt_commercial_portfolio_input",
    "blocked_asset_percentage",
    "concentration_risk_score",
    "coverage_score",
    "diversity_score",
    "generate_portfolio_governance_report",
    "load_portfolio_assets",
    "normalize_rights_status",
    "portfolio_health_score",
    "publishable_asset_percentage",
    "read_rights_status",
    "representation_score",
    "review_required_percentage",
    "rights_eligibility",
    "rights_gate",
    "select_candidate_outputs",
    "select_portfolio_candidates",
    "write_portfolio_governance_report",
]
