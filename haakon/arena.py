import pygame
import random


class Arena:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (int(width / 2), int(height / 2))
        self.radius = 500
        self.color = (125, 125, 125)

    def draw_arena(self, screen):
        arena = pygame.draw.circle(self, screen, self.color, self.position, self.radius)
        return arena
