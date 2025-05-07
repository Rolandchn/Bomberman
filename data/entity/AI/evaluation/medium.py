from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

import random

from game.GameStatus import GameStatus
from data.entity.AI.decision.terminal import terminal
from data.entity.AI.decision.value import value

from data.entity.AI.evaluation.behavior.attack import evaluate_attack_behavior
from data.entity.AI.evaluation.behavior.center import evaluate_center_behavior



def eval(simulated_world: GameWorld, status: GameStatus):
    if terminal(simulated_world):
        return value(simulated_world)
            
    player = next((p for p in simulated_world.player_group if p.status == status), None)
    if player is None:
        raise ValueError("MINMAX caller was not found")

    ax, ay = player.grid_x, player.grid_y
    ex, ey = simulated_world.map.get_enemie_pos(player)

    distance_to_enemy = abs(ax - ex) + abs(ay - ey)
    attack_score = max(0, 30 - distance_to_enemy * 5)

    center = (7, 7)
    distance_to_center = abs(ax - center[0]) + abs(ay - center[1])
    center_score = max(0, 20 - distance_to_center * 3)

    danger_penalty = -40 if simulated_world.map.is_in_explosion_range(ax, ay) else 0

    bomb_bonus = 0
    for bomb in simulated_world.bomb_group:
        if bomb.owner == player:
            if abs(bomb.grid_x - ex) + abs(bomb.grid_y - ey) <= bomb.spread:
                bomb_bonus += 30

    raw_score = attack_score + center_score + bomb_bonus + danger_penalty
    raw_score += random.randint(-10, 10)  # slight unpredictability

    return raw_score if status == GameStatus.P2 else -raw_score


