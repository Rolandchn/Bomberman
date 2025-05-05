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

        self.world = world


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
                    self.grid[Wall(col, row, self.world)] = (col, row)

                elif tile == ".":
                    Floor(col, row, self.world)
                
                elif tile == "S":
                    Floor(col, row, self.world)
                    self.spawn_points.append((col, row))
        
                elif tile == "X":
                    Floor(col, row, self.world)
                    
                    self.grid[Obstacle(col, row, self.world)] = (col, row)


    def generate_valued_grid(self):
        '''
        Output: Generate a valued map with sgame increasing as we go to the center of the map
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

        return pygame.sprite.spritecollideany(entity, self.world.wall_group, collided=lambda s1, s2: future_rect.colliderect(s2.rect)) is None


    def is_bomb_placeable(self, entity):
        return pygame.sprite.spritecollideany(entity, self.world.bomb_group) is None


    def entities_at_position(self, pos):
        return [entity for entity, coord in self.grid.items() if coord == pos]


    def get_obstacles_between(self, start_pos, end_pos):
        visited = set()
        queue = deque()
        queue.append((start_pos, [], []))  # (position, path, obstacles)

        while queue:
            (x, y), path, obstacles = queue.popleft()

            if (x, y) == end_pos:
                return obstacles  # return list of obstacle positions

            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if not (1 <= nx <= 13 and 1 <= ny <= 13):
                    continue
                if next_pos in visited:
                    continue

                entities = self.entities_at_position(next_pos)
                is_solid = any(isinstance(e, Wall) for e in entities)
                is_obstacle = any(isinstance(e, Obstacle) for e in entities)

                if is_solid:
                    continue

                new_obstacles = obstacles.copy()
                if is_obstacle:
                    new_obstacles.append(next_pos)

                queue.append((next_pos, path + [next_pos], new_obstacles))

        return []  # No path found


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

