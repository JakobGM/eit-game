import pygame
import random

class Arena():
    def __init__(self, width, height, player):
        self.width = 1000
        self.height = 850
        self.position = (int(width / 2), int(height / 2))
        self.radius = 500
        self.color = (125,125,125)


def draw_arena(surface, color, pos, radius):
    pygame.draw.circle(surface, color, pos, radius)
