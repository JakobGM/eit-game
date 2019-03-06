from dataclasses import dataclass
import pygame as pg


@dataclass
class Player1Settings:
    key_up: int = pg.K_w
    key_down: int = pg.K_s
    key_left: int = pg.K_a
    key_right: int = pg.K_d
    max_health: int = 6000
    mass: float = 2.0
    shield_radius: int = 5
    player_size = 60
    key_shield = pg.K_SPACE


@dataclass
class Player2Settings:
    key_up: int = pg.K_UP
    key_down: int = pg.K_DOWN
    key_left: int = pg.K_LEFT
    key_right: int = pg.K_RIGHT
    max_health: int = 6000
    mass: float = 1.0
    shield_radius: int = 5
    player_size = 50
    key_shield = pg.K_SPACE
