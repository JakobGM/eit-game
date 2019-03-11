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


class Slider():
    def __init__(self, name, val, maxi, mini, pos, surface):
        self.font = pygame.font.SysFont("Verdana", 12)
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 550
        self.screen = surface
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.txt_surf = self.font.render(name, 1, Colors.BLACK.value)
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
        pygame.draw.circle(self.button_surf, Colors.BLACK.value, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, Colors.ORANGE.value, (10, 10), 4, 0)

    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
        the basic slide surface
        """
        # static
        surf = self.surf.copy()
        # dynamic
        pos = (10 + int((self.val - self.mini)
                        / (self.maxi - self.mini) * 80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        # move of button box to correct screen position
        self.button_rect.move_ip(self.xpos, self.ypos)
        # screen
        self.screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
        The dynamic part; reacts to movement of the slider button.
        """
        self.val = (pygame.mouse.get_pos()[
                    0] - self.xpos - 10) / 80 * \
            (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


class Graph:
    def __init__(self, players, graph_type, figsize=[4, 4],
                 dpi=100, max_window=100):
        self.players = players
        self.figsize = figsize
        self.dpi = dpi
        self.points = [deque([-1], maxlen=max_window)]
        for i in players:
            self.points.append(deque([0], maxlen=max_window))
        self.graph_type = {
            'v': ['Velocity', 'Speed', 'Time', '.get_velocity()']}[graph_type]
        plt.style.use('dark_background')

    def plot(self):
        plt.close('all')
        self.fig = pylab.figure(figsize=self.figsize, dpi=self.dpi)

        for i in range(1, len(self.players) + 1):
            self.points[i].append(eval('self.players[{} - 1]'.format(i) +
                                       self.graph_type[3]))
        self.points[0].append(self.points[0][-1] + 1)
        ax = self.fig.gca()
        ax.set_ylabel(self.graph_type[1])
        ax.set_xlabel(self.graph_type[2])
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
                               self.position[1] -
                               self.player.data.player_size * self.y_move,
                               self.length * self.start_health
                               * self.player.data.player_size,
                               self.width * self.player.data.player_size))

        hf = pygame.draw.rect(screen,
                              Colors.GREEN.value,
                              (self.position[0] -
                               self.player.data.player_size * self.x_move,
                               self.position[1]
                               - self.player.data.player_size * self.y_move,
                               self.length * self.health *
                               self.player.data.player_size,
                               self.width * self.player.data.player_size))
        return hf, mh
