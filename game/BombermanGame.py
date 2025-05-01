import sys

import pygame

from game.GameStatus import GameStatus

from data.entity.Player import Player
from game.GameWord import GameWorld
from data.entity.IA import IA

from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH


class Game():
    def __init__(self):
        # Initialize general
        pygame.init()

        pygame.display.set_caption("Bomberman")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.selected_difficulty = None
        self.show_menu()

        # Initialize Game
        self.restart_game()

        self.once= True


    def handle_input(self):
        '''
        Output: check turn state and wait for player1 input before switching turn.  
        ''' 

        if self.world.turn_status == GameStatus.P1:
            if self.player1.input():
                self.world.turn_status = GameStatus.P2

                self.world.turn += 1

        elif self.world.turn_status == GameStatus.P2:
            if self.once:
                print(self.player2.minmax(self.world))
                self.once = False

            return
            if self.player2.input() :
                self.world.turn_status = GameStatus.P1



    def handle_event(self):
        '''
        Output: check if player is hit or is dead. If player died, respawn.  
        ''' 

        if self.player1.is_dead():
            self.game_over = True
            self.winner = GameStatus.P2

        if self.player2.is_dead():
            self.game_over = True
            self.winner = GameStatus.P1

        if self.player1.is_hit():
            self.player1.life -= 1
        
        if self.player2.is_hit():
            self.player2.life -= 1


    def run(self):
        '''
        Output: game loop  
        ''' 

        self.world.turn = 0

        RUNNING = True
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_over:
                self.handle_input()
                self.handle_event()

                self.world.update(self.world.turn)
                self.world.draw(self.screen)

            else :
                self.display_game_over()

            pygame.display.update()
            
            self.clock.tick(40)
        

    def display_game_over(self):

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

        self.game_over = False
        self.winner = None



    def show_menu(self):
        '''
        Affiche le menu de démarrage pour choisir la difficulté
        '''
        font = pygame.font.SysFont(None, 60)
        small_font = pygame.font.SysFont(None, 40)

        RUNNING = True
        while RUNNING:
            self.screen.fill((30, 30, 30))

            title = font.render("Choisissez la difficulté", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(title, title_rect)

            # Boutons
            buttons = [
                ("Facile", "facile", SCREEN_HEIGHT // 2 - 20),
                ("Moyen", "moyen", SCREEN_HEIGHT // 2 + 40),
                ("Difficile", "difficile", SCREEN_HEIGHT // 2 + 100),
            ]

            for label, difficulty, y in buttons:
                btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y, 200, 40)
                pygame.draw.rect(self.screen, (50, 150, 50), btn_rect)
                text = small_font.render(label, True, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=btn_rect.center))

                # Gérer clic
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_rect.collidepoint(event.pos):
                            self.selected_difficulty = difficulty
                            RUNNING = False

            pygame.display.update()
            self.clock.tick(60)