
import pygame
import random
from data.texture.config import TILE_SIZE, GRAY, BROWN, GRID_WIDTH, GRID_HEIGHT

class Map:
    def __init__(self):
        self.grid = [[" " for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.generate_walls()

    def generate_walls(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if x == 0 or y == 0 or x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1 or (x % 2 == 0 and y % 2 == 0):
                    self.grid[y][x] = "#"
                elif random.random() < 0.3 and not (x <= 2 and y <= 2):
                    self.grid[y][x] = "X"

    def is_walkable(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.grid[y][x] == " "
        return False

    def explode(self, x, y):
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if self.grid[ny][nx] == "X":
                    self.grid[ny][nx] = " "

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile = self.grid[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "#":
                    pygame.draw.rect(screen, GRAY, rect)
                elif tile == "X":
                    pygame.draw.rect(screen, BROWN, rect)