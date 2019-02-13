from haakon.graphics import *

class Player:
    #width = 200
    #height = 200

    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.max_health = 6000
        self.health = self.max_health
        self.velocity = 3  # Speed of player
        self.player_size = 30  # Radius of player
        self.color = (255, 128, 0, 128)  # Random player color (orange)
        self.shield_color = (0, 255, 0, 0)  # Random shield color (green)
        self.shape = Circle(self.x,self.y)

    def move(self, keys):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """
        if keys[pygame.K_w]:  # Top is zero, means up is negative and down is positive
            self.y -= self.velocity
        if keys[pygame.K_s]:
            self.y += self.velocity
        if keys[pygame.K_a]:  # Left is zero, hence left is negative, right is positive
            self.x -= self.velocity
        if keys[pygame.K_d]:
            self.x += self.velocity
