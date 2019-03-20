import numpy as np

from modules.arena import Arena, FrictionLayer
from modules.player import Player


def test_invokation_of_ArenaLayer() -> None:
    """
    Test if it is possible to create a Arena Layer
    """
    friction_matrix = np.ones((1000, 1000))
    friction = FrictionLayer(friction_matrix=friction_matrix)


def test_invokation_of_Arena_object() -> None:
    """
    Test if it is possible to create a Arena with a arena layer
    """
    friction_matrix = np.ones(2)
    friction = FrictionLayer(friction_matrix=friction_matrix)

    Arena(width=1000, height=1000, layers=[friction])


def test_update_force() -> None:
    """
    Test if it is possible to update the position of a player based on the force from the area layer
    """
    player = Player(0, 0, None)
    player.velocity = np.ones(2)
    player.position = 500 * np.ones(2)
    friction_matrix = np.ones((1000, 1000))
    friction = FrictionLayer(friction_matrix=friction_matrix)

    arena = Arena(width=1000, height=1000, layers=[friction])
    assert np.any(arena.force(player) != 0)
