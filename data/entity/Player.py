import pygame
from data.texture.config import TILE_SIZE, BLACK
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def handle_input(self, event, map, bombs):
        if event.type == KEYDOWN:
            dx, dy = 0, 0
            if event.key == K_LEFT:
                dx = -1
            elif event.key == K_RIGHT:
                dx = 1
            elif event.key == K_UP:
                dy = -1
            elif event.key == K_DOWN:
                dy = 1
            elif event.key == K_SPACE:
                bombs.place_bomb(self.x, self.y)
                return

            if map.is_walkable(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

    def draw(self, screen):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, BLACK, rect)