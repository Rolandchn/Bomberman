
import pygame

from typing import Tuple


from data.entity.Obstacle import Obstacle
from data.entity.Explosion import Explosion
from data.entity.GameWord import GameWorld

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], world:GameWorld, timer=2, spread=2):
        self.world = world
        super().__init__(self.world.bomb_group)

        # Position inside the grip in Map
        self.grid_x, self.grid_y = position

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.BOMBE.value)

        self.rect = self.image.get_rect(topleft=(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE))
        
        self.start_turn = None
        self.timer = timer
        self.spread = spread


    def update(self, game_turn:int):
        '''
        Output: update sprite by turn 
        ''' 

        if self.start_turn is None:
            self.start_turn = game_turn

        turns_passed = game_turn - self.start_turn
        
        if self.timer < turns_passed:
            self.kill()
            self.explode()


    def explode(self):
        '''
        Output: spread the explosion to all direction (up, down, left, right)  
        ''' 

        Explosion((self.grid_x, self.grid_y), self.world)

        # up, down, right, left
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for spread in range(1, self.spread):
                nx, ny = self.grid_x + dx * spread, self.grid_y + dy * spread

                tile_rect = self.rect.copy()
                tile_rect.topleft = (nx * TILE_SIZE, ny * TILE_SIZE)

                collided_wall = pygame.sprite.spritecollideany(self, self.world.wall_group, collided=lambda s1, s2: tile_rect.colliderect(s2.rect))

                # if explosion collides with obstacle, destroy it and remove it from wall_group in world         
                if isinstance(collided_wall, Obstacle):
                    collided_wall.kill()

                # if explosion collides with nothing, add it to explosion_group in world         
                elif collided_wall == None:
                    Explosion((nx, ny), self.world)

                