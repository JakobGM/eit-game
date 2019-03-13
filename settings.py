from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
import random


@dataclass
class ScreenSettings:
    """Settings for the screen."""

    height: int = 1000
    width: int = 1500
    font_size: int = 30
    font: str = "Comic Sans MS"


@dataclass
class ArenaSettings:
    """Settings for the arena."""

    x: int = 1000
    y: int = 1000


Color = namedtuple("Color", ["red", "green", "blue"])


class Colors(Enum):
    """Class storing colors."""

    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    YELLOW = Color(255, 255, 0)
    GREY = Color(200, 200, 200)
    ORANGE = Color(200, 100, 50)
    CYAN = Color(0, 255, 255)
    MAGENTA = Color(255, 0, 255)
    TRANS = Color(1, 1, 1)

    @staticmethod
    def random():
        """Return a random color."""
        return Color(
            random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)
        )


@dataclass
class PhysicsConsts:
    """Constants for the physic engine."""

    friction_const = 1
    drag_coefficient = 1
    input_modulation = 1500
    force_modulation = 50
    static_friction_limit = 5
