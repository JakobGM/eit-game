from typing import List

from modules.player import Player
from modules.arena import Arena
from settings import PhysicsConsts


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

    def boarder_collitions(self, player: Player) -> None:
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

            self.boarder_collitions(player)
            """
            # Periodic boundary condition
            if player.position[0] > self.arena.width:
                player.position[0] -= self.arena.width
            if player.position[0] < 0:
                player.position[0] += self.arena.width
            if player.position[1] > self.arena.height:
                player.position[1] -= self.arena.height
            if player.position[1] < 0:
                player.position[1] += self.arena.height
            """
