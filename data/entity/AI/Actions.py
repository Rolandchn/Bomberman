from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld
    from data.entity.Entity import Entity

from game.GameAction import Action



def actions(simulated_world: GameWorld, player: Entity):
        '''
        Output: return all the available actions in one state.
        '''
        actions = [Action.PLACE_BOMB]

        for move in Action.MOVE:
            if simulated_world.map.is_walkable(player, move):
                actions.append(move)

        return actions
