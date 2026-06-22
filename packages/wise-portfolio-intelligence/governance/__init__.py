"""Portfolio governance metrics for WISE Portfolio Intelligence."""

__all__ = [
    "PORTFOLIO_GOVERNANCE_REPORT_FILENAME",
    "PortfolioGovernanceReport",
    "blocked_asset_percentage",
    "concentration_risk_score",
    "coverage_score",
    "diversity_score",
    "generate_portfolio_governance_report",
    "load_portfolio_assets",
    "portfolio_health_score",
    "publishable_asset_percentage",
    "representation_score",
    "review_required_percentage",
    "write_portfolio_governance_report",
]


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"module 'governance' has no attribute {name!r}")

    from governance import metrics

    return getattr(metrics, name)
