

import pygame

from data.entity.Entity import Entity
from data.entity.EntityManager import EntityManager

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Explosion(Entity):
    def __init__(self, x:int, y:int, entities:EntityManager, duration=3):
        super().__init__((x, y), pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.explosion_group)

        self.entities = entities
        self.duration = duration

        self.image.fill(Color.EXPLOSION.value)


    def update(self):
        self.duration -= 1

        if self.duration <= 0:
            self.kill()