import numpy as np

from harald.agent import Player


def test_invocation_of_player():
    player = Player()
    force = player.force
    assert isinstance(force, np.ndarray)
    assert force.shape == (2,)
    assert np.all(force == 0)

    position = player.position
    assert np.all(position == 0)

    velocity = player.velocity
    assert np.all(velocity == 0)
