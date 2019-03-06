from dataclasses import dataclass
import pygame as pg
from enum import Enum
from collections import namedtuple
import random


@dataclass
class ScreenSettings:
    height: int = 1000
    width: int = 1000
    font_size: int = 30
    font: str = "Comic Sans MS"


@dataclass
class ArenaSettings:
    x: int = 1000
    y: int = 1000


Color = namedtuple("Color", ["red", "green", "blue"])


class Colors(Enum):
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)

    @staticmethod
    def random():
        return Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )


@dataclass
class PhysicsConsts:
    friction_const = 1
    drag_coefficient = 1
    input_modulation = 1500
    force_modulation = 50
    static_friction_limit = 5
