import numpy as np


class Player:
    def __init__(self, mass: float = 1.0):
        self.force = np.zeros(2)
        self.position = np.zeros(2, dtype=float)
        self.velocity = np.zeros(2, dtype=float)
        self.mass = mass
