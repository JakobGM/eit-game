"""Game class."""
import modules.arena as arena
import modules.player as player
import modules.graphics as graphics
from modules.physics import Physics
import numpy as np
import pygame as pg
from settings import ArenaSettings, Colors, ScreenSettings, Button, Texts, Slider
import players_settings as ps
from typing import List
import time
from input.UDP_connect import ConnectPhone
from modules.statistics import Statistics


class Game:
    """This class represents the whole game."""

    def __init__(self) -> None:
        """Initialize the game with all the components."""
        pg.init()
        pg.font.init()
        self.screen: graphics.Screen = graphics.Screen()

        # Statistics
        self.statistics = Statistics()

        # Sliders
        self.slides: List[graphics.Slider] = [
            graphics.Slider(Slider("Drag coefficient", 50, 0, 100, 1150, 820)),
            graphics.Slider(Slider("Friction", 10000, 0, 30000, 1150, 880)),
            graphics.Slider(Slider('Player 1 mass', 1, 0.01, 2, 1300, 820)),
            graphics.Slider(Slider('Player 2 mass', 1, 0.01, 2, 1300, 880)),
        ]

        # Players
        self.players: List[player.Player] = [
            player.Player(200, 200, ps.Player1Settings,
                          mass=self.slides[2], phone=ConnectPhone()),
            player.Player(300, 300, ps.Player2Settings, mass=self.slides[3]),
        ]

        # Plots
        self.graphs: List[graphics.Graph] = [graphics.Graph(
            self.players, "v"), graphics.Graph(self.players, "a", position=(1100, 400))]

        # Buttons
        self.buttons: List[graphics.Button] = [
            graphics.Button(
                Button(
                    "Start!", 700, 600, 100, 50, Colors.GREEN.value, Colors.BLUE.value
                )
            )
        ]

        # End screen buttons
        self.end_btn: List[graphics.Button] = [
            graphics.Button(
                Button(
                    "Retry", 600, 600, 100, 50, Colors.GREEN.value, Colors.BLUE.value
                )
            ),
            graphics.Button(
                Button("Quit", 800, 600, 100, 50,
                       Colors.RED.value, Colors.BLUE.value)
            ),
        ]

        # Layers
        self.layers: List[arena.ArenaLayer] = [
            arena.FrictionLayer(
                np.ones((ArenaSettings.x, ArenaSettings.y)
                        ), self.slides[1].get_value
            ),
            arena.AirResistanceLayer(self.slides[0].get_value),
        ]

        # Arena
        self.arena: arena.Arena = arena.Arena(
            ArenaSettings.x, ArenaSettings.y, layers=self.layers
        )

        # Physic engine
        self.physics: Physics = Physics(self)

        # Input boxes
        self.input_boxes = [graphics.InputBox(
            500, 400, 200, 32, text='player 1 name'), graphics.InputBox(
            800, 400, 200, 32, text='player 2 name')]

        # Score
        self.score_table = [graphics.Text(
            Texts(
                "Score table", ScreenSettings.width / 2, 200, 115
            )
        ),
            graphics.Text(
            Texts('', ScreenSettings.width /
                  2, 260, 80)
        ),
            graphics.Text(
            Texts('', ScreenSettings.width /
                  2, 320, 80)
        ),

        ]

    def run(self) -> None:
        """Run the whole game loop."""
        clock: pg.time.Clock = pg.time.Clock()

        while 1:
            if self.run_intro():
                break

        # Set player name
        self.players[0].name = self.input_boxes[0].text
        self.players[1].name = self.input_boxes[1].text

        self.cont_game: bool = True
        while self.cont_game:
            if not self.run_game(clock):
                # Give the winner points
                if self.players[0].health_bar.health > self.players[1].health_bar.health:
                    self.players[0].score += 1
                else:
                    self.players[1].score += 1

                # Add highscore
                self.score_table[1].msg = f"{self.players[0].name}: {self.players[0].score}"
                self.score_table[2].msg = f"{self.players[1].name}: {self.players[1].score}"
                while 1:
                    if self.run_end():
                        self.end_btn[0].clicked = False
                        break
                self.reset_game()
        stats = [player.name for player in sorted(self.players,
                                                  key=lambda x: x.score, reverse=True)]
        self.statistics.save(stats)

        pg.quit()

    def run_intro(self) -> bool:
        """Run the game introduction."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            for box in self.input_boxes:
                box.handle_event(event)

        for box in self.input_boxes:
            box.update()

        # Fill the screen with white
        self.screen.screen.fill(Colors.WHITE.value)

        # Draw text onto the screen
        graphics.Text(
            Texts(
                "EiT gruppe rød",
                ScreenSettings.width / 2,
                300,
                115,
            )
        ).draw(self.screen.screen)

        # Draw the buttions
        list(map(lambda x: x.draw(self.screen.screen), self.buttons))

        # Input boxes
        for box in self.input_boxes:
            box.draw(self.screen.screen)

        pg.display.update()

        return self.buttons[0].clicked

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

        if True in [p.health_bar.health <= 0 for p in self.players]:
            return False

        return run

    def run_end(self) -> bool:
        """Run when one player dies."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # Fill the screen with white
        self.screen.screen.fill(Colors.WHITE.value)

        # Draw text onto the screen
        list(map(lambda x: x.draw(self.screen.screen), self.score_table))

        # Draw the buttions
        list(map(lambda x: x.draw(self.screen.screen), self.end_btn))

        if self.end_btn[1].clicked:
            self.cont_game = False

        pg.display.update()
        return self.end_btn[0].clicked or self.end_btn[1].clicked

    def get_players(self) -> List[player.Player]:
        """Return all player in game."""
        return self.players

    def get_arena(self) -> arena.Arena:
        """Return game arena."""
        return self.arena

    def reset_game(self):
        list(map(lambda x: x.reset_position(), self.players))
        list(map(lambda x: x.health_bar.reset(), self.players))
