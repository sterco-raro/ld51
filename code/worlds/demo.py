import esper
import pygame
# TMP
from code.systems.ui import MenuRendering
from code.components.ui import UiSurface


def load(file_name):
	world = esper.World()

	# Active display reference
	screen 		= pygame.display.get_surface()
	screen_size = screen.get_size()

	# Entities
	background 	= world.create_entity()

	# Components
	# TMP
	world.add_component( background, UiSurface( color = (220, 80, 200), size = screen_size ) )

	# Systems
	# TMP
	world.add_processor( MenuRendering( scene_name = file_name ) )

	return world
