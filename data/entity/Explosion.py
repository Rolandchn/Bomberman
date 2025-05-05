

import pygame

from typing import Tuple

from game.GameWorld import GameWorld

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], world: GameWorld, duration=1):
        self.world = world
        super().__init__(self.world.explosion_group)

        # Position inside the grip in Map
        self.grid_x, self.grid_y = position

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color.EXPLOSION.value)

        self.rect = self.image.get_rect(topleft=(self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE))

        self.start_turn = self.world.turn
        self.duration = duration


    def update(self, game_turn: int):
        self.world.map.update_grid_explosion(self)
        
        turns_passed = game_turn - self.start_turn

        if self.duration <= turns_passed:
            self.world.map.update_grid_explosion(self, remove=True)
            self.kill()

    def clone(self, new_world):
        return Explosion((self.grid_x, self.grid_y), new_world)