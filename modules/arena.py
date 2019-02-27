from modules.graphics import *

import abc
from typing import List

import numpy as np
from numpy.linalg import norm
from modules.player import Player


class ArenaLayer(abc.ABC):
    """
    Abstract class representing the physical fields associated with the board
    """

    @abc.abstractmethod
    def force(self, player: Player) -> np.array:
        """Return force for specific player."""


class FrictionLayer(ArenaLayer):
    """
    Representing the physical friction field
    """

    def __init__(self, friction_matrix: np.ndarray) -> None:
        """
        :param friction_matrix: numpy array containing the friction coefficient at each pixel of the board
        """
        self.friction = friction_matrix

    def force(self, player: Player) -> np.array:
        """
        Calculate the friction force for a player.
        The force is constant as long as the player moves, and zero if the player does not move
        :return: the force of friction
        """
        velocity = player.velocity

        # If the velocity is 0 (or close), the force is [0, 0]
        if norm(velocity) < 10:
            return np.array([0.0, 0.0])

        position = player.position
        x, y = position.tolist()
        x, y = int(x), int(y)
        if 0 < x < self.friction.shape[1] and 0 < y < self.friction.shape[0]:
            mu = self.friction[int(x), int(y)]
            force = -mu * velocity / norm(velocity) * player.mass * 10
        else:
            force = np.array([0, 0])
        return force


class Arena:
    """
    The Arena class is used to represent the board of the game.
    It includes elements which is needed for graphics, and
    element needed for the physics engine.
    """

    def __init__(self, width, height, layers: List[ArenaLayer]) -> None:
        """
        :param width: number of pixels in the x direction of the board
        :param height: number of pixels in the y direction of the board
        :param layers: the different physical fields assosiated with the board
        """
        self.width = width
        self.height = height
        self.position = (int(width / 2), int(height / 2))
        self.radius = 500
        self.color = (90, 180, 90)
        self.shape = self.display()
        self.layers = layers

    def display(self):
        arena = Circle(self.position[0], self.position[1], self.color, self.radius)
        return arena

    def force(self, player):
        total_force = np.zeros(2, dtype=float)
        for layer in self.layers:
            total_force += layer.force(player=player)
        return total_force
