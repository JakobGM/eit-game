from typing import List

import numpy as np

from harald import agent, arena


class Physics:
    def __init__(self, arena: arena.Arena, players: List[agent.Player]):
        self.arena = arena
        self.players = players
