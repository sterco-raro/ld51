import random
import pygame # TODO Only import necessary variables/functions/classes
from copy 	import deepcopy
from esper 	import Processor
from code.settings 			import *
from code.timer 			import *
from code.components.cursor import *
from code.components.map 	import *
from code.systems.rendering import *


# -------------------------------------------------------------------------------------------------


class MouseInputHandler(Processor):
	"""Cursor movement, pipes selection and placement, ..."""

	def __init__(self, scene_name, cursor_entity, deck_area, grid_area):
		self.scene_name = scene_name
		self.cursor_entity = cursor_entity
		self.deck_area = deck_area
		self.grid_area = grid_area

		# Mouse Cursor component
		self.cursor = None
		# MenuRendering system
		self.rendering = None

		# Currently selected entity
		self.selected = -1

		# Actions cooldown
		self.actions_cooldown = Timer( duration = 100 )

	def handle_deck_input(self):
		"""Process user input on the deck"""
		collision = False
		mouse_left = False
		for ent, (button, item) in self.world.get_components( UiButton, UiItem ):

			collision = item.rect.collidepoint( self.cursor.rect.center )
			mouse_left, _, __ = pygame.mouse.get_pressed()

			# Check button state for hovering effect (only on basic fill-buttons)
			if (
				not button.image 					and
				(not button.hovering and collision) or
				(button.hovering and not collision)
			):
				button.hovering = not button.hovering

			if not self.actions_cooldown.active and collision and mouse_left:
				item.callback()
				self.actions_cooldown.activate()

	def handle_grid_input(self):
		"""Process user input on the grid"""
		mouse_left = False
		mouse_right = False
		for ent, sprite in self.world.get_component( Pipe ):

			# Mouse buttons state
			mouse_left, _, mouse_right = pygame.mouse.get_pressed()

			# Skip input/output sprites
			if sprite.fixed: continue

			# Mouse is colliding with the current sprite
			if not self.actions_cooldown.active and sprite.rect.collidepoint( self.cursor.rect.center ):
				# Mouse action: select
				if mouse_left and (self.selected == -1 or self.selected == ent):
					sprite.selected = not sprite.selected
					self.selected = ent if sprite.selected else -1
					self.actions_cooldown.activate()

				# Mouse action: rotate
				if mouse_right:
					sprite.rotate()
					self.actions_cooldown.activate()

	def process(self):
		# Get the MenuRendering reference
		if not self.rendering:
			self.rendering = self.world.get_processor( Rendering )
		# Get the cursor component
		if not self.cursor:
			self.cursor = self.world.component_for_entity( self.cursor_entity, Cursor )

		# Update cooldowns
		self.actions_cooldown.update()

		# Update cursor position
		self.cursor.rect.center = pygame.mouse.get_pos()

		# Handle deck input
		if self.deck_area.collidepoint( self.cursor.rect.center ):
			self.handle_deck_input()

		# Handle grid input
		elif self.grid_area.collidepoint( self.cursor.rect.center ):
			self.handle_grid_input()
