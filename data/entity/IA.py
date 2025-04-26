from __future__ import annotations
from typing import TYPE_CHECKING
import random
import pygame

if TYPE_CHECKING:
    from data.entity.GameWord import GameWorld


from core.Bomberman import GameStatus

from data.entity.Entity import Entity
from data.entity.Bombe import Bomb

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle, corner the player, ...)

    def __init__(self, status:GameStatus, world:GameWorld, difficulty="facile"):
        self.status = status
        super().__init__(world.map.respawn(self), pygame.Surface((TILE_SIZE, TILE_SIZE)), world.player_group)

        self.world = world
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
        
        ai_score = self.world.map.valued_grid[ai_y][ai_x]
        player_score = self.world.map.valued_grid[player_y][player_x]

        return ai_score - player_score


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

    def terminal(self):
        '''
        Output détermine si la partie est terminée (gagnant, perdant, égalité)
        '''
        for position in self.world.map.grid.items():
            if GameStatus.P1 in position or GameStatus.P2 in position:
                return True
        
        return False



    '''
    Méthode pour l'IA random
    '''
    def random_turn(self):
        '''
        IA Random : déplacement aléatoire + pose bombe aléatoire
        '''
        action = random.choice([self.move, self.bomb])
        
        return action()


    def move(self) -> bool:
        #Retourne une direction valide aléatoire
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = self.grid_x + dx
            ny = self.grid_y + dy

            if self.world.map.is_walkable(self, nx, ny):
                self.world.map.update_grid_position(self, nx, ny)
                self.grid_x = nx
                self.grid_y = ny

                self.update_rect()
                return True
            
        return False


    def bomb(self):
        #Pose une bombe sur la position actuelle
        Bomb((self.grid_x, self.grid_y), self.world)
        return True
    

    def is_hit(self):
        '''
        Output: check player sprite collides with any explosion. Return True if collides, otherwise False
        ''' 

        return pygame.sprite.spritecollideany(self, self.world.explosion_group)
    

    def __eq__(self, other):
        return isinstance(other, IA) and other.status == self.status


    def __hash__(self):
        return hash(self.status)