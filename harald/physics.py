import logging
from typing import List

import numpy as np

from haakon.player import Player
from haakon.arena import Arena

logger = logging.getLogger(__name__)


class Physics:
    """
    Creates a physics engine which is used to update the position of all players
    """
    def __init__(self, arena: Arena, players: List[Player], time_step: float):
        '''
        Initialize variables
        :param arena: Store the board of the game, including the physical fields
        :param players: A list of players
        :param time_step:
        '''
        self.arena = arena
        self.players = players
        self.time_step = time_step

    def move_players(self) -> None:
        '''

        :return:
        '''
        for player in self.players:
            # print(self.arena.force(player))
            force = 1500 * player.input.get_move()
            print(force, "\t", self.arena.force(player))
            force += 50 * self.arena.force(player)
            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            player.position += player.velocity * self.time_step
            if player.position[0] > self.arena.width:
                player.position[0] -= self.arena.width
            if player.position[0] < 0:
                player.position[0] += self.arena.width
            if player.position[1] > self.arena.height:
                player.position[1] -= self.arena.height
            if player.position[1] < 0:
                player.position[1] += self.arena.height
