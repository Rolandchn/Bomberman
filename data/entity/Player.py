from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.map.Map import Map
    from data.entity.EntityManager import EntityManager


import pygame

from data.entity.Entity import Entity
from data.entity.Bombe import Bomb

from data.texture.Color import Color
from data.texture.config import TILE_SIZE



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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            Bomb(self.grid_x, self.grid_y, self.entities)

            return True
        
        return False


    def handle_input(self, map:Map):
        self.move(map)
        self.bomb()


    def is_hit(self):
        return pygame.sprite.spritecollideany(self, self.entities.explosion_group)