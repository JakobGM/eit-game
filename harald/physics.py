import logging
from typing import List

import numpy as np

from haakon.player import Player
from harald import arena

logger = logging.getLogger(__name__)


class Physics:
    def __init__(self, arena: arena.Arena, players: List[Player], time_step: float):
        self.arena = arena
        self.players = players
        self.time_step = time_step

    def move_players(self) -> None:

        for player in self.players:

            force = 100 * player.input.get_move()
            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            player.position += player.velocity * self.time_step
