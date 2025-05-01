import sys

import pygame

from game.GameStatus import GameStatus
from game.GameState import GameState
from game.GameWord import GameWorld


from data.entity.Player import Player
from data.entity.IA import IA

from data.texture.Button import Button
from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH


class Game():
    def __init__(self):
        # Initialize general
        pygame.init()

        pygame.display.set_caption("Bomberman")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.selected_difficulty = None
        self.state = GameState.MENU


    def handle_input(self):
        '''
        Output: check turn state and wait for player1 input before switching turn.  
        ''' 

        if self.world.turn_status == GameStatus.P1:
            if self.player1.input():
                self.world.turn_status = GameStatus.P2


        elif self.world.turn_status == GameStatus.P2:
            if self.player2.input():
                self.world.turn_status = GameStatus.P1

                self.world.turn += 1


    def handle_event(self):
        '''
        Output: check if player is hit or is dead. If player died, respawn.  
        ''' 

        if self.player1.is_dead():
            self.is_game_over = True
            self.winner = GameStatus.P2

        if self.player2.is_dead():
            self.is_game_over = True
            self.winner = GameStatus.P1

        if self.player1.is_hit():
            self.player1.life -= 1
        
        if self.player2.is_hit():
            self.player2.life -= 1


    def run(self):
        RUNNING = True

        while RUNNING:
            if self.state == GameState.MENU:
                self.menu()

            elif self.state == GameState.PLAYING:
                self.game()

            elif self.state == GameState.GAME_OVER:
                self.game_over()


    def menu(self):
        """
        Displays the start menu to choose difficulty.
        """
        font = pygame.font.SysFont(None, 60)
        
        self.screen.fill((30, 30, 30))

        # Define buttons once
        easy_btn = Button(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2, "facile")
        medium_btn = Button(SCREEN_HEIGHT // 2, easy_btn.rect.centery + easy_btn.rect.height + 10, "moyen")
        hard_btn = Button(SCREEN_HEIGHT // 2, medium_btn.rect.centery + medium_btn.rect.height + 10, "difficile")

        # Draw title
        title = font.render("Choisissez la difficulté", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        # Draw buttons
        if easy_btn.draw(self.screen):
            self.state = GameState.PLAYING
            self.selected_difficulty = "facile"
            self.restart_game()

        elif medium_btn.draw(self.screen):
            self.state = GameState.PLAYING
            self.selected_difficulty = "moyen"
            self.restart_game()

        elif hard_btn.draw(self.screen):
            self.state = GameState.PLAYING
            self.selected_difficulty = "difficile"
            self.restart_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update()


    def game(self):
        '''
        Output: game loop  
        ''' 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.handle_input()
        self.handle_event()

        print(self.world.turn_status)

        self.world.update(self.world.turn)
        self.world.draw(self.screen)

        if self.is_game_over:
            self.state = GameState.GAME_OVER

        pygame.display.update()
        
        self.clock.tick(40)
        

    def game_over(self):

        '''
        Affiche l'écran de Game Over
        '''
        font = pygame.font.SysFont(None, 80)
        small_font= pygame.font.SysFont(None, 40)

        #texte pour gagnant
        if self.winner == GameStatus.P1: 
            winner_name = "Player 1"
        else: 
            winner_name = "Player 2"
        
        text = font.render(f"{winner_name} wins!", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-100))

        #bouton rejouer
        button_text = small_font.render("Rejouer", True, (255, 255, 255))
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        #affichage
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, rect)

        #Bouton
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Gérer clic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    self.restart_game()
                    self.state = GameState.PLAYING

            pygame.display.update()
            self.clock.tick(40)


    def restart_game(self):
        '''
            Réinitialise la partie (remet tout à zéro)
        '''
        self.world = GameWorld()
        self.world.map.generate_map()

        self.player1 = Player(self.world.map.get_spawn(GameStatus.P1), GameStatus.P1, self.world)
        self.player2 = IA(self.world.map.get_spawn(GameStatus.P2), GameStatus.P2, self.world, difficulty=self.selected_difficulty)

        self.world.turn_status = GameStatus.P1
        self.world.turn = 0

        self.is_game_over = False
        self.winner = None