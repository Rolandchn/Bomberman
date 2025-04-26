import pygame


from core.GameStatus import GameStatus

from data.entity.Player import Player
from data.entity.GameWord import GameWorld
from data.texture.Color import Color
from data.entity.IA import IA

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH





class Game():
    def __init__(self):
        # Initialize general
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman")
        self.clock = pygame.time.Clock()

        # Initialize Game
        self.world = GameWorld()

        self.player1 = Player(GameStatus.P1, Color.WHITE, self.world)
        self.ai = IA(GameStatus.P2, Color.BLACK, self.world)
        
        self.turn_status = GameStatus.P1
        self.turn = 0


    def handle_input(self):
        '''
        Output: check turn state and wait for player1 input before switching turn.  
        ''' 

        if self.turn_status == GameStatus.P1:
            if self.player1.input():
                self.turn_status = GameStatus.P2
                

        elif self.turn_status == GameStatus.P2:
            if self.ai.input():
                self.turn_status = GameStatus.P1
                print(self.world.map.grid)
                print("\n\n===============================================")

                self.turn += 1


    def handle_event(self):
        '''
        Output: check if player is hit or is dead. If player died, respawn.  
        ''' 

        if self.player1.is_dead():
                self.player1.kill()
                self.player1 = Player(GameStatus.P1, Color.WHITE, self.world)

        if self.ai.is_dead():
            self.ai.kill()
            self.ai = IA(GameStatus.P2, Color.BLACK, self.world)

        if self.player1.is_hit():
            self.player1.life -= 1
        
        if self.ai.is_hit():
            self.ai.life -= 1


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

            self.world.update(self.turn)
            self.world.draw(self.screen)

            pygame.display.update()
            
            self.clock.tick(40)
        
        pygame.quit()
