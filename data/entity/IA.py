from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from data.entity.EntityManager import EntityManager


import pygame

from data.entity.Entity import Entity

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle, corner the player, ...)
    def __init__(self, spawn:Tuple[int, int], entities:EntityManager):
        super().__init__(spawn, pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.player_group)

        self.life = 1

        self.entities = entities

        self.image.fill(Color.BLACK.value)

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

    def terminal(self):
        '''
        Output détermine si la partie est terminée (gagnant, perdant, égalité)
        '''
        pass
