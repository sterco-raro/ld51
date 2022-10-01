import pygame
from esper import Processor, set_handler
from code.components.cursor import *
from code.components.deck 	import *
from code.components.map 	import *
from code.components.sprite import *
from code.components.ui import *
from code.settings import *


# -------------------------------------------------------------------------------------------------


class Rendering(Processor):
	"""A simple renderer"""

	def __init__(self, scene_name, world_width, world_height):
		# World identifier
		self.scene_name = scene_name
		# Get a reference to the active display
		self.screen 		= pygame.display.get_surface()
		self.screen_size	= self.screen.get_size()

		# Pygame font
		self.font_size 	= TILE_SIZE
		self.font 		= pygame.font.SysFont(None, self.font_size)

		# Black surface to clear the screen
		self.background = pygame.Surface( (world_width, world_height) ).convert()
		self.background.fill((0, 0, 0))
		# Working canvas for sprite rendering
		self.canvas = pygame.Surface( (world_width, world_height) ).convert()
		# Working canvas for the grid area
		self.map_canvas = None
		# Working canvas for the deck area
		self.deck_canvas = None

		# Component references
		self.cursor 	= None
		self.timer 		= None
		self.tilemap 	= None
		self.deck 		= None

		# Flags
		self.debug 		= False # Activate debug rectangles (sprite, hitbox)
		self.redraw_map = True 	# Update the working canvas

		# Event handlers
		set_handler( "scene_change", self.on_scene_change )
		set_handler( "toggle_debug", self.on_toggle_debug )

	def on_scene_change(self, name):
		"""Notify the need to update this menu UI"""
		if name == self.scene_name: self.redraw_map = True

	def on_toggle_debug(self, value):
		"""Toggle debug routines"""
		self.debug = value
		self.redraw_map = True

	def process(self):
		# Get cursor component
		if not self.cursor:
			self.cursor = self.world.get_component(Cursor)[0][1]
		# Get map component
		if not self.tilemap:
			self.tilemap = self.world.get_component(PipeMap)[0][1]
		# Get deck component
		if not self.deck:
			self.deck = self.world.get_component(Deck)[0][1]
		# Get timer component
		if not self.timer:
			self.timer = self.world.get_component(Timer)[0][1]

		# Create working canvases when the dimensions are available
		if not self.map_canvas:
			self.map_canvas = pygame.Surface( (self.tilemap.world_width, self.tilemap.world_height) ).convert()
			self.map_canvas.fill((220, 40, 200))
			self.deck_canvas = pygame.Surface( (self.deck.width, self.deck.height) ).convert()
			self.deck_canvas.fill((220, 200, 40))

		# Clear the screen
		self.canvas.blit(self.background, (0, 0))

		# Clear grid background
		self.canvas.blit( 	self.map_canvas,
							(self.tilemap.offset_x, self.tilemap.offset_y),
							pygame.Rect(0, 0, self.tilemap.world_width, self.tilemap.world_height) )

		if self.debug:
			pygame.draw.rect(	self.canvas,
								(0, 0, 255),
								( 	self.tilemap.offset_x + TILE_SIZE,
									self.tilemap.offset_y + TILE_SIZE,
									self.tilemap.world_width - 2 * TILE_SIZE,
									self.tilemap.world_height - 2 * TILE_SIZE ),
								width = 5 )

		# Clear deck background
		self.canvas.blit( 	self.deck_canvas,
							(self.deck.offset_x, self.deck.offset_y),
							pygame.Rect(0, 0, self.deck.width, self.deck.height) )

		if self.debug:
			pygame.draw.rect(	self.canvas,
								(255, 0, 0),
								( 	self.deck.offset_x,
									self.deck.offset_y,
									self.deck.width,
									self.deck.height ),
								width = 5 )

		# Draw sprites
		for ent, sprite in self.world.get_component( Pipe ):
			self.canvas.blit( sprite.image, sprite.rect )
			if sprite.selected:
				pygame.draw.rect( self.canvas, (0, 255, 0), sprite.rect, width = 3 )
			elif self.debug:
				pygame.draw.rect( self.canvas, sprite.debug_color, sprite.rect, width=1 )

		# Draw UI buttons
		color = None
		for ent, button in self.world.get_component( UiButton ):
			if button.image:
				self.canvas.blit( button.image, button.rect )
			else:
				color = button.inactive_color if not button.hovering else button.active_color
				pygame.draw.rect( self.canvas, color, button.rect )

		# Draw UI text
		for ent, text in self.world.get_component( UiText ):
			self.canvas.blit( text.surface, text.rect )

		# Draw timer
		text = str(self.timer.value)
		text_size = self.font.size( text )
		text_surface = self.font.render( text, True, (255, 255, 255) )
		x = ( self.screen_size[0] - self.tilemap.world_width - TILE_SIZE ) // 2
		y = text_size[1] - text_size[1]//4
		text_rect = text_surface.get_rect( center = (x, y) )
		self.canvas.blit( text_surface, text_rect )

		# Draw mouse cursor
		self.canvas.blit( self.cursor.image, self.cursor.rect )

		# Stop map surfaces construction once done
		if self.redraw_map: self.redraw_map = False

		# Blit everything to the screen
		self.screen.blit( self.canvas, (0, 0) )
