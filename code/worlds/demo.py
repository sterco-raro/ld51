import esper
import pygame
from code.settings import *
from code.components.camera import CameraFollow
from code.components.hitbox import Hitbox
from code.components.map import Tile, TileMap
from code.components.sprite import StaticSprite
from code.systems.rendering import LayeredRendering


# -------------------------------------------------------------------------------------------------


def create_world_map(world):

	# Entity
	tilemap = world.create_entity()

	# Components
	tileset = {
		"0": Tile( file_name=SPRITE_WATER, 	layer=RENDERING_LAYERS["water"], 	scale_size=(48, 48), walkable=False ),
		"1": Tile( file_name=SPRITE_FLOOR, 	layer=RENDERING_LAYERS["ground"], 	walkable=True ),
		"2": Tile( file_name=SPRITE_WALL, 	layer=RENDERING_LAYERS["main"], 	walkable=False ),
		"3": Tile( file_name=SPRITE_CLOUD, 	layer=RENDERING_LAYERS["ceiling"], 	scale_size=(48, 48), walkable=True ),
	}
	tilemap_data = TileMap( file_name = "demo",
							layers = [ "water", "ground", "main", "ceiling" ],
							tileset = tileset )

	# Assign components to entity
	world.add_component( tilemap, tilemap_data )

	# Create wall entities for "main" layer
	for i in range(tilemap_data.map_height):
		for j in range(tilemap_data.map_width):

			# Empty cells
			if tilemap_data.level_data["main"][i][j] == "-1": continue

			# Entity
			entity = world.create_entity()

			# Components
			spawn_point = ( j * TILE_SIZE + TILE_SIZE//2, i * TILE_SIZE + TILE_SIZE//2 )
			wall_sprite = StaticSprite( file_name = "wall.png",
										layer = RENDERING_LAYERS["main"],
										spawn_point = spawn_point )
			# Assign components to entity
			world.add_component( entity, wall_sprite )
			world.add_component( entity, Hitbox( reference_rect = wall_sprite.rect ) )

	# World dimensions
	return ( tilemap_data.world_width, tilemap_data.world_height )


# -------------------------------------------------------------------------------------------------


def load(file_name):
	world = esper.World()

	# Active display reference
	screen 		= pygame.display.get_surface()
	screen_size = screen.get_size()

	width, height = create_world_map(world)

	# Entities
	background 	= world.create_entity()

	# Components
	background_sprite = StaticSprite( 	file_name = SPRITE_UNKNOWN,
										layer = RENDERING_LAYERS["main"],
										scale_size = screen_size,
										spawn_point = ( screen_size[0] // 2, screen_size[1] // 2 ) )
	world.add_component( background, background_sprite )
	world.add_component( background, CameraFollow( target=background_sprite ) )

	# Systems
	world.add_processor( LayeredRendering( scene_name=file_name, world_width=width, world_height=height ) )

	return world
