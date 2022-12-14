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
		self.card_slots = {} 	# Fixed cards position

	def _draw_random_hand(self, world, quantity):
		entity = -1
		height = 0
		choice = 0
		data = None
		spawn_point = None
		keys = list( PIPES.keys() )

		for i in range(self.hand_length):

			entity = world.create_entity()

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
			sprite.rect.x = self.card_slots[str(i)]["position"][0]
			sprite.rect.y = self.card_slots[str(i)]["position"][1]

			world.add_component( entity, sprite )
			self.current_hand.append( entity )
			self.card_slots[str(i)]["id"] = entity
			self.card_slots[str(i)]["occupied"] = True

	def _reset_card_slots(self):
		self.card_slots = {}

		data = None
		half_length = self.hand_length // 2
		first_col_x = self.offset_x + self.padding_outer
		second_col_x = first_col_x + TILE_SIZE + self.padding_inner
		base_row_y = self.offset_y + self.padding_outer
		for i in range(self.hand_length):
			if i < half_length:
				height = (i + 1) * TILE_SIZE + (i + 1) * self.padding_inner
				data = { "position": (first_col_x, base_row_y + height), "occupied": False, "id": -1 }
			else:
				height = (i + 1 - half_length) * TILE_SIZE + (i + 1 - half_length) * self.padding_inner
				data = { "position": (second_col_x, base_row_y + height), "occupied": False, "id": -1 }
			self.card_slots[str(i)] = data

	def clear_slot(self, position):
		for key, slot in self.card_slots.items():
			# Check if @position is inside the current slot
			if (
				(position[0] >= slot["position"][0] and position[0] <= slot["position"][0] + TILE_SIZE) and
				(position[1] >= slot["position"][1] and position[1] <= slot["position"][1] + TILE_SIZE)
			):
				# Clear slot
				slot["id"] = -1
				slot["occupied"] = False

	def draw(self, world):
		if len(self.current_hand) >= self.hand_length: return

		keys = list(PIPES.keys())

		pos_in_hand = "0"
		for key, slot in self.card_slots.items():
			if not slot["occupied"]:
				pos_in_hand = key
				break

		entity = world.create_entity()

		choice = random.choice( keys )
		while choice == "0" or choice == "1":
			choice = random.choice( keys )
		data = PIPES[ choice ]

		sprite = Pipe( 	file_name = data["sprite"],
						pipe_id = data["id"],
						left = data["left"],
						right = data["right"],
						up = data["up"],
						down = data["down"],
						fixed = data["fixed"] )
		sprite.rect.x = self.card_slots[pos_in_hand]["position"][0]
		sprite.rect.y = self.card_slots[pos_in_hand]["position"][1]

		world.add_component( entity, sprite )
		self.current_hand.append( entity )
		self.card_slots[pos_in_hand]["id"] = entity
		self.card_slots[pos_in_hand]["occupied"] = True

	def get_slot(self, position):
		for key, slot in self.card_slots.items():
			if (
				(position[0] >= slot["position"][0] and position[0] <= slot["position"][0] + TILE_SIZE) and
				(position[1] >= slot["position"][1] and position[1] <= slot["position"][1] + TILE_SIZE)
			):
				return slot["id"]
		return None

	def insert(self, entity, position, sprite = None):
		"""Put a new card in the inventory"""
		if entity in self.current_hand: return

		self.current_hand.append( entity )
		for key, slot in self.card_slots.items():
			# Check if @position is inside the current slot
			if (
				not slot["occupied"] 																	and
				(position[0] >= slot["position"][0] and position[0] <= slot["position"][0] + TILE_SIZE) and
				(position[1] >= slot["position"][1] and position[1] <= slot["position"][1] + TILE_SIZE)
			):
				# Update slot
				slot["id"] = entity
				slot["occupied"] = True
				# Update sprite position
				if sprite:
					sprite.rect.x = slot["position"][0]
					sprite.rect.y = slot["position"][1]

	def swap(self, world, entity, position, sprite):
		"""Move cards inside the inventory"""
		if not entity in self.current_hand: return

		old_home 	= "-1"
		old_entity 	= -1

		# Find this @entity's previous home and clear it
		for key, slot in self.card_slots.items():
			if slot["id"] == entity:
				old_home = key
				slot["id"] = -1
				slot["occupied"] = False
				break

		# Find the destination slot, move the @entity there and save the previous tenant
		for key, slot in self.card_slots.items():
			# Check if @position is inside the current slot
			if (
				(position[0] >= slot["position"][0] and position[0] <= slot["position"][0] + TILE_SIZE) and
				(position[1] >= slot["position"][1] and position[1] <= slot["position"][1] + TILE_SIZE)
			):
				# Store previous tenant
				old_entity = slot["id"]
				# Update new tenant
				slot["id"] = entity
				slot["occupied"] = True
				# Update sprite position
				sprite.rect.x = slot["position"][0]
				sprite.rect.y = slot["position"][1]

		# Relocate the previous tenant to its new home
		if old_entity != -1 and old_home != "-1":
			self.card_slots[old_home]["id"] = old_entity
			self.card_slots[old_home]["occupied"] = True
			old_sprite = world.component_for_entity( old_entity, Pipe )
			old_sprite.rect.x = self.card_slots[old_home]["position"][0]
			old_sprite.rect.y = self.card_slots[old_home]["position"][1]

	def remove(self, entity):
		if entity in self.current_hand:
			self.current_hand.remove( entity )
			for key, slot in self.card_slots.items():
				if slot["id"] == entity:
					slot["id"] = -1
					slot["occupied"] = False
					break

	def reset(self, world):

		# Remove old entities before resetting the current hand
		for card in self.current_hand:
			world.delete_entity( card )

		# Reset cards hand
		self.current_hand = []

		# Create card slots when missing
		if len(self.card_slots) < 10: self._reset_card_slots()

		# Create @hand_length random cards entities
		self._draw_random_hand(world, self.hand_length)
