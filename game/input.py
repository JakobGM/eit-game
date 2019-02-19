from typing import List
import time

import numpy as np

import pygame as pg

pg.init()


class Input:
    x: float
    y: float
    F: np.ndarray

    def __init__(self, x: float, y: float, keyevents):
        self.x = x
        self.y = y
        self.F = np.array([x, y])
        self.F = self.F / np.linalg.norm(self.F)

        if pg.K_SPACE in keyevents:
            self.spacebar_pressed = True
        else:
            self.spacebar_pressed = False


class Inputs:
    def __init__(self, players):
        """Constructor."""
        self.players = players
        self.is_down = {"up": False, "down": False, "left": False, "right": False}

        self.direction = {
            "up": (pg.K_w, pg.K_UP),
            "down": (pg.K_s, pg.K_DOWN),
            "left": (pg.K_a, pg.K_LEFT),
            "right": (pg.K_d, pg.K_RIGHT),
        }

    def latest(self) -> List[Input]:
        inputs = {}
        pressed = pg.key.get_pressed()
        for i, name in enumerate(self.players):
            x, y = 0, 0
            if pressed[self.direction["up"][i]]:
                self.is_down["up"] = True
                print("UP is pressed")
            else:
                self.is_down["up"] = False
                print("UP is released")

            if pressed[self.direction["down"][i]]:
                self.is_down["down"] = True
                print("down is pressed")
            else:
                self.is_down["down"] = False
                print("down is released")

            if pressed[self.direction["left"][i]]:
                self.is_down["left"] = True
                print("LEFT is pressed")
            else:
                self.is_down["left"] = False
                print("LEFT is released")

            if pressed[self.direction["right"][i]]:
                self.is_down["right"] = True
                print("RIGHT is pressed")
            else:
                self.is_down["right"] = False
                print("RIGHT is released")

            # inputs[name] = Input(x=x, y=y, keyevents=keyevents)
        # return inputs


players = ["kristoffer", "Sindre"]
player = Inputs(players)
screen_width = 400  # px
screen_height = 400  # px
c_x = int(screen_width / 2)  # Center of screen, x-dir.
c_y = int(screen_height / 2)  # Center of screen, y-dir.
screen = pg.display.set_mode(
    (screen_width, screen_height)
)  # drawing surface, what happenes if we have multiple?
input_fra_telefon = (1,5)
done = False
while not done:
    vinkel = np.arctan2(input_fra_telefon[1],input_fra_telefon[0])
    scale = np.sqrt(np.square(input_fra_telefon[0])+np.square(input_fra_telefon[1]))/10
    print("her")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        print(event)
        player.latest()
    pg.draw.polygon(
        screen,
        (255, 255, 255),
        (
            (c_x + 10, c_y),  # 1
            (c_x - 10, c_y),  # 2
            (c_x - 10, c_y + 100),  # 3
            (c_x - 30, c_y + 100),  # 4
            (c_x, c_y + 125),  # 5
            (c_x + 30, c_y + 100),  # 6
            (c_x + 10, c_y + 100),  # 7
        ),
        0,<
    )
    pg.display.flip()
    print(player.is_down)
"""self.direction["up"][i]"""
