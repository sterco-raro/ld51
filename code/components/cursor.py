from code.settings import *
from code.components.sprite import StaticSprite


# -------------------------------------------------------------------------------------------------


class Cursor(StaticSprite):
	"""Mouse cursor"""

	def __init__(
		self,
		*,
		file_name 	= SPRITE_CURSOR,
		layer 		= RENDERING_LAYERS["main"],
		scale_size 	= (64, 64),
		spawn_point = (-1024, -1024),
		debug_color = MAP_TILE_DEBUG_COLOR
	):
		super().__init__(
			file_name 	= file_name,
			layer 		= layer,
			scale_size 	= scale_size,
			spawn_point = spawn_point,
			debug_color = debug_color
		)
