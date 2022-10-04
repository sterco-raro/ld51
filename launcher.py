#
# Codename: LD51
#
# Authors:
#	unarmedpile@gmail.com
#	serviceoftaxi@gmail.com
#


try:
	import sys
	import pygame
	from code.game_manager import GameManager
except ImportError as importErr:
	print("Cannot load module. {}".format(importErr))
	sys.exit(2)


# -------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	manager = GameManager()
	manager.run()
	pygame.quit()
	sys.exit(0)
