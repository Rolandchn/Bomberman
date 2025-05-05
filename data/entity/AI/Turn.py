from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    

def turn(simulated_world: GameWorld):
        '''
        Output: retourne le joueur qui va joue
        '''
        for player in simulated_world.player_group:
            if player.status == simulated_world.turn_status:
                return player