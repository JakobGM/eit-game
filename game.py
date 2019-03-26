"""Game class."""
import modules.arena as arena
import modules.player as player
import modules.graphics as graphics
from modules.physics import Physics
import numpy as np
import pygame as pg
from settings import ArenaSettings, Colors, ScreenSettings, Button, Texts,\
Slider
import players_settings as ps
from typing import List
import time
from input.UDP_connect import ConnectPhone


class Game:
    """This class represents the game."""

    def __init__(self) -> None:
        """Initialize the game with all the components."""
        pg.init()
        pg.font.init()
        self.screen: graphics.Screen = graphics.Screen()

        # Players
        self.players: List[player.Player] = [
            player.Player(200, 200, ps.Player1Settings, ConnectPhone()),
            player.Player(300, 300, ps.Player2Settings),
        ]

        # Plots
        self.graphs: List[graphics.Graph] = [graphics.Graph(self.players, "v")]

        # Sliders
        self.slides: List[graphics.Slider] = [
            graphics.Slider(Slider("Drag coefficient", 50, 0, 100, 1350, 400)),
            graphics.Slider(Slider("Friction", 10000, 0, 30000, 1150, 400)),
        ]

        # Buttons
        self.buttons: List[graphics.Button] = [
            graphics.Button(
                Button('Start!', 600, 600, 100, 50, Colors.GREEN.value,
                       Colors.BLUE.value)),
            graphics.Button(
                Button('Help', 800, 600, 100, 50, Colors.RED.value,
                       Colors.BLUE.value)),
        ]

        # Layers
        self.layers: List[arena.ArenaLayer] = [
            arena.FrictionLayer(
                np.ones((ArenaSettings.x, ArenaSettings.y)),
                self.slides[1].get_value),
            arena.AirResistanceLayer(self.slides[0].get_value),
        ]

        # Arena
        self.arena: arena.Arena = arena.Arena(
            ArenaSettings.x, ArenaSettings.y, layers=self.layers)

        # Physic engine
        self.physics: Physics = Physics(self)

    def run(self) -> None:
        """Run the whole game loop."""
        clock: pg.time.Clock = pg.time.Clock()

        while 1:
            if not self.run_intro():
                break

        while 1:
            if not self.run_game(clock):
                break
        pg.quit()

    def run_intro(self) -> bool:
        """Run the game introduction."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # Fill the screen with white
        self.screen.screen.fill(Colors.WHITE.value)

        # Draw text onto the screen
        graphics.Text(
            Texts('EiT gruppe rød', ScreenSettings.width / 2,
                  ScreenSettings.height / 2, 115)).draw(self.screen.screen)

        # Draw the buttions
        list(map(lambda x: x.draw(self.screen.screen), self.buttons))

        pg.display.update()

        return not self.buttons[0].clicked

    def run_game(self, clock: pg.time.Clock) -> bool:
        """Run the game."""
        run: bool = True
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
        self.arena.draw(self.screen.screen)

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

        return run

    def show_game_over(self) -> None:
        """Run when one player dies."""
        # TODO
        time.sleep(1)

    def get_players(self) -> List[player.Player]:
        """Return all player in game."""
        return self.players

    def get_arena(self) -> arena.Arena:
        """Return game arena."""
        return self.arena
