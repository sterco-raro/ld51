import random
import pygame
from copy 	import deepcopy
from esper 	import Processor, set_handler, dispatch_event
from code.settings 			import *
from code.timer 			import *
from code.components.cursor import *
from code.components.map 	import *
from code.systems.rendering import *


# -------------------------------------------------------------------------------------------------


class MouseInputHandler(Processor):
	"""Cursor movement, pipes selection and placement, ..."""

	def __init__(self, scene_name, cursor_entity):
		self.scene_name = scene_name
		self.cursor_entity = cursor_entity

		# Component references
		self.cursor 	= None	# Cursor
		self.rendering 	= None	# MenuRendering
		self.deck 		= None	# Deck
		self.grid 		= None	# PipeMap

		# Currently selected entity
		self.selected_id		= -1
		self.selected_sprite 	= None

		# Actions cooldown
		self.actions_cooldown = Timer( duration = 200 )

		# Event handlers
		set_handler("reset_deck_hand", self.on_reset_deck_hand)
		set_handler( "healthcheck_error", self.on_healthcheck_error )

	def _clear_selection(self):
		self.selected_id = -1
		if self.selected_sprite:
			self.selected_sprite.selected = False
		self.selected_sprite = None

	def _fill_selection(self, entity, sprite):
		self.selected_id = entity
		self.selected_sprite = sprite

	def on_reset_deck_hand(self):
		if self.deck:
			self.deck.reset(self.world)
		self._clear_selection()

	def on_healthcheck_error(self, grid_position, direction_from):
		entity = self.world.create_entity()

		x = (grid_position[1] * TILE_SIZE + self.grid.offset_x + TILE_SIZE) - TILE_SIZE//2
		y = (grid_position[0] * TILE_SIZE + self.grid.offset_y + TILE_SIZE) - TILE_SIZE//2

		# rotate sprite following @direction_from
		angle = None
		if direction_from == "up": angle = 0.0
		if direction_from == "right": angle = -90.0
		if direction_from == "down": angle = -180.0
		if direction_from == "left": angle = -270.0

		animation = AnimatedSprite( duration = 1500,
									folder = "spurt",
									frames_table = { "images": [] },
									scale_size = (64, 64),
									spawn_point = (x, y),
									speed = 12,
									angle = angle )

		self.world.add_component( entity, animation )

	def handle_deck_input(self):
		"""Process user input on the deck"""
		collision = False
		mouse_left = False

		# Pipes management
		sprite = None
		for ent in self.deck.current_hand:

			sprite = self.world.component_for_entity( ent, Pipe )

			collision = sprite.rect.collidepoint( self.cursor.rect.center )
			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Mouse is colliding with the current sprite
			if not self.actions_cooldown.active and collision:

				# Mouse action: select
				if mouse_left:

					# Clicking on the previously selected sprite
					if self.selected_id == ent:
						self._clear_selection()

					# Clicking on another sprite
					else:

						# Swap selected sprites
						if self.selected_id != -1:

							# Swap between grid and deck
							if not self.selected_id in self.deck.current_hand:

								old_x = sprite.rect.x
								old_y = sprite.rect.y

								# Store new grid value
								self.grid.set( self.selected_sprite.rect.center, sprite.pipe_id )
								# Update sprite position
								sprite.rect.x = self.selected_sprite.rect.x
								sprite.rect.y = self.selected_sprite.rect.y
								# Clear deck slot
								self.deck.remove( ent )

								# Store new deck value (and update sprite position)
								self.deck.insert( self.selected_id, self.cursor.rect.center )
								self.selected_sprite.rect.x = old_x
								self.selected_sprite.rect.y = old_y

							# Swap inside the deck
							else:
								self.deck.swap( self.world,
												self.selected_id,
												self.cursor.rect.center,
												self.selected_sprite )

							dispatch_event( "on_play_sound", "pipe_drop" )

							self._clear_selection()

						# Select new sprite
						else:
							dispatch_event( "on_play_sound", "pipe_pick" )
							sprite.selected = True
							self._fill_selection( ent, sprite )

					# Avoid multiple clicks
					self.actions_cooldown.activate()

		# Buttons management
		for ent, (button, item) in self.world.get_components( UiButtonStates, UiItem ):

			collision = item.rect.collidepoint( self.cursor.rect.center )
			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Check button state for hovering effect
			if (not button.hovering and collision) or (button.hovering and not collision):
				button.hovering = not button.hovering

			# Activate item callback
			if not self.actions_cooldown.active and (collision and mouse_left):
				dispatch_event( "on_play_sound", "button_downup" )
				button.pressed = True
				item.callback()
				self._clear_selection()
				self.actions_cooldown.activate()
			elif not self.actions_cooldown.active and (not collision or not mouse_left):
				button.pressed = False


		# Mouse action: put selected item in inventory
		if not self.actions_cooldown.active:

			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Skip non interactable deck areas
			if not self.deck.interactable_area.collidepoint( self.cursor.rect.center ): return

			# Add sprite to inventory
			if mouse_left and self.selected_id != -1:

				# Clear old deck position
				if self.selected_id in self.deck.current_hand:
					self.deck.remove( self.selected_id )

				# Clear old grid position
				else:
					self.grid.set( self.selected_sprite.rect.center, "-1" )

				# Update deck
				self.deck.insert( 	self.selected_id,
									self.cursor.rect.center,
									self.selected_sprite )

				dispatch_event( "on_play_sound", "pipe_drop" )

				self._clear_selection()
				self.actions_cooldown.activate()

	def handle_grid_input(self):
		"""Process user input on the grid"""
		collision = False
		mouse_left = False
		mouse_right = False

		for ent, sprite in self.world.get_component( Pipe ):

			# Mouse buttons state
			collision = sprite.rect.collidepoint( self.cursor.rect.center )
			mouse_left, _, mouse_right = pygame.mouse.get_pressed()

			# Skip input/output sprites
			if sprite.fixed: continue

			# Mouse is colliding with the current sprite
			if not self.actions_cooldown.active and collision:

				# Mouse action: select
				if mouse_left:

					# Clicking on the previously selected sprite
					if self.selected_id == ent:
						self._clear_selection()

					# Clicking on another sprite
					else:

						# Swap selected sprites
						if self.selected_id != -1:

							# Swap between grid and deck
							if self.selected_id in self.deck.current_hand:

								old_center = self.selected_sprite.rect.center

								self.grid.set( self.cursor.rect.center, self.selected_sprite.pipe_id )
								self.selected_sprite.rect.x = sprite.rect.x
								self.selected_sprite.rect.y = sprite.rect.y

								self.deck.remove( self.selected_id )
								self.deck.insert( ent, old_center, sprite )
								sprite.rect.center = old_center

							# Swap inside the grid
							else:
								self.grid.swap( self.selected_sprite.rect.center,
												self.cursor.rect.center,
												self.selected_sprite.pipe_id )
								x = sprite.rect.x
								y = sprite.rect.y
								sprite.rect.x = self.selected_sprite.rect.x
								sprite.rect.y = self.selected_sprite.rect.y
								self.selected_sprite.rect.x = x
								self.selected_sprite.rect.y = y

							dispatch_event( "on_play_sound", "pipe_plop" )

							self._clear_selection()

						# Select new sprite
						else:
							dispatch_event( "on_play_sound", "pipe_pick" )
							sprite.selected = True
							self._fill_selection( ent, sprite )

					# Avoid multiple clicks
					self.actions_cooldown.activate()

				# Mouse action: rotate
				if mouse_right:
					dispatch_event( "on_play_sound", "pipe_rotate" )
					sprite.rotate()
					self.grid.set( self.cursor.rect.center, sprite.pipe_id )
					self._clear_selection()
					self.actions_cooldown.activate()

		# Mouse action: place selected item from deck
		if not self.actions_cooldown.active:

			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Skip non interactable grid areas
			if not self.grid.interactable_area.collidepoint( self.cursor.rect.center ): return

			# Skip already filled grid positions
			if self.grid.get( self.cursor.rect.center ) != "-1": return

			# Fill position with selected item
			if mouse_left and self.selected_id != -1:

				# Skip fixed pipes
				if self.selected_sprite.fixed: return

				# Update grid
				self.grid.set( self.selected_sprite.rect.center, "-1" )
				self.grid.set( self.cursor.rect.center, self.selected_sprite.pipe_id )
				# Update sprite position (grid-aligned)
				self.selected_sprite.rect.x = self.cursor.rect.centerx // TILE_SIZE * TILE_SIZE
				self.selected_sprite.rect.y = self.cursor.rect.centery // TILE_SIZE * TILE_SIZE

				# Remove selection from deck
				self.deck.remove( self.selected_id )

				dispatch_event( "on_play_sound", "pipe_plop" )

				# Reset selection
				self._clear_selection()
				self.actions_cooldown.activate()

	def process(self):
		if not self.cursor:
			self.cursor = self.world.component_for_entity( self.cursor_entity, Cursor )

		if not self.rendering:
			self.rendering = self.world.get_processor( Rendering )

		if not self.deck:
			self.deck = self.world.get_component( Deck )[0][1]

		if not self.grid:
			self.grid = self.world.get_component( PipeMap )[0][1]

		# Update cooldowns
		self.actions_cooldown.update()

		# Update cursor position
		self.cursor.rect.center = pygame.mouse.get_pos()

		# Handle deck input
		if self.deck.area.collidepoint( self.cursor.rect.center ):
			self.handle_deck_input()

		# Handle grid input
		elif self.grid.area.collidepoint( self.cursor.rect.center ):
			self.handle_grid_input()
