# Don't display the hello world message in the start
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame

from settings import *
from level import Level

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height)) # Make the screen
pygame.display.set_caption("Pygaman II") # Set the caption
clock = pygame.time.Clock() # Make a new clock

level = Level(screen, map_layout) # Set a new level


running = True
while running:
    for event in pygame.event.get(): # Loop through all of the event
        if event.type == pygame.QUIT: running = False # check if we've removed the window, if so stop
    
    level.run() # run the level

    pygame.display.update() # Update the display
    clock.tick(30) # Make the game run at max 30 fps (frames per second)

# quit
pygame.quit()
sys.exit()
exit()
