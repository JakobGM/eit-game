import modules.arena as arena
import modules.player as player
import modules.graphics as graphics
from modules.physics import Physics
import numpy as np
import pygame as pg
from settings import ArenaSettings, Colors
import players_settings as ps
from typing import List
import time
from input.UDP_connect import ConnectPhone


class Game:
    def __init__(self):
        """Initialize the game with different parameters."""
        pg.init()
        pg.font.init()
        self.screen = graphics.Screen()
        self.players = [
            player.Player(200, 200, ps.Player1Settings,
                          ConnectPhone()),
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
        self.screen_object = []
        self.graphs = [graphics.Graph(self.players, "v")]
        self.slides = [graphics.Slider("Friction", 1, 10, 0, 1300)]

    def run(self):
        """Run game."""
        clock = pg.time.Clock()

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    for s in self.slides:
                        if s.button_rect.collidepoint(pos):
                            s.hit = True
                elif event.type == pg.MOUSEBUTTONUP:
                    for s in self.slides:
                        s.hit = False

            self.screen.screen.fill(Colors.BLACK.value)
            self.arena.shape.draw(self.screen.screen)

            # Move players
            self.physics.move_players()

            # Draw players
            for p in self.players:
                p.update_health(self.arena.width / 2)
                p.draw(self.screen.screen)
            # Draw graphs
            for graph in self.graphs:
                graph.draw(self.screen.screen)

            # Draw sliders
            for s in self.slides:
                if s.hit:
                    pass
                    s.move()
            for s in self.slides:
                s.draw(self.screen.screen)

            pg.display.flip()
            clock.tick(60)
            # Check for game over
            for p in self.players:
                if p.health_bar.health == 0:
                    run = False
                    self.show_game_over()
        pg.quit()

    def show_game_over(self):
        # TODO
        time.sleep(1)

    def get_players(self) -> List[player.Player]:
        """Return all player in game."""
        return self.players

    def get_arena(self) -> arena.Arena:
        """Return game arena."""
        return self.arena
