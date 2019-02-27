from typing import List, Tuple, Dict
import numpy as np
import pygame as pg



class Input:
    def __init__(self, keys: Dict[str, int], input_phone=None):
        self.keys: Dict[str, int] = keys
        self.input_phone = input_phone

    def get_move(self):

        keys = Input.get_key_pressed()
        move = np.zeros(2)
        if self.input_phone:
            move += self.input_phone.vect_phone()

        if keys[self.keys["left"]]:
            move += np.array([-1, 0])

        if keys[self.keys["right"]]:
            move += np.array([1, 0])

        if keys[self.keys["up"]]:
            move += np.array([0, -1])

        if keys[self.keys["down"]]:
            move += np.array([0, 1])

        return move

    @staticmethod
    def get_key_pressed() -> Tuple[int]:
        return pg.key.get_pressed()
