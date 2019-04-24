from dataclasses import dataclass
import pygame as pg
from typing import Tuple


@dataclass
class PlayerSettings:
    """Settings common for all players."""

    shield: int = 100
    shield_color: Tuple[int] = (0, 255, 0, 0)
    health: int = 100


@dataclass
class Player1Settings:
    """Settings for player 1."""

    key_up: int = pg.K_w
    key_down: int = pg.K_s
    key_left: int = pg.K_a
    key_right: int = pg.K_d
    max_health: int = 6000
    player_size: int = 30
    shield_radius: int = int(0.1 * player_size)
    key_shield = pg.K_q


@dataclass
class Player2Settings:
    """Settings for player 2."""

    key_up: int = pg.K_UP
    key_down: int = pg.K_DOWN
    key_left: int = pg.K_LEFT
    key_right: int = pg.K_RIGHT
    max_health: int = 6000
    player_size: int = 30
    shield_radius: int = int(0.1 * player_size)
    key_shield: int = pg.K_SPACE
