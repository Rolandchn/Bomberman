from enum import Flag, auto



class Action(Flag):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE = MOVE_UP | MOVE_DOWN | MOVE_LEFT | MOVE_RIGHT
    
    PLACE_BOMB = auto()
