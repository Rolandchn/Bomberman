import pygame
from data.texture.config import TILE_SIZE


class Entity(pygame.sprite.Sprite):
    def __init__(self, spawn, image:pygame.Surface, *groups):
        super().__init__(*groups)

        self.image = image
        
        self.rect = self.image.get_rect(topleft=(spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE))
        
        # Position inside the grip in Map
        self.grid_x = spawn[0]
        self.grid_y = spawn[1]


    def update_rect(self):
        self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)
