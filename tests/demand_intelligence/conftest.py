"""Demand Intelligence test path configuration."""

import sys
from pathlib import Path

_PACKAGE_SRC = Path(__file__).resolve().parents[2] / "packages" / "wise-demand-intelligence" / "src"
if str(_PACKAGE_SRC) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_SRC))
