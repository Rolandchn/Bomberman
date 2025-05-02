from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWord import GameWorld
    from data.entity.Entity import Entity


from game.GameStatus import GameStatus
from data.entity.Explosion import Explosion
from data.entity.Bombe import Bomb

from data.entity.AI.Turn import turn
from data.entity.AI.Actions import actions
from data.entity.AI.Result import result
from data.entity.AI.Evaluation import eval


def minmax(simulated_world: GameWorld, depth=3):
    player: Entity = turn(simulated_world)
    print("===depth===", 3 - depth)

    for _ in simulated_world.map.grid:
        if isinstance(_, Explosion) or isinstance(_, Bomb):
            print(_, _.start_turn)

    if depth < 0:
        return eval(simulated_world, player), None

    # MIN
    if player.status == GameStatus.P1:
        best_value = float("inf")

        for action in actions(simulated_world, player):
            value, _ = minmax(result(simulated_world,  action), depth - 1)

            if value <= best_value:
                best_value = value
                best_action = action

        return best_value, best_action
        
    # MAX
    elif player.status == GameStatus.P2:
        best_value = float("-inf")

        for action in actions(simulated_world, player):
            value, _ = minmax(result(simulated_world, action), depth - 1)

            if best_value <= value:
                best_value = value
                best_action = action

        return best_value, best_action