from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from game.GameWord import GameWorld

from game.BombermanGame import GameStatus
from game.GameLogic import GameLogic

from data.entity.Entity import Entity
from game.GameAction import Action
from data.entity.Bombe import Bomb



class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle, corner the player, ...)

    def __init__(self, status: GameStatus, world: GameWorld, difficulty="facile"):
        self.status = status
        super().__init__(world.map.get_respawn(self.status), world, world.player_group)

        self.image.fill(self.status.value.value)

        self.difficulty = difficulty
        


    def input(self):
        if self.difficulty == "facile":
            return self.random_turn()

        elif self.difficulty == "moyen":
            pass #à implementer

        elif self.difficulty == "difficile":
            pass #à implementer (minMax)


    def turn(self):
        '''
        retourne le joueur qui va joue en fonction de la difficulté
        '''

        pass


    def action(self):
        '''
        Output: return all the available actions in one state.
        '''

        pass

    def eval(self, game_state):
        '''
        Output: evaluate the game state depending on the AI position.
        '''
        ai_x, ai_y = self.grid_x, self.grid_y
        player_x, player_y = self.world.map.get_enemies_pos(self)
        
        ai_sgame = self.world.map.valued_grid[ai_y][ai_x]
        player_sgame = self.world.map.valued_grid[player_y][player_x]

        return ai_sgame - player_sgame


    def value(self):
        '''
        Output: retourne une value à une position de la partie (négatif perd, 0 neutre, positif gagne) 
        '''
        pass

    def result(self):
        '''
        Output: retourne l'état de la partie après une action donnée
        '''
        pass

    def terminal(self, simulated_world: GameWorld):
        '''
        Output détermine si la partie est terminée (gagnant, perdant, égalité)
        '''
        for player in simulated_world.player_group:
            if simulated_world.map.grid.get(player) is None:
                return True
        
        return False


    def minmax(self):
        simulated_world = self.world.clone()

        if self.terminal(simulated_world):
            pass



    '''
    Méthode pour l'IA random
    '''
    def random_turn(self):
        '''
        IA Random : déplacement aléatoire + pose bombe aléatoire
        '''
        action = random.choice([Action.MOVE_UP,
                                Action.MOVE_DOWN,
                                Action.MOVE_LEFT,
                                Action.MOVE_RIGHT,
                                Action.PLACE_BOMB])
        
        return GameLogic.apply_action(self.world, self, action)
    

    def clone(self, new_world):
        copy = IA(self.status, new_world)
        
        copy.grid_x = self.grid_x
        copy.grid_y = self.grid_y
        copy.rect = self.rect

        return copy
    
    def groups_to_add(self):
        return ["player_group"]


    def __eq__(self, other):
        return isinstance(other, IA) and other.status == self.status


    def __hash__(self):
        return hash(self.status)