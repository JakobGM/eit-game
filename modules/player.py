from modules.graphics import Circle, Colors, HealthBar
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

        self.color = Colors.random()
        self.data = data
        self.shield_on = False
        self.health_bar = HealthBar(self, PlayerSettings.health)

    def get_velocity(self):
        return math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

    def shield(self):
        if self.input.shield_on():
            self.velocity = np.zeros(2)
            if(self.health_bar.health < self.health_bar.start_health):
                self.health_bar.health += 1  # Player regens health while shielded.
            return True
        return False

    def get_health_bar(self):
        return self.health_bar

    def get_position(self):
        return self.position

    def display(self):
        circle = Circle(
            self.position[0], self.position[1], self.color, self.data.player_size
        )
        return circle

    def display_shield(self):
        shield = Circle(
            self.position[0],
            self.position[1],
            PlayerSettings.shield_color,
            self.data.player_size + self.data.shield_radius,
        )
        return shield
