from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.GameWorld import GameWorld
    from data.entity.Entity import Entity

from data.map.structure.Obstacle import Obstacle
from data.map.structure.Wall import Wall

from data.texture.config import DESTINATION_POS, current_destination_index
from collections import deque

import random


def choose_best_or_next(ai: Entity):
    destinations = DESTINATION_POS[ai.status]
    idx = current_destination_index[ai.status]
    target = destinations[idx % len(destinations)]

    if (ai.grid_x, ai.grid_y) == target:
        # Arrived: move to next destination
        current_destination_index[ai.status] = (idx + 1) % len(destinations)
        target = destinations[current_destination_index[ai.status]]

    return target


def action_priority(act):
    if act.name.startswith("MOVE"):
        return 0
    elif act.name == "PLACE_BOMB":
        return 1
    elif act.name == "WAIT":
        return 2



def get_danger_penalty(world: GameWorld, x, y):
    margin = world.map.current_margin
    width, height = world.map.width, world.map.height

    in_explosion = is_in_explosion_range(x, y, world)
    in_shrinking_zone = x <= margin or x >= width - margin - 1 or y <= margin or y >= height - margin - 1

    if in_explosion or in_shrinking_zone:
        return float("-inf")  
    
    return 0



def get_safe_tiles_around(x, y, simulated_world: GameWorld, max_timer=5):
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
            if not is_in_explosion_range(nx, ny, simulated_world, max_timer=max_timer):
                safe_tiles.append((nx, ny))

        return safe_tiles


def get_obstacles_between(start_pos, end_pos, world: GameWorld):
        visited = set()
        queue = deque()
        queue.append((start_pos, [], []))  # (position, path, obstacles)

        while queue:
            (x, y), path, obstacles = queue.popleft()

            if (x, y) == end_pos:
                return obstacles  # return list of obstacle positions

            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if not (1 <= nx <= 13 and 1 <= ny <= 13):
                    continue
                if next_pos in visited:
                    continue

                entities = world.map.entities_at_position(next_pos)
                is_solid = any(isinstance(e, Wall) for e in entities)
                is_obstacle = any(isinstance(e, Obstacle) for e in entities)

                if is_solid:
                    continue

                new_obstacles = obstacles.copy()
                if is_obstacle:
                    new_obstacles.append(next_pos)

                queue.append((next_pos, path + [next_pos], new_obstacles))

        return []  # No path found


def is_in_explosion_range(x, y, simulated_world: GameWorld, max_timer=5):
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