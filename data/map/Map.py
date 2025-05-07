from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.Entity import Entity
    from data.entity.Bombe import Bomb
    from data.entity.Explosion import Explosion
    from game.GameWorld import GameWorld


import pygame
import math

from collections import defaultdict
from collections import deque

from game.GameAction import Action

from game.GameStatus import GameStatus

from data.map.structure.Wall import Wall
from data.map.structure.Floor import Floor
from data.map.structure.Obstacle import Obstacle

from data.texture.config import TILE_SIZE


class Map:
    def __init__(self, world: GameWorld):
        self.grid = defaultdict(tuple)
        self.valued_grid = []
        self.spawn_points = []

        self.width = 13
        self.height = 13

        self.world = world


    def generate_map(self):
        '''
        Output: Generate wall, floor and obstacle, and store them inside a sprite group in self.world  
        ''' 
        buff = []

        with open("./data/map/map2.txt", "r") as map:
            lines = map.read().splitlines()
            for line in lines:
                buff.append(list(line))

        for row, tiles in enumerate(buff):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    self.grid[Wall(col, row, self.world)] = (col, row)

                elif tile == ".":
                    Floor(col, row, self.world)
                
                elif tile == "S":
                    Floor(col, row, self.world)
                    self.spawn_points.append((col, row))
        
                elif tile == "X":
                    Floor(col, row, self.world)
                    
                    self.grid[Obstacle(col, row, self.world)] = (col, row)


    def update_valued_grid(self):
        '''
        Output: Update the valued grid with obstacle
        '''
        for wall in self.world.wall_group:
            if isinstance(wall, Wall):
                self.valued_grid[wall.grid_y][wall.grid_x] = 0

            elif isinstance(wall, Obstacle):
                self.valued_grid[wall.grid_y][wall.grid_x] = 50
    

    def update_grid_position(self, entity: Entity):
        self.grid[entity] = (entity.grid_x, entity.grid_y)


    def update_grid_obstacle(self, obstacle: Obstacle):
        if obstacle in self.grid: 
            del self.grid[obstacle]


    def update_grid_explosion(self, explosion: Explosion, remove = False):
        if remove and explosion in self.grid:
            del self.grid[explosion]

        else:
            self.grid[explosion] = (explosion.grid_x, explosion.grid_y)


    def update_grid_bomb(self, bomb: Bomb, remove = False):
        if remove and bomb in self.grid:
            del self.grid[bomb]
        
        else:
            self.grid[bomb] = (bomb.grid_y, bomb.grid_x)
        

    def is_walkable(self, entity: Entity, action: Action) -> bool:
        '''
        Output: Check if a tile is walkable for the player, return True if it's possible, otherwhise False. 
        '''

        nx, ny = entity.grid_x, entity.grid_y
        
        if action == Action.MOVE_UP:
            ny -= 1

        elif action == Action.MOVE_DOWN:
            ny += 1

        elif action == Action.MOVE_LEFT:
            nx -= 1

        elif action == Action.MOVE_RIGHT:
            nx += 1

        future_rect = entity.rect.copy()
        future_rect.topleft = (nx * TILE_SIZE, ny * TILE_SIZE)

        for wall in self.world.wall_group:
            if future_rect.colliderect(wall.rect):
                return False

        # --- Vérification autre joueur / IA
        for player in self.world.player_group:
            if player == entity:
                continue  # Ignore soi-même

            if player.grid_x == nx and player.grid_y == ny:
                return False  # Un autre joueur/IA est là


        return True


    def is_bomb_placeable(self, entity):
        return pygame.sprite.spritecollideany(entity, self.world.bomb_group) is None


    def entities_at_position(self, pos):
        return [entity for entity, coord in self.grid.items() if coord == pos]


    def get_spawn(self, status: GameStatus) -> Tuple[int, int]:
        '''
        Output: return a random spawn point on the map. 
        '''
        if status == GameStatus.P1: return self.spawn_points[0]
        elif status == GameStatus.P2: return self. spawn_points[-1]
    

    def get_enemie_pos(self, player: Entity):
        for p in self.world.player_group:
            if p != player:
                return(p.grid_x, p.grid_y)

