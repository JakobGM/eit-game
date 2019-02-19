import pygame as pg
import numpy as np
import UDP_connect as con


class Rotate:
    def __init__(self, vect, origin):
        self.vect = vect
        self.origin = np.matrix([[origin[0]], [origin[1]]])

    def rotate(self, tetha, scale):
        self.tetha = tetha
        self.scale = scale
        rot_matrix = np.matrix(
            [
                [np.cos(self.tetha), np.sin(self.tetha)],
                [-1 * np.sin(self.tetha), np.cos(self.tetha)],
            ]
        )
        x_vec = np.matrix([[self.vect[0]], [self.vect[1]]])
        rot_vec = rot_matrix * x_vec * self.scale / 2 + self.origin
        rot_vec = (round(float(rot_vec[0])), round(float(rot_vec[1])))
        print(type(rot_vec[0]))
        return rot_vec


class Filter:
    def __init__(self, time_constant = 1/120, gain = 0.15):
        self.gain = gain
        self.y = 0.0

    def lowpass(self, u):
        self.u = u
        self.y += self.gain * (self.u - self.y)
        return self.y


clock = pg.time.Clock()
screen_width = 1000  # px
screen_height = 1000  # px
c_x = int(screen_width / 2)  # Center of screen, x-dir.
c_y = int(screen_height / 2)  # Center of screen, y-dir.
origin = (c_x, c_y)
screen = pg.display.set_mode((screen_width, screen_height))
input_phone = con.connect_phone()
points_arrow = [
    (0, -10),
    (100, -10),
    (100, -20),
    (130, 0),
    (100, 20),
    (100, 10),
    (0, 10),
]
pg.init()
filter_x = Filter()
filter_y = Filter()

while 1:

    a = input_phone.vect_phone()
    a_filtered = (filter_x.lowpass(a[0]), filter_y.lowpass(a[1]))
    tetha = np.arctan2(a_filtered[1], a_filtered[0])
    scale = np.sqrt(np.square(a_filtered[1]) + np.square(a_filtered[0]))
    rotating_arrow = []

    for i, point in enumerate(points_arrow):
        rotation = Rotate(point, origin)
        rotating_arrow.append(rotation.rotate(tetha, scale))
    screen.fill((0, 0, 0))
    pg.draw.polygon(screen, (255, 255, 255), rotating_arrow)
    pg.display.flip()
    clock.tick(60)
