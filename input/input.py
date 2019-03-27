"""Input klasse."""
from typing import Tuple, Dict
import numpy as np
import pygame as pg
import multiprocessing
import threading
from input.UDP_connect import ConnectPhone


class Input:
    """This class represents the input module for players."""

    def __init__(self, keys: type, input_phone: ConnectPhone) -> None:
        """
        Initialize the input module for the given player.

        :param keys: The keys for the given player.
        :param input_phone: A phone to control the input.
        """
        self.keys: type = keys
        self.input_phone: ConnectPhone = input_phone
        if self.input_phone:
            thread = threading.Thread(
                target=self.input_phone.set_up, daemon=True)
            thread.start()

    def get_move(self) -> np.ndarray:
        """Move the player."""
        keys: Dict[int:int] = Input.get_key_pressed()
        move: np.ndarray = np.zeros(2)

        # Get input from the phone if one exists
        if self.input_phone:
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
        keys: Dict[int:int] = Input.get_key_pressed()
        if keys[self.keys.key_shield]:
            return True
        return False

    @staticmethod
    def get_key_pressed() -> Tuple[int]:
        """Get the keys for the player."""
        return pg.key.get_pressed()
