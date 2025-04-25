from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.Player import Player
    from data.entity.Entity import Entity
    from data.entity.EntityManager import EntityManager


import pygame
import random
import math

from data.entity.Wall import Wall
from data.entity.Floor import Floor
from data.entity.Obstacle import Obstacle

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Map:
    def __init__(self, entities:EntityManager):
        self.grid = []
        self.valued_grid = []
        self.spawn_point = []

        self.entities = entities

        self.generate_map()
        self.generate_valued_grid()


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
        self.read_map()

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


    def generate_valued_grid(self):
        '''
        Output: Generate a valued map with score increasing as we go to the center of the map
        '''

        nb_grid = (13, 13)
        nb_row, nb_column = nb_grid

        # add map border = 0
        self.valued_grid.append([0 for i in range(nb_row + 2)])
        self.valued_grid.append([0 for i in range(nb_row + 2)])

        column_increment = 0

        for row in range(math.ceil(nb_row / 2)):
            # add map border = 0
            buff = [0, 0]
            
            for column_value in range(math.ceil(nb_column / 2)):
                buff.insert(len(buff) // 2, column_value * 100 + column_increment)
                buff.insert(len(buff) // 2, column_value * 100 + column_increment)

            if nb_column % 2 != 0:
                buff.pop(len(buff) // 2)

            self.valued_grid.insert(len(self.valued_grid) // 2, buff)
            self.valued_grid.insert(len(self.valued_grid) // 2, buff)

            column_increment += 100

        if nb_row % 2 != 0:
            self.valued_grid.pop(len(self.valued_grid) // 2)
        

    def update_valued_grid(self):
        '''
        Output: Update the valued grid with player position and obstacle
        '''
        for wall in self.entities.wall_group:
            if isinstance(wall, Wall):
                self.valued_grid[wall.grid_y][wall.grid_x] = 0

            elif isinstance(wall, Obstacle):
                self.valued_grid[wall.grid_y][wall.grid_x] = 50
        


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
    
    def get_players_pos(self):
        players_pos = []

        for player in self.entities.player_group:
            players_pos.append((player.grid_x, player.grid_y))
            
        return players_pos
    
    def get_enemies_pos(self, player: Entity):
        enemies_pos = []

        for p in self.entities.player_group:
            if p != player:
                enemies_pos.append((p.grid_x, p.grid_y))

        return enemies_pos