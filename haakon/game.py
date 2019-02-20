import pygame
#from haakon.network import Network
from haakon.arena import *
from haakon.player import *
from haakon.graphics import *

class Game:
    def __init__(self):
        #self.net = Network()
        #self.player = Player(600, 600)
        self.player = Player(200, 200, 1000, 1000)
        self.arena = Arena(1000,1000)
        self.x = self.arena.width/2
        self.y = self.arena.height/2

    def run(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()

        screen = Screen()

        #self.arena.display(screen.screen)
        self.arena.shape.draw(screen.screen)
        self.player.shape.draw(screen.screen)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(60)

            keys = pygame.key.get_pressed()
            self.player.move(keys)

            screen.screen.fill((0, 0, 0))
            self.arena.shape.draw(screen.screen)
            if self.player.shield(keys) == True:
                self.player.shape = self.player.display_shield()
                self.player.shape.draw(screen.screen)

            self.player.shape = self.player.display()
            self.player.shape.draw(screen.screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
