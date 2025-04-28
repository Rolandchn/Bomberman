
import pygame
from data.texture.config import TILE_SIZE


from data.texture.Color import Color


class Floor(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.grid_x = x
        self.grid_y = y

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.GREEN.value)

        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * TILE_SIZE
        self.rect.y = self.grid_y * TILE_SIZE