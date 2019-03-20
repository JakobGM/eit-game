from typing import Tuple
import numpy as np
import pygame as pg
import multiprocessing


class Input:
    """This class represents the input module for players."""

    def __init__(self, keys, input_phone):
        """
        Initialize the input module for the given player.

        :param keys: The keys for the given player.
        :param input_phone: A phone to control the input.
        """
        self.keys = keys
        self.input_phone = input_phone
        if self.input_phone:
            process = multiprocessing.Process(target=self.input_phone.set_up)
            process.start()

    def get_move(self) -> np.ndarray:
        """Move the player."""
        keys = Input.get_key_pressed()
        move = np.zeros(2)

        # Get input from the phone if one exists
        if self.input_phone and self.input_phone.ready:
            move += self.input_phone.vect_phone()

        # Get input from keyboard.
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

    def shield_on(self) -> bool:
        """Check if the shield is on for the player."""
        keys = Input.get_key_pressed()
        if keys[self.keys.key_shield]:
            return True
        return False

    @staticmethod
    def get_key_pressed() -> Tuple[int]:
        """Get the keys for the player."""
        return pg.key.get_pressed()
