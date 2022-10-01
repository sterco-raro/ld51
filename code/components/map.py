from code.components.sprite import StaticSprite
from code.settings import *


# -------------------------------------------------------------------------------------------------


class Pipe(StaticSprite):
	"""A pipe sprite with connections"""

	def __init__(
		self,
		*,
		file_name 	= SPRITE_UNKNOWN,
		layer 		= RENDERING_LAYERS["main"],
		scale_size 	= (64, 64),
		spawn_point = (-1024, -1024),
		debug_color = MAP_TILE_DEBUG_COLOR,
		left = True, right = True, up = False, down = False,
		leftMale = False, rightMale = True, upMale = False, downMale = False,
		fixed = False
	):
		super().__init__(
			file_name 	= file_name,
			layer 		= layer,
			scale_size 	= scale_size,
			spawn_point = spawn_point,
			debug_color = debug_color
		)
		self.left 		= left
		self.leftMale 	= leftMale
		self.right 		= right
		self.rightMale	= rightMale
		self.up 		= up
		self.upMale		= upMale
		self.down		= down
		self.downMale	= downMale

		# Pipe state
		self.fixed = fixed
		self.selected = False

		# Copy of the original surface as a reference for transforms
		self.original = self.image
		self.angle = 0.0

	def rotate(self):
		self.angle += 90.0
		if self.angle >= 360.0:
			self.angle = 0.0
		self.image = pygame.transform.rotate( self.original, self.angle )


# -------------------------------------------------------------------------------------------------


class PipeMap:
	"""Pipe system map"""

	def __init__(self, width, height, offset_x, offset_y, tileset):
		self.map_width 	= width
		self.map_height = height
		self.tileset 	= tileset
		self.offset_x 	= offset_x
		self.offset_y 	= offset_y

		# Pixel dimensions
		self.world_width 	= self.map_width * TILE_SIZE
		self.world_height 	= self.map_height * TILE_SIZE

		# Map data
		self.level = []

		self.reset()

	def reset(self):
		self.level = []
		for row in range(self.map_height):
			self.level.append([])
			for col in range(self.map_width):
				self.level[row].append("-1")

	def get_at(self, row, col):
		if col < 0 or col > self.map_width: return
		if row < 0 or row > self.map_height: return

		return self.level[row][col]
