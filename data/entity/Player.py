from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.GameWord import GameWorld
    from core.Bomberman import GameStatus


import pygame

from data.entity.Entity import Entity
from data.entity.Bombe import Bomb

from data.texture.Color import Color
from data.texture.config import TILE_SIZE



class Player(Entity):
    def __init__(self, status:GameStatus, color:Color, world:GameWorld):
        self.status = status
        super().__init__(world.map.respawn(), pygame.Surface((TILE_SIZE, TILE_SIZE)), world.player_group)
        
        self.world = world

        self.image.fill(color.value)


    
    def input(self) -> bool:
        if self.move() : return True
        elif self.bomb() : return True

        return False
    

    def move(self) -> bool:
        '''
        Output: check player key input (up, down, left, right) and move
        ''' 

        has_moved = False
        keys = pygame.key.get_pressed()
        
        dx, dy = self.grid_x, self.grid_y

        if keys[pygame.K_LEFT]: 
            dx -= 1
            has_moved = True

        if keys[pygame.K_RIGHT]: 
            dx += 1
            has_moved = True

        if keys[pygame.K_UP]: 
            dy -= 1
            has_moved = True

        if keys[pygame.K_DOWN]: 
            dy += 1
            has_moved = True


        if has_moved and self.world.map.is_walkable(self, dx, dy):
            self.world.map.update_position(dx, dy, self)
            
            self.grid_x = dx
            self.grid_y = dy

            self.update_rect()

            return True

        return False
        

    def bomb(self) -> bool:
        '''
        Output: check player key input (space) and drop bomb  
        ''' 

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            Bomb((self.grid_x, self.grid_y), self.world)

            return True
        
        return False


    def is_hit(self):
        '''
        Output: check player sprite collides with any explosion. Return True if collides, otherwise False
        ''' 

        return pygame.sprite.spritecollideany(self, self.world.explosion_group)
    
    def is_dead(self):
        '''
        Output: check player life.
        ''' 

        return self.life <= 0


    def __eq__(self, other):
        return isinstance(other, Player) and other.status == self.status


    def __hash__(self):
        return hash(self.status)