


from enum import Enum, auto


class PowerUpType(Enum):
    RANGE = auto()
    KICK = auto()
    EXTRA_BOMB = auto()
    REMOTE = auto()


class PowerUp:
    def __init__(self, position, type):
        self.x, self.y = position

        self.type = type
        