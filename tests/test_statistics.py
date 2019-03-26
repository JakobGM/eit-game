from pathlib import Path

import pytest

from modules.statistics import Statistics


@pytest.fixture
def save_path(tmpdir):
    """Return a temporary save file path."""
    return Path(tmpdir) / 'savefile'


def test_creation_of_save_file(save_path):
    """Statistics object should automatically create save file."""
    stats = Statistics(save_path = save_path)
    save_path = stats.save_path
    assert save_path.exists()
