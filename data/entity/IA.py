from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.EntityManager import EntityManager


import pygame

from data.entity.Entity import Entity

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  follow td4 (strategie: take the center, destroy obstacle, corner the player, ...)
    def __init__(self, spawn:Tuple[int, int], entities:EntityManager):
        super().__init__(spawn, pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.player_group)

        self.life = 1

        self.entities = entities

        self.image.fill(Color.BLACK.value)
