
import pygame

from data.entity.Obstacle import Obstacle
from data.entity.Explosion import Explosion
from data.entity.GameWord import GameWorld
from data.entity.Entity import Entity

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Bomb(Entity):
    def __init__(self, x:int, y:int, world:GameWorld, timer=2, spread=2):
        super().__init__((x, y), pygame.Surface((TILE_SIZE, TILE_SIZE)), world.bomb_group)

        self.image.fill(Color.BOMBE.value)
        
        self.world = world

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

        Explosion(self.grid_x, self.grid_y, self.world)

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
                    Explosion(nx, ny, self.world)

                