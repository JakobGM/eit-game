import numpy as np


class Rotate:
    def __init__(self, vect, origin):
        self.vect = vect
        self.origin = np.matrix([[origin[0]], [origin[1]]])

    def rotate(self, tetha, scale):
        self.tetha = tetha
        self.scale = scale
        rot_matrix = np.matrix(
            [
                [np.cos(self.tetha), np.sin(self.tetha)],
                [-1 * np.sin(self.tetha), np.cos(self.tetha)],
            ]
        )
        x_vec = np.matrix([[self.vect[0]], [self.vect[1]]])
        rot_vec = rot_matrix * x_vec * self.scale / 2 + self.origin
        rot_vec = (round(float(rot_vec[0])), round(float(rot_vec[1])))
        return rot_vec


class Filter:
    def __init__(self, gain=0.15):
        self.gain = gain
        self.y = 0.0

    def lowpass(self, u):
        self.u = u
        self.y += self.gain * (self.u - self.y)
        return self.y
