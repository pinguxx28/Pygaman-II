import pygame

# Import all of our sprites
from block import Block
from player import Player
from shot import Shot
from enemy import Enemy
from enemy_shot import EnemyShot

from settings import *

class Level:
	def __init__(self, screen, layout):
		self.screen = screen

		self.map_layout = layout
		self.make_level(layout) # make the level

	def make_level(self, layout):
		# Make all of the groups
		self.player = pygame.sprite.GroupSingle()
		self.shots = pygame.sprite.Group()

		self.blocks = pygame.sprite.Group()

		self.enemies = pygame.sprite.Group()
		self.enemy_shots = pygame.sprite.Group()
		
		# Add all of the sprites
		enemy_types = ('q', 'p') # All of the enemy types
		# Loop through all of the cells
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				# Make the positions
				x = col_index * tile_size
				y = row_index * tile_size

				# Add the type of sprite relative to the character of the cell
				if cell == 'X': self.blocks.add(Block((x, y)))
				elif cell == 'O': self.player.add(Player((x, y)))
				elif cell in enemy_types: self.enemies.add(Enemy((x, y), cell))

	def player_coll_x(self):
		player = self.player.sprite # Get the player

		for block in self.blocks.sprites(): # Loop through all of the blocks
			if player.rect.colliderect(block): # If the player is colliding with a block
				# Set the player's x based on the player's current direction
				if player.facing.x > 0:
					player.rect.right = block.rect.left
					player.direction.x = 0
					player.facing.x = 0
				elif player.facing.x < 0:
					player.rect.left = block.rect.right
					player.direction.x = 0
					player.facing.x = 0

	def player_coll_y(self):
		player = self.player.sprite # Get the player

		for block in self.blocks.sprites(): # Loop through all of the blocks
			if player.rect.colliderect(block): # If the player is colliding with a rectangle

				if player.direction.y > 0: # If the player is falling
					# Make the player land on the block
					player.rect.bottom = block.rect.top
					player.direction.y = 0
					player.jump_timer = 0
					player.jumping = False
					player.jumped = False

				elif player.direction.y < 0: # Else if the player is going up/jumping
					# Bomp the player's head
					player.rect.top = block.rect.bottom
					player.direction.y = 0

	def player_dead(self):
		self.make_level(self.map_layout) # Reset the game
	
	def player_in_void(self):
		if self.player.sprite.rect.top > screen_height: # check if the sprite is in the void
			self.player_dead() # Reset the game AKA you lost

	def player_shot(self):
		for enemy_shot in self.enemy_shots.sprites(): # Loop through all of the enemy shot sprites
			if enemy_shot.rect.colliderect(self.player.sprite.rect) and not self.player.sprite.shot: # If the player is colliding with an enemy shot
				self.damage_player(enemy_shot.shot_dir) 
				enemy_shot.kill() # Kill the shot

	def damage_player(self, kb_dir):
		player = self.player.sprite # Get the player sprite
		
		player.faced_when_shot = player.facing.x # Store the player's facing direction in a variable, to use later
		player.facing.x = kb_dir # Set the facing to the shot direction
		player.shot_dir = kb_dir # Set the shot_dir to the shot direction
		player.launch_dir = kb_dir + 1
		player.health -= 1 # Decrese the player's life
		player.shot = True # Yes the player was shot
		player.health_after_shot = player.health # Store the health (used to make invincibility)

	def run(self):
		# update
		#==================

		# Move and update the player
		# Check the x first then the y
		self.player.sprite.update_x()
		self.player_coll_x()
		self.player.sprite.update_y()
		self.player_coll_y()

		self.player_shot() # Check if the player is shot by one of the enemies
		self.player_in_void() # Check if the player is in the void > screen_height

		shot = self.player.sprite.update() # update the player and return the player's "can shoot status"
		if shot: self.shots.add(Shot(self.player.sprite.rect.center, self.player.sprite.facing.x)) # If the shoot button is pressed, shoot


                for enemy in self.enemies.sprites():
                    shoot = enemy.update()
                    if shoot and enemy.shooter():
                        for enemy in self.enemies.sprites(): # Loop through all of the enemies
                            if enemy.shooter(): # If the enemy is a shooter (can shoot)
				self.enemy_shots.add(EnemyShot(enemy.rect.center, enemy.facing)) # Then shoot a shot/bullet

		self.enemies.update() # Update all of the enemies

		self.shots.update(self.enemies) # Update the player shots
		self.enemy_shots.update() # Update the enemy shots

		if self.player.sprite.health <= 0: self.make_level(self.map_layout) # Check if the player's health is below or equal to 0
		#==================
		self.screen.fill('Dimgrey') # Fill the screeen black to get rid of the previous frame

		# draw all of the sprites
		#==================
		self.player.draw(self.screen)
		self.enemies.draw(self.screen)
		self.blocks.draw(self.screen)
		self.shots.draw(self.screen)
		self.enemy_shots.draw(self.screen)

		#==================
