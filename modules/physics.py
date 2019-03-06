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

    def _boarder_collisions(self, player: Player) -> None:
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

    def _player_collisions(self) -> None:
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                # r1 and r2: position. R1 and R2 radius
                r1 = self.players[i].position
                r2 = self.players[j].position
                R1 = self.players[i].player_size
                R2 = self.players[j].player_size

                # Check if players have shield (which is added to the total radius)
                if self.players[i].shield_on:
                    R1 += self.players[i].shield_radius
                if self.players[j].shield_on:
                    R2 += self.players[j].shield_radius

                if np.linalg.norm(r1 - r2) < R1 + R2:
                    x1 = self.players[i].position
                    x2 = self.players[j].position
                    v1 = self.players[i].velocity.copy()
                    v2 = self.players[j].velocity.copy()
                    m1 = self.players[i].mass
                    m2 = self.players[j].mass
                    self.players[i].velocity -= (
                        2
                        * m2
                        / (m1 + m2)
                        * np.dot(v1 - v2, x1 - x2)
                        / np.linalg.norm(x1 - x2) ** 2
                        * (x1 - x2)
                    )
                    self.players[j].velocity -= (
                        2
                        * m1
                        / (m1 + m2)
                        * np.dot(v2 - v1, x2 - x1)
                        / np.linalg.norm(x2 - x1) ** 2
                        * (x2 - x1)
                    )
                    direction_vector = (r2 - r1) / np.linalg.norm(r2 - r1)

                    if np.linalg.norm(v1) > np.linalg.norm(v2):
                        self.players[j].position += (
                            R1 + R2 - np.linalg.norm(r2 - r1)
                        ) * direction_vector
                    elif np.linalg.norm(v2) > np.linalg.norm(v1):
                        self.players[i].position -= (
                            R1 + R2 - np.linalg.norm(r2 - r1)
                        ) * direction_vector
                    else:
                        self.players[i].position -= (
                            (R1 + R2 - np.linalg.norm(r2 - r1)) * direction_vector / 2
                        )

                        self.players[j].position += (
                            (R1 + R2 - np.linalg.norm(r2 - r1)) * direction_vector / 2
                        )

    def move_players(self) -> None:
        """
        Function used to update the position and velocity of all players
        The calculation is based on both user input modeled as a force and
        forces from the physical fields associated with the board.
        """

        for player in self.players:

            force = PhysicsConsts.input_modulation * player.input.get_move()

            # if not shield:
            # print(self.arena.force(player))
            force += PhysicsConsts.force_modulation * self.arena.force(player)

            acceleration = force / player.mass
            player.velocity += acceleration * self.time_step
            player.position += player.velocity * self.time_step

            self._player_collisions()
            self._boarder_collisions(player)
