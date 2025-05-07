from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity


from game.GameStatus import GameStatus
from game.GameAction import Action

from data.entity.AI.Turn import turn
from data.entity.AI.Actions import actions
from data.entity.AI.Result import result
from data.entity.AI.Evaluation.Evaluation import eval
from data.entity.AI.Terminal import terminal


def minmax(simulated_world: GameWorld, root_entity: GameStatus, depth=3, alpha=float('-inf'), beta=float('inf')):
    # TRI des actions (déplacements > bombe > rien)
    def action_priority(act):
        if act.name.startswith("MOVE"):
            return 0
        elif act.name == "PLACE_BOMB":
            return 1
        elif act.name == "WAIT":
            return 2
        
    player: Entity = turn(simulated_world)
    
    if terminal(simulated_world) or depth <= 0:
        return eval(simulated_world, root_entity), Action.WAIT

    # Déterminer l'ordre d'exploration des actions pour améliorer Alpha Beta
    possible_actions = actions(simulated_world,player)
    possible_actions.sort(key=action_priority)

    # Fallback: if only PLACE_BOMB is returned, and we want to avoid suicides
    if possible_actions == [Action.PLACE_BOMB]:
        # Only allow it if the AI has an escape route
        safe_tiles = simulated_world.map.get_safe_tiles_around(player.grid_x, player.grid_y)
        if not safe_tiles:
            possible_actions = [Action.WAIT]

    # MIN
    if player.status == GameStatus.P1:
        best_value = float("inf")
        best_action = Action.WAIT

        for action in possible_actions:
            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1, alpha, beta)

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
            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1, alpha, beta)

            if best_value < value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

            #ELAGAGE
            if beta <= alpha:
                break

        return best_value, best_action
