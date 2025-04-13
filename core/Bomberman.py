import pygame
from data.entity.Player import Player
from data.entity.Bombe import BombManager
from data.map.Map import Map
from data.entity.Wall import Wall
from data.texture.config import TILE_SIZE

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH



class Game():
    def __init__(self):
        # Initialize general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")
        self.clock = pygame.time.Clock()

        # Initialize Game
        self.map = Map()

        self.players = pygame.sprite.Group()
        self.player = Player(self.map.respawn(), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.players)

        self.bombs = BombManager(self.map)


    def handle_event(self):
        self.player.move(self.map)

    def update(self):
        self.bombs.update()

    def render(self, screen):
        self.map.draw(screen)
        self.bombs.draw(screen)
        self.players.draw(screen)


    def collision(self):
        pass

    def run(self):
        RUNNING = True
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bombs.place_bomb(self.player.grid_x, self.player.grid_y)

            self.handle_event()

            self.update()
            self.render(self.screen)

            pygame.display.update()
            
            self.clock.tick(10)
        
        pygame.quit()
