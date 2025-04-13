import pygame

from data.map.Map import Map
from data.entity.Player import Player
from data.entity.EntityManager import EntityManager

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


    def handle_input(self):
        if self.turn_state == "P1":
            if self.player.input(self.map):
                self.turn_state = "P2"

        elif self.turn_state == "P2":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.turn_state = "P1"
                self.turn += 1


    def handle_event(self):
        if self.player.is_hit():
            self.player.life -= 1


    def run(self):
        self.turn = 0

        RUNNING = True
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False

            self.handle_input()
            self.handle_event()

            if self.player.life <= 0:
                self.player.kill()
                self.player = Player(self.map.respawn(), self.entities)

            self.entities.update(self.turn)
            self.entities.draw(self.screen)

            pygame.display.update()
            
            self.clock.tick(10)
        
        pygame.quit()
