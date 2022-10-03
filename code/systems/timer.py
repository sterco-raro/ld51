from esper 	import Processor, dispatch_event
from code.settings 			import *
from code.timer 			import *
from code.components.deck 	import *


# -------------------------------------------------------------------------------------------------


class TimerController(Processor):
	"""Game timer controller"""

	def __init__(self, scene_name, timer_entity):
		self.scene_name = scene_name
		self.timer_entity = timer_entity

		# Timer component reference
		self.timer = None

		# End timer cooldown
		self.cooldown = Timer( 1000 )

	def process(self):
		if not self.timer:
			self.timer = self.world.component_for_entity(self.timer_entity, Timer)

		# Activate a small cooldown to handle events when the timer has reached its end
		if self.timer.value >= 10:
			self.cooldown.activate()
			# TODO Launch pipe system check

		# Update timers
		self.timer.update()
		self.cooldown.update()

		# Keep the timer inactive while the cooldown is still running
		if not self.cooldown.active:
			if not self.timer.active:
				self.timer.activate()
