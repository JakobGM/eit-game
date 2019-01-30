import pygame

# Initializes the game
x = pygame.init()
print(x)

gameDisplay = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Experts in Team")

# pygame.display.flip()

pygame.display.update()

gameExit = False

# Prevents the game from shutting down
# event is a log of what has happened
while not gameExit:
    for event in pygame.event.get():
        print(event)


# Exits the game
pygame.quit()
quit()
