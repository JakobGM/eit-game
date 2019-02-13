import numpy as np

from harald.arena import Arena, FrictionLayer
from harald.agent import Player


def test_invokation_of_ArenaLayer():
    friction_matrix = np.ones((1000, 1000))
    friction = FrictionLayer(friction_matrix=friction_matrix)


def test_invokation_of_Arena_object():
    friction_matrix = np.ones(2)
    friction = FrictionLayer(friction_matrix=friction_matrix)

    Arena(layers=[friction])


def test_update_foce():
    player = Player()
    player.velocity = np.ones(2)
    player.position = 500 * np.ones(2)
    friction_matrix = np.ones((1000, 1000))
    friction = FrictionLayer(friction_matrix=friction_matrix)

    arena = Arena(layers=[friction])
    assert np.any(arena.force(player) != 0)
