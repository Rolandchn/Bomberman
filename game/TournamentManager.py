import pygame
import sys
from data.entity.AI.AI import IA
from data.texture.config import MAX_TURN, SHRINK_INTERVAL, SCREEN_WIDTH, SCREEN_HEIGHT
from game.GameStatus import GameStatus
from game.GameWorld import GameWorld


class TournamentManager:
    def __init__(self,screen, ia_config, nb_rounds=3):

        self.match_history = []
        self.SHRINK_MARGIN = None
        self.world = None
        self.screen= screen
        self.ia_config = ia_config
        self.nb_rounds = nb_rounds

        #on initialiseles données
        self.results = {}
        self.total_matches = 0
        self.total_turns = 0
        self.ia_turns = {}

        # Générer IA
        for difficulty in ia_config:
            for i in range(1, ia_config[difficulty] + 1):
                ia_name = f"{difficulty}_IA{i}"
                self.results[ia_name] = {"wins" :0, "total_turns": []}
                self.ia_turns[ia_name] = []


    def start(self):
        #On génère toutes les IA
        ia_names = []
        for difficulty in self.ia_config:
            for i in range(1, self.ia_config[difficulty] + 1):
                ia_names.append((difficulty, f"{difficulty}_IA{i}"))

        for ia1 in ia_names:
            for ia2 in ia_names:
                if ia1==ia2:
                    continue

                for round in range(self.nb_rounds):
                    winner,turns = self.play_match(ia1, ia2)
                    # Enregistrement des stats
                    self.results[winner]["wins"] += 1
                    self.results[winner]["total_turns"].append(turns)
                    print(f"{ia1} vs {ia2} -> {winner} gagne en {turns} coups !!!")

        self.show_results()


    def play_match(self, ia1_info, ia2_info):


        ia1_diff, ia1_name = ia1_info
        ia2_diff, ia2_name = ia2_info

        winner_diff, turns = self.play_ia_vs_ia(ia1_diff,ia2_diff)

        # Convertir la difficulté gagnante en IA gagnante
        winner_name = ia1_name if winner_diff == ia1_diff else ia2_name

        self.ia_turns[winner_name].append(turns)
        self.total_turns += turns
        self.total_matches += 1

        self.match_history.append({
            "ia1": ia1_diff,
            "ia2": ia2_diff,
            "winner": winner_name,
            "turns": turns
        })

        return winner_name, turns


    def play_ia_vs_ia(self, ia1_diff, ia2_diff):
        self.world = GameWorld()
        self.world.map.generate_map()

        ia1 = IA(self.world.map.get_spawn(GameStatus.P1), GameStatus.P1, self.world, difficulty=ia1_diff)
        ia2 = IA(self.world.map.get_spawn(GameStatus.P2), GameStatus.P2, self.world, difficulty=ia2_diff)

        self.world.player_group.add(ia1, ia2)
        self.world.update(self.world.turn)


        self.world.turn = 0
        self.world.turn_status = GameStatus.P1

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.world.turn_status == GameStatus.P1:
                ia1.input()
                self.world.turn_status = GameStatus.P2
            else:
                ia2.input()
                self.world.turn_status = GameStatus.P1
                self.world.turn += 1

            self.world.update(self.world.turn)
            self.world.draw(self.screen)

            # Affichage du match en live
            font = pygame.font.SysFont(None, 30)
            info = f"{ia1_diff} VS {ia2_diff} - Coups joués : {self.world.turn}"
            text_surface = font.render(info, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20))

            pygame.display.update()

            #gestion des coups
            if ia1.is_hit():
                ia1.life -= 1
            if ia2.is_hit():
                ia2.life -= 1

                # Fin de partie
            if ia1.is_dead():
                pygame.time.wait(2000)
                return ia2_diff, self.world.turn

            if ia2.is_dead():
                pygame.time.wait(2000)
                return ia1_diff, self.world.turn

            # Gestion du rétrécissement
            if self.world.turn > MAX_TURN and (self.world.turn - MAX_TURN) % SHRINK_INTERVAL == 0:
                self.SHRINK_MARGIN = (self.world.turn - MAX_TURN) // SHRINK_INTERVAL
                self.world.map.shrink_boundary(self.SHRINK_MARGIN)

            clock.tick(30)


    def show_results(self):
        self.screen.fill((20, 20, 20))
        font = pygame.font.SysFont(None, 30)
        big_font = pygame.font.SysFont(None, 48)

        # Titre
        title = big_font.render("Résultats du Tournoi", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 40)))
        print("\n--- Classement final ---")
        y = 100

        # Total des victoires
        total_victories = sum(stats["wins"] for stats in self.results.values())

        # Classement par nombre de victoires décroissant
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]["wins"], reverse=True)

        for i,(ia_name, stats) in enumerate(sorted_results, start=1):
            wins = stats["wins"]
            percentage = (wins / total_victories) * 100 if total_victories > 0 else 0
            #Affichage console
            print(f"{ia_name} → {wins} victoires ({percentage:.2f}%)")
            #affichage ecran
            line = f"{i}. {ia_name} — {stats['wins']} victoires ({percentage:.2f}%)"
            text = font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (50, y))
            y += 40


        #details des matchs
        y += 20
        detail_title = font.render("Détails des matchs :", True, (255, 255, 255))
        self.screen.blit(detail_title, (50, y))
        y += 40

        for match in self.match_history:
            line = f"{match['ia1']} vs {match['ia2']} --> Gagnant : {match['winner']} en {match['turns']} coups"
            text = font.render(line, True, (180, 180, 180))
            self.screen.blit(text, (50, y))
            y += 40
            if y > SCREEN_HEIGHT - 100:  # Limite d'affichage
                break



        # Moyenne générale des coups par match
        avg_turns = self.total_turns / self.total_matches if self.total_matches > 0 else 0
        #console
        print(f"\nNombre moyen de coups par match : {avg_turns:.2f}")
        #ecran
        line = f"Nombre moyen de coups par match : {avg_turns:.2f}"
        text = font.render(line, True, (180, 180, 180))
        self.screen.blit(text, (50, y))
        y += 40


        # Moyenne de coups par IA gagnante
        print("\n--- Moyenne de coups par IA gagnante ---")
        #ecran
        title = font.render("Moyenne de coups par IA gagnante :", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, y + 20)))
        y += 40

        for ia_name, stats in self.results.items():
            turns = stats["total_turns"]
            if len(turns) > 0:
                avg = sum(turns) / len(turns)

                print(f"{ia_name} → {avg:.2f} coups en moyenne pour gagner")
                line = f"{ia_name} --> {avg:.2f} coups en moyenne pour gagner"

            else:
                print(f"{ia_name} → Aucun match gagné")
                line = f"{ia_name} --> Aucun match gagné"

            text = font.render(line, True, (180, 180, 180))
            self.screen.blit(text, (50, y))
            y += 30

        # Bouton "Retour Menu"
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect, border_radius=10)
        button_text = font.render("Retour Menu", True, (255, 255, 255))
        self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.display.update()

        # Boucle d'attente pour interaction
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False