from modules.graphics import *
import numpy as np
from input.input import Input


class Player:
    def __init__(self, x: float, y: float, keys, max_health=6000, mass: float = 1.0):
        """
        :param x: initial x-position
        :param y: initial y-position
        :param keys: dictionary used to store which keys that belongs to the player
        :param max_health:
        :param mass: mass used to calculate force from the input and friction
        """
        self.mass = mass
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2, dtype=float)
        self.input = Input(keys)
        self.max_health = max_health
        self.health = self.max_health
        self.player_size = 10  # Radius of player
        self.color = Colors.random()
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)
        self.shape = self.display()
        self.shield_radius = 5

    def shield(self, keys):
        if keys[pygame.K_SPACE]:
            draw_shield = True  # Flags shield to be drawn
            self.velocity = np.zeros(
                2, dtype=float
            )  # Player cannot move while shielded
            self.health += 25  # Player regens health while shielded.
            return True
        else:
            # self.velocity = 10
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
