"""Root test configuration — shared fixture discovery."""

import sys
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parent
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))

pytest_plugins = ["registry.conftest", "reference.conftest", "discovery.conftest"]
