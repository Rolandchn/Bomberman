from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.Player import Player
    from data.entity.EntityManager import EntityManager


import pygame
import random

from data.entity.Wall import Wall
from data.entity.Floor import Floor
from data.entity.Obstacle import Obstacle

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Map:
    def __init__(self, entities:EntityManager):
        self.grid = []
        self.spawn_point = []

        self.entities = entities

        self.read_map()
        self.generate_map()


    def read_map(self):
        '''
        Output: Read the map.txt file and store the content in grid
        '''

        with open("./data/map/map.txt", "r") as map:
            for line in map:
                self.grid.append(line)


    def generate_map(self):
        '''
        Output: Generate wall, floor and obstacle, and store them inside a sprite group in self.entities  
        ''' 

        for row, tiles in enumerate(self.grid):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    self.entities.wall_group.add(Wall(col, row, Color.WALL.value, TILE_SIZE))

                elif tile == ".":
                    self.entities.floor_group.add(Floor(col, row, Color.GREEN.value, TILE_SIZE))
                
                elif tile == "S":
                    self.entities.floor_group.add(Floor(col, row, Color.SPAWN.value, TILE_SIZE))
                    self.spawn_point.append((col, row))
        
                elif tile == "X":
                    self.entities.wall_group.add(Obstacle(col, row, Color.OBSTACLE.value, TILE_SIZE))
                    self.entities.floor_group.add(Floor(col, row, Color.GREEN.value, TILE_SIZE))

        

    def is_walkable(self, player:Player, dx:int, dy:int) -> bool:
        '''
        Output: Check if a tile is walkable for the player, return True if it's possible, otherwhise False. 
        '''

        future_rect = player.rect.copy()
        future_rect.topleft = (dx * TILE_SIZE, dy * TILE_SIZE)

        return not pygame.sprite.spritecollideany(player, self.entities.wall_group, collided=lambda s1, s2: future_rect.colliderect(s2.rect))


    def respawn(self) -> Tuple[int, int]:
        '''
        Output: return a random spawn point on the map. 
        '''
        
        return random.choice(self.spawn_point)
    