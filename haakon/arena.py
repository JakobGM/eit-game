import pygame
import random

class Arena():
    def __init__(self, width, height, player):
        position = (int(width / 2), int(height / 2))
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        pygame.init()
        pygame.font.init()
        pygame.display.flip()



def draw_arena(surface, color, pos, radius):
    pygame.draw.circle(surface, color, pos, radius)
