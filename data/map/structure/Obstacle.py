from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.GameWord import GameWorld


import pygame
from data.texture.config import TILE_SIZE

from data.texture.Color import Color


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.grid_x = x
        self.grid_y = y

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.OBSTACLE.value)

        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * TILE_SIZE
        self.rect.y = self.grid_y * TILE_SIZE


    def kill(self, world: GameWorld):
        world.map.update_grid_explosion(self)

        super().kill()


    def clone(self):
        return Obstacle(self.grid_x, self.grid_y)
    
    def groups_to_add(self):
        return ["wall_group"]