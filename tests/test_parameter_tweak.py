import numpy as np

from game import Game
from modules.physics import Physics
import modules.arena as arena
import modules.player as player
import players_settings as ps

from settings import PhysicsConsts, ArenaSettings


def test_friction_to_high(capsys) -> None:
    """
    Test reaction to a too high friction constant
    """
    PhysicsConsts.friction_const = 1
    assert PhysicsConsts.friction_const == 1

    # Layers
    layers = [
        arena.FrictionLayer(
            np.ones((ArenaSettings.x, ArenaSettings.y)), PhysicsConsts.friction_const
        ),
        arena.AirResistanceLayer(PhysicsConsts.drag_coefficient),
    ]

    # Arena
    arena = arena.Arena(ArenaSettings.x, ArenaSettings.y, layers=layers)

    # Players
    players = [player.Player(200, 200, ps.Player1Settings)]

    # Physic engine
    physics = Physics()

    physics.move_players(players)


def test_drag_to_high() -> None:
    """
    Test reaction to a too high drag constant
    """
    PhysicsConsts.friction_const = 1
    print(PhysicsConsts.friction_const)


def test_drag_plus_friction_to_hig() -> None:
    """
    Test reaction if drag and friction coefficients are low enough seperately, but the combo is too high
    """
