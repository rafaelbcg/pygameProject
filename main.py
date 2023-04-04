# Simple pygame program
# Import the pygame library
import pygame, random, player, enemy, cloud

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#set up the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#initialize the pygame library
pygame.init()

# Drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

gamer = player.Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(gamer)


# Run until the user asks to quit
running = True
while running:

    movement = 0

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #if K_ESCAPE is key hit?
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = enemy.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = cloud.Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    gamer.update(pressed_keys)

    # Update enemy position
    enemies.update()
    clouds.update()

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(gamer, enemies):
        # If so, then remove the player and stop the loop
        gamer.kill()
        running = False

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

