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
            
    player: Entity = None
    opponent: Entity = None
    for p in simulated_world.player_group:
        if p.status == status:
            player = p
        else:
            opponent = p

    if player is None or opponent is None:
        raise ValueError("MINMAX caller was not found")

    player_x, player_y = (player.grid_x, player.grid_y)
    opponent_x, opponent_y = (opponent.grid_x, opponent.grid_y)

    CENTER_POS = (math.floor(simulated_world.map.width / 2), math.floor(simulated_world.map.height / 2) - 1)
    ENEMY_DETECTION_RANGE = 8
    
    opponent_distance = abs(opponent_x - player_x) + abs(opponent_y - player_y)

    if opponent_distance <= ENEMY_DETECTION_RANGE:
        raw_score = evaluate_attack_behavior(simulated_world, player, opponent)

    else:
        raw_score = evaluate_center_behavior(simulated_world, player, CENTER_POS)

    # Flip score if current player is MIN
    return raw_score if status == GameStatus.P2 else -raw_score


