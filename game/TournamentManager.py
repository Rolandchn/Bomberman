import pygame
import sys
from data.entity.AI.AI import IA
from game.GameStatus import GameStatus
from game.GameWorld import GameWorld


class TournamentManager:
    def __init__(self,screen, ia_config, nb_rounds=3):

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
                self.results[ia_name] = 0
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
                    self.results[winner] += 1
                    print(f"{ia1} vs {ia2} -> {winner} gagne en {turns} coups !!!")

        self.show_results()


    def play_match(self, ia1_info, ia2_info):

        ia1_diff, ia1_name = ia1_info
        ia2_diff, ia2_name = ia2_info

        winner_diff, turns = self.play_ia_vs_ia(ia1_diff,ia2_diff)

        # Convertir la difficulté gagnante en IA gagnante
        winner_name = ia1_name if winner_diff == ia1_diff else ia2_name

        return winner_name, turns



    def show_results(self):
        print("\n--- Classement final ---")
        total_victories = sum(self.results.values())

        sorted_results = sorted(self.results.items(), key=lambda x: x[1], reverse=True)
        for ia_name, wins in sorted_results:
            percentage = (wins / total_victories) * 100 if total_victories > 0 else 0
            print(f"{ia_name} → {wins} victoires ({percentage:.2f}%)")

        avg_turns = self.total_turns / self.total_matches if self.total_matches > 0 else 0
        print(f"\nNombre moyen de coups par match : {avg_turns:.2f}")

        print("\n--- Moyenne de coups par IA gagnante ---")
        for ia_name, turns_list in self.ia_turns.items():
            if len(turns_list) > 0:
                avg = sum(turns_list) / len(turns_list)
                print(f"{ia_name} → {avg:.2f} coups en moyenne pour gagner")
            else:
                print(f"{ia_name} → Aucun match gagné")


    def play_ia_vs_ia(self, ia1_diff, ia2_diff):
        self.world = GameWorld()
        self.world.map.generate_map()

        ia1 = IA(self.world.map.get_spawn(GameStatus.P1), GameStatus.P1, self.world, difficulty=ia1_diff)
        ia2 = IA(self.world.map.get_spawn(GameStatus.P2), GameStatus.P2, self.world, difficulty=ia2_diff)

        self.world.player_group.add(ia1, ia2)

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

            # ✅ Affichage du match en live
            font = pygame.font.SysFont(None, 30)
            info = f"{ia1_diff} VS {ia2_diff} - Coups joués : {self.world.turn}"
            text_surface = font.render(info, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20))

            pygame.display.update()

            # Fin de partie
            if ia1.is_dead():
                pygame.time.wait(2000)
                return ia2_diff, self.world.turn

            if ia2.is_dead():
                pygame.time.wait(2000)
                return ia1_diff, self.world.turn

            clock.tick(30)