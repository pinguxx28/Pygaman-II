import pygame

from settings import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type):
        super().__init__()
        # Set the image
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(self.color_image(enemy_type))
        # Get the rect
        self.rect = self.image.get_rect(topleft = pos)
        # Set the type
        self.enemy_type = enemy_type
        # Get facing dir
        self.facing = self.get_facing()
        # Set the health
        self.health = 3
        # Shot variables (when self got shot)
        self.shot_timer = 0
        self.shot = False
        # Shoot variables (when self shoot)
        self.shoot_timer = 0
        self.shoot_interval = randint(60, 90)

    def shooter(self): 
        # Returns true if self is a shooter
        shooters = ('p', 'q')
        if self.enemy_type in shooters:
            return True
        return False

    def get_facing(self): # Get the direction its facing
        facing = 1
        left_facing = ('q')
        if self.enemy_type in left_facing:
            facing = -1

        return facing

    def color_image(self, enemy_type):
        # Color the enemy depending on the type
        color = "White"
        if enemy_type == "q" or enemy_type == "p": # Shooter-left
            color = (0, 255, 0)
            
        return color

    def manage_shot(self):
        if self.shot: # If we've just been shot
            self.shot_timer += 1 # Increase the shot timer

            # Make that cool gradient when you shoot an enemy
            if self.shot_timer < 4:
                self.image.fill((255/3*self.shot_timer, 255-255/3*self.shot_timer, 0))
            elif self.shot_timer > 7:
                color = (255-255/3*(self.shot_timer-8), 255/3*(self.shot_timer-8), 0)
                self.image.fill(color)

            if self.shot_timer > 10: # Remove the gradient when done
                self.shot_timer = 0
                self.shot = False

    def manage_shoot(self):
        self.shoot_timer += 1 # Increase the shoot timer
        if self.shoot_timer > self.shoot_interval:
            self.shoot_timer = 0
            self.shoot_interval = randint(600, 900) # Set the shoot interval to a random number between 1s and 1.5s
            return True
        return False

    def update(self):
        self.manage_shot()
        
        if self.health <= 0: self.kill() # kill if dead
        return self.manage_shoot()
        
