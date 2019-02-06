import pygame
#from haakon.network import Network
from haakon.canvas import *
from haakon.arena import *


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

    def draw(self, g):
        pygame.draw.rect(g, self.color, (self.x, self.y, self.width, self.height), 0)

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


class Game:
    def __init__(self):
        #self.net = Network()
        self.width = 1000  # px
        self.height = 850  # px
        self.player = Player(50, 50)
        #self.arena = Arena()
        #self.player2 = Player(100, 100)
        #self.canvas = Canvas(self.width, self.height, "Testing...")
        # self.center_x = int(self.width / 2)  # Center of screen, x-dir.
        # self.center_y = int(self.height / 2)  # Center of screen, y-dir.
        self.arena_color = (125,125,125)
        self.arena_pos = (100,100)
        self.arena_radius = 100

    def run(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))

        center_x = int(self.width / 2)  # Center of screen, x-dir.
        center_y = int(self.height / 2)  # Center of screen, y-dir.

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(60)

            keys = pygame.key.get_pressed()

            # Checks if the player is shielded
            if keys[pygame.K_SPACE]:
                draw_shield = True  # Flags shield to be drawn
                self.player.velocity = 0  # Player cannot move while shielded
                self.player.health += 25  # Player regens health while shielded.

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            # Clear screen
            screen.fill((0, 0, 0))

            # Drawing arena
            draw_arena(screen, self.arena_color, self.arena_pos, self.arena_radius)

            """
            # Drawing player
            player.draw_player(
                screen, player_size, player_pos, player_color, shield_color, draw_shield
            )

            # Draw position text
            t2s.write(screen, (0, 255, 180), (25, 25), pos_string)

            # Drawing shield text
            t2s.write(screen, (0, 255, 180), (25, 50), shield_string)

            # Drawing healthbar
            healthbar.draw(screen, player_health, screen_width)

            # Draw Coin
            draw_coin.coin(screen, (250, 400))

            # Flips the newly drawn page to the window
            """
            pygame.display.flip()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0
