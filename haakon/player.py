from haakon.graphics import *
import numpy as np
from haakon.input import Input


class Player:
    def __init__(self, X, Y, keys, max_health=6000, mass: float = 1.0):
        self.x = X
        self.y = Y
        self.mass = mass
        self.max_health = max_health
        self.health = self.max_health
        self.velocity = 6  # Speed of player
        self.player_size = 10  # Radius of player
        self.color = Colors.random()
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)
        self.shape = self.display()
        self.shield_radius = 5
        self.position = np.array([X, Y])
        self.input = Input(keys)

    def shield(self, keys):
        if keys[pygame.K_SPACE]:
            draw_shield = True  # Flags shield to be drawn
            self.velocity = 0  # Player cannot move while shielded
            self.health += 25  # Player regens health while shielded.
            return True
        else:
            self.velocity = 3
            return False

    def display(self):
        circle = Circle(self.x, self.y, self.color, self.player_size)
        return circle

    def display_shield(self):
        shield = Circle(
            self.x, self.y, self.shield_color, self.player_size + self.shield_radius
        )
        return shield
