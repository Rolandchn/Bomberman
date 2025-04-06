
import pygame
from data.texture.config import BOMB_TIMER, EXPLOSION_DURATION, TILE_SIZE, RED


class BombManager:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.bombs = []
        self.explosions = []

    def place_bomb(self, x, y):
        self.bombs.append({'pos': (x, y), 'time': pygame.time.get_ticks()})

    def update(self):
        now = pygame.time.get_ticks()

        for bomb in self.bombs[:]:
            if now - bomb['time'] >= BOMB_TIMER:
                x, y = bomb['pos']
                self.explosions.append({'pos': (x, y), 'time': now})
                self.tilemap.explode(x, y)
                self.bombs.remove(bomb)

        for exp in self.explosions[:]:
            if now - exp['time'] >= EXPLOSION_DURATION:
                self.explosions.remove(exp)

    def draw(self, screen):
        for bomb in self.bombs:
            x, y = bomb['pos']
            pygame.draw.circle(screen, RED, (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), TILE_SIZE // 3)

        for exp in self.explosions:
            x, y = exp['pos']
            pygame.draw.rect(screen, RED, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))