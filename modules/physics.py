from typing import List
import numpy as np

from modules.player import Player
from modules.arena import Arena
from settings import PhysicsConsts


class Physics:
    """
    Creates a physics engine which is used to update the position of all players
    """

    def __init__(self, game, time_step: float) -> None:
        """
        Constructor

        :param game: Used to get the arena layers and all players
        :param time_step: Time discretization used to calculate the next position
        """
        self.arena = game.get_arena()
        self.players = game.get_players()
        self.time_step = time_step

    def boarder_collisions(self, player: Player) -> None:
        """
        Simulates elastic collisions with the walls. To prevent the player from moving through the wall, the position is
        fixed, and the velocity reflected according to conservation to momentum.

        :param player: the given player to be investigated.
        """

        if player.position[0] - player.player_size <= 0:
            player.position[0] = player.player_size
            player.velocity[0] = -player.velocity[0]

        elif player.position[0] + player.player_size >= self.arena.width:
            player.position[0] = self.arena.width - player.player_size
            player.velocity[0] = -player.velocity[0]

        if player.position[1] - player.player_size <= 0:
            player.position[1] = player.player_size
            player.velocity[1] = -player.velocity[1]

        elif player.position[1] + player.player_size >= self.arena.height:
            player.position[1] = self.arena.height - player.player_size
            player.velocity[1] = -player.velocity[1]

    def player_collisions(self) -> None:
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                if np.abs(self.players[i].position - self.players[j].position) <= self.players[i].:
                    pass

    def move_players(self) -> None:
        """
        Function used to update the position and velocity of all players
        The calculation is based on both user input modeled as a force and
        forces from the physical fields associated with the board.
        """

        for player in self.players:
            force = PhysicsConsts.input_modulation * player.input.get_move()

            # print(self.arena.force(player))
            force += PhysicsConsts.force_modulation * self.arena.force(player)

            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            player.position += player.velocity * self.time_step

            self.boarder_collisions(player)
