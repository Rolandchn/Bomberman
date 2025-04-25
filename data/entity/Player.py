from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.map.Map import Map
    from data.entity.EntityManager import EntityManager


import pygame

from enum import Enum, auto

from data.entity.Entity import Entity
from data.entity.Bombe import Bomb

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class PlayerStatus(Enum):
    P1: int = auto()
    P2: int = auto()
    P3: int = auto()
    P4: int = auto()
    IA: int = auto()


class Player(Entity):
    def __init__(self, spawn:Tuple[int, int], entities:EntityManager):
        super().__init__(spawn, pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.player_group)

        self.life = 1

        self.entities = entities

        self.image.fill(Color.WHITE.value)


    
    def input(self, map:Map) -> bool:
        if self.move(map) : return True
        elif self.bomb() : return True

        return False
    

    def move(self, map:Map) -> bool:
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


        if map.is_walkable(self, dx, dy):
            self.grid_x = dx
            self.grid_y = dy

            self.update_rect()
            
        return has_moved
        

    def bomb(self) -> bool:
        '''
        Output: check player key input (space) and drop bomb  
        ''' 

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            Bomb(self.grid_x, self.grid_y, self.entities)

            return True
        
        return False


    def handle_input(self, map:Map):
        '''
        Output: check player key input
        ''' 

        self.move(map)
        self.bomb()


    def is_hit(self):
        '''
        Output: check player sprite collides with any explosion. Return True if collides, otherwise False
        ''' 

        return pygame.sprite.spritecollideany(self, self.entities.explosion_group)
    
    def is_dead(self):
        '''
        Output: check player life.
        ''' 

        return self.life <= 0
    
 