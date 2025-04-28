from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.Entity import Entity
    from data.entity.GameWord import GameWorld

from data.entity.Action import Action
from data.entity.Bombe import Bomb



class GameLogic:
    @staticmethod
    def apply_action(world: GameWorld, entity: Entity, action: Action) -> bool:

        if action in Action.MOVE:
            if world.map.is_walkable(entity, action):
            
                if action == Action.MOVE_UP: entity.grid_y -= 1
                elif action == Action.MOVE_DOWN: entity.grid_y += 1
                elif action == Action.MOVE_LEFT: entity.grid_x -= 1
                elif action == Action.MOVE_RIGHT: entity.grid_x += 1

                entity.update_rect()
                
                world.map.update_grid_position(entity)

            else:
                return False # if player is struck
                
        elif action == Action.PLACE_BOMB:
            world.map.update_grid_bomb(Bomb((entity.grid_x, entity.grid_y), world))

        return True