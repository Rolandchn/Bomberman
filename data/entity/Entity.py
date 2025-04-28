from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.GameWord import GameWorld


import pygame


from data.texture.config import TILE_SIZE



class Entity(pygame.sprite.Sprite):
    def __init__(self, position: int, world: GameWorld, *groups):
        super().__init__(*groups)

        self.world = world

        self.life = 1
        # Position inside the grip in Map
        self.spawn_point = position
        self.grid_x, self.grid_y = self.spawn_point

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE))


    def update_rect(self):
        self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)


    def is_dead(self):
        '''
        Output: check player life.
        '''
        return self.life <= 0
    
    def is_hit(self):
        '''
        Output: check player sprite collides with any explosion. Return True if collides, otherwise False
        ''' 

        return pygame.sprite.spritecollideany(self, self.world.explosion_group)

    def respawn(self):
        self.life = 1
        self.grid_x, self.grid_y = self.spawn_point

        self.world.map.update_grid_position(self)    