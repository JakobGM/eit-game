"""Player class."""
from modules.graphics import Colors, HealthBar, Circle
import numpy as np
from input.input import Input
from players_settings import PlayerSettings
import math
import pygame as pg
from settings import ArenaSettings
from input.UDP_connect import ConnectPhone


class Player:
    """This class a player class."""

    def __init__(
        self, x: float, y: float, data: type, phone: ConnectPhone = None
    ) -> None:
        """
        Initialize a player with given parameters.

        :param x: initial x-position
        :param y: initial y-position
        :param data: Dataclass used to store player settings
        """
        self.mass: float = data.mass
        self.position: np.ndarray = np.array([x, y], dtype=float)
        self.velocity: np.ndarray = np.zeros(2, dtype=float)
        self.acceleration: np.ndarray = np.zeros(2, dtype=float)

        self.input: Input = Input(data, phone)
        self.name = ''

        self.color: Colors = Colors.random()
        self.data: type = data
        self.shield_on: bool = False
        self.health_bar: HealthBar = HealthBar(self, PlayerSettings.health)

    def get_velocity(self) -> float:
        """Return the velocity of the player."""
        return math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

    def get_acceleration(self) -> float:
        """Return the velocity of the player."""
        return math.sqrt(self.acceleration[0] ** 2 + self.acceleration[1] ** 2)

    def shield(self) -> bool:
        """Turn on the shield."""
        if self.input.shield_on():
            self.velocity = np.zeros(2)
            if self.health_bar.health < self.health_bar.start_health:
                # Player regens health while shielded.
                self.health_bar.health += 1
            return True
        return False

    def update_health(self) -> None:
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

    def get_position(self) -> np.ndarray:
        """Return the position of the player."""
        return self.position

    def draw(self, screen: pg.Surface) -> None:
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

    def draw_shield(self, screen: pg.Surface) -> None:
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
