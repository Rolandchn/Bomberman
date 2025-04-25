from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import random
import pygame

if TYPE_CHECKING:
    from data.entity.EntityManager import EntityManager
    from data.map.Map import Map

from data.entity.Entity import Entity
from data.entity.Bombe import Bomb

from data.texture.Color import Color
from data.texture.config import TILE_SIZE


class IA(Entity):
    # difficulty:
    #   easy: random
    #   moderate:  min max td4 (strategie: take the center, destroy obstacle, corner the player, ...)
    def __init__(self, spawn:Tuple[int, int], entities:EntityManager, map: Map, difficulty="facile"):
        super().__init__(spawn, pygame.Surface((TILE_SIZE, TILE_SIZE)), entities.player_group)

        self.life = 1
        self.entities = entities
        self.image.fill(Color.BLACK.value)
        self.difficulty = difficulty
        self.map = map

    def turn(self):
        '''
        retourne le joueur qui va joue en fonction de la difficulté
        '''

        if self.difficulty == "facile":
            self.random_turn()

        elif self.difficulty == "moyen":
            pass #à implementer

        elif self.difficulty == "difficile":
            pass #à implementer (minMax)

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
        pass

    def terminal(self):
        '''
        Output détermine si la partie est terminée (gagnant, perdant, égalité)
        '''
        pass

    '''
    Méthode pour l'IA random
    '''


    def random_turn(self):
        '''
        IA Random : déplacement aléatoire + pose bombe aléatoire
        '''
        direction = self.get_random_direction()
        self.move(direction)

        # Bombe avec 10% de chance
        if random.random() < 0.1:
            self.place_bomb()

    def get_random_direction(self) -> Tuple[int, int]:
        #Retourne une direction valide aléatoire
        directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = self.grid_x + dx
            ny = self.grid_y + dy
            if self.map.is_tile_walkable(nx, ny):
                return dx, dy
        return 0, 0

    def move(self, direction:Tuple[int, int]):
        #deplace l'IA si la case est libre
        dx, dy = direction
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if self.map.is_tile_walkable(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_rect()


    def place_bomb(self):
            #Pose une bombe sur la position actuelle
            Bomb(self.grid_x, self.grid_y, self.entities)

