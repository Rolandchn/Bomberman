from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity


from game.GameStatus import GameStatus

from data.entity.AI.Turn import turn
from data.entity.AI.Actions import actions
from data.entity.AI.Result import result
from data.entity.AI.Evaluation import eval
from data.entity.AI.Terminal import terminal

def minmax(simulated_world: GameWorld, root_entity:GameStatus, depth=3, alpha=float('-inf'), beta=float('inf')):
    player: Entity = turn(simulated_world)
    
    if terminal(simulated_world) or depth <= 0:
        return eval(simulated_world, root_entity), None
    
    # MIN
    if player.status == GameStatus.P1:
        best_value = float("inf")
        best_action = None

        for action in actions(simulated_world, player):
            value, _ = minmax(result(simulated_world,  action), root_entity, depth - 1, alpha, beta)

            if value < best_value:
                best_value = value
                best_action = action

            beta = min(beta, best_value)

            #si beta <= alpha : on arrête d'explorer
            if beta <= alpha:
                break

        return best_value, best_action
        
    # MAX
    elif player.status == GameStatus.P2:
        best_value = float("-inf")
        best_action = None

        for action in actions(simulated_world, player):
            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1, alpha, beta)

            if best_value > value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

            #si beta <= alpha -> on arrête d'explorer
            if beta <= alpha:
                break
            
        return best_value, best_action