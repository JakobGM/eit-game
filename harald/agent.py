import numpy as np


class Player:
    def __init__(self):
        self.force = np.zeros(2)
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
