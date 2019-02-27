import settings
import pygame
from settings import Colors


class Screen:
    def __init__(self):
        self.width = settings.ScreenSettings.width
        self.height = settings.ScreenSettings.height
        self.screen = pygame.display.set_mode((self.width, self.height))


class Circle:
    def __init__(self, x=50, y=50, color=Colors.RED, radius=10):
        self.position = (int(x), int(y))
        self.radius = radius
        self.color = color

    def draw(self, screen):  # Screen is a pygame.surface object
        return pygame.draw.circle(screen, self.color, self.position, self.radius)
