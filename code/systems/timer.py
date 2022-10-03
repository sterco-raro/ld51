from esper 					import Processor, dispatch_event
from code.settings 			import *
from code.timer 			import *
from code.components.deck 	import *
from code.components.sprite	import *


# -------------------------------------------------------------------------------------------------


class TimerController(Processor):
	"""Game timer controller"""

	def __init__(self, scene_name, timer_entity):
		self.scene_name 	= scene_name
		self.timer_entity 	= timer_entity

		# Components references
		self.timer 	= None
		self.grid 	= None

		# End timer cooldown
		self.cooldown = Timer( 3200 )


		self.status = ""
		self.first_run = True

	def _check_error(self, pos, direction_from):
		if self.status == "error":
			dispatch_event( "on_play_sound", "fart", 2 )
			dispatch_event( "healthcheck_error", pos, direction_from )

	def _check_ok(self):
		if self.status == "error":
			dispatch_event( "on_play_sound", "snap", 1 )

	def _healthcheck(self, grid_pos, direction_from):
		value = self.grid._get_at(grid_pos[1], grid_pos[0])

		# bad value
		if not value or value == "-1":
			self.status = "error"
			return

		# good value
		if value == PIPE_OUTPUT:
			self.status = "ok"
			return

		# go left
		if direction_from != "left" and PIPES[value]["left"]:
			self._healthcheck( ( grid_pos[0], grid_pos[1] - 1 ), "left" )
			self._check_error( ( grid_pos[0], grid_pos[1] - 1 ), "left" )
			self._check_ok()
			if self.status == "error" or self.status == "ok": return
		# go up
		if direction_from != "up" and PIPES[value]["up"]:
			self._healthcheck( ( grid_pos[0] - 1, grid_pos[1] ), "up" )
			self._check_error( ( grid_pos[0] - 1, grid_pos[1] ), "up" )
			self._check_ok()
			if self.status == "error" or self.status == "ok": return
		# go right
		if direction_from != "right" and PIPES[value]["right"]:
			self._healthcheck( ( grid_pos[0], grid_pos[1] + 1 ), "right" )
			self._check_error( ( grid_pos[0], grid_pos[1] + 1 ), "right" )
			self._check_ok()
			if self.status == "error" or self.status == "ok": return
		# go down
		if direction_from != "down" and PIPES[value]["down"]:
			self._healthcheck( ( grid_pos[0] + 1, grid_pos[1] ), "down" )
			self._check_error( ( grid_pos[0] + 1, grid_pos[1] ), "down" )
			self._check_ok()
			if self.status == "error" or self.status == "ok": return

	def grid_healthcheck(self):
		if len(self.grid.active_inputs) > 0:
			# foreach active input do healthcheck(grid_pos_below)
			for i in range(len(self.grid.active_inputs)):
				self._healthcheck( ( self.grid.active_inputs[i][0] + 1, self.grid.active_inputs[i][1] ), "up" )
				self.status = ""

	def prepare_flush(self):
		# choose a rundom subset of available inputs
		random_inputs = random.randint(1, len(self.grid.inputs))
		inputs = []
		choice = None
		for i in range(random_inputs):
			choice = random.choice(self.grid.inputs)
			if choice in inputs: continue
			inputs.append( choice )
			# show visual cue
			entity = self.world.create_entity()
			x = choice[1] * TILE_SIZE + self.grid.offset_x + TILE_SIZE//2
			y = choice[0] * TILE_SIZE + self.grid.offset_y + TILE_SIZE//2
			sprite = AnimatedSprite( 	duration = 1500,
										folder = "warning",
										frames_table = { "images": [] },
										scale_size = (32, 32),
										spawn_point = (x,y),
										speed = 6 )
			self.world.add_component( entity, sprite )
		# store active inputs in the grid
		self.grid.active_inputs = inputs

	def process(self):
		if not self.timer:
			self.timer = self.world.component_for_entity( self.timer_entity, Timer )

		if not self.grid:
			self.grid = self.world.get_component( PipeMap )[0][1]

		# Activate a small cooldown to handle events when the timer has reached its end
		if self.timer.value >= 10:
			self.cooldown.activate()
			if not self.first_run:
				dispatch_event( "on_play_sound", "rattleflush" )
				self.grid_healthcheck()
			self.first_run = False

		# Update timers
		self.timer.update()
		self.cooldown.update()

		# Keep the timer inactive while the cooldown is still running
		if not self.cooldown.active:
			if not self.timer.active:
				if not self.first_run:
					dispatch_event( "on_play_sound", "weird" )
					self.prepare_flush()
				self.timer.activate()
