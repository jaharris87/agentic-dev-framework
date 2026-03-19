"""Shared pytest fixtures.

Add project-wide fixtures here. These are automatically available to all tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to the fixtures/ directory containing static test data."""
    return FIXTURES_DIR


@pytest.fixture
def tmp_data_dir(tmp_path: Path) -> Path:
    """Temporary directory for throwaway test data (caches, DBs, etc.)."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def fixed_rng_seed() -> int:
    """Fixed random seed for deterministic tests."""
    return 42
