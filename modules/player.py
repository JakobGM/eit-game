from modules.graphics import Circle, Colors
import numpy as np
from input.input import Input
from players_settings import PlayerSettings
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

        self.health = PlayerSettings.shield_color
        self.color = Colors.random()
        self.data = data

    def get_velocity(self):
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    def shield(self):
        if self.input.shield_on():
            self.velocity = np.zeros(2)
            self.health += 25  # Player regens health while shielded.
            return True
        return False

    def display(self):
        circle = Circle(self.position[0], self.position[1], self.color,
                        self.data.player_size)
        return circle

    def display_shield(self):
        shield = Circle(
            self.position[0],
            self.position[1],
            PlayerSettings.shield_color,
            self.data.player_size + self.shield_radius,
        )
        return shield
