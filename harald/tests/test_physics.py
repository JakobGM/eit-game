from harald.physics import Physics
from harald.arena import Arena
from harald.agent import Player


def test_invokation_of_physics_object():
    """Check if we are able to create Physics object."""
    players = [Player(), Player()]
    arena = Arena()
    physics = Physics(
        arena=arena,
        players=players,
    )
