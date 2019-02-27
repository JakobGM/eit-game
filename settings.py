from dataclasses import dataclass


@dataclass
class ScreenSettings:
    height: int = 1000
    width: int = 1000


@dataclass
class PhysicsConsts:
    friction_const = 1
    drag_coefficient = 1
    input_modulation = 1500
    force_modulation = 50
    static_friction_limit = 5
