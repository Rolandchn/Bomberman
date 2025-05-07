from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld

import random

from game.BombermanGame import GameStatus
from game.GameLogic import GameLogic

from data.entity.Entity import Entity
from game.GameAction import Action

from data.entity.AI.MinMax import minmax


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
            return self.easy_mode()

        elif self.difficulty == "moyen":
            return self.medium_mode()

        elif self.difficulty == "difficile":
            return self.hard_mode()


    '''
    Méthode pour l'IA facile
    '''
    def easy_mode(self):
        """
        IA Random : déplacement aléatoire + pose bombe aléatoire
        """
        action = random.choice([Action.MOVE_UP,
                                Action.MOVE_DOWN,
                                Action.MOVE_LEFT,
                                Action.MOVE_RIGHT,
                                Action.PLACE_BOMB])
        
        return GameLogic.apply_action(self.world, self, action)
    

    '''
    Méthode pour l'IA moyen
    '''

    def medium_mode(self):
        _, action =  minmax(self.world, self.status, depth=3)

        return GameLogic.apply_action(self.world, self, action)

    '''
        Méthode pour l'IA difficile
    '''

    def hard_mode(self):
        _, action = minmax(self.world, self.status, depth=3)

        return GameLogic.apply_action(self.world, self, action)



    def clone(self, new_world):
        return IA((self. grid_x, self.grid_y), self.status, new_world)