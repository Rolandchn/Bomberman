
import pygame

from data.texture.Color import Color



class Wall(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, color:Color, size:int):
        super().__init__()

        self.grid_x = x
        self.grid_y = y
        self.color = color

        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = self.grid_x * size
        self.rect.y = self.grid_y * size