import pygame

from settings import *
from math import ceil

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keys import *
class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.state = 'normal' # NEEDS to be before we set the image
		# Make the image
		self.set_image('idle', 0, 0)
		# Make the rect
		self.rect = self.image.get_rect(topleft = pos)
		# Key down events
		self.right_pressed = self.left_pressed = False
		self.jump_pressed = False
		self.shoot_pressed = False
		# Current direction
		self.direction = pygame.Vector2((0, 0))
		self.facing = pygame.Vector2((0, 0))
		# Jumping variables
		self.jumping = False
		self.jumped = False # If the current airtime was a jump
		self.jump_timer = 0
		# Shooting variables
		self.can_shoot = True
		self.shoot_timer = 0
		# The player's health
		self.health = 10
		# Shot variables
		self.shot = False
		self.faced_when_shot = 0
		self.shot_dir = 0
		self.invincible_timer = 0
		self.health_after_shot = 0
		self.anim_frame = 1
		self.launch_dir = 0
		# Sound variables
		self.jump_sound = pygame.mixer.Sound('audio/jump.wav') # Load a jump sound
		self.gun_shot_sound = pygame.mixer.Sound('audio/gun_shot.wav') # Load a shot sound
		self.gun_shot_sound.set_volume(0.1)

	def set_image(self, animation_name, anim_frame, flip):
		anim_frame = ceil(anim_frame) # Round up the animation frame

		if animation_name == 'idle':
			if self.state == 'invincible': # If we're invincible
				image = f'assets/player_invincible{anim_frame}.png' # Load our invincible image
			else: image = 'assets/player.png'# Else load our normal image

			self.image = pygame.image.load(image).convert_alpha() # Use our image from the image variable

		elif animation_name == 'running': 
			if self.state == 'invincible': # If we're invincible
				image = f'assets/player_running{anim_frame}_invincible.png' # Load the current anim frame running as invincible
			else: image = f'assets/player_running{anim_frame}.png' # Else load it normally

			self.image = pygame.image.load(image).convert_alpha() # Use our image from the image variable
			self.image = pygame.transform.flip(self.image, flip, False) # Flip the image if necessary

		elif animation_name == 'punched':
			self.image = pygame.image.load('assets/player_punched.png') # Load the player punched image
			self.image = pygame.transform.flip(self.image, ceil(-flip), False) # Flip the image if necessary

		else: print(animation_name)
		

		self.image = pygame.transform.scale(self.image, (tile_size, tile_size-2)) # Scale our image to the tile size-1

	def get_pressed(self):
		keys = pygame.key.get_pressed() # Get all of the pressed keys

		# Set all of the variables based on the pressed keys
		self.right_pressed = keys[RIGHT]
		self.left_pressed = keys[LEFT]

		self.jump_pressed = keys[JUMP]

		self.shoot_pressed = keys[SHOOT]

	def set_dir(self):
		if self.right_pressed: # If we're pressing right
			self.set_image('running', self.anim_frame, False) # Display the animation frame
			self.direction.x += 1.5 # Set the direction (it is actually the speed but oh well)
			self.facing.x = 1 # Set the direction the player is facing in

		if self.left_pressed: # If we're pressing left
			self.set_image('running', self.anim_frame, True) # Display the animte frame
			self.direction.x -= 1.5 # Set the direction (it is actually the speed but oh well)
			self.facing.x = -1 # Set the direction the player is facing in

		if not (self.left_pressed or self.right_pressed): # If we're not pressing a directional key
			self.set_image('idle',self.anim_frame, 0) # Set the image to idle 

		if self.jump_pressed and self.state != 'punched': # If we're pressing space and we were just not punched
			# The 'not self.jumping' needs to be there because the player jumps in an arc, which means:
			# While the player is jumping, the direction y is gonna be 0 without hitting something
			if not self.jumping and self.direction.y == 0: # If we're standing still (y) and not in a jump (see line 93)
				self.direction.y = -14 # Set the player's jumping velocity
				# Set the jumping variables
				self.jumping = True
				self.jumped = True # Indicates that the current airtime was a jump not a fall

				self.jump_sound.play() # Play our happy little jump sound

			elif self.jumped and self.jump_timer < 4 and self.direction.y < 0: # If we're in the first few frames of a jump
				# Increase the y velocity
				self.direction.y -= 4.6
				self.jump_timer += 1 # Frame control

		self.direction.y += 2.8 # Gravity

	def update_x(self, scrollable, outside):
		level_scroll = 0
		# Check if the level is scrollable
		if scrollable:
			# If the level is scrollable
			# Check if the player is near an edge and if he's moving towards it
			if self.rect.right >= screen_width * 0.65 and self.direction.x > 0 and outside[1]:
				level_scroll = -round(self.direction.x)
			elif self.rect.left <= screen_width * 0.35 and self.direction.x < 0 and outside[0]:
				level_scroll = -round(self.direction.x)
			else:
				self.rect.x += round(self.direction.x) # Increase our current position by a round number
		else:
			# If not just do the default
			self.rect.x += round(self.direction.x) # Increase our current position by a round number

		if self.state == 'punched': # If we were just punched
			self.rect.x += (7 - self.invincible_timer / 3) * self.shot_dir # Move the player back in a smooth punch animation

		# friction
		self.direction.x *= 0.8

		return level_scroll

	def update_y(self):
		self.rect.y += self.direction.y # Move on the y axis

	def max_y_vel(self):
		if self.direction.y > tile_size - 1: self.direction.y = tile_size - 1 # Make sure we never fall faster than the tile size
		# This makes it so that we can't clip through blocks
	
	def shoot(self):
		if not self.can_shoot: # If we can't shoot
			self.shoot_timer += 1 # Increase the timer

			if self.shoot_timer > 5: # If the timer's over 5
				self.can_shoot = True # Make us able to shoot
				self.shoot_timer = 0 # Reset the timer
		
		# If we can shoot and we're holding down shoot
		# If we were just not punched
		# OBSERVATE, DON'T CHANGE THE 25 FOR SOMETHING LOWER, THE PLAYER IS FACING THE WRONG WAY
		elif self.can_shoot and self.shoot_pressed and (self.invincible_timer == 0 or self.invincible_timer >= 25):
			self.can_shoot = False # Make it so that we can't shoot

			self.gun_shot_sound.play() # Play our gun shot sound
			return True # (Meaning we shoot)

		return False # (Meaning we didn't shoot)

	def handle_shot(self):
		if self.shot: # If we are in shot stage (meaning we were just shot)

			self.invincible_timer += 1 # Increase our invincible timer
			self.health = self.health_after_shot # Make sure we are invincible (meaning we can't loose a life)

			if self.invincible_timer <= 20: # If we're still being punched
				
				self.set_image('punched', self.anim_frame, self.launch_dir) # Set our animation

				self.direction.x = 0 # Make sure we can't run anywhere
				self.facing.x = self.shot_dir # And make sure we don't change our direction

				self.state = 'punched' # Set our state

				# This all makes it feel like you have really lost control of the player

			elif self.invincible_timer > 20 and self.invincible_timer <= 21: # Right when we can move
				self.facing.x = self.faced_when_shot # Set our direction
				self.state = 'invincible' # Set our state

			if self.invincible_timer > 60: # When we're done
				self.state = 'normal'
				# Reset everything
				self.shot = False
				self.invincible_timer = 0
				self.faced_when_shot = 0
				self.health_after_shot = 0

	def check_inside_bounds_x(self):
		if self.rect.right > screen_width: self.rect.right = screen_width
		if self.rect.left < 0: self.rect.left = 0

	def update(self):
		# Call all of the functions
		self.get_pressed()
		self.set_dir()
		self.max_y_vel()
		self.handle_shot()
		self.check_inside_bounds_x()

		# Increase our current animation frame
		self.anim_frame += 0.2
		if self.anim_frame > 2:
			self.anim_frame = 0.2

		return self.shoot() # Return if we shot
