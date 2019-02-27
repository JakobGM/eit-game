from typing import List

import numpy as np

from haakon.player import Player
from haakon.arena import Arena


class Physics:
    """
    Creates a physics engine which is used to update the position of all players
    """

    def __init__(self, arena: Arena, players: List[Player], time_step: float) -> None:
        """
        Constructor
        :param arena: Store the board of the game, including the physical fields
        :param players: A list of players
        :param time_step: Time discretization used to calculate the next position
        """
        self.arena = arena
        self.players = players
        self.time_step = time_step

    def move_players(self) -> None:
        """
        Function used to update the position and velocity of all players
        The calculation is based on both user input modeled as a force and
        forces from the physical fields associated with the board.
        """
        for player in self.players:
            force = 1500 * player.input.get_move()
            force += 50 * self.arena.force(player)
            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            player.position += player.velocity * self.time_step

            # Periodic boundary condition
            if player.position[0] > self.arena.width:
                player.position[0] -= self.arena.width
            if player.position[0] < 0:
                player.position[0] += self.arena.width
            if player.position[1] > self.arena.height:
                player.position[1] -= self.arena.height
            if player.position[1] < 0:
                player.position[1] += self.arena.height
