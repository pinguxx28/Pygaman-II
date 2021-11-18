import pygame

from settings import *

class Shot(pygame.sprite.Sprite):
	def __init__(self, pos, dir):
		super().__init__()
		# Set the image
		self.image = pygame.Surface((tile_size/3, tile_size/4))
		self.image.fill((30, 30, 30))
		# Get the rect
		self.rect = self.image.get_rect(center = pos)
		# Set the dir
		self.dir = self.set_dir(dir)
		# Shot speed
		self.speed = 12

	def set_dir(self, dir): # Set the direction
		if dir > 0: return 1
		elif dir < 0: return -1
		elif dir == 0: return 1

	def check_outside(self):
		canvas = (0, 0, screen_width, screen_height) # Make a canvas rect
		if not self.rect.colliderect(canvas): self.kill() # Kill self if not inside canvas

	def update(self, enemies):
		self.check_outside() # Call the function

		self.rect.x += self.speed * self.dir # Move the shot

		for enemy in enemies.sprites(): # Loop through all of the enemies
			if enemy.rect.colliderect(self.rect): # If colliding with enemy
				enemy.health -= 1 # Make the enemy's health go down
				enemy.shot = True # Say that the enemy is show
				self.kill() # Kill self