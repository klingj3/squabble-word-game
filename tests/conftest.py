"""Point DATA_ROOT at packaged data before imports."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("DATA_ROOT", str(ROOT / "game" / "data"))


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--run-integration", action="store_true", default=False)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--run-integration"):
        skip = pytest.mark.skip(reason="pass --run-integration to run network tests")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip)
