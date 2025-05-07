from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld

import pygame



def terminal(simulated_world: GameWorld):
    '''
    Output: détermine si la partie est terminée (gagnant, perdant, égalité)
    '''
    for player in simulated_world.player_group:
        if pygame.sprite.spritecollideany(player, simulated_world.explosion_group) is not None:
            return True
    
    return False