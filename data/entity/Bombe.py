
import pygame

from data.texture.config import TILE_SIZE
from data.texture.Color import Color
from data.entity.Entity import Entity
from data.entity.EntityManager import EntityManager
from data.entity.Obstacle import Obstacle
from data.entity.Explosion import Explosion



class Bomb(Entity):
    def __init__(self, x, y, entities:EntityManager, timer=2, spread=2):
        super().__init__((x, y), pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.bomb_group)

        self.image.fill(Color.BOMBE.value)
        
        self.entities = entities

        self.timer = timer
        self.spread = spread


    def update(self):
        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            self.explode()


    def explode(self):
        Explosion(self.grid_x, self.grid_y, self.entities)

        # up, down, right, left
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for spread in range(1, self.spread):
                nx, ny = self.grid_x + dx * spread, self.grid_y + dy * spread

                tile_rect = self.rect.copy()
                tile_rect.topleft = (nx * TILE_SIZE, ny * TILE_SIZE)

                collided_wall = pygame.sprite.spritecollideany(self, self.entities.wall_group, collided=lambda s1, s2: tile_rect.colliderect(s2.rect))
                
                print(collided_wall)
                if isinstance(collided_wall, Obstacle):
                    print("aaaa")
                    collided_wall.kill()
                
                elif collided_wall == None:
                    Explosion(nx, ny, self.entities)

                