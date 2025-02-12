

from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (144, 238, 144)

    SPAWN = (79, 227, 79)

    OBSTACLE = (128, 128, 128)
    BRICK = (170, 74, 68)

    BOMBE = (0, 128, 128)
    EXPLOSION = (255, 0, 0)