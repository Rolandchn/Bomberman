from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.GameWord import GameWorld
    from core.Bomberman import GameStatus


import pygame

from data.entity.GameLogic import GameLogic
from data.entity.Action import Action
from data.entity.Entity import Entity



class Player(Entity):
    def __init__(self, status:GameStatus, world:GameWorld):
        self.status = status
        super().__init__(world.map.respawn(self), world.player_group)
        
        self.world = world

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

        if action is not None and GameLogic.apply_action(self.world, self, action): return True
        return False

    
    def is_hit(self):
        '''
        Output: check player sprite collides with any explosion. Return True if collides, otherwise False
        ''' 

        return pygame.sprite.spritecollideany(self, self.world.explosion_group)

    def kill(self):
        self.world.map.update_grid_position(self)

        super().kill()


    def clone(self, new_world):
        copy = Player(self.status, new_world)

        copy.grid_x = self.grid_x
        copy.grid_y = self.grid_y
        copy.rect = self.rect

        return copy
        
    def groups_to_add(self):
        return ["player_group"]


    def __eq__(self, other):
        return isinstance(other, Player) and other.status == self.status


    def __hash__(self):
        return hash(self.status)