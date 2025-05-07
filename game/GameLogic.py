from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.Entity import Entity
    from game.GameWorld import GameWorld

from game.GameAction import Action
from data.entity.Bombe import Bomb



class GameLogic:
    @staticmethod
    def apply_action(world: GameWorld, entity: Entity, action: Action) -> bool:
        if action is None:
            return False
        
        if action in Action.MOVE:
            if world.map.is_walkable(entity, action):
            
                if action == Action.MOVE_UP: entity.grid_y -= 1
                elif action == Action.MOVE_DOWN: entity.grid_y += 1
                elif action == Action.MOVE_LEFT: entity.grid_x -= 1
                elif action == Action.MOVE_RIGHT: entity.grid_x += 1

                entity.update_rect()

                                
        elif action == Action.PLACE_BOMB:
            if world.map.is_bomb_placeable(entity):
                Bomb((entity.grid_x, entity.grid_y), world, entity)

        elif action == Action.WAIT:
            return True

        return True