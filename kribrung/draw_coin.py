import pygame

def coin(surface, pos):
    color = (180, 200, 17)
    size = 5
    border_color = (0, 0, 0)
    border_size = 1
    pygame.draw.circle(surface, border_color, pos, size + border_size)
    pygame.draw.circle(surface, color, pos, size)
