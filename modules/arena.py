from modules.graphics import *

import abc
from typing import List

import numpy as np
from numpy.linalg import norm
from modules.player import Player
from settings import PhysicsConsts

import time  # bad test to friction change


class ArenaLayer(abc.ABC):
    """
    Abstract class representing the physical fields associated with the board
    """

    @abc.abstractmethod
    def force(self, player: Player, input_force: np.ndarray, total_force: np.ndarray, max_input: float) -> np.array:
        """Return force for specific player."""


class FrictionLayer(ArenaLayer):
    """
    Representing the physical friction field
    """

    def __init__(self, friction_matrix: np.ndarray, friction_const: float) -> None:
        """
        :param friction_matrix: numpy array containing the friction coefficient at each pixel of the board
        """
        self.friction = friction_matrix
        self.friction_const = 0.0001
        self.friction_func = friction_const
        self.start_time = time.time()

    def force(self, player: Player, input_force: np.ndarray, total_force: np.ndarray, max_input: float) -> np.array:
        """
        Calculate the friction force for a player.
        The force is constant as long as the player moves, and zero if the player does not move
        :return: the force of friction
        """

        # Short variable name for the velocity of the player
        velocity = player.velocity

        # If the velocity is 0 (or close) and there is no input:
        if norm(velocity) < PhysicsConsts.static_friction_limit and np.linalg.norm(input_force) == 0:
            player.velocity = np.zeros(2)
            force = np.zeros(2)
            return force

        # If the velocity is 0 (or close) and there is input, the force is directed along input force:
        if norm(velocity) < PhysicsConsts.static_friction_limit and np.linalg.norm(input_force) > 0:
            position = player.position
            x, y = position.tolist()
            x, y = int(x), int(y)

            mu = self.friction[int(x), int(y)] * \
                self.friction_const * self.friction_func()
            force_friction = - mu * input_force / np.linalg.norm(
                input_force) * player.mass * 10 * PhysicsConsts.force_modulation

            # Check if there is small enough friction to start movement
            if np.linalg.norm(force_friction) < max_input:
                return force_friction
            else:
                player.velocity = np.zeros(2)
                force = -input_force
                return force

        # Else moving with constant friction (which may or may not be equal (mening full stop) or less than the input
        position = player.position
        x, y = position.tolist()
        x, y = int(x), int(y)

        mu = self.friction[int(x), int(y)] * \
            self.friction_const * self.friction_func()
        force_friction = force = -mu * velocity / np.linalg.norm(
            velocity) * player.mass * 10 * PhysicsConsts.force_modulation

        if np.linalg.norm(force_friction) > max_input:
            player.velocity = np.zeros(2)
            force = -input_force
            return force

        return force_friction


class AirResistanceLayer(ArenaLayer):
    """
    Representing the physical friction field
    """

    def __init__(self, drag_coefficient: float) -> None:
        """
        Constructor
        :param drag_coefficient: float representing the drag coefficient. This is proportional to geometric shape of the
        object, air density, and the relative speed of the fluid.
        """
        self.drag_coefficient = 0.000001
        self.drag_func = drag_coefficient

    def force(self, player: Player, input_force: np.ndarray, total_force: np.ndarray, max_input: float) -> np.array:
        """
        Calculate the air resistance for a player. The force is given by the eqn.

        F = - C_d * |v|^2 * (v / |v|)  = - C_d * |v| * v,

        where v is velocity vector, and C_d drag coefficient

        :return: ndarray containing the air resistance
        """

        drag_force = -self.drag_coefficient * np.linalg.norm(player.velocity) \
            * player.velocity * PhysicsConsts.force_modulation * \
            self.drag_func()

        # Case 1: Input = 0, velocity = 0
        if np.linalg.norm(input_force) == 0 and np.linalg.norm(player.velocity) == 0:
            print('Case 1: Input = 0, vel = 0')

            # Drag must be zeros
            assert(np.linalg.norm(drag_force) == 0)
            return np.zeros(2)

        # Case 2: Input = 0, velocity > 0
        elif np.linalg.norm(input_force) == 0 and np.linalg.norm(player.velocity) > 0:
            print('Case 2: Input = 0, vel > 0')

            # Manipulating to make friction + drag < input force (to preventing unphysical behavior:
            if np.linalg.norm(total_force) + np.linalg.norm(drag_force) < max_input:
                print('alt er ok!')
                return drag_force
            else:
                print('for stor drag!')
                player.velocity = np.zeros(2)
                return -total_force
                # fiks dette etter å sjekke om dette er en sitasjon som kan skje!

        # Case 3: Input > 0, velocity = 0
        elif np.linalg.norm(input_force) > 0 and np.linalg.norm(player.velocity) == 0:
            print('Case 3: Input > 0, vel = 0')
            assert(np.linalg.norm(drag_force) < 1e-10)
            return np.zeros(2)

        # Case 4: Input > 0, velocity > 0
        elif np.linalg.norm(input_force) > 0 and np.linalg.norm(player.velocity) > 0:
            print('Case 4: Input > 0, vel > 0')
            # Goal reach terminal speed!
            # Therefore the drag cannot be larger than the total force
            if np.linalg.norm(drag_force) > np.linalg.norm(total_force) + 1:
                print('too high drag. terminal!')

                return drag_force/np.linalg.norm(total_force)
            else:
                return drag_force

        return np.zeros(2)


class Arena:
    """
    The Arena class is used to represent the board of the game.
    It includes elements which is needed for graphics, and
    element needed for the physics engine.
    """

    def __init__(self, width, height, layers: List[ArenaLayer]) -> None:
        """
        :param width: number of pixels in the x direction of the board
        :param height: number of pixels in the y direction of the board
        :param layers: the different physical fields assosiated with the board
        """
        self.width = width
        self.height = height
        self.position = (int(width / 2), int(height / 2))
        self.radius = 500
        self.color = (90, 180, 90)
        self.shape = self.display()
        self.layers = layers

    def display(self):
        arena = Circle(self.position[0],
                       self.position[1], self.color, self.radius)
        return arena

    def force(self, player: Player, input_force: np.ndarray, max_input: float):
        total_force = np.zeros(2, dtype=float)
        for layer in self.layers:
            total_force += layer.force(player=player, input_force=input_force, total_force=input_force + total_force,
                                       max_input=max_input)
        return total_force
