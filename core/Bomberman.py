import pygame

from enum import Enum

from data.map.Map import Map
from data.entity.Player import Player
from data.entity.EntityManager import EntityManager
from data.texture.Color import Color
from data.entity.IA import IA

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH


class GameTurn(Enum):
    PLAYER = 0
    IA = 1


class Game():
    def __init__(self):
        # Initialize general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")
        self.clock = pygame.time.Clock()

        self.ia_move_delay = 500  # millisecondes
        self.last_ia_move_time = pygame.time.get_ticks()

        # Initialize Game
        self.entities = EntityManager()

        self.map = Map(self.entities)

        self.player1 = Player(Color.WHITE, self.map.spawn_point[0], self.entities)
        self.player2 = IA(Color.BLACK, self.map.spawn_point[-1], self.entities, self.map, difficulty="facile")
        
        self.turn_state = GameTurn.PLAYER
        self.turn = 0


    def handle_input(self):
        '''
        Output: check turn state and wait for player1 input before switching turn.  
        ''' 

        if self.turn_state == GameTurn.PLAYER:
            if self.player1.input(self.map):
                self.turn_state = GameTurn.IA

        elif self.turn_state == GameTurn.IA:
            if self.player2.input():
                self.turn_state = GameTurn.PLAYER

                self.turn += 1



    def handle_event(self):
        '''
        Output: check if player is hit or is dead. If player died, respawn.  
        ''' 

        if self.player1.is_dead():
                self.player1.kill()
                self.player1 = Player(Color.WHITE, self.map.spawn_point[0], self.entities)


        if self.player2.is_dead():
            self.player2.kill()
            self.player2 = IA(Color.BLACK, self.map.spawn_point[-1], self.entities, self.map, difficulty="facile")

        if self.player1.is_hit():
            self.player1.life -= 1
        
        if self.player2.is_hit():
            self.player2.life -= 1


    def run(self):
        '''
        Output: game loop  
        ''' 

        self.turn = 0

        RUNNING = True
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False

            self.handle_input()
            self.handle_event()

            self.entities.update(self.turn)
            self.entities.draw(self.screen)

            pygame.display.update()
            
            self.clock.tick(10)
        
        pygame.quit()
