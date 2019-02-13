import pygame

class Screen():
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width,self.height))

class Circle():
    def __init__(self,x = 50,y = 50):
        self.position = (x,y)
        self.radius = 50
        self.color = ((255,255,255))

    def draw(self, screen): # Screen is a pygame.surface object
        return pygame.draw.circle(screen, self.color, self.position, self.radius)

