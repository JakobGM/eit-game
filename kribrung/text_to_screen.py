import pygame
import pygame.freetype
# If shaking text, use another font size.
# 22 seems to be working fine for the current font, check documentation for more info on specific font sizes available.
def write(surface, color, pos, text):
    font = pygame.freetype.Font(None, 22)
    font.render_to(surface, pos, text, color)
