import pygame


def draw_player(screen, size, pos, player_color, shield_color, shielded):
    shield_radius = 5

    if shielded:
        pygame.draw.circle(screen, shield_color, pos, size + shield_radius)  # Shield
    pygame.draw.circle(screen, (0, 0, 0), pos, size + 2)  # Border
    pygame.draw.circle(screen, player_color, pos, size)  # Actual player
