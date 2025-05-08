from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld

import random

from game.BombermanGame import GameStatus
from game.GameLogic import GameLogic

from data.entity.Entity import Entity

from data.entity.AI.decision.minMax import minmax
from data.entity.AI.difficulty import EASY, MEDIUM, HARD


class IA(Entity):
    #   difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle)
    #   strong:  min max td4 (strategie: corner the player, reaction to player following, reaction to player fleeing ...)

    def __init__(self, position, status: GameStatus, world: GameWorld, difficulty="facile"):
        super().__init__(position, status, world, world.player_group)

        self.image.fill(self.status.value.value)

        self.difficulty = difficulty
        


    def input(self):
        if self.difficulty == "facile":
            _, action = minmax(self.world, self.status, EASY.depth, EASY.eval_fn)

        elif self.difficulty == "moyen":
            _, action = minmax(self.world, self.status, MEDIUM.depth, MEDIUM.eval_fn)

        elif self.difficulty == "difficile":
            _, action = minmax(self.world, self.status, HARD.depth, HARD.eval_fn)

        return GameLogic.apply_action(self.world, self, action)


    def clone(self, new_world):
        return IA((self. grid_x, self.grid_y), self.status, new_world)