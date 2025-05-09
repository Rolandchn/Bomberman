from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity


from data.entity.AI.utils import get_danger_penalty, get_safe_tiles_around, get_obstacles_between


def evaluate_chase_behavior(world: GameWorld, player: Entity, target: Entity):
    px, py = player.grid_x, player.grid_y
    tx, ty = target.grid_x, target.grid_y

    distance_to_enemy = abs(px - tx) + abs(py - ty)

    chase_score = max(0, 50 - distance_to_enemy * 10)
    chase_score += get_danger_penalty(world, px, py)

    # --- Obstacle Between AI and Enemy ---
    path_obstacles = get_obstacles_between((px, py), (tx, ty), world)
    num_obstacles = len(path_obstacles)

    # Check if existing AI bombs threaten those obstacles
    player_bombs = [bomb for bomb in world.bomb_group if bomb.owner == player]
    bomb_threatens_obstacle = False

    for bomb in player_bombs:
        bx, by = bomb.grid_x, bomb.grid_y
        for ox, oy in path_obstacles:
            if abs(bx - ox) + abs(by - oy) <= bomb.spread:
                bomb_threatens_obstacle = True
                break
        if bomb_threatens_obstacle:
            break

    if num_obstacles > 0:
        if bomb_threatens_obstacle:
            chase_score += 50 + 10 * num_obstacles  # reward if bomb will break through
        else:
            chase_score -= 5 * num_obstacles  # discourage standing still if no bomb is set
            if distance_to_enemy <= 3:
                chase_score += 30  # encourage placing bomb to open a path


    # Strong penalty if stuck in danger
    if not get_safe_tiles_around(px, py, world):
        chase_score -= 300

    return chase_score

