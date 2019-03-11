import modules.arena as arena
import modules.player as player
import modules.graphics as graphics
from modules.physics import Physics
import numpy as np
import pygame as pg
from settings import ArenaSettings
import players_settings as ps
from modules.text import Text
from typing import List


class Game:
    def __init__(self):
        """Initialize the game with different parameters."""
        self.players = [
            player.Player(200, 200, ps.Player1Settings),
            player.Player(300, 300, ps.Player2Settings),
        ]

        self.arena_size = (ArenaSettings.x, ArenaSettings.y)
        self.layers = [
            arena.FrictionLayer(
                np.ones((self.arena_size[0], self.arena_size[1]))),
            arena.AirResistanceLayer(0.00001),
        ]
        self.arena = arena.Arena(
            self.arena_size[0], self.arena_size[1], layers=self.layers
        )

        self.x = self.arena.width / 2
        self.y = self.arena.height / 2
        self.physics = Physics(self, time_step=1 / 60)
        self.screen_object = [
            Text(800, 50, "Velocity: ", self.players[0].get_velocity)]
        self.graphs = [graphics.Graph(self.players, "velocity")]

    def run(self):
        """Run game."""
        pg.init()
        pg.font.init()
        clock = pg.time.Clock()

        screen = graphics.Screen()

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            screen.screen.fill((0, 0, 0))

            self.arena.shape.draw(screen.screen)

            for screen_object in self.screen_object:

                screen.screen.blit(
                    screen_object.get_element(),
                    (screen_object.x, screen_object.y)
                )

            self.physics.move_players()

            for p in self.players:
                if p.shield():
                    p.display_shield().draw(screen.screen)
                p.display().draw(screen.screen)
                health_bar = p.get_health_bar()
                health_bar.draw(screen.screen)
            for graph in self.graphs:
                graph.plot()
                screen.screen.blit(graph.get_plot(), (1100, 0))
            pg.display.flip()
            clock.tick(60)
        pg.quit()

    def get_players(self) -> List[player.Player]:
        """Return all player in game."""
        return self.players

    def get_arena(self) -> arena.Arena:
        """Return game arena."""
        return self.arena
