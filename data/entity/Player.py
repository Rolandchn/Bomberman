from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.map.Map import Map


import pygame

from data.entity.Entity import Entity
from data.texture.Color import Color



class Player(Entity):
    def __init__(self, spawn, image, *groups):
        super().__init__(spawn, image, *groups)
        self.image.fill(Color.WHITE.value)


    def move(self, map:Map):
        keys = pygame.key.get_pressed()
        
        dx, dy = self.grid_x, self.grid_y

        if keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_DOWN]: dy += 1

        if map.is_walkable(self, dx, dy):
            self.grid_x = dx
            self.grid_y = dy

            self.update_rect()
        

    def draw(self, screen):
        pygame.draw.rect(screen, Color.BLACK.value, self.rect)