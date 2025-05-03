from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld
    from data.entity.Entity import Entity


from game.GameStatus import GameStatus

from data.entity.AI.Turn import turn
from data.entity.AI.Actions import actions
from data.entity.AI.Result import result
from data.entity.AI.Evaluation import eval


def minmax(simulated_world: GameWorld, root_entity:GameStatus, depth=4):
    player: Entity = turn(simulated_world)

    if depth < 0:
        return eval(simulated_world, root_entity), None
    
    print(f"==============================depth {4 - depth}==============================")

    # MIN
    if player.status == GameStatus.P1:
        best_value = float("inf")

        for action in actions(simulated_world, player):
            print("MIN", action, "from depth:", 4 - depth)
                
            value, _ = minmax(result(simulated_world,  action), root_entity, depth - 1)

            if value <= best_value:
                best_value = value
                best_action = action
            
        print("result depth:", 4 - depth, best_value, best_action)

        return best_value, best_action
        
    # MAX
    elif player.status == GameStatus.P2:
        best_value = float("-inf")

        for action in actions(simulated_world, player):
            print("MAX", action, "from depth:", 4 - depth)

            value, _ = minmax(result(simulated_world, action), root_entity, depth - 1)

            if best_value <= value:
                best_value = value
                best_action = action
            
        print("result depth:", 4 - depth, best_value, best_action)

        return best_value, best_action