from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from game.BombermanGame import GameStatus

import pygame

from game.GameLogic import GameLogic
from game.GameAction import Action
from data.entity.Entity import Entity



class Player(Entity):
    def __init__(self, position, status: GameStatus, world: GameWorld):
        super().__init__(position, status, world, world.player_group)
        
        self.image.fill(self.status.value.value)

    
    def input(self) -> bool:
        keys = pygame.key.get_pressed()

        action = None
        if keys[pygame.K_UP]: 
            action = Action.MOVE_UP

        elif keys[pygame.K_DOWN]: 
            action = Action.MOVE_DOWN
        
        elif keys[pygame.K_LEFT]: 
            action = Action.MOVE_LEFT

        elif keys[pygame.K_RIGHT]: 
            action = Action.MOVE_RIGHT

        elif keys[pygame.K_SPACE]:
            action = Action.PLACE_BOMB

        return GameLogic.apply_action(self.world, self, action)

    

    def clone(self, new_world):
        return Player((self. grid_x, self.grid_y), self.status, new_world)

    def groups_to_add(self):
        return ["player_group"]