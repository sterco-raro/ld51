import os
import pathlib
import pygame

# General
GAME_NAME 		= "LD 51"
GAME_VERSION 	= "0.1"

FPS_LIMIT 			= 60.0
FIXED_DELTA_TIME 	= 0.01

SCREEN_MODE_FLAGS = pygame.DOUBLEBUF
#SCREEN_MODE_FLAGS = pygame.FULLSCREEN | pygame.DOUBLEBUF

PROFILING_MODE = "w+"
PROFILING_PATH = "profiling.txt"
PROFILING_FILE = open(PROFILING_PATH, PROFILING_MODE)

# Resources
GRAPHICS_FOLDER = os.path.join(pathlib.Path(__file__).parent.resolve().parent, "graphics")

SPRITE_UNKNOWN 				= "unknown.png"
SPRITE_CURSOR 				= "menu_cursor.png"
SPRITE_PIPE_CROSS 			= "pipes/cross.png"
SPRITE_PIPE_VERTICAL 		= "pipes/vertical.png"
SPRITE_PIPE_HORIZONTAL 		= "pipes/horizontal.png"
SPRITE_PIPE_INPUT 			= "pipes/output_orange.png"
SPRITE_PIPE_OUTPUT 			= "pipes/input_orange.png"
SPRITE_PIPE_BENT_LEFT_UP 	= "pipes/bent_left_up.png"
SPRITE_PIPE_BENT_LEFT_DOWN 	= "pipes/bent_left_down.png"
SPRITE_PIPE_BENT_RIGHT_UP 	= "pipes/bent_right_up.png"
SPRITE_PIPE_BENT_RIGHT_DOWN	= "pipes/bent_right_down.png"
SPRITE_PIPE_T_LEFT 			= "pipes/t_left.png"
SPRITE_PIPE_T_RIGHT 		= "pipes/t_right.png"
SPRITE_PIPE_T_UP 			= "pipes/t_up.png"
SPRITE_PIPE_T_DOWN 			= "pipes/t_down.png"

PIPES = {
	"0": 	{ "sprite": SPRITE_PIPE_INPUT, 			"left": False, 	"right": False, "up": False, "down": True, "fixed": True },
	"1": 	{ "sprite": SPRITE_PIPE_OUTPUT, 		"left": False, 	"right": False, "up": True,  "down": False, "fixed": True },
	"2": 	{ "sprite": SPRITE_PIPE_VERTICAL, 		"left": False, 	"right": False, "up": True,  "down": True, "fixed": False },
	"3": 	{ "sprite": SPRITE_PIPE_HORIZONTAL, 	"left": True, 	"right": True, 	"up": False, "down": False, "fixed": False },
	"4": 	{ "sprite": SPRITE_PIPE_BENT_LEFT_UP, 	"left": True, 	"right": False, "up": True,  "down": False, "fixed": False },
	"5": 	{ "sprite": SPRITE_PIPE_BENT_LEFT_DOWN, "left": True, 	"right": False, "up": False, "down": True, "fixed": False },
	"6": 	{ "sprite": SPRITE_PIPE_BENT_RIGHT_UP, 	"left": False, 	"right": True, 	"up": True,  "down": False, "fixed": False },
	"7": 	{ "sprite": SPRITE_PIPE_BENT_RIGHT_DOWN,"left": False, 	"right": True, 	"up": False, "down": True, "fixed": False },
	"8": 	{ "sprite": SPRITE_PIPE_T_LEFT, 		"left": True, 	"right": False, "up": True,  "down": True, "fixed": False },
	"9": 	{ "sprite": SPRITE_PIPE_T_RIGHT, 		"left": False, 	"right": True, 	"up": True,  "down": True, "fixed": False },
	"10": 	{ "sprite": SPRITE_PIPE_T_UP, 			"left": True, 	"right": True, 	"up": True,  "down": False, "fixed": False },
	"11": 	{ "sprite": SPRITE_PIPE_T_DOWN, 		"left": True, 	"right": True, 	"up": False, "down": True, "fixed": False },
	"12": 	{ "sprite": SPRITE_PIPE_CROSS, 			"left": True, 	"right": True, 	"up": True,  "down": True, "fixed": False },
}

# Window
WINDOW_TITLE = GAME_NAME

SCREEN_WIDTH 	= 1280
SCREEN_HEIGHT 	= 720

VIEWPORT_WIDTH 	= SCREEN_WIDTH
VIEWPORT_HEIGHT = SCREEN_HEIGHT

# Map
TILE_SIZE = 64

# Physics
VECTOR_ZERO 			= pygame.Vector2(0, 0)
SPEED_MAX 				= 20.0
SPEED_BASE 				= 10.0
FRICTION_BASE_FLOOR 	= 0.5 		# 0.5 = almost meaningless, 0.1 = meaningful
ACCELERATION_BASE_FLOOR = 0.5 		# 0.5 = almost meaningless, 0.1 = meaningful

# Colors
STATIC_SPRITE_DEBUG_COLOR 	= (40, 220, 220)
ANIMATED_SPRITE_DEBUG_COLOR = (40, 220, 220)
MAP_TILE_DEBUG_COLOR 		= (220, 220, 40)
HITBOX_DEBUG_COLOR 			= (220, 40, 220)

# Z-axis sorting layers
RENDERING_LAYERS = {
	"void": 	-1,
	"water": 	 0,
	"ground": 	 1,
	"main": 	 2,
	"ceiling": 	 3
}

# Animations
ANIM_SPEED_DINOSAUR 	= 12 	# TODO animation speed unit is ?
ANIM_DURATION_DINOSAUR 	= 0 	# in milliseconds
ANIM_TABLE_DINOSAUR 	= { "idle": [], "moving": [], "hurt": [], "kick": [] }

ANIM_SPEED_EXPLOSION 	= 12 	# TODO animation speed unit is ?
ANIM_DURATION_EXPLOSION = 1500 	# in milliseconds
ANIM_TABLE_EXPLOSION 	= { "big": [] }

# Player actions (in milliseconds)
PLAYER_COOLDOWN_BOMB 	= 1000
PLAYER_DURATION_ATTACK 	= 500
PLAYER_DURATION_HURT 	= 500