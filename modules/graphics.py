import settings
import pygame
from settings import Colors
from players_settings import PlayerSettings
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
from collections import deque
matplotlib.use("Agg")


class Graph:
    def __init__(self, players, graph_type, figsize=[4, 4],
                 dpi=100, max_window=100):
        self.players = players
        self.figsize = figsize
        self.dpi = dpi
        self.points = [deque([-1], maxlen=max_window)]
        for i in players:
            self.points.append(deque([0], maxlen=max_window))
        self.graph_type = graph_type

    def plot(self):
        plt.close('all')
        self.fig = pylab.figure(figsize=self.figsize, dpi=self.dpi)

        for i in range(1, len(self.players) + 1):
            self.points[i].append(self.players[i - 1].get_velocity())
        self.points[0].append(self.points[0][-1] + 1)
        ax = self.fig.gca()

        for i in range(1, len(self.points)):
            ax.plot(self.points[0], self.points[i])
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.canvas.draw()
        renderer = self.canvas.get_renderer()
        self.raw_data = renderer.tostring_rgb()

    def get_plot(self):
        """Return the plot."""
        size = self.canvas.get_width_height()
        return pygame.image.fromstring(self.raw_data, size, "RGB")


class Screen:
    def __init__(self):
        self.width = settings.ScreenSettings.width
        self.height = settings.ScreenSettings.height
        self.screen = pygame.display.set_mode((self.width, self.height))


class Circle:
    def __init__(self, x=50, y=50, color=Colors.RED, radius=10):
        self.position = (int(x), int(y))
        self.radius = radius
        self.color = color

    def draw(self, screen):
        return pygame.draw.circle(screen, self.color,
                                  self.position, self.radius)


class HealthBar:
    def __init__(self, player, health, length=0.015, width=0.3,
                 y_move=1.4, x_move=0.7):
        """Class for storing health."""
        self.start_health = health
        self.health = health
        self.player = player
        self.length = length
        self.width = width
        self.y_move = 1.4
        self.x_move = 0.7
        self.position = player.get_position()

    def draw(self, screen):
        mh = pygame.draw.rect(screen,
                              Colors.RED.value,
                              (self.position[0] -
                               self.player.data.player_size * self.x_move,
                               self.position[1]
                               - self.player.data.player_size * self.y_move,
                               self.length * self.start_health *
                               self.player.data.player_size,
                               self.width * self.player.data.player_size))

        hf = pygame.draw.rect(screen,
                              Colors.GREEN.value,
                              (self.position[0] -
                               self.player.data.player_size * self.x_move,
                               self.position[1] -
                               self.player.data.player_size * self.y_move,
                               self.length * self.health
                               * self.player.data.player_size,
                               self.width * self.player.data.player_size))
        return hf, mh
