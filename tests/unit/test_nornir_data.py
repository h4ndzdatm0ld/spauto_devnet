"""Nornir data tests."""
import os

from tests.conftest import CONFIGS_DIR


def test_directory_configs():
    """Assert our testing config directory exists."""
    assert os.path.exists(CONFIGS_DIR)
