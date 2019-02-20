import logging
from typing import List

import numpy as np

from haakon.player import Player
from haakon.arena import Arena

logger = logging.getLogger(__name__)


class Physics:
    def __init__(self, arena: Arena, players: List[Player], time_step: float):
        self.arena = arena
        self.players = players
        self.time_step = time_step

    def move_players(self) -> None:

        for player in self.players:

            force = 1500 * player.input.get_move()
            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            """
            if player.position[0] + player.velocity[0] * self.time_step > 1000:
                player.position[0] = player.velocity[0] *self.time_step - 1000
            if player.position[0] + player.velocity[0] * self.time_step < 0:
                player.position[0] = player.velocity[0] *self.time_step + 1000

            if player.position[1] + player.velocity[1] * self.time_step > 1000:
                player.position[1] = player.velocity[1]*self.time_step - 1000
            if player.position[1] + player.velocity[1] * self.time_step > 1000:
                player.position[1] = player.velocity[1] *self.time_step + 1000
            """
            player.position += player.velocity * self.time_step
            if player.position[0] > self.arena.width:
                player.position[0] -= self.arena.width
            if player.position[0] < 0:
                player.position[0] += self.arena.width
            if player.position[1] > self.arena.height:
                player.position[1] -= self.arena.height
            if player.position[1] < 0:
                player.position[1] += self.arena.height

