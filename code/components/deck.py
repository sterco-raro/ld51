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
		self.padding_outer	= 22
		self.padding_inner	= 20

		# Sections rectangles for rendering and input purposes
		self.area = pygame.Rect( self.offset_x, self.offset_y, self.width, self.height )
		self.interactable_area = self.area

		self.current_hand = [] 	# Current cards entities
		self.hand_length = 10 	# How many cards are shown with a new hand
		self.card_slots = [] 	# Fixed cards position

	def _draw_random_hand(self, world, quantity):
		pipe = -1
		height = 0
		choice = 0
		data = None
		spawn_point = None
		keys = list( PIPES.keys() )

		for i in range(self.hand_length):

			pipe = world.create_entity()

			# TODO weighted chances instead of random choice
			choice = random.choice(keys)
			while choice == "0" or choice == "1":
				choice = random.choice(keys)
			data = PIPES[choice]

			sprite = Pipe( 	file_name = data["sprite"],
							pipe_id = data["id"],
							left = data["left"],
							right = data["right"],
							up = data["up"],
							down = data["down"],
							fixed = data["fixed"] )
			sprite.rect.x = self.card_slots[i][0]
			sprite.rect.y = self.card_slots[i][1]

			world.add_component( pipe, sprite )
			self.current_hand.append( pipe )

	def reset(self, world):

		# Remove old entities before resetting the current hand
		for card in self.current_hand:
			world.delete_entity( card )

		# Reset cards hand
		self.current_hand = []

		# Create card slots when missing
		if len(self.card_slots) < 10:
			self.card_slots = []

			first_col_x = self.offset_x + self.padding_outer
			second_col_x = first_col_x + TILE_SIZE + self.padding_inner
			base_row_y = self.offset_y + self.padding_outer
			for i in range(10):
				if i < 5:
					height = (i + 1) * TILE_SIZE + (i + 1) * self.padding_inner
					self.card_slots.append( ( first_col_x, base_row_y + height ) )
				else:
					height = (i + 1 - 5) * TILE_SIZE + (i + 1 - 5) * self.padding_inner
					self.card_slots.append( ( second_col_x, base_row_y + height ) )

		# Create @hand_length random cards entities
		self._draw_random_hand(world, self.hand_length)

	def remove(self, entity):
		if entity in self.current_hand:
			self.current_hand.remove( entity )
