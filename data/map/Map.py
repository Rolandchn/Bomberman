from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.Entity import Entity
    from data.entity.Bombe import Bomb
    from game.GameWorld import GameWorld
    from data.entity.Explosion import Explosion


import pygame

from collections import defaultdict

from game.GameAction import Action
from game.GameStatus import GameStatus

from data.map.structure.Wall import Wall
from data.map.structure.Fire import Fire
from data.map.structure.Floor import Floor
from data.map.structure.Obstacle import Obstacle

from data.texture.config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT


class Map:
    def __init__(self, world: GameWorld):
        self.grid = defaultdict(tuple)
        self.spawn_points = []

        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.world = world
        self.current_margin = 0


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


    def shrink_boundary(self, margin: int):
        self.current_margin = margin
        
        width, height = self.width, self.height

        # Define bounds of the playable area
        min_bound = 1 + self.current_margin
        max_bound_x = width - 1 - self.current_margin  # exclude outer wall
        max_bound_y = height - 1 - self.current_margin

        for x in range(1, width - 1):  # Only within (1, 13)
            for y in range(1, height - 1):
                if x < min_bound or x >= max_bound_x or y < min_bound or y >= max_bound_y:
                    # Place an obstacle to shrink the play area
                    if (x, y) not in self.grid:  # Avoid duplicating
                        self.grid[Fire(x, y, self.world)] = (x, y)



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

