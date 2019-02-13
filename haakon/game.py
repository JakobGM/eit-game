import pygame
#from haakon.network import Network
from haakon.canvas import *
from haakon.arena import *
from haakon.player import *
from haakon.graphics import *

class Game:
    def __init__(self):
        #self.net = Network()
        self.player = Player(50, 50)
        self.arena = Arena(1000,850)

    def run(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()

        screen = Screen()
        player = Circle()
        player.draw(screen.screen)

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

            pygame.display.flip()

        pygame.quit()
