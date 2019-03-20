import time
from typing import List
import numpy as np

from modules.player import Player
from modules.arena import Arena
from settings import PhysicsConsts


class Physics:
    """
    Create a physics engine which is used to update
    the position of all players.
    """

    def __init__(self, game) -> None:
        """
        Constructor

        :param game: Used to get the arena layers and all players
        :param time_step: Time discretization used to calculate the next position
        """
        self.arena = game.get_arena()
        self.players = game.get_players()
        self.current_time = time.perf_counter()  # time.time()

    def _boarder_collisions(self, player: Player) -> None:
        """
        Simulate elastic collisions with the walls. To prevent the player
        from moving through the wall, the position is fixed, and the velocity
        reflected according to conservation to momentum.

        :param player: the given player to be investigated.
        """
        if player.position[0] - player.data.player_size <= 0:
            player.position[0] = player.data.player_size
            player.velocity[0] = -player.velocity[0]

        elif player.position[0] + player.data.player_size >= self.arena.width:
            player.position[0] = self.arena.width - player.data.player_size
            player.velocity[0] = -player.velocity[0]

        if player.position[1] - player.data.player_size <= 0:
            player.position[1] = player.data.player_size
            player.velocity[1] = -player.velocity[1]

        elif player.position[1] + player.data.player_size >= self.arena.height:
            player.position[1] = self.arena.height - player.data.player_size
            player.velocity[1] = -player.velocity[1]

        # check collisions:
        for player_i in [p for p in self.players if p is not player]:
            r1 = player.position
            r2 = player_i.position
            R1 = player.data.player_size
            R2 = player_i.data.player_size
            if np.linalg.norm(r1 - r2) < R1 + R2:
                pass

    def _player_collisions(self) -> None:
        """
        Simulates elastic collisions between the players.
        Both velocity and position is updated. The velocity is updated based on physical conditions.
        The position is updated to prevent the players to have overlaping positions, and to prevent the players to move
        through the walls.

        :return: Updates velocity and positions of the players
        """

        # Looping through all players and checking collisions with the other players.
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):

                # r1 and r2: position. R1 and R2 radius
                r1 = self.players[i].position.copy()
                r2 = self.players[j].position.copy()
                R1 = self.players[i].data.player_size
                R2 = self.players[j].data.player_size

                # Check if players have shield (which is added to the total radius)
                if self.players[i].input.shield_on():
                    R1 += self.players[i].data.shield_radius
                if self.players[j].input.shield_on():
                    R2 += self.players[j].data.shield_radius

                # Check if there is collisions
                if np.linalg.norm(r1 - r2) < R1 + R2:
                    v1 = self.players[i].velocity.copy()
                    v2 = self.players[j].velocity.copy()
                    m1 = self.players[i].mass
                    m2 = self.players[j].mass

                    # Update velocity
                    self.players[i].velocity -= (
                        2
                        * m2
                        / (m1 + m2)
                        * np.dot(v1 - v2, r1 - r2)
                        / np.linalg.norm(r1 - r2) ** 2
                        * (r1 - r2)
                    )
                    self.players[j].velocity -= (
                        2
                        * m1
                        / (m1 + m2)
                        * np.dot(v2 - v1, r2 - r1)
                        / np.linalg.norm(r2 - r1) ** 2
                        * (r2 - r1)
                    )

                    # Fixing positions such that the players are touching each other
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

                    # Fixing the positions in case that any of the players are crossing the borders
                    r1 = self.players[i].position.copy()
                    r2 = self.players[j].position.copy()
                    if r1[0] - R1 < 0 or r2[0] - R2 < 0:

                        diff = min(abs(R1 - r1[0]), abs(R2 - r2[0]))
                        self.players[i].position[0] += diff
                        self.players[j].position[0] += diff

                    if r1[0] + R1 > self.arena.width or (r2[0] + R2) > self.arena.width:
                        diff = min(
                            abs(r1[0] + R1 - self.arena.width),
                            abs(r2[0] + R2 - self.arena.width),
                        )
                        self.players[i].position[0] -= diff
                        self.players[j].position[0] -= diff

                    if r1[1] - R1 < 0 or r2[1] - R2 < 0:
                        diff = min(abs(R1 - r1[1]), abs(R2 - r2[1]))
                        self.players[i].position[1] += diff
                        self.players[j].position[1] += diff

                    if (
                        r1[1] + R1 > self.arena.height
                        or (r2[1] + R2) > self.arena.height
                    ):
                        diff = min(
                            abs(r1[1] + R1 - self.arena.height),
                            abs(r2[1] + R2 - self.arena.height),
                        )
                        self.players[i].position[1] -= diff
                        self.players[j].position[1] -= diff

    def move_players(self) -> None:
        """
        Function used to update the position and velocity of all players
        The calculation is based on both user input modeled as a force and
        forces from the physical fields associated with the board.
        """

        dt = time.perf_counter() - self.current_time
        # time.time() - self.current_time
        self.current_time = time.perf_counter()  # time.time()

        for player in self.players:
            if player.shield():
                continue

            force = PhysicsConsts.input_modulation * player.input.get_move()
            force += self.arena.force(player, force, PhysicsConsts.input_modulation, dt)

            # Eulers method
            acceleration = force / player.mass
            player.velocity += acceleration * dt
            player.position += player.velocity * dt

            self._boarder_collisions(player)

        self._player_collisions()
