import numpy as np
import pygame

arrow = [[0, 0], [0, 1], [8, 1], [7, 3], [12, 0], [7, -3], [8, -1], [0, -1]]


class Figure:
    def __init__(self, figure):
        self.figure = figure

    def _makeComplex(self, point):
        return complex(point[0], point[1])

    def _getAngle(self, input_vector):
        input_complex = self._makeComplex(input_vector)
        return np.angle(input_complex)

    def translateFigure(self, translation_vector, input_figure):
        translation_vector = translation_vector
        return_figure = []

        for i, point in enumerate(input_figure):
            return_figure.append(point + translation_vector)

        return return_figure

    def scaleFigure(self, scale, input_figure):
        return scale * np.asarray(input_figure)

    def rotateFigure(self, rotation_vector, input_figure):
        angle = self._getAngle(rotation_vector)
        return_figure = []
        for i, point in enumerate(input_figure):
            complex_point = self._makeComplex(point)
            complex_rotation = self._makeComplex([np.cos(angle), np.sin(angle)])
            rotated_point_complex = complex_point * complex_rotation
            return_figure.append(
                [rotated_point_complex.real, rotated_point_complex.imag]
            )
        return return_figure

    def transform_figure(self, scale, input_vector, translation):
        transformed_figure = self.scaleFigure(scale, self.figure)
        transformed_figure = self.rotateFigure(input_vector, transformed_figure)
        transformed_figure = self.translateFigure(
            translation, transformed_figure
        )
        return transformed_figure

"""
def main():
    global arrow
    pygame.init()
    t = 0
    translation = np.asarray([350, 200])
    scale = 10
    arrow_inst = Figure(arrow)

    pygame.init()
    screen_width = 700
    screen_height = 400
    screen = pygame.display.set_mode([screen_width, screen_height])
    clock = pygame.time.Clock()

    while 1:
        screen.fill((0, 0, 0))
        t += 0.1
        input_vector = [np.cos(-t),np.sin(-t)]
        arrow_inst.transform_figure(scale,input_vector,translation)
        pygame.draw.polygon(screen, (255, 255, 255),arrow_inst.transform_figure(10,input_vector,translation))
        pygame.display.flip()
        clock.tick(30)
"""


