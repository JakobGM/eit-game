import pygame

class Screen():
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width,self.height))

class Circle():
    def __init__(self):
        self.position = (500,500)
        self.radius = 500
        self.color = ((255,255,255))

    def draw(self, screen): # Screen is a pygame.surface object
        return pygame.draw.circle(screen, self.color, self.position, self.radius)

