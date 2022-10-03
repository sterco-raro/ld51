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
		pipe_id 	= PIPE_VERTICAL,
		left = True, right = True, up = False, down = False,
		fixed = False
	):
		super().__init__(
			file_name 	= file_name,
			layer 		= layer,
			scale_size 	= scale_size,
			spawn_point = spawn_point,
			debug_color = debug_color
		)
		self.pipe_id 	= pipe_id
		self.left 		= left
		self.right 		= right
		self.up 		= up
		self.down		= down

		# Pipe state
		self.fixed = fixed
		self.selected = False

		# Copy of the original surface as a reference for transforms
		self.original = self.image
		self.angle = 0.0

	def rotate(self):
		self.angle -= 90.0
		if self.angle <= -360.0:
			self.angle = 0.0
		self.image = pygame.transform.rotate( self.original, self.angle )
		# Update connections
		left 	= False
		up 		= False
		right 	= False
		down 	= False
		if self.left: 	up 		= True
		if self.up: 	right 	= True
		if self.right:	down 	= True
		if self.down: 	left 	= True
		self.left 	= left
		self.up 	= up
		self.right 	= right
		self.down 	= down


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
		self.width 	= self.map_width * TILE_SIZE
		self.height = self.map_height * TILE_SIZE

		# Sections rectangles for rendering and input purposes
		self.area = pygame.Rect( 0, 0, self.width, self.height )
		self.interactable_area = pygame.Rect( 	self.offset_x + TILE_SIZE,
												self.offset_y + TILE_SIZE,
												self.width - 2 * TILE_SIZE,
												self.height - 2 * TILE_SIZE )

		# Map data
		self.level 			= []
		self.inputs			= []
		self.active_inputs 	= []
		self.outputs 		= []

		self.reset()

	def reset(self):
		self.level 			= []
		self.inputs			= []
		self.active_inputs 	= []
		self.outputs 		= []
		for row in range(self.map_height):
			self.level.append([])
			for col in range(self.map_width):
				self.level[row].append("-1")

	def _get_at(self, row, col):
		if col < 0 or col > self.map_width: return
		if row < 0 or row > self.map_height: return

		return self.level[col][row]

	def _set_at(self, row, col, value):
		if col < 0 or col > self.map_width: return
		if row < 0 or row > self.map_height: return

		self.level[col][row] = value

	def get(self, pos):
		row = pos[0] // TILE_SIZE - self.offset_x // TILE_SIZE
		col = pos[1] // TILE_SIZE - self.offset_y // TILE_SIZE
		return self._get_at(row, col)

	def set(self, pos, value):
		row = pos[0] // TILE_SIZE - self.offset_x // TILE_SIZE
		col = pos[1] // TILE_SIZE - self.offset_y // TILE_SIZE
		self._set_at(row, col, value)

	def swap(self, old_pos, new_pos, value):
		old_value = self.get( new_pos )
		self.set( old_pos, old_value )
		self.set( new_pos, value )
