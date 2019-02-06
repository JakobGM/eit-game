class Player:
    width = 50
    height = 50

    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.health = 6000
        self.velocity = 3  # Speed of player
        self.player_size = 30  # Radius of player
        self.color = (255, 128, 0, 128)  # Random player color (orange)
        # self.shield_color = (0, 255, 0, 0)  # Random shield color (green)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity
