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

    attack_score = max(0, 50 - distance_to_enemy * 10)

    # Bomb placement bonus if enemy is in bomb range
    for bomb in world.bomb_group:
        if bomb.owner == ai:
            if abs(bomb.grid_x - ex) + abs(bomb.grid_y - ey) <= bomb.spread:
                attack_score += 120

    # Encourage bomb placement when near enough
    if distance_to_enemy <= 3:
        attack_score += 40

    # --- Obstacle Between AI and Enemy ---
    path_obstacles = world.map.get_obstacles_between((ax, ay), (ex, ey))
    num_obstacles = len(path_obstacles)

    # Check if existing AI bombs threaten those obstacles
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
            attack_score += 50 + 10 * num_obstacles  # reward if bomb will break through
        else:
            attack_score -= 5 * num_obstacles  # discourage standing still if no bomb is set
            if distance_to_enemy <= 3:
                attack_score += 30  # encourage placing bomb to open a path

    # Trapping logic
    escape_routes = world.map.get_safe_tiles_around(ex, ey)
    if len(escape_routes) == 0:
        attack_score += 100
    elif len(escape_routes) == 1:
        attack_score += 50
    elif len(escape_routes) == 2:
        attack_score += 20

    # Encourage moving if safe
    if not world.map.is_in_explosion_range(ax, ay):
        attack_score += 10

    return attack_score


