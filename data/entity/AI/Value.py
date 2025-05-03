from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld

import pygame


from game.GameStatus import GameStatus



def value(simulated_world: GameWorld):
    '''
    Output: détermine si la partie terminée est gagnant pour P1 ou P2 ou null
    '''
    player_collided = pygame.sprite.groupcollide(simulated_world.player_group, simulated_world.explosion_group,
                                                 dokilla=False, dokillb=False)

    print("DEAD", player_collided)

    if 1 < len(player_collided):
        return 0
    
    key, _ = next(iter(player_collided.items()))
    
    # P1 dead
    if key.status == GameStatus.P1:
        return float("inf")
    
    # P2 dead
    elif key.status == GameStatus.P2:
        return float("-inf")