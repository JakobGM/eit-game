import settings
import pygame
from settings import Colors, Texts
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
import numpy as np
from collections import deque
from typing import Tuple, List, NamedTuple

matplotlib.use("Agg")


class Slider:
    """This class represent slider."""

    def __init__(self, settings):
        """Initialize the slider wiht a Slider namedtuple"""
        self.font = pygame.font.SysFont("Verdana", 12)
        self.val = settings.val  # start value
        self.maxi = settings.max  # maximum at slider position right
        self.mini = settings.min  # minimum at slider position left
        self.xpos = settings.xpos  # x-location on screen
        self.ypos = settings.ypos
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False
        self.txt_surf = self.font.render(settings.name, 1, Colors.BLACK.value)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, Colors.GREY.value, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, Colors.ORANGE.value, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, Colors.WHITE.value, [10, 30, 80, 5], 0)

        # this surface never changes
        self.surf.blit(self.txt_surf, self.txt_rect)

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(Colors.TRANS.value)
        self.button_surf.set_colorkey(Colors.TRANS.value)
        pygame.draw.circle(
            self.button_surf, Colors.BLACK.value, (10, 10), 6, 0)
        pygame.draw.circle(
            self.button_surf, Colors.ORANGE.value, (10, 10), 4, 0)

    def get_value(self):
        """Get the value of the current position of the slider."""
        return self.val

    def draw(self, screen):
        """ Combination of static and dynamic graphics in a copy of
        the basic slide surface
        """
        # static
        surf = self.surf.copy()
        # dynamic
        pos = (10 + int((self.val - self.mini) /
                        (self.maxi - self.mini) * 80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        # move of button box to correct screen position
        self.button_rect.move_ip(self.xpos, self.ypos)
        # screen
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """The dynamic part; reacts to movement of the slider button."""
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (
            self.maxi - self.mini
        ) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


class Graph:
    """This class a matplotlib graph class."""

    def __init__(
        self,
        players,
        graph_type,
        figsize=[4, 4],
        dpi=100,
        max_window=200,
        position=(1100, 0),
    ):
        """Initialize the plot with given parameters."""
        self.players = players
        self.position: Tuple[int] = position
        self.points: List[deque] = [deque([-1], maxlen=max_window)]
        for i in players:
            self.points.append(deque([0], maxlen=max_window))
        self.graph_type = {
            "v": ["Velocity over time", "Velocity", "Time", ".get_velocity()"],
            "a": ["Acceleration", "Acceleration", "Time", ".get_acceleration()"],
        }[graph_type]
        plt.style.use("dark_background")
        self.fig = pylab.figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.gca()
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.max_count = 15
        self.counter = self.max_count
        self.image = None

    def draw(self, screen):
        """Draw the plot onto the screen."""
        self.clean()
        self.update()
        if self.counter % self.max_count != 0:
            self.counter += 1

        else:
            self.counter = 1
            for i in range(1, len(self.points)):
                self.ax.plot(self.points[0], self.points[i])

            self.ax.set_ylabel(self.graph_type[1])
            self.ax.set_xlabel(self.graph_type[2])
            self.ax.set_title(self.graph_type[0])
            self.canvas.draw()
            renderer = self.canvas.get_renderer()
            self.raw_data = renderer.tostring_rgb()
            size = self.canvas.get_width_height()
            self.image = pygame.image.fromstring(
                self.raw_data, size, "RGB"
            ).convert_alpha()
        screen.blit(self.image, self.position)

    def update(self):
        """Update the values to be plotted."""
        for i in range(1, len(self.players) + 1):
            self.points[i].append(
                eval("self.players[{} - 1]".format(i) + self.graph_type[3])
            )
        self.points[0].append(self.points[0][-1] + 1)

    def clean(self):
        """Clean the canvas for old plot."""
        self.ax.cla()


class Screen:
    """This class represents the screen of a game."""

    def __init__(self):
        """
        Initialize the screen with parameters.

        The parameters are taken from
        the screenSettings data class.
        """
        self.width = settings.ScreenSettings.width
        self.height = settings.ScreenSettings.height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF
        )
        self.screen.set_alpha(None)


class Circle:
    """This class represents a circle."""

    def __init__(
        self, x: float = 50, y: float = 50, color: Colors = Colors.RED, radius: int = 10
    ) -> None:
        """Initialize the circle."""
        self.position: Tuple[int, int] = (int(x), int(y))
        self.radius: int = radius
        self.color: Colors = color

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the circle onto the screen."""
        return pygame.draw.circle(screen, self.color, self.position, self.radius)


class HealthBar:
    """This class represents the health of a player."""

    def __init__(
        self,
        player,
        health: int,
        length: float = 0.015,
        width: float = 0.3,
        y_move: float = 1.4,
        x_move: float = 0.7,
    ) -> None:
        """Initialize the health bar."""
        self.start_health: int = health
        self.health: int = health
        self.player = player
        self.length: float = length
        self.width: float = width
        self.y_move: float = y_move
        self.x_move: float = x_move
        self.position: np.ndarray = player.get_position()

    def reset(self):
        self.health = self.start_health
        self.position = self.player.get_position()

    def update_health(self, health: int) -> None:
        """Update the health of the health bar."""
        if health >= 0 and health <= 100:
            self.health = health

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the health bar onto the screen."""
        pygame.draw.rect(
            screen,
            Colors.RED.value,
            (
                self.position[0] - self.player.data.player_size * self.x_move,
                self.position[1] - self.player.data.player_size * self.y_move,
                self.length * self.start_health * self.player.data.player_size,
                self.width * self.player.data.player_size,
            ),
        )

        if self.health == 0:
            return
        pygame.draw.rect(
            screen,
            Colors.GREEN.value,
            (
                self.position[0] - self.player.data.player_size * self.x_move,
                self.position[1] - self.player.data.player_size * self.y_move,
                self.length * self.health * self.player.data.player_size,
                self.width * self.player.data.player_size,
            ),
        )


class Text:
    """This class represent text."""

    def __init__(self, settings) -> None:
        """Initialize a button with a Texts namedtuple."""
        self.settings = settings
        self.msg = self.settings.msg
        self.smallText = pygame.font.SysFont("comicsansms", settings.font_size)

    def draw(self, screen: pygame.Surface):
        """Draw the text onto the screen."""
        textSurf, textRect = self.text_objects(
            self.msg, self.smallText)
        textRect.center = ((self.settings.w), (self.settings.h))
        screen.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, Colors.BLACK.value)
        return textSurface, textSurface.get_rect()


class Button:
    """This class represent button with text."""

    def __init__(self, settings, font_size=20) -> None:
        """Initialize a button with a Button namedtuple."""
        self.settings = settings
        self.font_size = font_size
        self.clicked = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button and text onto the screen."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            self.settings.x + self.settings.w > mouse[0] > self.settings.x
            and self.settings.y + self.settings.h > mouse[1] > self.settings.y
        ):
            pygame.draw.rect(
                screen,
                self.settings.ac,
                (self.settings.x, self.settings.y,
                 self.settings.w, self.settings.h),
            )

            if click[0]:
                self.clicked = True
        else:
            pygame.draw.rect(
                screen,
                self.settings.ic,
                (self.settings.x, self.settings.y,
                 self.settings.w, self.settings.h),
            )

        text = Text(
            Texts(
                self.settings.msg,
                self.settings.x + (self.settings.w / 2),
                self.settings.y + (self.settings.h / 2),
                self.font_size,
            )
        )

        text.draw(screen)


pygame.font.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
