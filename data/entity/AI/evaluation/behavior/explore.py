from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

import random

from data.entity.AI.utils import get_danger_penalty, get_safe_tiles_around, get_obstacles_between, is_in_explosion_range


def evaluate_explore_behavior(world: GameWorld, ai: Entity, destination_pos):
    ax, ay = ai.grid_x, ai.grid_y
    cx, cy = destination_pos

    score = 0

    # Penalize distance from destination (exploration goal)
    distance = abs(ax - cx) + abs(ay - cy)
    score -= distance * 5

    # Penalize being in danger: bomb blast or border zone
    danger_penalty = get_danger_penalty(world, ax, ay)
    if danger_penalty == float("-inf"):
        return danger_penalty
    score += danger_penalty

    # Check for nearby bombs (threat or own)
    ai_bombs = [bomb for bomb in world.bomb_group if bomb.owner == ai]
    path_obstacles = get_obstacles_between((ax, ay), (cx, cy), world)
    num_obstacles = len(path_obstacles)

    bomb_threatens_obstacle = False
    for bomb in ai_bombs:
        bx, by = bomb.grid_x, bomb.grid_y
        for ox, oy in path_obstacles:
            if abs(bx - ox) + abs(by - oy) <= bomb.spread:
                bomb_threatens_obstacle = True
                break
        if bomb_threatens_obstacle:
            break

    # Encourage breaking obstacles, but only if it's safe
    if num_obstacles > 0:
        if bomb_threatens_obstacle:
            if get_safe_tiles_around(ax, ay, world):
                score += 30 + 5 * num_obstacles  # good: can break and escape
            else:
                score -= 100  # bad: could get trapped
        else:
            if get_safe_tiles_around(ax, ay, world):
                score += 10  # okay: can bomb if needed
            else:
                score -= 20  # not worth risking it

    # Slight reward for safe proximity to open space (exploration value)
    safe_tiles = get_safe_tiles_around(ax, ay, world)
    score += len(safe_tiles) * 2

    return score
