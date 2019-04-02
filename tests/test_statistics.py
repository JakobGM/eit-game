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


def test_retrieval_of_player_true_skill(stats):
    """Test calculation of player TrueSkill."""
    # At first, the best player placed 2nd a couple of times
    stats.save(ranking=['better', 'best', 'good'])
    stats.save(ranking=['better', 'best', 'good'])

    # But then they win three games in a row
    stats.save(ranking=['best', 'better', 'good'])
    stats.save(ranking=['best', 'better', 'good'])
    stats.save(ranking=['best', 'better', 'good'])

    # The best player should now be considered best
    true_skills = stats.true_skill()
    assert list(true_skills.keys()) == ['best', 'better', 'good']
    assert true_skills['best'].mu > true_skills['better'].mu


def test_win_probability(stats):
    """Test the calculation of player win probabilities."""
    # At first two new players will have equal win probabilities
    prediction = stats.win_probability(['player_1', 'player_2'])
    assert prediction['player_1'] == pytest.approx(prediction['player_2'])

    # Their probabilities sum to 1
    assert prediction['player_1'] + prediction['player_2'] == pytest.approx(1)

    # And the probability of drawing is ~44.7%
    assert prediction['draw'] == pytest.approx(0.447, abs=1e-3)

    # Now, player one wins 20 times against player two
    for _ in range(20):
        stats.save(ranking=['player_1', 'player_2'])

    # The probability of player 1 winning is now close to 100%
    new_prediction = stats.win_probability(['player_1', 'player_2'])
    assert new_prediction['player_1'] > 0.99
    assert new_prediction['draw'] < 0.05
