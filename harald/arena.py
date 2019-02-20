import abc
import logging
from typing import List

import numpy as np
from numpy.linalg import norm

from harald.agent import Player

logger = logging.getLogger(__name__)


class ArenaLayer(abc.ABC):
    @abc.abstractmethod
    def force(self, player: Player) -> np.array:
        """Return force for specific player."""


class FrictionLayer(ArenaLayer):
    def __init__(self, friction_matrix: np.ndarray) -> None:
        self.friction = friction_matrix

    def force(self, player: Player) -> np.array:
        velocity = player.velocity

        # If the velocity is 0 (or close), the force is [0, 0]
        if norm(velocity) < 0.1:
            return np.array([0.0, 0.0])

        position = player.position
        logger.debug(position)

        x, y = position.tolist()
        x, y = int(x), int(y)
        if 0 < x < self.friction.shape[1] and 0 < y < self.friction.shape[0]:
            mu = self.friction[int(x), int(y)]
            force = -mu * velocity / norm(velocity)
        else:
            force = np.array([0, 0])
        return force


class Arena:
    def __init__(self, layers: List[ArenaLayer]) -> None:
        self.layers = layers

    def force(self, player):
        total_force = np.zeros(2, dtype=float)
        for layer in self.layers:
            total_force += layer.force(player=player)
        return total_force