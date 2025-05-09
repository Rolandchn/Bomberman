from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity


from data.entity.AI.utils import get_danger_penalty, get_safe_tiles_around, get_obstacles_between



def evaluate_center_behavior(world: GameWorld, player: Entity, center_pos):
    px, py = player.grid_x, player.grid_y
    cx, cy = center_pos

    distance = abs(px - cx) + abs(py - cy)

    # Base score: closer to center is better
    score = -distance * 5
    score += get_danger_penalty(world, px, py)

    # --- Obstacle Between AI and Enemy ---
    path_obstacles = get_obstacles_between((px, py), center_pos, world)
    num_obstacles = len(path_obstacles)

    # Check if any of AI's bombs can destroy them
    ai_bombs = [bomb for bomb in world.bomb_group if bomb.owner == player]

    bomb_threatens_obstacle = False
    for bomb in ai_bombs:
        bx, by = bomb.grid_x, bomb.grid_y
        for ox, oy in path_obstacles:
            if abs(bx - ox) + abs(by - oy) <= bomb.spread:
                bomb_threatens_obstacle = True
                break
        if bomb_threatens_obstacle:
            break

    if num_obstacles > 0:
        if bomb_threatens_obstacle:
            score += 30 + 5 * num_obstacles  # reward breaking path
        else:
            score -= 5 * num_obstacles  # penalize if no bomb yet

     # Penalize if bomb threatens but no safe tile
    if bomb_threatens_obstacle and not get_safe_tiles_around(px, py, world):
        score -= 200


    return score
