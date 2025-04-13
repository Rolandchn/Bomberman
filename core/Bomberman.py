import pygame
from data.entity.Player import Player
from data.map.Map import Map
from data.entity.EntityManager import EntityManager
from data.texture.config import TILE_SIZE

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH



class Game():
    def __init__(self):
        # Initialize general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")
        self.clock = pygame.time.Clock()

        # Initialize Game
        self.entities = EntityManager()

        self.map = Map(self.entities)
        self.player = Player(self.map.respawn(), self.entities)

        self.turn_state = "P1"


    def handle_event(self):
        if self.turn_state == "P1":
            if self.player.input(self.map):
                self.turn_state = "P1"

        elif self.turn_state == "P2":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.turn_state = "P1"
            

    def collision(self):
        pass

    def run(self):
        RUNNING = True
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False

            print(self.turn_state)
            self.handle_event()

            self.entities.update()
            self.entities.draw(self.screen)

            pygame.display.update()
            
            self.clock.tick(10)
        
        pygame.quit()
