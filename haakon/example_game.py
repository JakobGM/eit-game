import pygame
import random
import player
import arena
import text_to_screen as t2s
import healthbar
import numpy as np
import draw_coin


pygame.init()
pygame.font.init()

# Window
screen_width = 1000  # px
screen_height = 850  # px
center_x = int(screen_width / 2)  # Center of screen, x-dir.
center_y = int(screen_height / 2)  # Center of screen, y-dir.

screen = pygame.display.set_mode(
    (screen_width, screen_height)
)  # drawing surface, what happenes if we have multiple?

# Player
player_health_max = 6000  # Unused so far, got an idea of making an healthbar using this
player_health = player_health_max
player_velocity = 3  # Speed of player
player_size = 30  # Radius of player
player_color = (255, 128, 0, 128)  # Random player color (orange)
shield_color = (0, 255, 0, 0)  # Random shield color (green)

# Bounds
x_lowerbound = player_size
x_upperbound = screen_width - player_size
y_lowerbound = player_size
y_upperbound = screen_height - player_size

# Arena
arena_pos = (center_x, center_y)  # Centered arena
if screen_width < screen_height:  # Relative arenaradius dependent on the window size.
    arena_radius = int(screen_width / 2 - screen_width / 5)
else:  # Relative arenaradius dependent on the window size.
    arena_radius = int(screen_height / 2 - screen_height / 5)
arena_color = (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
)  # Random arena color

done = False  # init for the code to enter while loop
x = center_x  # starting pos x for interactive element
y = center_y  # starting pos y for interactive element

# FPS limiting
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Might want to use an eventqueue instead of if statements example follows:
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        # is_blue = not is_blue
        # if is_blue:
        # player_velocity = 0
        # draw_shield = True
        # else:
        # player_velocity = 3
        # draw_shield = False

    # Shortening for readability
    pressed = pygame.key.get_pressed()

    # Checks if the player is shielded
    if pressed[pygame.K_SPACE]:
        draw_shield = True  # Flags shield to be drawn
        player_velocity = 0  # Player cannot move while shielded
        player_health += 25  # Player regens health while shielded.
    else:
        draw_shield = False
        player_velocity = 3
    player_pos = (x, y)

    # Input check
    if pressed[pygame.K_w]:  # Top is zero, means up is negative and down is positive
        y -= player_velocity
        if y <= y_lowerbound:
            y = y_lowerbound
    if pressed[pygame.K_s]:
        y += player_velocity
        if y >= y_upperbound:
            y = y_upperbound
    if pressed[pygame.K_a]:  # Left is zero, hence left is negative, right is positive
        x -= player_velocity
        if x <= x_lowerbound:
            x = x_lowerbound
    if pressed[pygame.K_d]:
        x += player_velocity
        if x >= x_upperbound:
            x = x_upperbound

    # Player health
    if (
        int(np.sqrt(np.square(x - screen_width / 2) + np.square(y - screen_height / 2)))
        > arena_radius
    ):
        player_health -= 50
    if player_health <= 0:
        done = True
    if player_health >= player_health_max:
        player_health = player_health_max

    # Screenstrings needs to be defined inside the while for updating reasons
    pos_string = "x: " + str(x) + " y: " + str(y)
    shield_string = "Shields: " + str(draw_shield)
    player_health_str = "Health: " + str(player_health)

    # Clear screen
    screen.fill((0, 0, 0))

    # Drawing arena
    arena.draw_arena(screen, arena_color, arena_pos, arena_radius)

    # Drawing player
    player.draw_player(
        screen, player_size, player_pos, player_color, shield_color, draw_shield
    )

    # Draw position text
    t2s.write(screen, (0, 255, 180), (25, 25), pos_string)

    # Drawing shield text
    t2s.write(screen, (0, 255, 180), (25, 50), shield_string)

    # Drawing healthbar
    healthbar.draw(screen, player_health, screen_width)

    # Draw Coin
    draw_coin.coin(screen, (250, 400))

    # Flips the newly drawn page to the window
    pygame.display.flip()

    # Forcing 60 FPS max
    clock.tick(60)
