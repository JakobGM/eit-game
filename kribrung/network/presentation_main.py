import pygame as pg
import UDP_connect as con
import presentation_input as input_
import numpy as np
import random as rd
import text_to_screen as t2s
import pygame.freetype

pg.init()
clock = pg.time.Clock()
screen_width = 1000  # px
screen_height = 1000  # px
c_x = int(screen_width / 2)  # Center of screen, x-dir.
c_y = int(screen_height / 2)  # Center of screen, y-dir.
origin = (c_x, c_y)

screen = pg.display.set_mode((screen_width, screen_height))
input_phone = con.connect_phone()

points_arrow = [(0, -7), (100, -7), (100, -20), (135, 0), (100, 20), (100, 7), (0, 7)]

filter_x = input_.Filter()
filter_y = input_.Filter()

change_color = 0
r = 0
g = 0
b = 0
color_time = 4

phone_input_text = t2s.Text()  # This should maybe be a lib instead, discuss
phone_input_text_pos = (20, 20)
filtered_input_text = t2s.Text()
filtered_input_text_pos = (20, 40)
text_color = (255, 255, 255)
font = pg.freetype.Font(None, 22)


while 1:
    screen.fill((0, 0, 0))
    if change_color > color_time:
        r = rd.randint(140, 255)
        g = rd.randint(0, 200)
        b = rd.randint(0, 200)
        change_color = 0

    a = tuple(input_phone.vect_phone()[0])
    a_filtered = (filter_x.lowpass(a[0]), filter_y.lowpass(a[1]))
    tetha = np.arctan2(a_filtered[1], a_filtered[0])
    scale = np.sqrt(np.square(a_filtered[1]) + np.square(a_filtered[0]))
    rotating_arrow = []

    input_string = "Input from phone x:{} y:{}".format(a[0], a[1])
    filtered_string = "Filtered input from phone x:{} y:{}".format(
        a_filtered[0], a_filtered[1]
    )

    font.render_to(screen, filtered_input_text_pos, filtered_string, text_color)
    font.render_to(screen, phone_input_text_pos, input_string, text_color)

    for i, point in enumerate(points_arrow):
        rotation = input_.Rotate(point, origin)
        rotating_arrow.append(rotation.rotate(tetha, scale))

    pg.draw.polygon(screen, (r, g, b), rotating_arrow)
    clock.tick(60)
    pg.display.flip()

    change_color += 1
