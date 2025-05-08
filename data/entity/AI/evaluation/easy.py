from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld


from game.GameStatus import GameStatus
from data.entity.AI.decision.terminal import terminal
from data.entity.AI.decision.value import value

from data.entity.AI.evaluation.behavior.explore import evaluate_explore_behavior
from data.entity.AI.utils import choose_best_or_next

def eval(simulated_world: GameWorld, status: GameStatus):
    if terminal(simulated_world):
        return value(simulated_world)
            
    ai = None
    for player in simulated_world.player_group:
        if player.status == status:
            ai = player
            break

    if ai is None:
        raise ValueError("MINMAX caller was not found")

    current_target = choose_best_or_next(ai)

    raw_score = evaluate_explore_behavior(simulated_world, ai, current_target)

    # Flip score if current player is MIN
    return raw_score if status == GameStatus.P2 else -raw_score

