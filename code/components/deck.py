import random
from code.settings import *
from code.components.map import *


# -------------------------------------------------------------------------------------------------


class Deck:
	"""Deck area"""

	def __init__(self, width, height, offset_x, offset_y):
		self.deck_width 	= width
		self.deck_height 	= height
		self.offset_x 		= offset_x
		self.offset_y 		= offset_y

		# Pixel dimensions
		self.width 			= self.deck_width * TILE_SIZE
		self.height 		= self.deck_height * TILE_SIZE
		self.padding 		= TILE_SIZE

		self.current_hand = [] 	# Current cards entities
		self.hand_length = 5 	# How many cards are shown with a new hand

	def reset(self, world):

		# Remove old entities before resetting the current hand
		for card in self.current_hand:
			world.delete_entity( card )

		# Reset cards hand
		self.current_hand = []

		# Create @hand_length random cards entities
		pipe = -1
		height = 0
		choice = 0
		data = None
		spawn_point = None
		keys = list( PIPES.keys() )
		for i in range(self.hand_length):

			pipe = world.create_entity()

			choice = random.choice(keys)
			while choice == "0" or choice == "1":
				choice = random.choice(keys)
			data = PIPES[choice]

			height = TILE_SIZE * (i + 1)
			spawn_point = ( self.offset_x + self.padding * 2,
							self.offset_y + height + self.padding )

			sprite = Pipe( 	file_name = data["sprite"],
							spawn_point = spawn_point,
							left = data["left"],
							right = data["right"],
							up = data["up"],
							down = data["down"],
							fixed = data["fixed"] )

			world.add_component( pipe, sprite )
			self.current_hand.append( pipe )

