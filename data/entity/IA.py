from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.EntityManager import EntityManager
    from data.map.Map import Map


import pygame

from data.entity.Entity import Entity

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle, corner the player, ...)
    def __init__(self, color:Color, spawn:Tuple[int, int], map:Map, entities:EntityManager):
        super().__init__(spawn, pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.player_group)

        self.life = 1
        self.image.fill(color.value)

        self.map = map
        self.entities = entities


    def turn(self):
        '''
        retourne le joueur qui va joue (minmax)
        '''
        pass

    def action(self):
        '''
        Output: return all the available actions in one state.
        '''

        pass

    def eval(self):
        '''
        Output: évalue la position 
        '''
        ia_x, ia_y = self.grid_x, self.grid_y
        player_x, player_y = self.map.get_players_pos()
        pass

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
        pass
