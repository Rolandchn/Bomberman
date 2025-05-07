from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity



def evaluate_center_behavior(world: GameWorld, ai: Entity, center_pos):
    ax, ay = ai.grid_x, ai.grid_y
    cx, cy = center_pos

    distance = abs(ax - cx) + abs(ay - cy)
    danger_penalty = -300 if world.map.is_in_explosion_range(ax, ay) else 0
    # Base score: closer to center is better
    score = -distance * 5 + danger_penalty

    # --- Obstacle Analysis ---
    path_obstacles = world.map.get_obstacles_between((ax, ay), center_pos)
    num_obstacles = len(path_obstacles)

    # Check if any of AI's bombs can destroy them
    ai_bombs = [bomb for bomb in world.bomb_group if bomb.owner == ai]
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
            score -= 5 * num_obstacles  # mildly penalize if no bomb yet

    if bomb_threatens_obstacle:
        safe_tiles = world.map.get_safe_tiles_around(ax, ay)
        if not safe_tiles:
            score -= 200

    return score


def evaluate_attack_behavior(world: GameWorld, ai: Entity, enemy_pos):
    ax, ay = ai.grid_x, ai.grid_y
    ex, ey = enemy_pos
    distance_to_enemy = abs(ax - ex) + abs(ay - ey)

    # Base: Encourage moving closer (but not sitting still right next to the enemy)
    attack_score = max(0, 50 - distance_to_enemy * 10)

    # Bomb placement bonus if enemy is already in danger zone
    for bomb in world.bomb_group:
        if bomb.owner == ai:
            if abs(bomb.grid_x - ex) + abs(bomb.grid_y - ey) <= bomb.spread:
                attack_score += 120  # stronger reward for effective bombs

    # Encourage placing a bomb if close enough to hit enemy
    if distance_to_enemy <= 3:
        attack_score += 40  # suggests bomb opportunity is good

    # Reward for threatening escape routes (trapping behavior)
    escape_routes = world.map.get_safe_tiles_around(ex, ey)
    if len(escape_routes) == 0:
        attack_score += 100  # enemy is trapped
    elif len(escape_routes) == 1:
        attack_score += 50   # partially trapped
    elif len(escape_routes) == 2:
        attack_score += 20   # low mobility

    # Slight bonus for approaching from safe tiles
    if not world.map.is_in_explosion_range(ax, ay):
        attack_score += 10

    return attack_score

