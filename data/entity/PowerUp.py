from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld


import pygame

from enum import Enum, auto
from data.texture.config import TILE_SIZE

class PowerUpType(Enum):
    RANGE = auto()
    KICK = auto()
    EXTRA_BOMB = auto()
    REMOTE = auto()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, position, world: GameWorld):
        super().__init__(world.powerup_group)
        self.grid_x, self.grid_y = position
        self.rect = pygame.Rect(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.image = self.get_image()


    def get_image(self):
        raise NotImplementedError
        

class ExtraBomb(PowerUp):
    def get_image(self):
        raw_image = pygame.image.load("assets/powerups/extra_bomb.png").convert_alpha()
        return pygame.transform.scale(raw_image, (TILE_SIZE, TILE_SIZE))


class BombRange(PowerUp):
    def get_image(self):
        raw_image = pygame.image.load("assets/powerups/range_up.png").convert_alpha()
        return pygame.transform.scale(raw_image, (TILE_SIZE, TILE_SIZE))