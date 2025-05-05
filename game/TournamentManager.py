import pygame
import sys
from data.entity.AI.IA import IA
from game.GameStatus import GameStatus
from game.GameWorld import GameWorld


class TournamentManager:
    def __init__(self, difficulties, nb_rounds=3):
        self.difficulties = difficulties# Liste des IA ["facile", "moyen", "difficile"]
        self.nb_rounds = nb_rounds
        self.results = {difficulty: 0 for difficulty in difficulties}

    def start(self):
        for ia1_diff in self.difficulties:
            for ia2_diff in self.difficulties:
                if ia1_diff == ia2_diff:
                    continue  # Pas de match contre soi-même

                for round in range(self.nb_rounds):
                    winner = self.play_match(ia1_diff, ia2_diff)
                    self.results[winner] += 1
                    print(f"{ia1_diff} vs {ia2_diff} -> {winner} gagne !")

        self.show_results()

    def play_match(self, ia1_diff, ia2_diff):
        # Créer le monde
        world = GameWorld()
        world.map.generate_map()

        # Créer deux IA avec les difficultés données
        ia1 = IA(world.map.get_spawn(GameStatus.P1),GameStatus.P1, world, difficulty=ia1_diff)
        ia2 = IA(world.map.get_spawn(GameStatus.P2),GameStatus.P2, world, difficulty=ia2_diff)

        world.player_group.add(ia1, ia2)

        # Boucle de jeu jusqu'à ce que l'un meure
        world.turn = 0
        world.turn_status = GameStatus.P1

        clock = pygame.time.Clock()
        while True:
            if world.turn_status == GameStatus.P1:
                ia1.input()
                world.turn_status = GameStatus.P2
            else:
                ia2.input()
                world.turn_status = GameStatus.P1
                world.turn += 1

            world.update(world.turn)

            if ia1.is_dead():
                return ia2_diff
            if ia2.is_dead():
                return ia1_diff

            clock.tick(30)

    def show_results(self):
        print("\n--- Classement final ---")
        sorted_results = sorted(self.results.items(), key=lambda x: x[1], reverse=True)
        for difficulty, wins in sorted_results:
            print(f"{difficulty} → {wins} victoires")