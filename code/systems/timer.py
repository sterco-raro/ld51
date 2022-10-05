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
		self.cooldown = Timer( 2000 )

		# Matrix used as map for already visited locations during the 10s routine check
		self.navigation_map = []

	def _reset_navigation_map(self):
		if not self.grid: return

		self.navigation_map = []

		for row in range(self.grid.map_height):
			self.navigation_map.append([])
			for col in range(self.grid.map_width):
				self.navigation_map[row].append(False)

	def _failure(self, grid_pos, direction_from, value):
		dispatch_event( "on_play_sound", "fart", 2 )
		dispatch_event( "healthcheck_error", grid_pos, direction_from )
		return "failure"




	# TODO
	# TODO Avoid spawning the same sound more than once
	# TODO Multiple AnimatedSprite on the same tile
	# TODO Avoid flushing sound when system is connected correctly
	# TODO





	def _healthcheck(self, grid_pos, direction_from):

		# Get current grid value
		value = self.grid._get_at( grid_pos[1], grid_pos[0] )

		# Location already visited: loop detected
		if self.navigation_map[grid_pos[1]][grid_pos[0]]:
			print("LOOP DETECTED")
			return "failure"

		# New location
		self.navigation_map[grid_pos[1]][grid_pos[0]] = True

		# Missing pipe: failure
		if value is None or value == "-1":
			return self._failure( grid_pos, direction_from, value )

		# Output pipe: success
		if value == PIPE_OUTPUT:
			return "success"

		# Check if there's a connection with the direction we're coming from
		if (
			(direction_from == "left" 	and not PIPES[value]["right"]) 	or
			(direction_from == "up" 	and not PIPES[value]["down"]) 	or
			(direction_from == "right" 	and not PIPES[value]["left"]) 	or
			(direction_from == "down" 	and not PIPES[value]["up"])
		):
			print("missing connection")
			return self._failure( grid_pos, direction_from, value )

		# Check next links
		if direction_from != "left" and PIPES[value]["right"]:
			return self._healthcheck( (grid_pos[0], grid_pos[1] + 1), "right" )

		if direction_from != "up" and PIPES[value]["down"]:
			return self._healthcheck( (grid_pos[0] + 1, grid_pos[1]), "down" )

		if direction_from != "right" and PIPES[value]["left"]:
			return self._healthcheck( (grid_pos[0], grid_pos[1] - 1), "left" )

		if direction_from != "down" and PIPES[value]["up"]:
			return self._healthcheck( (grid_pos[0] - 1, grid_pos[1]), "up" )

	def grid_healthcheck(self):
		error = False
		if len(self.grid.active_inputs) > 0:
			# For each currently active input pipe
			for i in range(len(self.grid.active_inputs)):
				# Clean navigation map
				self._reset_navigation_map()
				# Run system healthcheck
				status = self._healthcheck( (self.grid.active_inputs[i][0] + 1, self.grid.active_inputs[i][1]), "down" )
				if status == "failure":
					error = True
		return error

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
		if self.timer.value >= 5: # TODO CHANGEME BACK TO 10
			self.cooldown.activate()
			dispatch_event( "on_play_sound", "rattleflush" )
			if not self.grid_healthcheck():
				dispatch_event( "on_play_sound", "snap" )

		# Update timers
		self.timer.update()
		self.cooldown.update()

		# Keep the timer inactive while the cooldown is still running
		if not self.cooldown.active:
			if not self.timer.active:
				dispatch_event( "on_play_sound", "weird" )
				self.prepare_flush()
				self.timer.activate()
