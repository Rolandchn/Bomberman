from __future__ import annotations
from typing import TYPE_CHECKING
import random
import pygame

if TYPE_CHECKING:
    from game.GameWord import GameWorld

from game.BombermanGame import GameStatus
from game.GameLogic import GameLogic

from data.entity.Entity import Entity
from game.GameAction import Action



class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle)
    #   strong:  min max td4 (strategie: corner the player, reaction to player following, reaction to player fleeing ...)

    def __init__(self, position, status: GameStatus, world: GameWorld, difficulty="facile"):
        super().__init__(position, status, world, world.player_group)

        self.image.fill(self.status.value.value)

        self.difficulty = difficulty
        


    def input(self):
        if self.difficulty == "facile":
            return self.easy_mode()

        elif self.difficulty == "moyen":
            return self.medium_mode()

        elif self.difficulty == "difficile":
            pass #à implementer (minMax)



    '''
    Méthode pour l'IA facile
    '''
    def easy_mode(self):
        '''
        IA Random : déplacement aléatoire + pose bombe aléatoire
        '''
        action = random.choice([Action.MOVE_UP,
                                Action.MOVE_DOWN,
                                Action.MOVE_LEFT,
                                Action.MOVE_RIGHT,
                                Action.PLACE_BOMB])
        
        return GameLogic.apply_action(self.world, self, action)
    

    '''
    Méthode pour l'IA moyen
    '''

    def turn(self, simulated_world: GameWorld):
        '''
        Output: retourne le joueur qui va joue
        '''
        for player in simulated_world.player_group:
            if player.status == simulated_world.turn_status:
                return player


    def actions(self, simulated_world: GameWorld, player: Entity):
        '''
        Output: return all the available actions in one state.
        '''
        actions = [Action.PLACE_BOMB]

        for move in Action.MOVE:
            if simulated_world.map.is_walkable(player, move):
                actions.append(move)

        return actions


    def eval(self, simulated_world: GameWorld):
        '''
        Output: evaluate the game state depending on the AI position.
        '''
        simulated_world.map.generate_valued_grid()

        p: Entity = self.turn(simulated_world)
        ai_x, ai_y = p.grid_x, p.grid_y

        player_x, player_y = simulated_world.map.get_enemie_pos(p)
        
        ai_sgame = simulated_world.map.valued_grid[ai_y][ai_x]
        player_sgame = simulated_world.map.valued_grid[player_y][player_x]

        return ai_sgame - player_sgame


    def result(self):
        '''
        Output: retourne l'état de la partie après une action donnée
        '''
        pass


    def terminal(self, simulated_world: GameWorld):
        '''
        Output: détermine si la partie est terminée (gagnant, perdant, égalité)
        '''
        for player in simulated_world.player_group:
            if pygame.sprite.spritecollideany(player, simulated_world.explosion_group) is not None:
                return True
        
        return False
    
    def result(self, world: GameWorld, action: Action):
        new_world = world.clone()

        player = self.turn(new_world)

        GameLogic.apply_action(new_world, player, action)

        if world.turn_status == GameStatus.P1:
            new_world.turn_status = GameStatus.P2

        if world.turn_status == GameStatus.P2:
            new_world.turn_status = GameStatus.P1
            new_world.turn += 1

        return new_world


    def minmax(self, simulated_world: GameWorld, depth=1):
        if depth < 0 or self.terminal(simulated_world):
            return self.eval(simulated_world), None

        player = self.turn(simulated_world)

        # MIN
        if player.status == GameStatus.P1:
            best_value = 999

            for possible_action in self.actions(simulated_world, player):
                value, _ = self.minmax(self.result(simulated_world, possible_action), depth - 1)

                best_value = min(best_value, value)
            
            return best_value, possible_action
            
        # MAX
        elif player.status == GameStatus.P2:
            best_value = -999

            for possible_action in self.actions(simulated_world, player):
                value, _ = self.minmax(self.result(simulated_world, possible_action), depth - 1)

                best_value = max(best_value, value)
            
            return best_value, possible_action


    def medium_mode(self):
        _, action =  self.minmax(self.world) 
    
        return GameLogic.apply_action(self.world, self, action)



    def clone(self, new_world):
        return IA((self. grid_x, self.grid_y), self.status, new_world)