import pygame


def draw(surface, health, screen_width):
    green = (0, 255, 0)
    red = (255, 0, 0)
    max_health = 6000
    pygame.draw.rect(surface, red, (screen_width - 201, 10, 182, 22))
    pygame.draw.rect(
        surface, green, (screen_width - 200, 11, int(health * 180 / max_health), 20)
    )
