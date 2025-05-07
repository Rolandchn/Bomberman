from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

import pygame

from typing import Tuple


from data.map.structure.Obstacle import Obstacle
from data.entity.Explosion import Explosion
from game.GameWorld import GameWorld

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], world: GameWorld, owner: Entity, timer=6, spread=1):
        self.world = world
        super().__init__(self.world.bomb_group, self.world.wall_group)

        # Position inside the grip in Map
        self.grid_x, self.grid_y = position
        self.owner = owner

        self.font = pygame.font.SysFont(None, 24)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.BOMBE.value)

        self.rect = self.image.get_rect(topleft=(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE))
        
        self.start_turn = self.world.turn
        self.timer = timer
        self.spread = spread
        self.tick = 1


    def update(self, game_turn: int):
        '''
        Output: update sprite by turn 
        ''' 
        self.world.map.update_grid_bomb(self)

        self.tick = game_turn - self.start_turn
        
        if self.timer <= self.tick:
            self.kill()
            self.explode()

    def draw(self, game_turn, screen):
        screen.blit(self.image, self.rect)
        
        # Draw timer text on bomb
        timer_text = self.font.render(str(self.timer - (game_turn - self.start_turn)), True, (255, 255, 255)) 
        text_rect = timer_text.get_rect(center=self.rect.center)
        screen.blit(timer_text, text_rect)


    def explode(self):
        '''
        Output: spread the explosion to all direction (up, down, left, right)  
        ''' 

        Explosion((self.grid_x, self.grid_y), self.world)

        # up, down, right, left
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for spread in range(1, self.spread + 1):
                nx, ny = self.grid_x + dx * spread, self.grid_y + dy * spread

                tile_rect = self.rect.copy()
                tile_rect.topleft = (nx * TILE_SIZE, ny * TILE_SIZE)

                collided_wall = pygame.sprite.spritecollideany(self, self.world.wall_group, collided=lambda s1, s2: tile_rect.colliderect(s2.rect))

                # if explosion collides with obstacle, destroy it and remove it from wall_group in world         
                if isinstance(collided_wall, Obstacle):
                    collided_wall.kill(self.world)

                # if explosion collides with nothing, add it to explosion_group in world         
                elif isinstance(collided_wall, Bomb) or collided_wall == None:
                    Explosion((nx, ny), self.world)

    def kill(self):
        self.world.map.update_grid_bomb(self, remove=True)

        super().kill()

    def clone(self, new_world: GameWorld):
        bomb = Bomb((self.grid_x, self.grid_y), new_world, self.owner)
        bomb.start_turn = self.start_turn
        
        return bomb