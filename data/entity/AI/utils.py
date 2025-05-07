from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld

import random


from game.GameAction import Action



def get_random_action():
    return random.choice([
        Action.MOVE_UP,
        Action.MOVE_DOWN,
        Action.MOVE_LEFT,
        Action.MOVE_RIGHT,
        Action.PLACE_BOMB
    ])


def action_priority(act):
    if act.name.startswith("MOVE"):
        return 0
    elif act.name == "PLACE_BOMB":
        return 1
    elif act.name == "WAIT":
        return 2



def get_danger_penalty(world: GameWorld, x, y):
    if world.map.is_in_explosion_range(x, y):
        return float("-inf")  # or -inf to signify certain death
    return 0


def get_safe_tiles_around(x, y, simulated_world: GameWorld, max_timer=3):
        """
        Returns a list of (x, y) positions around the given tile that are walkable and not in explosion range.
        - `world` is used to access bombs and danger info.
        - `max_timer` defines how far in the future we consider danger.
        """
        safe_tiles = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if tile is walkable
            entities = simulated_world.map.entities_at_position((nx, ny))
            is_blocked = any(e in simulated_world.wall_group for e in entities)
            
            if is_blocked:
                continue

            # Check explosion range using world's helper
            if not is_in_explosion_range(nx, ny, max_timer=max_timer):
                safe_tiles.append((nx, ny))

        return safe_tiles



def is_in_explosion_range(x, y, simulated_world: GameWorld, max_timer=3):
    """
    Returns True if tile (x, y) is in the explosion range of any active bomb.
    """
    for bomb in simulated_world.bomb_group:
        if bomb.tick < max_timer:
            continue  # Skip bombs that are too far from exploding
        
        bx, by = bomb.grid_x, bomb.grid_y
        spread = bomb.spread

        # Include bomb's own tile
        if bx == x and by == y:
            return True

        # Check 4 directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for distance in range(1, spread + 1):
                nx, ny = bx + dx * distance, by + dy * distance
                if any(e in simulated_world.wall_group for e in simulated_world.map.entities_at_position((nx, ny))):
                    break  # Explosion stops at walls and obstacle

                if nx == x and ny == y:
                    return True

    return False