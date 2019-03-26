import numpy as np
import pygame
import time

def makeComplex(input_vector):
    return complex(input_vector[0],input_vector[1])

def getAngle(input_vector):
    input_complex = makeComplex(input_vector)
    return np.angle(input_complex)
def translateFigure(translation_vector,input_figure):
    return_figure = []
    for i,point in enumerate(input_figure):
         return_figure.append(point+translation_vector)
    return np.asarray(return_figure)

def scaleFigure(scale,input_figure):
    return scale*np.asarray(input_figure)

def rotateFigure(angle,input_figure):
    return_figure = []
    for i,point in enumerate(input_figure):
        complex_point = makeComplex(point)
        complex_rotation = makeComplex([np.cos(angle),np.sin(angle)])
        rotated_point_complex = complex_point*complex_rotation
        return_figure.append([rotated_point_complex.real,rotated_point_complex.imag])
    return return_figure


arrow = [
    [0, 0],
    [0, 1],
    [8, 1],
    [7, 3],
    [12, 0],
    [7, -3],
    [8, -1],
    [0, -1]
    ]



def main():
    global arrow
    pygame.init()
    arrow = np.asarray(arrow)

    translation = np.asarray([350,200])
    rotation = -0.05
    arrow = scaleFigure(10,arrow)
    arrow_rotated = rotateFigure(rotation, arrow)
    arrow = translateFigure(translation,arrow_rotated)


    pygame.init()
    screen_width=700
    screen_height=400
    screen = pygame.display.set_mode([screen_width,screen_height])
    clock = pygame.time.Clock()
    while 1:
        screen.fill((0,0,0))

        arrow_rotated = rotateFigure(rotation, arrow_rotated)
        arrow_rotated_translated = translateFigure(translation,arrow_rotated)
        pygame.draw.polygon(screen,(255,255,255),arrow_rotated_translated)
        print(arrow_rotated_translated[4])
        pygame.display.flip()
        clock.tick(30)

main()