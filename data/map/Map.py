from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.Player import Player
    from data.entity.Entity import Entity
    from data.entity.GameWord import GameWorld


import pygame
import math

from collections import defaultdict

from core.GameStatus import GameStatus

from data.entity.Wall import Wall
from data.entity.Floor import Floor
from data.entity.Obstacle import Obstacle

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Map:
    def __init__(self, world:GameWorld):
        self.grid = defaultdict(list)
        self.valued_grid = []
        self.spawn_point = []

        self.world = world

        self.generate_map()
        self.generate_valued_grid()


    def generate_map(self):
        '''
        Output: Generate wall, floor and obstacle, and store them inside a sprite group in self.world  
        ''' 
        buff = []

        with open("./data/map/map.txt", "r") as map:
            lines = map.read().splitlines()
            for line in lines:
                buff.append(list(line))

        for row, tiles in enumerate(buff):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    self.world.wall_group.add(Wall(col, row, Color.WALL.value, TILE_SIZE))

                elif tile == ".":
                    self.world.floor_group.add(Floor(col, row, Color.GREEN.value, TILE_SIZE))
                
                elif tile == "S":
                    self.world.floor_group.add(Floor(col, row, Color.SPAWN.value, TILE_SIZE))
                    self.spawn_point.append((col, row))
        
                elif tile == "X":
                    obstacle = Obstacle(col, row, Color.OBSTACLE.value, TILE_SIZE)
                    
                    self.world.wall_group.add(obstacle)
                    self.world.floor_group.add(Floor(col, row, Color.GREEN.value, TILE_SIZE))

                    self.grid[(col, row)].append(obstacle)


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
        Output: Update the valued grid with obstacle
        '''
        for wall in self.world.wall_group:
            if isinstance(wall, Wall):
                self.valued_grid[wall.grid_y][wall.grid_x] = 0

            elif isinstance(wall, Obstacle):
                self.valued_grid[wall.grid_y][wall.grid_x] = 50
    


    def update_grid_position(self, entity:Entity, nx:int, ny:int):
        try:
            self.grid[(entity.grid_x, entity.grid_y)].remove(entity)
        
            if len(self.grid[(entity.grid_x, entity.grid_y)]) == 0:
                del self.grid[(entity.grid_x, entity.grid_y)]
        
        except(ValueError):
            pass

        self.grid[(nx, ny)].append(entity)


    def update_grid_explosion(self, obstacle:Obstacle):
            self.grid[(obstacle.grid_x, obstacle.grid_y)].remove(obstacle)
            
            if len(self.grid[(obstacle.grid_x, obstacle.grid_y)]) == 0:
                del self.grid[(obstacle.grid_x, obstacle.grid_y)]


    def is_walkable(self, player:Player, nx:int, ny:int) -> bool:
        '''
        Output: Check if a tile is walkable for the player, return True if it's possible, otherwhise False. 
        '''

        future_rect = player.rect.copy()
        future_rect.topleft = (nx * TILE_SIZE, ny * TILE_SIZE)

        return not pygame.sprite.spritecollideany(player, self.world.wall_group, collided=lambda s1, s2: future_rect.colliderect(s2.rect))


    def respawn(self, entity) -> Tuple[int, int]:
        '''
        Output: return a random spawn point on the map. 
        '''
        if entity.status == GameStatus.P1:
            self.grid[(self.spawn_point[0])].append(entity)

            return self.spawn_point[0]
        
        elif entity.status == GameStatus.P2:
            self.grid[(self.spawn_point[-1])].append(entity)

            return self. spawn_point[-1]
        

    def get_players_pos(self):
        players_pos = []

        for player in self.world.player_group:
            players_pos.append((player.grid_x, player.grid_y))
            
        return players_pos
    

    def get_enemies_pos(self, player: Entity):
        enemies_pos = []

        for p in self.world.player_group:
            if p != player:
                enemies_pos.append((p.grid_x, p.grid_y))

        return enemies_pos

