import pygame

from settings import *

class Block(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		# Set the image
		self.image = pygame.Surface((tile_size, tile_size))
		self.image.fill('Black')
		# Get the rect
		self.rect = self.image.get_rect(topleft = pos)
	
	def update(self, level_scroll):
		self.rect.x += level_scroll