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
	margin_x = TILE_SIZE
	margin_y = TILE_SIZE
	offset_x = SCREEN_WIDTH - grid_width * TILE_SIZE - margin_x
	offset_y = 0 + margin_y
	tilemap_data = PipeMap( width = grid_width,
							height = grid_height,
							offset_x = offset_x,
							offset_y = offset_y,
							tileset = PIPES )

	# Assign components to entity
	world.add_component( tilemap, tilemap_data )

	# Build map structure
	tilemap_data.level[0][2] = "0"
	tilemap_data.level[1][2] = "2"
	tilemap_data.level[0][5] = "0"
	tilemap_data.level[1][5] = "8"
	tilemap_data.level[0][7] = "0"
	tilemap_data.level[1][7] = "2"
	tilemap_data.level[grid_height - 1][1] = "1"
	tilemap_data.level[grid_height - 2][1] = "7"
	tilemap_data.level[grid_height - 1][4] = "1"
	tilemap_data.level[grid_height - 2][4] = "7"
	tilemap_data.level[grid_height - 1][5] = "1"
	tilemap_data.level[grid_height - 2][5] = "2"
	tilemap_data.level[grid_height - 1][6] = "1"
	tilemap_data.level[grid_height - 2][6] = "2"

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
					left=PIPES[tilemap_data.level[row][col]]["left"],
					right=PIPES[tilemap_data.level[row][col]]["right"],
					up=PIPES[tilemap_data.level[row][col]]["up"],
					down=PIPES[tilemap_data.level[row][col]]["down"],
					fixed=PIPES[tilemap_data.level[row][col]]["fixed"]
				)
			)

	# Grid area
	return pygame.Rect( tilemap_data.offset_x, tilemap_data.offset_y, tilemap_data.world_width, tilemap_data.world_height )


def create_deck(world, font, deck_width, deck_height):

	# Entities
	deck = world.create_entity()
	reroll_button = world.create_entity()

	# Components
	deck_component = Deck( width=deck_width, height=deck_height, offset_x=TILE_SIZE, offset_y=TILE_SIZE )
	world.add_component( deck, deck_component )

	text = "Reroll"
	text_surface = font.render( text, True, (255, 255, 255) )
	text_size = font.size(text)
	text_rect = text_surface.get_rect( center = ( text_size[0] + deck_component.offset_x, text_size[1] + deck_component.offset_y ) )
	image = UiButton( rect = pygame.Rect( text_rect.x - 5, text_rect.y - 5, text_rect.w + 10, text_rect.h + 10 ), inactive_color = ( 200, 20, 20 ) )
	image.rect.center = text_rect.center
	world.add_component( reroll_button, image )
	world.add_component( reroll_button, UiText( text=text, surface=text_surface, rect=text_rect, size=32 ) )
	world.add_component( reroll_button, UiItem( rect=image.rect, callback=lambda: deck_component.reset(world) ) )

	return pygame.Rect( deck_component.offset_x, deck_component.offset_y, deck_component.width, deck_component.height )


# -------------------------------------------------------------------------------------------------


def load(file_name):
	world = esper.World()

	# Active display reference
	screen 		= pygame.display.get_surface()
	screen_size = screen.get_size()

	# Pygame font object
	font = pygame.font.SysFont(None, 32)

	# Create game area grid
	grid_area = create_grid(world, 10, 9)

	# Create side deck interface
	deck_area = create_deck(world, font, 4, 9)

	# Entities
	cursor = world.create_entity()
	timer = world.create_entity()

	# Components
	world.add_component( cursor, Cursor() )
	world.add_component( timer, Timer( 10000 ) )

	# Systems
	world.add_processor( TimerController( scene_name=file_name, timer_entity=timer ) )
	world.add_processor( MouseInputHandler( scene_name=file_name, cursor_entity=cursor, deck_area=deck_area, grid_area=grid_area ) )
	world.add_processor( Rendering( scene_name=file_name, world_width=screen_size[0], world_height=screen_size[1] ) )

	return world