import abc
from collections import namedtuple
from enum import Enum
import random

import pygame

X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

Color = namedtuple("Color", ["red", "green", "blue"])


class Colors(Enum):
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)

    @staticmethod
    def random():
        # return cls(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        return Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )


class Screen:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width, self.height))


class Circle:
    def __init__(self, x=50, y=50, color=Colors.RED, radius=10):
        self.position = (x, y)
        self.radius = radius
        self.color = color

    def draw(self, screen):  # Screen is a pygame.surface object
        return pygame.draw.circle(screen, self.color, self.position, self.radius)
