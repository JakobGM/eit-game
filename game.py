import modules.arena as arena
import modules.player as player
import modules.graphics as graphics
from modules.physics import Physics
import numpy as np
import pygame as pg
from settings import ArenaSettings, Player1Settings
from modules.text import Text


class Game:
    def __init__(self):
        self.player = player.Player(
            200,
            200,
            Player1Settings,
        )
        self.arena_size = (ArenaSettings.x, ArenaSettings.y)
        self.layers = [
            arena.FrictionLayer(np.ones((self.arena_size[0], self.arena_size[1]))),
            arena.AirResistanceLayer(0.00001),
        ]
        self.arena = arena.Arena(self.arena_size[0], self.arena_size[1], layers=self.layers)
        self.x = self.arena.width / 2
        self.y = self.arena.height / 2
        self.physics = Physics(
            arena=self.arena, players=[self.player], time_step=1 / 60
        )
        self.screen_object = [Text(800, 50, 'Velocity: ', self.player.get_velocity)]

    def run(self):
        pg.init()
        pg.font.init()
        clock = pg.time.Clock()

        screen = graphics.Screen()

        self.player.shape.draw(screen.screen)

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            keys = pg.key.get_pressed()


            screen.screen.fill((0, 0, 0))

            self.arena.shape.draw(screen.screen)

            for screen_object in self.screen_object:
                screen.screen.blit(screen_object.get_element(), (screen_object.x, screen_object.y))

            if self.player.shield(keys):
                self.player.shape = self.player.display_shield()
                self.player.shape.draw(screen.screen)
            else:
                # Physics
                self.physics.move_players()

            self.player.shape = self.player.display()
            self.player.shape.draw(screen.screen)
            pg.display.flip()
            clock.tick(60)
        pg.quit()
