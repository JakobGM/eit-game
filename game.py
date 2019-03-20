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
    """This class represents the game."""

    def __init__(self):
        """Initialize the game with all the components."""
        pg.init()
        pg.font.init()
        self.screen = graphics.Screen()

        # Players
        self.players: List[player.Player] = [
            player.Player(200, 200, ps.Player1Settings, ConnectPhone()),
            player.Player(300, 300, ps.Player2Settings),
        ]

        # Plots
        self.graphs = [graphics.Graph(self.players, "v")]

        # Sliders
        self.slides = [
            graphics.Slider("Drag coefficient", 0.001, 100, 0, 1350),
            graphics.Slider("Friction", 1, 50000, 0, 1150),
        ]

        # Layers
        self.layers: list[arena.ArenaLayer] = [
            arena.FrictionLayer(
                np.ones((ArenaSettings.x, ArenaSettings.y)), self.slides[1].get_value
            ),
            arena.AirResistanceLayer(self.slides[0].get_value),
        ]

        # Arena
        self.arena: arena.Arena = arena.Arena(
            ArenaSettings.x, ArenaSettings.y, layers=self.layers
        )

        # Physic engine
        self.physics = Physics(self)

    def run(self):
        """Run game."""
        clock = pg.time.Clock()

        run = True
        while run:
            # Check for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                # Code for slides
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    for s in self.slides:
                        if s.button_rect.collidepoint(pos):
                            s.hit = True
                elif event.type == pg.MOUSEBUTTONUP:
                    for s in self.slides:
                        s.hit = False

            # Fill the screen with black to remove old drawings
            self.screen.screen.fill(Colors.BLACK.value)

            # Draw arena
            self.arena.shape.draw(self.screen.screen)

            # Update sliders (Is this an Ok placement?)
            # self.arena.layers[0].friction_const = self.slides[1].get_value()
            # self.arena.layers[1].drag_coefficient = self.slides[0].get_value()

            # Move players
            self.physics.move_players()

            # Draw players
            for p in self.players:
                p.update_health()
                p.draw(self.screen.screen)

            # Draw plots
            for graph in self.graphs:
                graph.draw(self.screen.screen)

            # Move sliders
            for s in self.slides:
                if s.hit:
                    pass
                    s.move()

            # Draw sliders
            for s in self.slides:
                s.draw(self.screen.screen)

            pg.display.flip()
            clock.tick(60)
        pg.quit()

    def show_game_over(self):
        """Run when one player dies."""
        # TODO
        time.sleep(1)

    def get_players(self) -> List[player.Player]:
        """Return all player in game."""
        return self.players

    def get_arena(self) -> arena.Arena:
        """Return game arena."""
        return self.arena
