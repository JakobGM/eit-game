import pygame

# from haakon.network import Network
from haakon.arena import *
from haakon.player import *
from haakon.graphics import *
from harald.physics import Physics
import kribrung.network.UDP_connect as con


class Game:
    def __init__(self):
        # self.net = Network()
        # self.player = Player(600, 600)
        self.player = Player(
            200,
            200,
            {
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
            },
        )
        self.arena_size = (1000, 1000)
        self.layers = [FrictionLayer(np.ones((self.arena_size[0], self.arena_size[1])))]
        self.arena = Arena(self.arena_size[0], self.arena_size[1], layers=self.layers)
        self.x = self.arena.width / 2
        self.y = self.arena.height / 2
        self.physics = Physics(
            arena=self.arena, players=[self.player], time_step=1 / 60
        )

    def run(self):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()

        screen = Screen()

        # self.arena.draw_arena(screen)

        self.player.shape.draw(screen.screen)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            # Physics
            self.physics.move_players()

            # self.player.move(keys)

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
