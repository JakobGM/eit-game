import pygame as pg
import UDP_connect as con
import presentation_input as input_
import numpy as np
import random as rd
import text_to_screen as t2s
import pygame.freetype

pg.init()
clock = pg.time.Clock()
screen_width = 800  # px
screen_height = 800  # px
c_x = int(screen_width / 2)  # Center of screen, x-dir.
c_y = int(screen_height / 2)  # Center of screen, y-dir.
origin = (c_x, c_y)

screen = pg.display.set_mode((screen_width, screen_height))
input_phone = con.connect_phone()

points_arrow = [(0, -7), (100, -7), (100, -20), (135, 0), (100, 20), (100, 7), (0, 7)]

filter_x = input_.Filter()
filter_y = input_.Filter()

change_color = 0
r = 255
g = 255
b = 255
color_time = 4

phone_input_text = t2s.Text()  # This should maybe be a lib instead, discuss
phone_input_text_pos = (20, 20)
filtered_input_text = t2s.Text()
filtered_input_text_pos = (20, 40)
text_color = (255, 255, 255)
font = pg.freetype.Font(None, 22)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    a, b = input_phone.vect_phone()
    a = tuple(a)

    a_filtered = (filter_x.lowpass(a[0]), filter_y.lowpass(a[1]))
    tetha = np.arctan2(a_filtered[1], a_filtered[0])
    scale = np.sqrt(np.square(a_filtered[1]) + np.square(a_filtered[0]))
    rotating_arrow = []

    x_string = "X: {}".format(round(a_filtered[0],2))
    y_string = "Y: {}".format(round(a_filtered[1],2))
    scale_string = "Scale: {}".format(round(scale,2))
    tetha_string = "Theta: {}".format(round(tetha,2))
    is_flipped_string = "Er telefonen snudd? {}".format(b)

    font.render_to(screen, (20, 20), x_string, text_color)
    font.render_to(screen, (20, 40), y_string, text_color)
    font.render_to(screen, (140, 20), scale_string, text_color)
    font.render_to(screen, (140, 40), tetha_string, text_color)
    font.render_to(screen, (20, 60), is_flipped_string, text_color)

    for i, point in enumerate(points_arrow):
        rotation = input_.Rotate(point, origin)
        rotating_arrow.append(rotation.rotate(tetha, scale))

    pg.draw.polygon(screen, (r, g, b), rotating_arrow)
    pg.display.flip()
    clock.tick(60)
