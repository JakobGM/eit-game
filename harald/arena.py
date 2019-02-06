import abc

import numpy as np
from numpy.linalg import norm

from harald.agent import Player


class Arena:
    def __init__(layers: List[ArenaLayer]) -> None:
        self.layers = layers

    def force(player):
        total_force = np.zeros(2, dtype=float)
        for layer in layers:
            total_force += layer.force(player=player)
        return total_force


class ArenaLayer(abc.ABC):
    @abc.abstractmethod
    def force(self, player: Player) -> np.array:
        """Return force for specific player."""


class FrictionLayer(ArenaLayer):
    def __init__(self, friction_matrix: np.ndarray) -> None:
        self.friction = friction_matrix

    def force(self, player: Player) -> np.array:
        velocity = player.velocity
        if norm(velocity) == 0:
            return np.array([0., 0.])

        position = player.position
        x, y = position.tolist()
        mu = self.friction[int(x), int(y)]
        force = -mu * velocity / norm(velocity)
        return force
