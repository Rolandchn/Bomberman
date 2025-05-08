from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity


from game.GameStatus import GameStatus
from game.GameAction import Action

from data.entity.AI.decision.turn import turn
from data.entity.AI.decision.result import result
from data.entity.AI.decision.terminal import terminal

from data.entity.AI.actions import actions
from data.entity.AI.utils import action_priority, get_safe_tiles_around



def minmax(simulated_world: GameWorld, root_entity: GameStatus, depth, eval_fn, alpha=float('-inf'), beta=float('inf')):
    player: Entity = turn(simulated_world)
    
    if terminal(simulated_world) or depth <= 0:
        return eval_fn(simulated_world, root_entity), Action.WAIT

    # Déterminer l'ordre d'exploration des actions pour améliorer Alpha Beta
    possible_actions = actions(simulated_world,player)
    
    # TRI des actions (déplacements > bombe > rien)
    possible_actions.sort(key=action_priority)

    # MIN
    if player.status == GameStatus.P1:
        best_value = float("inf")
        best_action = Action.WAIT

        for action in possible_actions:
            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1, eval_fn, alpha, beta)

            if value < best_value:
                best_value = value
                best_action = action

            beta = min(beta, best_value)

            # ELAGAGE
            if beta <= alpha:
                break

        return best_value, best_action

    # MAX
    elif player.status == GameStatus.P2:
        best_value = float("-inf")
        best_action = Action.WAIT

        for action in possible_actions:
            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1, eval_fn, alpha, beta)

            if best_value < value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

            #ELAGAGE
            if beta <= alpha:
                break

        return best_value, best_action
