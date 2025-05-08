import sys

import pygame

from game.GameStatus import GameStatus
from game.GameState import GameState
from game.GameWorld import GameWorld
from game.GameLogic import GameLogic
from game.GameAction import Action
from game.TournamentManager import TournamentManager


from data.entity.Player import Player
from data.entity.AI.AI import IA

from data.texture.Button import Button
from data.texture.config import SCREEN_HEIGHT, SCREEN_WIDTH, MAX_TURN, SHRINK_INTERVAL


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
        if self.player1.is_hit():
            self.player1.life -= 1
        
        if self.player2.is_hit():
            self.player2.life -= 1

        if self.player1.is_dead():
            self.is_game_over = True
            self.winner = GameStatus.P2

        if self.player2.is_dead():
            self.is_game_over = True
            self.winner = GameStatus.P1

        if self.world.turn > MAX_TURN and (self.world.turn - MAX_TURN) % SHRINK_INTERVAL == 0:
            self.SHRINK_MARGIN = (self.world.turn - MAX_TURN) // SHRINK_INTERVAL
            self.world.map.shrink_boundary(self.SHRINK_MARGIN)


    def run(self):
        RUNNING = True

        while RUNNING:
            if self.state == GameState.MENU:
                self.menu()

            elif self.state == GameState.PLAYING:
                self.game()

            elif self.state == GameState.GAME_OVER:
                self.game_over()
            
            elif self.state == GameState.TOURNAMENT:
                self.tournament()


    def menu(self):
        """
        Displays the start menu to choose difficulty.
        """
        font = pygame.font.SysFont(None, 60)
        
        self.screen.fill((30, 30, 30))

        # Define buttons once
        easy_btn = Button(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2, "Facile")
        medium_btn = Button(SCREEN_HEIGHT // 2, easy_btn.rect.centery + easy_btn.rect.height + 10, "Moyen")
        hard_btn = Button(SCREEN_HEIGHT // 2, medium_btn.rect.centery + medium_btn.rect.height + 10, "Difficile")
        tournament_btn = Button(SCREEN_HEIGHT // 2, hard_btn.rect.centery + hard_btn.rect.height + 10, "Tournois Bot")

        # Draw title
        title = font.render("Choisissez la difficulté", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        # Draw buttons
        easy_btn.draw(self.screen)
        medium_btn.draw(self.screen)
        hard_btn.draw(self.screen)
        tournament_btn.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if easy_btn.handle_event(event):
                self.state = GameState.PLAYING
                self.selected_difficulty = "facile"
                self.restart_game()

            elif medium_btn.handle_event(event):
                self.state = GameState.PLAYING
                self.selected_difficulty = "moyen"
                self.restart_game()

            elif hard_btn.handle_event(event):
                self.state = GameState.PLAYING
                self.selected_difficulty = "difficile"
                self.restart_game()

            elif tournament_btn.handle_event(event):
                self.state = GameState.TOURNAMENT

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

        self.world.update(self.world.turn)
        
        self.handle_event()
        
        self.world.draw(self.screen)

        if self.is_game_over:
            self.state = GameState.GAME_OVER

        pygame.display.update()
        
        self.clock.tick(60)
        

    def game_over(self):

        '''
        Affiche l'écran de Game Over
        '''
        font = pygame.font.SysFont(None, 80)

        #affichage
        self.screen.fill((0, 0, 0))
        
        #texte pour gagnant
        if self.winner == GameStatus.P1: winner_name = "Player 1"
        else: winner_name = "Player 2"
        
        text = font.render(f"{winner_name} wins!", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-100))

        self.screen.blit(text, rect)
        
        #bouton rejouer
        replay_btn = Button(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2, "Rejouer")
        menu_btn = Button(SCREEN_HEIGHT // 2, replay_btn.rect.centery + replay_btn.rect.height + 10, "Menu")

        #Bouton
        replay_btn.draw(self.screen)
        menu_btn.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if replay_btn.handle_event(event):
                self.state = GameState.PLAYING
                self.restart_game()

            if menu_btn.handle_event(event):
                self.state = GameState.MENU

            pygame.display.update()


    def tournament(self):
        # Afficher un fond + texte pendant le tournoi
        self.screen.fill((30, 30, 30))

        font = pygame.font.SysFont(None, 60)
        text = font.render("Tournoi IA en cours...", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        pygame.display.update()

        tournament = TournamentManager(["facile", "moyen", "difficile"], nb_rounds=3)
        tournament.start()

        print("tournament")

        # Une fois le tournoi terminé, retourner au menu
        self.state = GameState.MENU
        

    def restart_game(self):
        '''
            Réinitialise la partie (remet tout à zéro)
        '''
        self.world = GameWorld()
        self.world.map.generate_map()

        self.player1 = IA(self.world.map.get_spawn(GameStatus.P1), GameStatus.P1, self.world, difficulty=self.selected_difficulty)
        self.player2 = IA(self.world.map.get_spawn(GameStatus.P2), GameStatus.P2, self.world, difficulty=self.selected_difficulty)


        self.world.turn_status = GameStatus.P1
        self.world.turn = 0

        self.world.update(self.world.turn)

        self.SHRINK_MARGIN = (self.world.turn - MAX_TURN) // SHRINK_INTERVAL
        
        self.is_game_over = False
        self.winner = None

    @staticmethod
    def test():
        world = GameWorld()
        world.map.generate_map()

        player1 = Player(world.map.get_spawn(GameStatus.P1), GameStatus.P1, world)
        player2 = IA(world.map.get_spawn(GameStatus.P2), GameStatus.P2, world, difficulty="moyen")

        world.turn = 0
        world.turn_status = GameStatus.P1
        GameLogic.apply_action(world, player1, Action.MOVE_RIGHT)

        world.turn_status = GameStatus.P2
        
        player2.input()

        print("end")