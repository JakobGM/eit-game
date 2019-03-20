from modules.graphics import Circle, Colors, HealthBar
import numpy as np
from input.input import Input
from players_settings import PlayerSettings
import math
from settings import ArenaSettings


class Player:
    """This class a player class."""

    def __init__(self, x: float, y: float, data, phone=None):
        """
        Initialize a player with given parameters.

        :param x: initial x-position
        :param y: initial y-position
        :param data: Dataclass used to store player settings
        """
        self.mass = data.mass
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2, dtype=float)

        self.input = Input(data, phone)

        self.color = Colors.random()
        self.data = data
        self.shield_on = False
        self.health_bar = HealthBar(self, PlayerSettings.health)

    def get_velocity(self):
        """Return the velocity of the player."""
        return math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

    def shield(self):
        """Turn on the shield."""
        if self.input.shield_on():
            self.velocity = np.zeros(2)
            if self.health_bar.health < self.health_bar.start_health:
                # Player regens health while shielded.
                self.health_bar.health += 1
            return True
        return False

    def update_health(self):
        """Update the health of the player."""
        arena_radius = ArenaSettings.x / 2
        if (
            math.sqrt(
                (self.position[0] - arena_radius) ** 2
                + (self.position[1] - arena_radius) ** 2
            )
            + self.data.player_size
            > arena_radius
        ):
            self.health_bar.update_health(self.health_bar.health - 1)

    def get_position(self):
        """Return the position of the player."""
        return self.position

    def draw(self, screen):
        """
        Draw the player onto the screenself.

        :param screen: The screen of the game.
        """
        self.health_bar.draw(screen)
        if self.shield():
            self.draw_shield(screen)
        Circle(
            self.position[0], self.position[1], self.color, self.data.player_size
        ).draw(screen)

    def draw_shield(self, screen):
        """
        Draw the shield onto the screenself.

        :param screen: The screen of the game.
        """
        Circle(
            self.position[0],
            self.position[1],
            PlayerSettings.shield_color,
            self.data.player_size + self.data.shield_radius,
        ).draw(screen)
