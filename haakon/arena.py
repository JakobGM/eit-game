import pygame
import random
from haakon.graphics import *

class Arena():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (int(width / 2), int(height / 2))
        self.radius = 500
        self.color = (90,180,90)
        self.shape = self.display()

    def display(self):
        arena = Circle(self.position[0], self.position[1],self.color, self.radius)
        return arena
