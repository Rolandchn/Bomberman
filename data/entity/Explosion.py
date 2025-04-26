

import pygame

from typing import Tuple

from data.entity.GameWord import GameWorld

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], world:GameWorld, duration=3):
        self.world = world
        super().__init__(self.world.explosion_group)

        # Position inside the grip in Map
        self.grid_x, self.grid_y = position

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.EXPLOSION.value)

        self.rect = self.image.get_rect(topleft=(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE))

        self.duration = duration


    def update(self):
        self.duration -= 1

        if self.duration <= 0:
            self.kill()

    def groups_to_add(self):
        return ["explosion_group"]