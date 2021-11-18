import pygame

from settings import *

class EnemyShot(pygame.sprite.Sprite):
	def __init__(self, pos, shot_dir):
		super().__init__()
		# Set the image
		self.image = pygame.Surface((tile_size/3, tile_size/4))
		self.image.fill('Red')
		# Get the rect
		self.rect = self.image.get_rect(center = pos)
		# Moving variables
		self.shot_dir = shot_dir
		self.speed = 11

	def check_outside(self):
		canvas = (0, 0, screen_width, screen_height) # Make a canvas rect
		if not self.rect.colliderect(canvas): self.kill() # Kill self if not inside canvas

	def update(self, level_scroll):
		self.check_outside() # Check if self is outside

		self.rect.x += level_scroll # scroll self
		self.rect.x += self.shot_dir * self.speed # Move self