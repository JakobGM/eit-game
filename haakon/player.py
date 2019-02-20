from haakon.graphics import *
import numpy as np

class Player:
    def __init__(self, X, Y, arena_x, arena_y):
        self.arena_x = arena_x
        self.arena_y = arena_y
        self.x = X
        self.y = Y
        self.max_health = 6000
        self.health = self.max_health
        self.max_velocity = 5
        self.velocity = 5  # Speed of player
        self.player_size = 10  # Radius of player
        self.color = Colors.random()
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)
        self.shape = self.display()
        self.shield_radius = 5
        self.position = np.array([X,Y])

    def move(self, keys):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """
        if keys[pygame.K_w]:  # Top is zero, means up is negative and down is positive
            if (self.y - self.velocity < 0):
                self.y -= (self.velocity - self.arena_y)
            else:
                self.y -= self.velocity
        if keys[pygame.K_s]:
            if (self.y + self.velocity > self.arena_y):
                self.y += self.velocity - self.arena_y
            else:
                self.y += self.velocity
        if keys[pygame.K_a]:  # Left is zero, hence left is negative, right is positive
            if (self.x - self.velocity < 0):
                self.x -= (self.velocity - self.arena_x)
            else:
                self.x -= self.velocity
        if keys[pygame.K_d]:
            if (self.x + self.velocity > self.arena_x):
                self.x += self.velocity - self.arena_x
            else:
                self.x += self.velocity

    def shield(self, keys):
        if keys[pygame.K_SPACE]:
            draw_shield = True  # Flags shield to be drawn
            self.velocity = 0  # Player cannot move while shielded
            self.health += 25  # Player regens health while shielded.
            return True
        else:
            self.velocity = self.max_velocity
            return False

    def display(self):
        circle = Circle(self.x,self.y, self.color, self.player_size)
        return circle

    def display_shield(self):
        shield = Circle(self.x,self.y, self.shield_color, self.player_size + self.shield_radius)
        return shield
