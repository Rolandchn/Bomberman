from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from game.GameStatus import GameStatus


import random



def eval(world: GameWorld, player: GameStatus):
    return random.randint(-50, 50)
