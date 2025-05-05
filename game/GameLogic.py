from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.Entity import Entity
    from game.GameWorld import GameWorld
    from data.entity.PowerUp import PowerUp, PowerUpType


from game.GameAction import Action



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
                
                GameLogic.handle_powerup_pickup(world, entity)

                entity.update_rect()
                                
        elif action == Action.PLACE_BOMB:
            return entity.bomb_manager.place_bomb(world)

        return True
    

    @staticmethod
    def apply_powerup(entity: Entity, powerup: PowerUp):
        if powerup.type == PowerUpType.RANGE:
            entity.bomb_manager.bomb_range += 1

        elif powerup.type == PowerUpType.EXTRA_BOMB:
            entity.bomb_manager.max_bombs += 1


    @staticmethod
    def handle_powerup_pickup(world: GameWorld, entity: Entity):
        for powerup in world.powerup_group:
            if (powerup.x, powerup.y) == (entity.grid_x, entity.grid_y):
                GameLogic.apply_powerup(entity, powerup)
                world.powerup_group.remove(powerup)
