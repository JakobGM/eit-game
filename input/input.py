from typing import Tuple
import numpy as np
import pygame as pg


class Input:
    def __init__(self, player, keys, input_phone=None):
        self.keys = keys
        self.player1 = player
        self.input_phone = input_phone

    def get_move(self):

        keys = Input.get_key_pressed()
        move = np.zeros(2)
        if self.input_phone:
            move += self.input_phone.vect_phone()

        if keys[self.keys.key_left]:
            move += np.array([-1, 0])

        if keys[self.keys.key_right]:
            move += np.array([1, 0])

        if keys[self.keys.key_up]:
            move += np.array([0, -1])

        if keys[self.keys.key_down]:
            move += np.array([0, 1])

        # Normalize input to a sphere
        if np.linalg.norm(move) > 1:
            move /= np.sqrt(2)
        return move

    def shield_on(self):
        keys = Input.get_key_pressed()
        if keys[self.keys.key_shield]:
            return True
        return False

    @staticmethod
    def get_key_pressed() -> Tuple[int]:
        return pg.key.get_pressed()
