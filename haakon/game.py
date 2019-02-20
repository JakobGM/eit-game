import pygame
from network import Network

class Player():
    def __init__(self):
        self.player_health_max = 6000  # Unused so far, got an idea of making an healthbar using this
        self.player_health = player_health_max
        self.player_velocity = 3  # Speed of player
        self.player_size = 30  # Radius of player
        self.player_color = (255, 128, 0, 128)  # Random player color (orange)
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)


class Game()
    def __init__(self):
        self.screen_width = 1000  # px
        self.screen_height = 850  # px
        self.center_x = int(self.screen_width / 2)  # Center of screen, x-dir.
        self.center_y = int(self.screen_height / 2)  # Center of screen, y-dir.
