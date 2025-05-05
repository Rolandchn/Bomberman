
from data.entity.Bombe import Bomb
import pygame


class BombManager:
    def __init__(self, owner, max_bombs=1, bomb_range=2):
        self.owner = owner
        self.max_bombs = max_bombs
        self.bomb_range = bomb_range
        self.active_bombs = []


    def can_place_bomb(self):
        return len(self.active_bombs) < self.max_bombs and pygame.sprite.spritecollideany(self.owner, self.owner.world.bomb_group) is None


    def place_bomb(self, world):
        if not self.can_place_bomb():
            return False

        position = (self.owner.grid_x, self.owner.grid_y)
        bomb = Bomb(position, world, self.owner, spread=self.bomb_range)

        # Hook up removal callback
        bomb.on_explode_callback = self.remove_bomb

        self.active_bombs.append(bomb)

        return True


    def remove_bomb(self, bomb):
        if bomb in self.active_bombs:
            self.active_bombs.remove(bomb)
