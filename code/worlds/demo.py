import esper
import pygame
from code.settings import *
from code.timer import *
from code.components.deck import *
from code.components.map import *
from code.components.sprite import *
from code.components.ui import *
from code.systems.input import *
from code.systems.rendering import *
from code.systems.timer import *


# -------------------------------------------------------------------------------------------------


def create_grid(world, grid_width, grid_height):

	# Entity
	tilemap = world.create_entity()

	# Components
	offset_x = DECK_WIDTH * TILE_SIZE
	offset_y = 0
	tilemap_data = PipeMap( width = grid_width,
							height = grid_height,
							offset_x = offset_x,
							offset_y = offset_y,
							tileset = PIPES )

	# Assign components to entity
	world.add_component( tilemap, tilemap_data )

	# Build map structure
	tilemap_data.level[0][2] = PIPE_INPUT
	tilemap_data.level[1][2] = PIPE_VERTICAL
	tilemap_data.level[0][5] = PIPE_INPUT
	tilemap_data.level[1][5] = PIPE_T_LEFT
	tilemap_data.level[0][7] = PIPE_INPUT
	tilemap_data.level[1][7] = PIPE_VERTICAL
	tilemap_data.level[grid_height - 1][1] = PIPE_OUTPUT
	tilemap_data.level[grid_height - 2][1] = PIPE_BENT_RIGHT_DOWN
	tilemap_data.level[grid_height - 1][4] = PIPE_OUTPUT
	tilemap_data.level[grid_height - 2][4] = PIPE_BENT_LEFT_DOWN
	tilemap_data.level[grid_height - 1][6] = PIPE_OUTPUT
	tilemap_data.level[grid_height - 2][6] = PIPE_VERTICAL

	# Create components for the base map
	for row in range(grid_height):
		for col in range(grid_width):

			# Empty cells
			if tilemap_data.level[row][col] == "-1": continue

			# Entity
			entity = world.create_entity()

			# Components
			spawn_point = (
				col * TILE_SIZE + TILE_SIZE//2 + tilemap_data.offset_x,
				row * TILE_SIZE + TILE_SIZE//2 + tilemap_data.offset_y
			)

			# Assign components to entity
			world.add_component(
				entity,
				Pipe(
					file_name=PIPES[tilemap_data.level[row][col]]["sprite"],
					spawn_point=spawn_point,
					pipe_id=PIPES[tilemap_data.level[row][col]]["id"],
					left=PIPES[tilemap_data.level[row][col]]["left"],
					right=PIPES[tilemap_data.level[row][col]]["right"],
					up=PIPES[tilemap_data.level[row][col]]["up"],
					down=PIPES[tilemap_data.level[row][col]]["down"],
					fixed=PIPES[tilemap_data.level[row][col]]["fixed"]
				)
			)


def create_deck(world, font, deck_width, deck_height):

	# Entities
	deck = world.create_entity()
	left_button = world.create_entity()
	right_button = world.create_entity()

	# Deck
	deck_component = Deck( width=deck_width, height=deck_height, offset_x=0, offset_y=0 )
	deck_component.reset(world)
	world.add_component( deck, deck_component )

	# First button
	text = "Draw"
	text_surface = font.render( text, True, (255, 255, 255) )
	text_size = font.size(text)
	text_rect = text_surface.get_rect( center = ( 	deck_component.offset_x + deck_component.padding_outer + TILE_SIZE//2,
													deck_component.offset_y + deck_component.padding_outer + TILE_SIZE//2 ) )
	image = UiButtonStates( normal_image_filename = SPRITE_BUTTON_NORMAL,
							pressed_image_filename = SPRITE_BUTTON_PRESSED,
							hovering_image_filename = SPRITE_BUTTON_HOVERING )
	image.rect.center = text_rect.center
	world.add_component( left_button, image )
	world.add_component( left_button, UiText( text=text, surface=text_surface, rect=text_rect, size=32 ) )
	world.add_component( left_button, UiItem( rect=image.rect, callback=lambda: deck_component.draw(world) ) )

	# Second button
	text = "Boh?"
	text_surface = font.render( text, True, (255, 255, 255) )
	text_size = font.size(text)
	text_rect = text_surface.get_rect( center = ( 	(deck_component.offset_x + deck_component.padding_outer + TILE_SIZE//2) + deck_component.padding_inner + TILE_SIZE,
													deck_component.offset_y + deck_component.padding_outer + TILE_SIZE//2 ) )
	image = UiButtonStates( normal_image_filename = SPRITE_BUTTON_NORMAL,
							pressed_image_filename = SPRITE_BUTTON_PRESSED,
							hovering_image_filename = SPRITE_BUTTON_HOVERING )
	image.rect.center = text_rect.center
	world.add_component( right_button, image )
	world.add_component( right_button, UiText( text=text, surface=text_surface, rect=text_rect, size=32 ) )


# -------------------------------------------------------------------------------------------------


def load(file_name):
	world = esper.World()

	# Active display reference
	screen 		= pygame.display.get_surface()
	screen_size = screen.get_size()

	# Pygame font object
	font = pygame.font.SysFont(None, 24)

	# Create game area grid
	create_grid(world, GRID_WIDTH, GRID_HEIGHT)

	# Create side deck interface
	create_deck(world, font, DECK_WIDTH, DECK_HEIGHT)

	# Entities
	cursor = world.create_entity()
	timer = world.create_entity()

	# Components
	world.add_component( cursor, Cursor() )
	world.add_component( timer, Timer( 10000 ) )

	# Systems
	world.add_processor( TimerController( scene_name=file_name, timer_entity=timer ) )
	world.add_processor( MouseInputHandler( scene_name=file_name, cursor_entity=cursor ) )
	world.add_processor( Rendering( scene_name=file_name, world_width=screen_size[0], world_height=screen_size[1] ) )

	return world
