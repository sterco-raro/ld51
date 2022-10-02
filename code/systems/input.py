import random
import pygame # TODO Only import necessary variables/functions/classes
from copy 	import deepcopy
from esper 	import Processor, set_handler
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
		self.selected_from_deck = False

		# Actions cooldown
		self.actions_cooldown = Timer( duration = 100 )

		# Event handlers
		set_handler("reset_deck_hand", self.on_reset_deck_hand)

	def _clear_selection(self):
		self.selected_id = -1
		self.selected_sprite = None
		self.selected_from_deck = False

	def _fill_selection(self, entity, sprite, from_deck = False):
		self.selected_id = entity
		self.selected_sprite = sprite
		self.selected_from_deck = from_deck

	def on_reset_deck_hand(self):
		if self.deck:
			self.deck.reset(self.world)
		self._clear_selection()

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

						# Deselect old sprite
						sprite.selected = False
						self._clear_selection()

					# Clicking on another sprite
					else:
						# Deselect old sprite
						if self.selected_id != -1:
							self.selected_sprite.selected = False

						# Select new sprite
						sprite.selected = True
						self._fill_selection( ent, sprite, True )

					self.actions_cooldown.activate()

		# Buttons management
		for ent, (button, item) in self.world.get_components( UiButton, UiItem ):

			collision = item.rect.collidepoint( self.cursor.rect.center )
			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Check button state for hovering effect (only on basic fill-buttons)
			if (
				# Should this button be enabled?
				self.selected_from_deck				and
				# Toggle hovering only one time: when the mouse enters or exits the button rectangle
				not button.image 					and
				(not button.hovering and collision) or
				(button.hovering and not collision)
			):
				button.hovering = not button.hovering

			# Activate item callback
			if (
				not self.actions_cooldown.active 					and
				(collision and mouse_left)							and
				(self.selected_from_deck and self.selected_id != -1)
			):
				item.callback()
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

						# Deselect old sprite
						sprite.selected = False
						self._clear_selection()

					# Clicking on another sprite
					else:

						# Deselect old sprite
						if self.selected_id != -1:
							self.selected_sprite.selected = False

						# Select new sprite
						sprite.selected = True
						self._fill_selection( ent, sprite, False )

					self.actions_cooldown.activate()

				# Mouse action: rotate
				if mouse_right:
					sprite.rotate()
					if self.selected_sprite:
						self.selected_sprite.selected = False
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
			if mouse_left and (self.selected_from_deck and self.selected_id != -1):
				# Get selected sprite
				sprite = self.world.component_for_entity( self.selected_id, Pipe )

				# Skip fixed pipes
				if sprite.fixed: return

				# Update grid
				self.grid.set( self.cursor.rect.center, sprite.pipe_id )
				# Update sprite position (grid-aligned)
				sprite.rect.x = self.cursor.rect.centerx // TILE_SIZE * TILE_SIZE
				sprite.rect.y = self.cursor.rect.centery // TILE_SIZE * TILE_SIZE

				# Remove selection from deck
				self.deck.remove( self.selected_id )

				# Reset selection
				sprite.selected = False
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
