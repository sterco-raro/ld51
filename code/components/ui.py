import pygame

from typing import Callable
from dataclasses import dataclass

from code.settings import TILE_SIZE
from code.utils import load_scaled_image


# -------------------------------------------------------------------------------------------------


@dataclass
class UiButton:
	"""Button background (color or image) with hovering support"""
	file_name: str = None
	active_color: tuple = (40, 220, 40)
	inactive_color: tuple = (0, 0, 0)
	rect: pygame.Rect = None
	image: pygame.Surface = None
	size: tuple = (64, 64)
	hovering: bool = False

	def __post_init__(self):
		if self.file_name:
			self.image = load_scaled_image(self.file_name, self.size)
			self.rect = self.image.get_rect()


# -------------------------------------------------------------------------------------------------


@dataclass
class UiButtonStates:
	"""Button with different images for normal, hovering, pressed states"""
	normal_image_filename: str = None
	pressed_image_filename: str = None
	hovering_image_filename: str = None

	normal_image: pygame.Surface = None
	pressed_image: pygame.Surface = None
	hovering_image: pygame.Surface = None

	size: tuple = (TILE_SIZE, TILE_SIZE)
	rect: pygame.Rect = None
	image: pygame.Surface = None

	_pressed: bool = False
	_hovering: bool = False

	def __post_init__(self):
		if self.normal_image_filename:
			self.normal_image = load_scaled_image( self.normal_image_filename, self.size )
		if self.pressed_image_filename:
			self.pressed_image = load_scaled_image( self.pressed_image_filename, self.size )
		if self.hovering_image_filename:
			self.hovering_image = load_scaled_image( self.hovering_image_filename, self.size )

		self.image = self.normal_image
		self.rect = self.image.get_rect()

	@property
	def hovering(self):
		return self._hovering

	@hovering.setter
	def hovering(self, value):
		self._hovering = value
		if self._hovering:
			self.image = self.hovering_image
		else:
			self.image = self.normal_image

	@property
	def pressed(self):
		return self._pressed

	@pressed.setter
	def pressed(self, value):
		self._pressed = value
		if self._pressed:
			self.image = self.pressed_image
		else:
			self.image = self.normal_image


# -------------------------------------------------------------------------------------------------


@dataclass
class UiCursor:
	"""Mouse cursor"""
	file_name: str = "unknown.png"
	size: tuple = (48, 48)

	def __post_init__(self):
		self.image = load_scaled_image(self.file_name, self.size)
		self.rect = self.image.get_rect()


# -------------------------------------------------------------------------------------------------


@dataclass
class UiImage:
	"""Image loaded from disk"""
	file_name: str = "unknown.png"
	size: tuple = (64, 64)

	def __post_init__(self):
		self.image = load_scaled_image(self.file_name, self.size)
		self.rect = self.image.get_rect()


# -------------------------------------------------------------------------------------------------


@dataclass
class UiItem:
	"""Logical item with an action"""
	rect: pygame.Rect
	callback: Callable[[None], None]


# -------------------------------------------------------------------------------------------------


@dataclass
class UiSurface:
	"""Basic monochrome pygame.Surface"""
	color: tuple = (255, 255, 255)
	size: tuple = (64, 64)

	def __post_init__(self):
		self.image = pygame.Surface(self.size)
		self.image.fill(self.color)
		self.rect = self.image.get_rect()


# -------------------------------------------------------------------------------------------------


@dataclass
class UiText:
	"""Ui text container"""
	text: str = ""
	surface: pygame.Surface = None
	rect: pygame.Rect = None
	size: int = 32
