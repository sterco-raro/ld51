from esper import Processor
from code.settings import *
from code.components.sprite import AnimatedSprite


# -------------------------------------------------------------------------------------------------


class AnimationController(Processor):
	"""Update all AnimatedSprite components"""

	def process(self):
		# Animations completed during the current frame
		completed_animations = []

		# Update all animations
		for ent, animation in self.world.get_component(AnimatedSprite):

			animation.update(FIXED_DELTA_TIME)

			# The current animation needs to be deleted
			if animation.completed:
				completed_animations.append(ent)

		# Delete all completed animations
		for entity in completed_animations:
			self.world.delete_entity(entity)
