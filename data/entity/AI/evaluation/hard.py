from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

import math

from game.GameStatus import GameStatus
from data.entity.AI.decision.terminal import terminal
from data.entity.AI.decision.value import value

from data.entity.AI.evaluation.behavior.attack import evaluate_attack_behavior
from data.entity.AI.evaluation.behavior.center import evaluate_center_behavior


def eval(simulated_world: GameWorld, status: GameStatus):
    '''
    Output: evaluate the game state depending on the AI position.
    '''
    if terminal(simulated_world):
        return value(simulated_world)
            
    ai = None
    for player in simulated_world.player_group:
        if player.status == status:
            ai = player
            break

    if ai is None:
        raise ValueError("MINMAX caller was not found")

    ai_x, ai_y = ai.grid_x, ai.grid_y
    player_x, player_y = simulated_world.map.get_enemie_pos(ai)

    CENTER_POS = (math.ceil(simulated_world.map.width / 2), math.ceil(simulated_world.map.height // 2))
    ENEMY_DETECTION_RANGE = 8
    
    player_distance = abs(player_x - ai_x) + abs(player_y - ai_y)

    if player_distance <= ENEMY_DETECTION_RANGE:
        raw_score = evaluate_attack_behavior(simulated_world, ai, (player_x, player_y))

    else:
        raw_score = evaluate_center_behavior(simulated_world, ai, CENTER_POS)

    # Flip score if current player is MIN
    return raw_score if status == GameStatus.P2 else -raw_score


