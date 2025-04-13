from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.entity.Player import Player


import pygame
import random

from data.texture.config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT
from data.texture.Color import Color
from data.entity.Wall import Wall
from data.entity.Floor import Floor
from data.entity.Obstacle import Obstacle


class Map:
    def __init__(self):
        self.grid = []
        self.spawn_point = []

        self.wall_group = pygame.sprite.Group()
        self.floor_group = pygame.sprite.Group()

        self.read_map()
        self.generate_map()

    def read_map(self):
        with open("./data/map/map.txt", "r") as map:
            for line in map:
                self.grid.append(line)


    def generate_map(self):
        for row, tiles in enumerate(self.grid):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    self.wall_group.add(Wall(row, col, Color.WALL.value, TILE_SIZE))

                elif tile == ".":
                    self.floor_group.add(Floor(row, col, Color.GREEN.value, TILE_SIZE))
                
                elif tile == "S":
                    self.floor_group.add(Floor(row, col, Color.SPAWN.value, TILE_SIZE))
                    self.spawn_point.append((row, col))
        
                elif tile == "X":
                    self.wall_group.add(Obstacle(row, col, Color.OBSTACLE.value, TILE_SIZE))
        

    def is_walkable(self, player:Player, dx, dy):
        future_rect = player.rect.copy()
        future_rect.topleft = (dx * TILE_SIZE, dy * TILE_SIZE)

        return not pygame.sprite.spritecollideany(player, self.wall_group, collided=lambda s1, s2: future_rect.colliderect(s2.rect))



    def explode(self, x, y):
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if self.grid[ny][nx] == "X":
                    self.grid[ny][nx] = " "


    def draw(self, screen):
        self.wall_group.update()
        self.floor_group.update()

        self.wall_group.draw(screen)
        self.floor_group.draw(screen)
        

    def respawn(self):
        return random.choice(self.spawn_point)
    