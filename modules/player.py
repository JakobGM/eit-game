from modules.graphics import *
import numpy as np
from input.input import Input
import math


class Player:
    def __init__(self, x: float, y: float, data):
        """
        :param x: initial x-position
        :param y: initial y-position
        :param data: Dataclass used to store player settings
        """
        self.mass = data.mass
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2, dtype=float)

        self.input = Input(self, data)

        self.max_health = data.max_health
        self.health = self.max_health
        self.player_size = data.player_size  # Radius of player
        self.color = Colors.random()
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)
        self.shape = self.display()
        self.shield_radius = data.shield_radius
        self.data = data

    def get_velocity(self):
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    def shield(self, keys):
        if keys[self.data.key_shield]:
            self.velocity = np.zeros(2)
            self.health += 25  # Player regens health while shielded.
            return True
        return False

    def display(self):
        circle = Circle(
            self.position[0], self.position[1], self.color, self.player_size
        )
        return circle

    def display_shield(self):
        shield = Circle(
            self.position[0],
            self.position[1],
            self.shield_color,
            self.player_size + self.shield_radius,
        )
        return shield
