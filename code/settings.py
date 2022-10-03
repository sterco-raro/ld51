import os
import pathlib
import pygame

DEBUG = False

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
SPRITE_CURSOR 				= "cursors/hand_point.png"
SPRITE_CURSOR_OPEN			= "cursors/hand_open.png"
SPRITE_CURSOR_CLOSED		= "cursors/hand_closed.png"

SPRITE_GRID_BG 				= "gridbg.png"
SPRITE_DECK_BG 				= "deck/deckbg_10slots_baked.png"
SPRITE_BUTTON_NORMAL 		= "deck/deckgrid_button.png"
SPRITE_BUTTON_PRESSED 		= "deck/deckgrid_button_pressed.png"
SPRITE_BUTTON_HOVERING 		= "deck/deckgrid_button_hover.png"

SPRITE_PIPE_CROSS 			= "pipes/cross.png"
SPRITE_PIPE_VERTICAL 		= "pipes/vertical.png"
SPRITE_PIPE_HORIZONTAL 		= "pipes/horizontal.png"
SPRITE_PIPE_INPUT 			= "pipes/input_orange.png"
SPRITE_PIPE_OUTPUT 			= "pipes/output_orange.png"
SPRITE_PIPE_BENT_LEFT_UP 	= "pipes/bent_left_up.png"
SPRITE_PIPE_BENT_LEFT_DOWN 	= "pipes/bent_left_down.png"
SPRITE_PIPE_BENT_RIGHT_UP 	= "pipes/bent_right_up.png"
SPRITE_PIPE_BENT_RIGHT_DOWN	= "pipes/bent_right_down.png"
SPRITE_PIPE_T_LEFT 			= "pipes/t_left.png"
SPRITE_PIPE_T_RIGHT 		= "pipes/t_right.png"
SPRITE_PIPE_T_UP 			= "pipes/t_up.png"
SPRITE_PIPE_T_DOWN 			= "pipes/t_down.png"

PIPE_INPUT 				= "0"
PIPE_OUTPUT 			= "1"
PIPE_VERTICAL 			= "2"
PIPE_HORIZONTAL 		= "3"
PIPE_BENT_LEFT_UP 		= "4"
PIPE_BENT_LEFT_DOWN 	= "5"
PIPE_BENT_RIGHT_UP 		= "6"
PIPE_BENT_RIGHT_DOWN 	= "7"
PIPE_T_LEFT 			= "8"
PIPE_T_RIGHT 			= "9"
PIPE_T_UP 				= "10"
PIPE_T_DOWN 			= "11"
PIPE_CROSS 				= "12"

PIPES = {
	PIPE_INPUT: 			{ "id": PIPE_INPUT, "sprite": SPRITE_PIPE_INPUT, 			"left": False, 	"right": False, "up": False, "down": True, "fixed": True },
	PIPE_OUTPUT: 			{ "id": PIPE_OUTPUT, "sprite": SPRITE_PIPE_OUTPUT, 		"left": False, 	"right": False, "up": True,  "down": False, "fixed": True },
	PIPE_VERTICAL: 			{ "id": PIPE_VERTICAL, "sprite": SPRITE_PIPE_VERTICAL, 		"left": False, 	"right": False, "up": True,  "down": True, "fixed": False },
	PIPE_HORIZONTAL: 		{ "id": PIPE_HORIZONTAL, "sprite": SPRITE_PIPE_HORIZONTAL, 	"left": True, 	"right": True, 	"up": False, "down": False, "fixed": False },
	PIPE_BENT_LEFT_UP: 		{ "id": PIPE_BENT_LEFT_UP, "sprite": SPRITE_PIPE_BENT_LEFT_UP, 	"left": True, 	"right": False, "up": True,  "down": False, "fixed": False },
	PIPE_BENT_LEFT_DOWN: 	{ "id": PIPE_BENT_LEFT_DOWN, "sprite": SPRITE_PIPE_BENT_LEFT_DOWN, "left": True, 	"right": False, "up": False, "down": True, "fixed": False },
	PIPE_BENT_RIGHT_UP: 	{ "id": PIPE_BENT_RIGHT_UP, "sprite": SPRITE_PIPE_BENT_RIGHT_UP, 	"left": False, 	"right": True, 	"up": True,  "down": False, "fixed": False },
	PIPE_BENT_RIGHT_DOWN: 	{ "id": PIPE_BENT_RIGHT_DOWN, "sprite": SPRITE_PIPE_BENT_RIGHT_DOWN,"left": False, 	"right": True, 	"up": False, "down": True, "fixed": False },
	PIPE_T_LEFT: 			{ "id": PIPE_T_LEFT, "sprite": SPRITE_PIPE_T_LEFT, 		"left": True, 	"right": False, "up": True,  "down": True, "fixed": False },
	PIPE_T_RIGHT: 			{ "id": PIPE_T_RIGHT, "sprite": SPRITE_PIPE_T_RIGHT, 		"left": False, 	"right": True, 	"up": True,  "down": True, "fixed": False },
	PIPE_T_UP: 				{ "id": PIPE_T_UP, "sprite": SPRITE_PIPE_T_UP, 			"left": True, 	"right": True, 	"up": True,  "down": False, "fixed": False },
	PIPE_T_DOWN: 			{ "id": PIPE_T_DOWN, "sprite": SPRITE_PIPE_T_DOWN, 		"left": True, 	"right": True, 	"up": False, "down": True, "fixed": False },
	PIPE_CROSS: 			{ "id": PIPE_CROSS, "sprite": SPRITE_PIPE_CROSS, 			"left": True, 	"right": True, 	"up": True,  "down": True, "fixed": False },
}

# Window
WINDOW_TITLE = GAME_NAME

SCREEN_WIDTH 	= 832
SCREEN_HEIGHT 	= 576

VIEWPORT_WIDTH 	= SCREEN_WIDTH
VIEWPORT_HEIGHT = SCREEN_HEIGHT

# Map
TILE_SIZE = 64

DECK_WIDTH 	= 3
DECK_HEIGHT = 9

GRID_WIDTH 	= 10
GRID_HEIGHT = 9

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

# Audio
GAME_OST = "sounds/ld51fuckmeonmydeathbed.mp3"

SOUNDS = [
	"button_downup.wav",
	"button_down.wav",
	"button_up.wav",
	"fart.wav",
	"flush.wav",
	"pipe_drop.wav",
	"pipe_pick.wav",
	"pipe_plop.wav",
	"pipe_rotate.wav",
	"rattle.wav",
	"rattleflush.wav",
	"snap.wav",
	"weird.wav",
]
