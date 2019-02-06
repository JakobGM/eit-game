import numpy as np

from harald.physics import Physics
from harald.arena import Arena
from harald.agent import Player


def test_invokation_of_physics_object():
    """Check if we are able to create Physics object."""
    players = [Player(), Player()]
    arena = Arena()
    physics = Physics(arena=arena, players=players)


def test_update_players():
    """Test movement of players based on player force."""
    player = Player()

    # Downwards force
    player.force = np.array([0, -1])

    arena = Arena()
    physics = Physics(arena=arena, players=[player])

    # Originally located at the origin
    np.testing.assert_array_equal(
        player.position,
        np.array([0, 0]),
    )

    # Move one step down
    physics.move_players()
    np.testing.assert_array_equal(
        player.position,
        np.array([0, -1]),
    )

    # Change force towards right
    player.force = np.array([1, 0])
    physics.move_players()
    np.testing.assert_array_equal(
        player.position,
        np.array([1, -1]),
    )
