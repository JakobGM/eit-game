from pathlib import Path

from modules.statistics import Statistics

def test_creation_of_save_file():
    """Statistics object should automatically create save file."""
    stats = Statistics()
    save_path = stats.save_path
    assert save_path.exists()
