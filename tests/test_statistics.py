from pathlib import Path

import pytest

from modules.statistics import Statistics


@pytest.fixture
def save_path(tmpdir):
    """Return a temporary save file path."""
    return Path(tmpdir) / 'savefile'


@pytest.fixture
def stats(save_path):
    """Return a statistics object which will be recycled after the test."""
    return Statistics(save_path=save_path)


def test_creation_of_save_file(save_path):
    """Statistics object should automatically create save file."""
    stats = Statistics(save_path=save_path)
    save_path = stats.save_path
    assert save_path.exists()


def test_saving_the_winner_of_a_game(save_path):
    """Test the saving and retrieval of game rankings."""
    # First, create a completely new statistics object
    stats = Statistics(save_path=save_path)

    # Save the results of two consecutive games
    stats.save(ranking=['gold1', 'bronze1', 'silver1', 'loser1'])
    stats.save(ranking=['gold2', 'bronze2', 'silver2', 'loser2'])

    # Check if the results are immediatly retrievable
    expected_rankings = [
        ['gold1', 'bronze1', 'silver1', 'loser1'],
        ['gold2', 'bronze2', 'silver2', 'loser2']
    ]
    assert stats.data.all_rankings == expected_rankings

    # And then check if the same data can be retrieved after a "restart"
    del stats
    new_stats = Statistics(save_path=save_path)
    assert new_stats.data.all_rankings == expected_rankings


def test_retrieval_of_all_players(stats):
    """We should be able to retrieve all the players that have played."""
    stats.save(ranking=['Jon', 'Robert', 'Eddard'])
    stats.save(ranking=['Robert', 'Cercei'])
    assert stats.all_players == {'Jon', 'Robert', 'Eddard', 'Cercei'}
