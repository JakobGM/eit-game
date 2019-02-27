import numpy as np

from modules.physics import Physics
from modules.arena import Arena
from modules.player import Player


def test_invokation_of_physics_object():
    """Check if we are able to create Physics object."""
    players = [Player(), Player()]
    arena = Arena(layers=[])
    Physics(arena=arena, players=players, time_step=0.1)


def test_move_player():
    """
    Check if the code is able to change the position of a player
    """
    player = Player()

    # Initialize a player
    player.mass = 100
    player.force = np.array([-10.0, 0.0])
    player.position = np.array([10.0, 10.0])
    player.velocity = np.array([50.0, 50.0])
    assert np.any(np.not_equal(player.force, np.zeros(2)))
    assert np.any(np.not_equal(player.position, np.zeros(2)))
    assert np.any(np.not_equal(player.velocity, np.zeros(2)))

    # Initialize a area
    arena = Arena(layers=[])

    physics = Physics(arena=arena, players=[player], time_step=0.1)
    physics.move_players()
    np.testing.assert_array_equal(player.velocity, np.array([49.99, 50]))
    np.testing.assert_array_equal(player.position, np.array([14.999, 15]))
