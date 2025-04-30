from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld

import pygame
from data.texture.config import TILE_SIZE


from data.texture.Color import Color



class Wall(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, world: GameWorld):
        super().__init__(world.wall_group)

        self.grid_x = x
        self.grid_y = y

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.WALL.value)

        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * TILE_SIZE
        self.rect.y = self.grid_y * TILE_SIZE


    def clone(self, new_world):
        return Wall(self.grid_x, self.grid_y, new_world)